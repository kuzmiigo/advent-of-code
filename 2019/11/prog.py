import logging
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from queue import Queue
from threading import Event, Thread


###############################################################################
# Intcomputer
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
        self._state = defaultdict(lambda: 0, enumerate(p))
        self._name = name
        self._io = io
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
        self.is_running = True
        self._debug('START')

        while True:
            self._num_ops += 1
            if self._num_ops > MAX_OPERATIONS:
                self._error(f'max operations exceeded: {MAX_OPERATIONS}')
                break
            opcode = self._next_opcode()
            operation = self._ops.get(opcode, self._op_default)
            if not operation():
                break

        self._debug(f'STOP after {self._num_ops} operations')
        if self._done_event:
            self._done_event.set()

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
        return True

    def _op_mul(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = x * y
        self._debug(f'x={x}, y={y}, dst={dst}')
        return True

    def _op_in(self):
        dst = self._next_arg(True)
        self._state[dst] = self._io.read()
        self._debug(f'val={self._state[dst]}, dst={dst}')
        return True

    def _op_out(self):
        x = self._next_arg()
        self._io.write(x)
        self._debug(f'x={x}')
        return True

    def _op_jnz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x != 0:
            self._pointer = y
        self._debug(f'x={x}, y={y}, ptr={self._pointer}')
        return True

    def _op_jz(self):
        x = self._next_arg()
        y = self._next_arg()
        if x == 0:
            self._pointer = y
        self._debug(f'x={x}, y={y}, ptr={self._pointer}')
        return True

    def _op_le(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x < y else 0)
        self._debug(f'x={x}, y={y}, dst={dst}, val={self._state[dst]}')
        return True

    def _op_eq(self):
        x = self._next_arg()
        y = self._next_arg()
        dst = self._next_arg(True)
        self._state[dst] = (1 if x == y else 0)
        self._debug(f'x={x}, y={y}, dst={dst}, val={self._state[dst]}')
        return True

    def _op_arb(self):
        x = self._next_arg()
        self._relative_base += x
        self._debug(f'x={x}, relbase={self._relative_base}')
        return True

    def _op_ret(self):
        self._debug(f'RET')
        return False

    def _op_default(self):
        self._error(f'wrong opcode {self._opcode}')
        return False


###############################################################################
# Main part
###############################################################################

turns = {
    'L': ('D', 'U'),
    'R': ('U', 'D'),
    'U': ('L', 'R'),
    'D': ('R', 'L')
}

deltas = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


def read_file(name):
    with open(name, 'r') as f:
        return filter(None, map(str.strip, f.readlines()))


def start_computer(programme):
    done_event = Event()
    qs = [Queue() for _ in range(2)]
    io = QueueIO(qs[0], qs[1])
    c = IntcodeComputer(programme, f'PAINT', io, done_event)
    c.start()
    return qs, done_event


def run(programme, start_colour=0, debug=False):
    panels = defaultdict(lambda: 0)
    panels[(0, 0)] = start_colour

    qs, done_event = start_computer(programme)
    qin, qout = qs
    direction, x, y = 'U', 0, 0

    while not done_event.isSet():
        colour = panels[(x, y)]
        qin.put(colour)
        new_colour = qout.get()
        turn = qout.get()
        if debug:
            print(f'dir={direction} x={x} y={y} colour={colour} -> ', end='')
            print(f'colour={new_colour} turn={turn}')
        panels[(x, y)] = new_colour
        direction = turns[direction][turn]
        dx, dy = deltas[direction]
        x += dx
        y += dy

    return panels


def print_panels(panels):
    min_x = min([x for x, y in panels.keys()])
    max_x = max([x for x, y in panels.keys()])
    min_y = min([y for x, y in panels.keys()])
    max_y = max([y for x, y in panels.keys()])

    for y in range(max_y, min_y - max_y - 1, -1):
        for x in range(min_x, max_x - min_x + 1):
            print('*' if panels[(x, y)] == 1 else ' ', end='')
        print()


programme = list(read_file(sys.argv[1]))[0]

# Part 1
panels = run(programme, 0)
print(1, len(panels.keys()))

# Part 2
panels = run(programme, 1)
print(2)
print_panels(panels)
