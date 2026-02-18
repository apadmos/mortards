import os


class FlexiArgs:

    def __init__(self, args:dict):
        self.args = args

    def get(self, names:str):
        names = names.split(',')
        for name in names:
            if name in self.args:
                return self.args[name]
        return None
