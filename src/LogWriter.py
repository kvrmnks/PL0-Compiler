class LogWriter:
    def __init__(self, path: str):
        self.f = open(path, 'w')
        self.total_line = 0

    def write(self, *args):
        self.total_line += 1
        for x in args:
            self.f.write(str(x))
            self.f.write(' ')
        self.f.write("\n")
