class StackEntry:
    def __init__(self, num: int, hint: str):
        self.value = num
        self.hint = hint

    def __str__(self):
        return '[value: {0}, hint: {1}]'.format(self.value, self.hint)

    def __repr__(self):
        return self.__str__()


class Simulator:
    def __init__(self, code: [str]):

        self.codes = [(x.split(" ")[0].lower(), int(x.split(" ")[1]), int(x.split(" ")[2])) for x in
                      code]  # type: list[(str, int, int)]
        self.stack = []  # type: list[StackEntry]
        self.init_counter = []  # type: list[int]
        # self.instruction_pointer = 0
        self.program_pointer = 0
        # self.stack_pointer = 0
        self.base_point = 0
        print(self.codes)

    def step(self) -> bool:
        if self.program_pointer >= len(self.codes):
            return False
        cmd = self.codes[self.program_pointer]

        # print(cmd)
        # print(self.stack)
        # print(self.base_point)
        self.program_pointer += 1
        if cmd[0] == 'jmp':
            self.program_pointer = cmd[2]
        elif cmd[0] == 'lod':
            if cmd[1] > 1:
                print('not permitted for visiting level ' + cmd[1])
                return False
                # exit(-1)
            tmp_base = self.base_point
            for i in range(cmd[1]):
                tmp_base = self.stack[tmp_base].value
            self.stack.append(StackEntry(self.stack[tmp_base + cmd[2]].value, 'lod'))
        elif cmd[0] == 'sto':
            if cmd[1] > 1:
                print('not permitted for visiting level ' + cmd[1])
                return False
                # exit(-1)
            tmp_base = self.base_point
            for i in range(cmd[1]):
                tmp_base = self.stack[tmp_base].value
            self.stack[tmp_base + cmd[2]] = self.stack[-1]
            self.stack[tmp_base + cmd[2]].hint = 'sto'
            self.stack = self.stack[:-1]  # type: list[StackEntry]
        elif cmd[0] == 'lit':
            self.stack.append(StackEntry(cmd[2], 'lit'))

        elif cmd[0] == 'jpc':
            if self.stack[-1].value == 0:
                self.program_pointer = cmd[2]
            self.stack.pop()

        elif cmd[0] == 'call':
            if cmd[1] > 1:
                print('not permitted for visiting level ' + cmd[1])
                return False
                # exit(-1)
            tmp_base = self.base_point
            for i in range(cmd[1]):
                tmp_base = self.stack[tmp_base].value
            lr = len(self.stack)
            self.stack.append(StackEntry(tmp_base, 'call_0'))
            self.stack.append(StackEntry(self.base_point, 'call_1?'))
            self.stack.append(StackEntry(self.program_pointer, 'call_2'))
            self.base_point = len(self.stack) - 3
            self.program_pointer = cmd[2]

        elif cmd[0] == 'int':
            for i in range(cmd[2]):
                self.stack.append(StackEntry(0, 'int'))
            self.init_counter.append(cmd[2])
        elif cmd[0] == 'opr' and cmd[2] == 0:
            lr = self.stack[self.base_point + 1].value
            if self.base_point == 0 and self.stack[self.base_point].value == 0:
                print('terminated')
                return False
            self.program_pointer = self.stack[self.base_point + 2].value
            self.base_point = self.stack[self.base_point + 1].value
            self.stack = self.stack[:-self.init_counter[-1]]
            self.init_counter.pop()
            self.stack = self.stack[:-3]

        elif cmd[0] == 'opr' and cmd[2] == 1:  # contrary
            self.stack[-1].value = -self.stack[-1].value
        elif cmd[0] == 'opr' and cmd[2] == 2:  # +
            self.stack[-2].value = self.stack[-2].value + self.stack[-1].value
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 3:  # -
            self.stack[-2].value = self.stack[-2].value - self.stack[-1].value
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 4:  # *
            self.stack[-2].value = self.stack[-2].value * self.stack[-1].value
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 5:  # /
            self.stack[-2].value = self.stack[-2].value // self.stack[-1].value
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 6:  # odd
            self.stack[-1].value = self.stack[-1].value % 2
            self.stack[-1].value = 1 - self.stack[-1].value
        elif cmd[0] == 'opr' and cmd[2] == 8:  # eq
            self.stack[-2].value = self.stack[-2].value - self.stack[-1].value
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 9:  # neq
            self.stack[-2].value = self.stack[-2].value - self.stack[-1].value
            if self.stack[-2].value != 0:
                self.stack[-2].value = 0
            elif self.stack[-2].value == 0:
                self.stack[-2].value = 1
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 10:  # less than
            self.stack[-2].value = self.stack[-2].value - self.stack[-1].value
            if self.stack[-2].value < 0:
                self.stack[-2].value = 0
            else:
                self.stack[-2].value = 1
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 11:  # greater than or qe
            self.stack[-2].value = - self.stack[-2].value + self.stack[-1].value
            if self.stack[-2].value <= 0:
                self.stack[-2].value = 0
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 12:  # greater than
            self.stack[-2].value = - self.stack[-2].value + self.stack[-1].value
            if self.stack[-2].value < 0:
                self.stack[-2].value = 0
            else:
                self.stack[-2].value = 1
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 13:  # less than or qe
            self.stack[-2].value = self.stack[-2].value - self.stack[-1].value
            if self.stack[-2].value <= 0:
                self.stack[-2].value = 0
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 14:  # write
            print(self.stack[-1].value)
            self.stack.pop()
        elif cmd[0] == 'opr' and cmd[2] == 16:  # read
            print('now read:')
            x = int(input())
            self.stack.append(StackEntry(x, 'read'))
        else:
            print('what is this?')
            return False
        return True

    def reset(self):
        self.stack = []  # type: list[StackEntry]
        # self.instruction_pointer = 0
        self.program_pointer = 0
        # self.stack_pointer = 0
        self.base_point = 0

    def debug_mode(self):
        _r = self.step()
        while _r:
            # input()
            print(self.codes[self.program_pointer])
            _r = self.step()
            print([(i, x) for (i, x) in reversed(list(enumerate(self.stack)))], '\n pc: ', self.program_pointer,
                  '\n ss: ', self.base_point)
            print('\n')

    def release_mode(self):

        _r = self.step()
        while _r:
            # input()
            _r = self.step()
            # print(self.stack, self.program_pointer)


if __name__ == '__main__':
    codes = list(filter(lambda x: x != "", open('abab.txt').read().split('\n')))
    s = Simulator(codes)
    # s.debug_mode()
    s.release_mode()
