from agent_parts.chat_history import ChatHistory

from tools.tool_box import ToolBox
from tools.tool_cmd_interface import ToolCmdInterface


class EchoAgent:

    def __init__(self, system_prompt: str, short_name: str = "EchoAgent"):
        """
        This "agent" is just the logic for chat interactions, input, output, branching, etc.
        :param sandbox:
        :param model:
        """
        self.short_name = short_name
        self.chat = ChatHistory()
        self.chat.add_system_message(system_prompt, pinned=True)

    def get_llm_response_to_chat(self) -> dict:
        print("🤔🤔🤔")
        return self.chat.get_messages()[-1]

    def after_llm_response(self):
        """the response has already been added to the chat, """
        pass

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
            print("🔥 cleared context 🔥")
            self.chat.clear()
            return self.get_user_input()

        if user_cmd in ["s", "show"]:
            self.print_chat_state()
            return self.get_user_input()

        if user_cmd in ["m", "multi", "multiline", "large", "start"]:
            print("😂 Ready for large content 🤪")
            user_cmd = self.large_input()

        return user_cmd

    def print_chat_state(self):
        messages = self.chat.get_messages()
        if len(messages) > 10:
            messages = messages[-10:]
            print(f"Showing last 10 messages of {len(messages)}")
        print("\n".join([str(msg) for msg in messages]))

    def run(self, initial_user_message: str = None, nag=False) -> ChatHistory:
        tools = ToolBox(write_sandbox="media/")
        tool_picker = ToolCmdInterface()

        def do_loop(user_input: str) -> None:
            if user_input:
                self.chat.add_user_message(user_input)
            resp = self.get_llm_response_to_chat()
            if not resp:
                print("🤯 No assistant response 🤯")
                return None
            content = resp["content"]
            thoughts = resp.get("thinking")
            tool_calls = resp.get("tool_calls")
            if tool_calls:
                print("🧰 Structured tool calls... what now?")
                return None

            if not content and not thoughts:
                print("🤯 No assistant thoughts or content 🤯")
                return None

            if not content and thoughts:
                """Bro is just thinking and not doing"""
                self.chat.add_user_message(
                    content=f"You thought of this idea:\n💭{thoughts}💭\n\nNOW TAKE ACTION BY executing a tool or replying with content, not thoughts."
                    , pinned=False)
                self.print_chat_state()
                return None

            self.chat.add_assistant_message(content=content, thinking=thoughts, nickname=self.short_name)
            self.print_chat_state()

            tool_commands = tool_picker.parse_tool_requests(resp["content"]) or []
            tool_results = ""
            for tool_cmd in tool_commands:
                tool_result = tools.execute_tool(tool_cmd)
                tool_results += f"Result of {tool_cmd}: {tool_result}"

            self.after_llm_response()

            """Nagging. Maybe if we remind the agent what they are supposed to be doing every message
            they will stay on task"""
            if nag and initial_user_message:
                self.chat.add_system_message(f"Remember, your assignment was specifically: {initial_user_message}. "
                                             f"If this is already complete, respond with 'done'.", pinned=False)

            if tool_results:
                self.chat.add_assistant_message(tool_results, pinned=False)
                self.print_chat_state()
                do_loop('')

            return None

        if initial_user_message:
            do_loop(initial_user_message)

        while True:
            user_input = self.get_user_input()
            if user_input in ["exit", "quit"]:
                break
            do_loop(user_input)

        return self.chat


if __name__ == "__main__":
    ea = EchoAgent(system_prompt="You are a brainless echo agent that just replies with what you are asked.")
    ea.run()
