class ConsoleInterface:

    def large_input(self) -> str:
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line in ["EOF", "exit", "end", "done"]:
                break
            lines.append(line)
        return "\n".join(lines)

    def get_user_input(self):
        user_cmd = input("😎😕🤔: ")
        if user_cmd == "clear":
            return "clear"

        if user_cmd in ["s", "show"]:
            return "show"

        if user_cmd in ["quit", "exit", "x", "q"]:
            return "quit"

        if user_cmd in ["m", "multi", "multiline", "large", "start"]:
            print("😂 Ready for large content 🤪")
            user_cmd = self.large_input()

        return user_cmd
