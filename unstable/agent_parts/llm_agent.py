from agent_parts.chat_parts.chat_history import ChatHistory
from agent_parts.chat_parts.chat_message import ChatMessage
from agent_parts.user_interface.console_interface import ConsoleInterface

from tools.tool_box import ToolBox


class LLMAgent:

    def __init__(self, system_prompt: str, llm_interface, chat_length: int = 1000):
        """
        This "agent" is just the logic for chat interactions, input, output, branching, etc.
        :param sandbox:
        :param model:
        """
        self.llm_interface = llm_interface
        self.user_interface = ConsoleInterface()
        self.chat = ChatHistory()
        self.chat_length = chat_length
        self.chat.add_system_message(system_prompt, pinned=True)

    def print_chat_state(self):
        messages = self.chat.get_messages()
        if len(messages) > 10:
            messages = messages[-10:]
            print(f"Showing last 10 messages of {len(messages)}")
        print("\n".join([str(msg) for msg in messages]))

    def run(self, initial_user_message: str = None, nag=False) -> ChatHistory:
        tools = ToolBox(write_sandbox="media/")

        def do_loop(user_input: str) -> None:
            self.chat.trim_to(self.chat_length)
            if user_input:
                self.chat.add_user_message(user_input)
            resp = self.llm_interface.send_chat(self.chat)
            if not resp:
                print("🤯 No assistant response 🤯")
                return None
            resp: ChatMessage = self.llm_interface.parse_response(resp)

            if resp.tool_calls:
                print("🧰 Structured tool calls... what now?")
                return None

            if not resp.message and not resp.thinking:
                print("🤯 No assistant thoughts or content 🤯")
                return None

            self.chat.add_message(resp)
            self.print_chat_state()

            """Nagging. Maybe if we remind the agent what they are supposed to be doing every message
            they will stay on task"""
            if nag and initial_user_message:
                self.chat.add_system_message(f"Remember, your assignment was specifically: {initial_user_message}. "
                                             f"If this is already complete, respond with 'done'.", pinned=False)
            return None

        if initial_user_message:
            do_loop(initial_user_message)

        while True:
            user_input = self.user_interface.get_user_input()
            if user_input == "quit":
                break
            if user_input == "show":
                self.print_chat_state()
                continue
            do_loop(user_input)

        return self.chat


if __name__ == "__main__":
    ea = LLLMAgent(system_prompt="You are a brainless echo agent that just replies with what you are asked.")
    ea.run()
