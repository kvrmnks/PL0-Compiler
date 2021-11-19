class Procedure:

    def __init__(self, name: str, level: int):
        self.father = ""
        self.name = name
        self.const_dict = dict()
        self.var_dict = dict()
        self.var_offset_counter = 3
        self.level = level
        self.address = -1
        # print("what?")

    def add_cost(self, name: str, value: int):
        if name in self.const_dict:
            print("Error: redefinition in procedure " + self.name + ' of const ' + name)
            exit(-1)
        self.const_dict[name] = value
        print(self.const_dict)

    def add_var(self, name: str):
        if name in self.var_dict:
            print("Error: redefinition in procedure " + self.name + ' of var ' + name)
            exit(-1)
        self.var_dict[name] = (0, self.var_offset_counter)
        self.var_offset_counter += 1
        print(self.var_dict)

    def __str__(self):
        return str(dict({
            'father': self.father,
            'name': self.name,
            'const_dict': self.const_dict,
            'var_dict': self.var_dict,
            'level': self.level
        }))

    def __repr__(self):
        return self.__str__()


class InterRep:
    def __init__(self):
        self.procedure_dict = dict()
        self.current_procedure = Procedure("", 0)

    def add_procedure(self, procedure_name: str, level: int):
        f = self.current_procedure.name
        self.procedure_dict[procedure_name] = Procedure(procedure_name, level)
        self.current_procedure = self.procedure_dict[procedure_name]
        self.current_procedure.father = f

    def add_const(self, name: str, value: int):
        self.current_procedure.add_cost(name, value)

    def add_var(self, name: str):
        self.current_procedure.add_var(name)

    # 按照父亲边寻找变量 or 常量 变量后一位为1 否则为0
    # level 差 值 变量/常量
    def find_by_name(self, name: str) -> (int, (int, int), int):
        tmp_state = self.current_procedure
        while True:
            if name in tmp_state.var_dict:
                return self.current_procedure.level - tmp_state.level, tmp_state.var_dict[name], 1
            if name in tmp_state.const_dict:
                return self.current_procedure.level - tmp_state.level, tmp_state.const_dict[name], 0
            if tmp_state.father == "":
                return None
            else:
                tmp_state = self.procedure_dict[tmp_state.father]

    def __repr__(self):
        return str(dict({
            'procedure_dict': self.procedure_dict,
            'current_procedure': self.current_procedure
        }))

    def __str__(self):
        return self.__repr__()