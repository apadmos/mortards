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
        unsupervised_limit = 2

        def do_loop(user_input: str, unsupervised_count: int) -> None:
            self.chat.trim_to(self.chat_length)
            if user_input:
                self.chat.add_user_message(user_input)
            resp = self.llm_interface.send_chat(self.chat)
            if not resp:
                print("🤯 No assistant response 🤯")
                return None

            resp: ChatMessage = self.llm_interface.parse_response(resp)
            self.chat.add_message(resp)
            if resp.tool_calls:
                self.print_chat_state()
                tool_results = "TOOL CALL RESULTS:\n"
                for tc in resp.tool_calls:
                    result = tools.execute_tool(tc)
                    tool_results += f"{tc.call_description}: {result}\n"
                self.chat.add_system_message(tool_results, pinned=False)
                self.print_chat_state()
                if unsupervised_count < unsupervised_limit:
                    return do_loop("", unsupervised_count + 1)
                else:
                    print("-----------The machine is going wild. Press Enter to continue, or say something-------")
                    return None

            if not resp.message and not resp.thinking:
                print("🤯 No assistant thoughts or content 🤯")
                return None

            self.print_chat_state()

            """Nagging. Maybe if we remind the agent what they are supposed to be doing every message
            they will stay on task"""
            if nag and initial_user_message:
                self.chat.add_system_message(f"Remember, your assignment was specifically: {initial_user_message}. "
                                             f"If this is already complete, respond with 'done'.", pinned=False)
            return None

        if initial_user_message:
            do_loop(initial_user_message, 0)

        while True:
            user_input = self.user_interface.get_user_input()
            if user_input == "clear":
                print("🔥 cleared context 🔥")
                self.chat.clear()
                continue

            if user_input == "quit":
                break
            if user_input == "show":
                self.print_chat_state()
                continue
            do_loop(user_input, 0)

        return self.chat
