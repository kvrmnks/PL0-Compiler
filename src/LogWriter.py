class Command:
    def __init__(self, cmd: str, level: int, num: int):
        self.cmd = cmd
        self.level = level
        self.num = num


class LogWriter:
    def __init__(self, path: str):
        self.f = open(path, 'w')
        self.total_line = 0
        self.cmd_arr = []

    def flush(self):
        for x in self.cmd_arr:
            self.f.write(x.cmd + ' ' + str(x.level) + ' ' + str(x.num) + '\n')
            # self.f.write()

    def write(self, cmd: str, level: int, num: int):
        self.cmd_arr.append(Command(cmd, level, num))
        self.total_line += 1

    def bwrite(self, *args):
        self.total_line += 1
        for x in args:
            self.f.write(str(x))
            self.f.write(' ')
        self.f.write("\n")
