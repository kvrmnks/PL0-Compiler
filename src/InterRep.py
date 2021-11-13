class Procedure:
    def __int__(self, name: str):
        self.father = None
        self.name = name
        self.const_dict = dict()
        self.var_dict = dict()

    def __init__(self, name: str, f):
        self.name = name
        self.father = f
        self.const_dict = dict()
        self.var_dict = dict()


class InterRep:
    def __init__(self):
        self.procedure_dict = dict()
        self.current_procedure = None

    def add_procedure(self, procedure_name: str, father: str):
        if father == "":
            self.procedure_dict[procedure_name] = Procedure(procedure_name)
            self.current_procedure = self.procedure_dict[procedure_name]
        else:
            self.procedure_dict[procedure_name] = Procedure(procedure_name, self.procedure_dict[father])
            self.current_procedure = self.procedure_dict[procedure_name]
