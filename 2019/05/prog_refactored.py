import fileinput

DEBUG = False
MAX_OPERATIONS = 1000


class IntcodeComputer:
    def __init__(self, programme):
        p = [int(x) for x in programme.split(',')]
        self._state = dict(enumerate(p))
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

    def dump(self, msg=None):
        if msg:
            print(msg, end=' ')
        print(f'pointer: {self._pointer}, state: {self._state}')

    def _debug(self, msg=None):
        if DEBUG:
            self.dump(msg)

    def _error(self, msg=None):
        if msg:
            print('ERROR', msg)
        self.dump('ERROR')

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
        x = int(input("Enter a number: "))
        self._state[dst] = x
        return True

    def _op_out(self):
        print(self._next_arg())
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


lines = list(filter(lambda s: s.strip(), fileinput.input()))
for line in lines:
    if len(lines) > 1:
        print('Running programme:')
        print(line)
    computer = IntcodeComputer(line)
    computer.run()
    print('')
