import argparse
import itertools
import logging
import queue
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from threading import Thread

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


class InteractiveIO(AbstractIO):
    def read(self):
        return int(input("Enter a number: "))

    def write(self, n):
        print(n)

    def stop(self):
        pass


class QueueIO(AbstractIO):
    def __init__(self, input_queue, output_queue):
        self._input_queue = input_queue
        self._output_queue = output_queue
        self._is_running = True

    def read(self):
        while self._is_running:
            try:
                return int(self._input_queue.get(timeout=1))
            except queue.Empty:
                pass

    def write(self, n):
        self._output_queue.put(n)

    def stop(self):
        self._is_running = False


class IntcodeComputer(Thread):
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
        return list(filter(None, map(str.strip, f.readlines())))


def parse_programme(s):
    return [int(x) for x in s.split(',')]


def start_computer(programme):
    qs = [queue.Queue() for _ in range(2)]
    io = QueueIO(qs[0], qs[1])
    c = IntcodeComputer(programme, f'ASCII', io)
    c.start()
    return qs, c


def computer_session(programme, input_):
    qs, computer = start_computer(programme)
    qin, qout = qs
    for i in input_:
        qin.put(i)
    output = qout.get()
    computer.stop()
    return output


def run1(programme):
    size = 50

    space = {}
    # Possible starting x-coordinate for the beam
    start_x = 0

    for y in range(size):
        before_beam = True
        after_beam = False
        for x in range(size):
            if x < start_x or after_beam:
                space[(x, y)] = '.'
            else:
                radar = computer_session(programme, [x, y])
                if radar == 1:
                    space[(x, y)] = '#'
                    if before_beam:
                        before_beam = False
                        start_x = x
                else:
                    space[(x, y)] = '.'
                    if not before_beam:
                        after_beam = True
    return space


def run2(programme):
    ship_size = 100
    start_y = 900  # Educated guess

    # Key: y-coordinate, value: set of corresponding x-coordinates
    space = defaultdict(set)
    # Possible starting and ending x-coordinates for the beam
    start_x = 0
    end_x = 0

    # Scan the first row in detail
    print('Init scanner...', end='', file=sys.stderr, flush=True)
    before_beam = True
    for x in itertools.count():
        radar = computer_session(programme, [x, start_y])
        if radar == 1:
            if before_beam:
                start_x = x
                before_beam = False
            space[start_y].add(x)
            end_x = x
        else:
            if not before_beam:
                break
    print('\r\033[K', end='', file=sys.stderr, flush=True)

    # For other rows, check beam boundaries in expected x-coordinates only
    for y in itertools.count(start_y + 1):
        print('\r', y, sep='', end='', file=sys.stderr, flush=True)
        before_beam = True
        for x in itertools.count(start_x):
            if before_beam:
                if x - end_x > 10:  # Safety measure
                    break
                radar = computer_session(programme, [x, y])
                if radar == 1:
                    before_beam = False
                    space[y].add(x)
                    start_x = x
            else:
                if x <= end_x:  # Skip computer checks for expected coordinates
                    space[y].add(x)
                else:
                    radar = computer_session(programme, [x, y])
                    if radar == 1:
                        space[y].add(x)
                        end_x = x
                    else:
                        if x - end_x > 10:  # Safety measure
                            break
        ship_coordinates = check_ship(space, ship_size, y)
        if ship_coordinates:
            break
    print('\r', end='', file=sys.stderr, flush=True)
    return ship_coordinates


def check_ship(space, ship_size, last_y):
    if last_y < ship_size or len(space[last_y]) < ship_size:
        return None
    common = space[last_y]  # Common x-coordinates
    for y in range(last_y - ship_size + 1, last_y):
        if len(space[y]) < ship_size:
            return None
        common = common.intersection(space[y])
        if len(common) < ship_size:
            return None
    return (min(common), last_y - ship_size + 1)


def print_map(space):
    max_x = max([x for x, y in space.keys()])
    max_y = max([y for x, y in space.keys()])

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(space.get((x, y), ' '), end='')
        print()


#
# Init
#

parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input filename')
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose')
args = parser.parse_args()
verbose = args.verbose

programme = parse_programme(read_file(args.filename)[0])

#
# Part 1
#

space = run1(programme)
if verbose:
    print_map(space)
print(1, len([v for v in space.values() if v == '#']))

#
# Part 2
#

coords = run2(programme)
print(2, coords[0] * 10000 + coords[1])
