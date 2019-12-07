import itertools
import logging
import sys
from abc import ABC, abstractmethod
from queue import Queue
from threading import Event, Thread

logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(levelname)s %(message)s',)

TRACE = False
MAX_OPERATIONS = 1000


class AbstractIO(ABC):
    @abstractmethod
    def read(self):
        return 0

    @abstractmethod
    def write(self, n):
        pass


class InteractiveIO(AbstractIO):
    def read(self):
        return int(input("Enter a number: "))

    def write(self, n):
        print(n)


class QueueIO(AbstractIO):
    def __init__(self, input_queue, output_queue):
        self._input_queue = input_queue
        self._output_queue = output_queue

    def read(self):
        return int(self._input_queue.get())

    def write(self, n):
        self._output_queue.put(n)


class IntcodeComputer(Thread):
    def __init__(self, programme, name='WALL-E', io=InteractiveIO(),
                 done_event=None):
        super(IntcodeComputer, self).__init__(name=name)
        p = [int(x) for x in programme.split(',')]
        self._state = dict(enumerate(p))
        self._name = name
        self._io = io
        self._done_event = done_event
        self._pointer = 0
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
            99: self._op_ret
        }

    def run(self):
        self.is_running = True
        self._debug('START')

        for i in range(MAX_OPERATIONS):
            opcode = self._next_opcode()
            operation = self._ops.get(opcode, self._op_default)
            if not operation():
                break
            self._debug('STEP ')

        if i >= MAX_OPERATIONS:
            self._error(f'stopped after {i} operations')
        self._debug('STOP ')
        if self._done_event:
            self._done_event.set()

    def dump(self):
        return f'pointer: {self._pointer}, state: {self._state}'

    def _debug(self, msg=None):
        logging.debug(msg)
        if TRACE:
            logging.debug(self.dump())

    def _error(self, msg=None):
        logging.error(msg)
        logging.debug(self.dump())

    def _next_value(self):
        value = self._state[self._pointer]
        self._pointer += 1
        return value

    def _next_opcode(self):
        instruction = self._next_value()
        self._parameter_modes, self._opcode = divmod(instruction, 100)
        return self._opcode

    def _next_parameter_mode(self):
        self._parameter_modes, mode = divmod(self._parameter_modes, 10)
        return mode

    def _next_arg(self, write_mode=False):
        mode = self._next_parameter_mode()
        arg = self._next_value()
        if not write_mode and mode == 0:
            arg = self._state[arg]
        return arg

    def _op_add(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = x + y
        return True

    def _op_mul(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = x * y
        return True

    def _op_in(self):
        dst = self._next_arg(True)
        self._state[dst] = self._io.read()
        return True

    def _op_out(self):
        self._io.write(self._next_arg())
        return True

    def _op_jnz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x != 0:
            self._pointer = y
        return True

    def _op_jz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x == 0:
            self._pointer = y
        return True

    def _op_le(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x < y else 0)
        return True

    def _op_eq(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x == y else 0)
        return True

    def _op_ret(self):
        return False

    def _op_default(self):
        self._error(f'wrong opcode {self._opcode}')
        return False


def read_file(name):
    with open(name, 'r') as f:
        return filter(None, map(str.strip, f.readlines()))


def start_computers(programme, num_copies):
    done_event = Event()
    qs = [Queue() for _ in range(num_copies)]
    computers = []
    for i in range(num_copies):
        e = done_event if i == num_copies - 1 else None
        io = QueueIO(qs[i], qs[(i + 1) % len(qs)])
        computers.append(IntcodeComputer(programme, f'C-{i}', io, e))
    for c in computers:
        c.start()
    return qs, done_event


def run(programme, num_copies=1, loop_mode=False):
    first_mode = num_copies if loop_mode else 0
    mode_range = range(first_mode, first_mode + num_copies)
    best_settings = ()
    max_output = 0
    for settings in itertools.permutations(mode_range):
        qs, done_event = start_computers(programme, num_copies)
        for i, s in enumerate(settings):
            qs[i].put(s)
        qs[0].put(0)
        done_event.wait()
        curr_output = int(qs[0].get())
        if curr_output > max_output:
            max_output = curr_output
            best_settings = settings
    print(max_output, best_settings)


# Simple run() for part 1:
#
# def run(programme):
#     num_copies = 5
#     best_settings = ()
#     max_output = 0
#     for s in itertools.permutations(range(num_copies)):
#         prev_output = 0
#         for i in range(num_copies):
#             inputs = [s[i], prev_output]
#             computer = IntcodeComputer(programme, inputs)
#             prev_output = computer.run()[0]
#         if prev_output > max_output:
#             max_output = prev_output
#             best_settings = s
#     print(max_output)

# The same IntcodeComputer works with puzzles for day 5 (with InteractiveIO):
#
# computer = IntcodeComputer(programme)
# computer.run()

loop_mode = int(sys.argv[1]) == 2
lines = list(read_file(sys.argv[2]))

for line in lines:
    if len(lines) > 1:
        print('Running programme:')
        print(line)
    run(programme=line, num_copies=5, loop_mode=loop_mode)
    print('')
