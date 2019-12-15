import curses
import logging
import queue
import sys
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from os import system
from threading import Thread


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

rev_moves = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}

deltas = {
    1: (0, -1),
    2: (0, 1),
    3: (-1, 0),
    4: (1, 0)
}


def read_file(name):
    with open(name, 'r') as f:
        return list(filter(None, map(str.strip, f.readlines())))


def parse_programme(s):
    return [int(x) for x in s.split(',')]


def sign(x):
    return (x > 0) - (x < 0)


def print_tiles(tiles):
    _ = system('clear')
    min_x = min([x for x, y in tiles.keys()])
    max_x = max([x for x, y in tiles.keys()])
    min_y = min([y for x, y in tiles.keys()])
    max_y = max([y for x, y in tiles.keys()])

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            print(tiles.get((x, y), ' '), end='')
        print()


def start_computer(programme):
    qs = [queue.Queue() for _ in range(2)]
    io = QueueIO(qs[0], qs[1])
    c = IntcodeComputer(programme, f'Arcade', io)
    c.start()
    return qs, c


def update_space(space, x, y, c=' ', screen=None):
    space[(x, y)] = c
    if screen:
        screen.addch(19 - y, 21 + x, c)
        screen.refresh()


def run(programme, screen=None, delay=0):
    qs, computer = start_computer(programme)
    qin, qout = qs

    space = defaultdict(lambda: ' ')
    space[(0, 0)] = '.'

    def talk_to_droid(command):
        qin.put(command)
        return qout.get()

    def explore(x, y, last_move=None):
        time.sleep(delay)
        for direction, (dx, dy) in deltas.items():
            if space[(x + dx, y + dy)] == ' ':
                responce = talk_to_droid(direction)
                if responce == 0:
                    update_space(space, x + dx, y + dy, '#', screen)
                elif responce == 1:
                    update_space(space, x + dx, y + dy, '.', screen)
                    explore(x + dx, y + dy, direction)
                elif responce == 2:
                    update_space(space, x + dx, y + dy, 'O', screen)
                    explore(x + dx, y + dy, direction)
        if last_move:
            move_back = rev_moves[last_move]
            responce = talk_to_droid(move_back)
            assert responce != 0

    try:
        explore(0, 0, None)
    except KeyboardInterrupt:
        space = None
    finally:
        computer.stop()
    return space


def find_o(space):
    my_space = space.copy()
    stack = [(0, 0, 0)]
    while stack:
        length, x, y = stack.pop(0)
        if my_space[(x, y)] == 'O':
            return length
        my_space[(x, y)] = '*'
        for _, (dx, dy) in deltas.items():
            if my_space[(x + dx, y + dy)] in ['.', 'O']:
                stack.append((length + 1, x + dx, y + dy))
    return -1


def find_coords(space, symbol='.'):
    return [coords for coords, t in space.items() if t == symbol]


def fill(space, screen=None, delay=0):
    my_space = space.copy()
    mins = 0
    while len(find_coords(my_space, '.')) > 0:
        time.sleep(delay)
        mins += 1
        for x, y in find_coords(my_space, 'O'):
            for dx, dy in deltas.values():
                if my_space[(x + dx, y + dy)] == '.':
                    update_space(my_space, x + dx, y + dy, 'O', screen)
    return mins


#
# Main
#

programme = parse_programme(read_file(sys.argv[1])[0])

screen = curses.initscr()
curses.curs_set(0)
delay = 0.005

space = run(programme, screen, delay)

if space:
    path_length = find_o(space)
    time_to_fill = fill(space, screen, delay * 2)

curses.endwin()

if not space:
    exit(1)

print_tiles(space)
print(1, path_length)
print(2, time_to_fill)
