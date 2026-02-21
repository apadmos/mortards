class ToolRequest:

    def __init__(self, name: str, args: dict, call_id=None):
        self.name = name
        self.args = args or {}
        self.call_description = call_id or self.description()

    def description(self) -> str:
        return f"{self.name}({", ".join([f"{k}={v}" for k, v in self.args.items()])})"

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

    def __str__(self):
        return self.description()
