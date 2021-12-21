import fileinput


hexmap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


class Message:
    def __init__(self, msg):
        self.msg = msg
        self.i = 0
        self.size = len(msg)

    def index(self):
        return self.i

    def reset(self):
        self.i = 0

    def read(self, n):
        v = self.msg[self.i: self.i+n]
        self.i += n
        return v

    def read_int(self, n):
        return int(self.read(n), 2)

    def version(self):
        return self.read_int(3)

    def type(self):
        return self.read_int(3)

    def value(self):
        s = ''
        while self.i < self.size:
            cont = self.read_int(1)
            s += self.read(4)
            if cont == 0:
                break
        v = int(s, 2)
        return v

    def op_type(self):
        return self.read_int(1)

    def op_len(self):
        return self.read_int(15)

    def op_count(self):
        return self.read_int(11)


class Packet:
    def __init__(self, version, type):
        self.version = version
        self.type = type
        self.value = None
        self.op = []

    def _get_fun(self):
        funs = {
            0: self._sum,
            1: self._prod,
            2: self._min,
            3: self._max,
            4: self._val,
            5: self._greater,
            6: self._less,
            7: self._equal
        }
        return funs[self.type]

    def sum_ver(self):
        s = self.version
        for p in self.op:
            s += p.sum_ver()
        return s

    def calc(self):
        return self._get_fun()()

    def _sum(self):
        res = self.op[0].calc()
        for p in self.op[1:]:
            res += p.calc()
        return res

    def _prod(self):
        res = self.op[0].calc()
        for p in self.op[1:]:
            res *= p.calc()
        return res

    def _min(self):
        res = self.op[0].calc()
        for p in self.op[1:]:
            res = min(res, p.calc())
        return res

    def _max(self):
        res = self.op[0].calc()
        for p in self.op[1:]:
            res = max(res, p.calc())
        return res

    def _val(self):
        return self.value

    def _greater(self):
        res = self.op[0].calc() > self.op[1].calc()
        return 1 if res else 0

    def _less(self):
        res = self.op[0].calc() < self.op[1].calc()
        return 1 if res else 0

    def _equal(self):
        res = self.op[0].calc() == self.op[1].calc()
        return 1 if res else 0


def parse_input(lines):
    res = []
    for line in lines:
        binary = ''
        for c in line.strip():
            binary += hexmap[c]
        res.append(Message(binary))
    return res


def parse_op(msg):
    res = []
    id = msg.op_type()
    if id == 0:
        op_len = msg.op_len()
        max_idx = msg.index() + op_len
        while msg.index() < max_idx:
            res.append(parse_packet(msg))
    else:
        op_count = msg.op_count()
        for _ in range(op_count):
            res.append(parse_packet(msg))
    return res


def parse_packet(msg):
    ver = msg.version()
    typ = msg.type()
    res = Packet(ver, typ)
    if typ == 4:
        res.value = msg.value()
    else:
        res.op = parse_op(msg)
    return res


def run1(msg):
    p = parse_packet(msg)
    print(p.sum_ver())


def run2(msg):
    p = parse_packet(msg)
    print(p.calc())


lines = list(fileinput.input())
messages = parse_input(lines)

for i, msg in enumerate(messages):
    if i > 0:
        print()
    run1(msg)
    msg.reset()
    run2(msg)
