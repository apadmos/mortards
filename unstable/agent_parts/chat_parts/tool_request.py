class ToolRequest:

    def __init__(self, name: str, args: dict):
        self.name = name
        self.args = args or {}

    def args_length(self) -> int:
        return len(self.args)

    def get_first_arg(self):
        return next(iter(self.args.values()))

    def get(self, names: str, required: bool = False):
        names = names.split(',')
        for name in names:
            if name in self.args:
                return self.args[name]
        if required:
            raise ValueError(f"Provide at least one of the arguments {names}")
        return None
