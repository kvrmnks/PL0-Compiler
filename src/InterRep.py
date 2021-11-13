class Procedure:

    def __init__(self, name: str):
        self.father = ""
        self.name = name
        self.const_dict = dict()
        self.var_dict = dict()
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
        self.var_dict[name] = 0
        print(self.var_dict)

    def __str__(self):
        return str(dict({
            'father': self.father,
            'name': self.name,
            'const_dict': self.const_dict,
            'var_dict': self.var_dict
        }))

    def __repr__(self):
        return self.__str__()


class InterRep:
    def __init__(self):
        self.procedure_dict = dict()
        self.current_procedure = Procedure("")

    def add_procedure(self, procedure_name: str):
        f = self.current_procedure.name
        self.procedure_dict[procedure_name] = Procedure(procedure_name)
        self.current_procedure = self.procedure_dict[procedure_name]
        self.current_procedure.father = f

    def add_const(self, name: str, value: int):
        self.current_procedure.add_cost(name, value)

    def add_var(self, name: str):
        self.current_procedure.add_var(name)

    def __repr__(self):
        return str(dict({
            'procedure_dict': self.procedure_dict,
            'current_procedure': self.current_procedure
        }))

    def __str__(self):
        return self.__repr__()