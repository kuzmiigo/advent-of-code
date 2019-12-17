import logging
import queue
import sys
from abc import ABC, abstractmethod
from collections import defaultdict
from threading import Thread


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

turns = {
    'L': ('D', 'U'),
    'R': ('U', 'D'),
    'U': ('L', 'R'),
    'D': ('R', 'L')
}

deltas = {
    'L': (-1, 0),
    'R': (1, 0),
    'U': (0, -1),
    'D': (0, 1)
}


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


def run(programme, vacuum_prog=None):
    if vacuum_prog:
        programme[0] = 2
    qs, computer = start_computer(programme)
    qin, qout = qs
    if vacuum_prog:
        for code in vacuum_prog:
            qin.put(code)
        qin.put(110)  # 'n'
        qin.put(10)
    output = ''
    result = None
    while computer.is_running() or not qout.empty():
        c = qout.get()
        if c < 256:
            output += chr(c)
        else:
            output += str(c)
            result = c
    return output, result


def parse_screen(camera_output):
    screen = {}
    for y, line in enumerate(camera_output.split()):
        for x, c in enumerate(line):
            if c != '.':
                screen[(x, y)] = c
    return screen


def find_alignments(screen):
    scaffold = set(screen.keys())
    intersections = []
    for s in scaffold:
        x, y = s
        n = [(x + dx, y + dy) for dx, dy in deltas.values()]
        if len(scaffold.intersection(n)) > 2:
            intersections.append(s)
    return sum([x * y for x, y in intersections])


# Works only when single turns (left or right) are needed.
def select_turn(screen, x, y, direction):
    for i, turn in enumerate(['L', 'R']):
        new_direction = turns[direction][i]
        dx, dy = deltas[new_direction]
        if screen.get((x + dx, y + dy)) == '#':
            return turn, new_direction
    return None, None


# Simple strategy that works for this puzzle.
def find_path(screen):
    x, y = [k for k, v in screen.items() if v == '^'][0]
    output = []
    direction = 'U'
    seen = set()
    seen.add((x, y))
    while direction:
        dx, dy = deltas[direction]
        steps = 0
        while screen.get((x + dx, y + dy)) == '#':
            x, y = x + dx, y + dy
            seen.add((x, y))
            steps += 1
        if steps > 0:
            output.append(str(steps))
        turn, direction = select_turn(screen, x, y, direction)
        if turn:
            output.append(turn)
    if seen != set(screen.keys()):
        print('Warning: incomplete path!')
    return output


def convert_vacuum_prog(prog_source):
    return [ord(d) for d in '\n'.join(prog_source + [''])]


#
# Init
#

programme = parse_programme(read_file(sys.argv[1])[0])

#
# Part 1
#

camera_scan, _ = run(programme)
print(camera_scan)
screen = parse_screen(camera_scan)
alignment = find_alignments(screen)
print(1, alignment)

#
# Part 2
#

# TODO: Use code to convert the found path into a program for the vacuum robot.
# For now, it was done manually.
# vacuum_prog_source = ','.join(find_path(screen))
# print(vacuum_prog_source)

vacuum_prog_source = [
    'A,B,A,C,B,A,C,B,A,C',
    'L,12,L,12,L,6,L,6',
    'R,8,R,4,L,12',
    'L,12,L,6,R,12,R,8'
]

vacuum_prog = convert_vacuum_prog(vacuum_prog_source)
output, dust = run(programme, vacuum_prog)
# print(output)
print(2, dust)
