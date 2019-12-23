import argparse
import logging
import queue
import sys
import threading
import time
from abc import ABC, abstractmethod
from collections import defaultdict


IDLE_TIMEOUT_SEC = 0.1
INPUT_QUEUE_DELAY_SEC = 0.1
NAT_CHECK_DELAY_SEC = 0.1

verbose = False


###############################################################################
# Intcode computer
###############################################################################

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(levelname)s %(message)s',)

TRACE = False
MAX_OPERATIONS = 1000000


class AbstractIO(ABC):
    @abstractmethod
    def read(self):
        return 0

    @abstractmethod
    def write(self, n):
        pass

    @abstractmethod
    def stop(self, n):
        pass

    @abstractmethod
    def is_idle(self, n):
        pass


class InteractiveIO(AbstractIO):
    def __init__(self):
        self._last_written_ts = 0

    def read(self):
        return int(input("Enter a number: "))

    def write(self, n):
        self._last_written_ts = time.time()
        print(n)

    def stop(self):
        pass

    def is_idle(self, n):
        return time.time() - self._last_written_ts > IDLE_TIMEOUT_SEC


class QueueIO(AbstractIO):
    def __init__(self, input_queue, output_queue):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._is_running = True
        self._last_written_ts = 0

    def read(self):
        try:
            return int(self._input_queue.get(timeout=INPUT_QUEUE_DELAY_SEC))
        except queue.Empty:
            return -1

    def write(self, n):
        self._last_written_ts = time.time()
        self._output_queue.put(n)

    def stop(self):
        self._is_running = False

    def is_idle(self):
        return self._input_queue.empty() and \
            (time.time() - self._last_written_ts > IDLE_TIMEOUT_SEC)


