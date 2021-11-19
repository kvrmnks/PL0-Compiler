class LogWriter:
    def __init__(self, path: str):
        self.f = open(path, 'w')

    def write(self, *args):
        for x in args:
            self.f.write(str(x))
            self.f.write(' ')
        self.f.write("\n")
