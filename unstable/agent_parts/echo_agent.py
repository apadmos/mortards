import os

import requests

from agent_parts.chat_history import ChatHistory


class EchoAgent:

    def __init__(self, system_prompt:str):
        """
        This "agent" is just the logic for chat interactions, input, output, branching, etc.
        :param sandbox:
        :param model:
        """
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

    def run(self, initial_user_message: str = None) -> ChatHistory:

        def do_loop(user_input:str) -> None:
            self.chat.add_user_message(user_input)
            resp = self.get_llm_response_to_chat()
            if not resp:
                print("🤯 No assistant response 🤯")
                return None
            self.chat.add_assistant_message(resp["content"], resp.get("thinking"))
            self.print_chat_state()
            self.after_llm_response()
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