class IntcodeComputer(threading.Thread):
    def __init__(self, programme, name='WALL-E', io=InteractiveIO(),
                 done_event=None):
        super(IntcodeComputer, self).__init__(name=name)
        self._state = defaultdict(lambda: 0, enumerate(programme))
        self._name = name
        self._io = io
        self._is_running = False
        self._done_event = done_event
        self._pointer = 0
        self._relative_base = 0
        self._num_ops = 0
        self._parameter_modes = 0
        self._opcode = 0
        self._ops = {
            1: self._op_add,
            2: self._op_mul,
            3: self._op_in,
            4: self._op_out,
            5: self._op_jnz,
            6: self._op_jz,
            7: self._op_le,
            8: self._op_eq,
            9: self._op_arb,
            99: self._op_ret
        }

    def run(self):
        self._is_running = True
        self._debug('START')

        while self._is_running:
            self._num_ops += 1
            if self._num_ops > MAX_OPERATIONS:
                self._error(f'max operations exceeded: {MAX_OPERATIONS}')
                break
            opcode = self._next_opcode()
            operation = self._ops.get(opcode, self._op_default)
            operation()

        self._debug(f'STOP after {self._num_ops} operations')
        if self._done_event:
            self._done_event.set()

    def stop(self):
        self._is_running = False
        self._io.stop()

    def is_running(self):
        return self._is_running

    def is_idle(self):
        return self._io.is_idle()

    def dump(self):
        ks = sorted(self._state.keys())
        state = ','.join(map(str, [f'{k}:{self._state[k]}' for k in ks]))
        return (f'#{self._num_ops} P={self._pointer} '
                f'RB={self._relative_base} S={state}')

    def _debug(self, msg=None, with_dump=TRACE):
        caller = sys._getframe(1).f_code.co_name
        logging.debug(f'fun={caller}, {msg}')
        if with_dump:
            logging.debug(self.dump())

    def _error(self, msg=None):
        logging.error(msg)
        logging.debug(self.dump())

    def _next_value(self):
        value = self._state[self._pointer]
        self._pointer += 1
        self._debug(f'val={value}', False)
        return value

    def _next_opcode(self):
        instruction = self._next_value()
        self._parameter_modes, self._opcode = divmod(instruction, 100)
        return self._opcode

    def _next_parameter_mode(self):
        self._parameter_modes, mode = divmod(self._parameter_modes, 10)
        self._debug(f'mode={mode}', False)
        return mode

    def _next_arg(self, write_mode=False):
        mode = self._next_parameter_mode()
        arg = self._next_value()
        if mode == 2:
            arg = self._relative_base + arg
        if not write_mode and mode != 1:
            arg = self._state[arg]
        self._debug(f'arg={arg}', False)
        return arg

    def _op_add(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = x + y
        self._debug(f'x={x}, y={y}, dst={dst}')

    def _op_mul(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = x * y
        self._debug(f'x={x}, y={y}, dst={dst}')

    def _op_in(self):
        dst = self._next_arg(True)
        self._state[dst] = self._io.read()
        self._debug(f'val={self._state[dst]}, dst={dst}')

    def _op_out(self):
        x = self._next_arg()
        self._io.write(x)
        self._debug(f'x={x}')

    def _op_jnz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x != 0:
            self._pointer = y
        self._debug(f'x={x}, y={y}, ptr={self._pointer}')

    def _op_jz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x == 0:
            self._pointer = y
        self._debug(f'x={x}, y={y}, ptr={self._pointer}')

    def _op_le(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x < y else 0)
        self._debug(f'x={x}, y={y}, dst={dst}, val={self._state[dst]}')

    def _op_eq(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x == y else 0)
        self._debug(f'x={x}, y={y}, dst={dst}, val={self._state[dst]}')

    def _op_arb(self):
        x = self._next_arg()
        self._relative_base += x
        self._debug(f'x={x}, relbase={self._relative_base}')

    def _op_ret(self):
        self._debug(f'RET')
        self.stop()

    def _op_default(self):
        self._error(f'wrong opcode {self._opcode}')
        self.stop()


###############################################################################
# Main part
###############################################################################


def read_file(name):
    with open(name, 'r') as f:
        return f.readlines()


def parse_programme(s):
    return [int(x) for x in s.split(',')]


def start_computers(programme, num_copies):
    # done_event = threading.Event()
    qis = [queue.Queue() for _ in range(num_copies)]
    qos = [queue.Queue() for _ in range(num_copies)]
    computers = []
    for i in range(num_copies):
        # e = done_event if i == num_copies - 1 else None
        io = QueueIO(qis[i], qos[i])
        qis[i].put(i)
        computers.append(IntcodeComputer(programme, f'NIC-{i}', io))
    for c in computers:
        c.start()
    return qis, qos, computers


def run(programme, num_copies=1):
    qis, qos, computers = start_computers(programme, num_copies)
    nat_x = None
    nat_y = None
    first_nat_y = None
    prev_nat_y = [0]

    def check_nat():
        if not nat_x or not nat_y:
            return False
        for i in range(num_copies):
            if not computers[i].is_idle():
                return False
        if verbose:
            print('-------------------------------------> NAT', nat_x, nat_y)
        else:
            print(f'\r{nat_y}', end='', file=sys.stderr, flush=True)
        qis[0].put(nat_x)
        qis[0].put(nat_y)
        if nat_y == prev_nat_y[0] and nat_y != 0:
            print('\r\033[K', end='', file=sys.stderr, flush=True)
            return True
        prev_nat_y[0] = nat_y
        time.sleep(NAT_CHECK_DELAY_SEC)
        return False

    while True:
        if check_nat():
            for i in range(num_copies):
                computers[i].stop()
            return first_nat_y, prev_nat_y[0]
        for i in range(num_copies):
            try:
                n = qos[i].get_nowait()
            except queue.Empty:
                continue
            x = qos[i].get()
            y = qos[i].get()
            if verbose:
                print(f'{i:3d}   {n:3d}   {x:10d} {y:15d}')
            if n == 255:
                nat_x = x
                nat_y = y
                if first_nat_y is None:
                    first_nat_y = nat_y
            else:
                qis[n].put(x)
                qis[n].put(y)


#
# Init
#

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input filename')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
args = parser.parse_args()
verbose = args.verbose

#
# Main
#

programme = parse_programme(read_file(args.filename)[0])
first_nat_y, duplicate_nat_y = run(programme, 50)
print(1, first_nat_y)
print(2, duplicate_nat_y)
