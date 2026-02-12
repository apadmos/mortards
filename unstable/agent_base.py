import os

import requests

from tool_interface import ToolInterface, InterfaceException


class BaseChatAgent:
    OLLAMA_URL = "http://localhost:11434/api/chat"

    def __init__(self, sandbox, model):
        self.model = model
        self.sandbox = os.path.abspath(sandbox)
        if not os.path.isdir(self.sandbox):
            raise ValueError(f"{self.sandbox} is not a valid directory")

        self.messages = []
        self.tools = ToolInterface(sandbox=self.sandbox)
        self._init_system_message()

    def _init_system_message(self):
        self.messages.append({
            "role": "system",
            "content": self.system_prompt(),
        })

    def system_prompt(self):
        raise NotImplementedError

    def chat_request(self, messages, stream=False):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
        }
        resp = requests.post(self.OLLAMA_URL, json=payload, timeout=600)
        resp.raise_for_status()
        return resp.json()

    def assistant_response(self):
        print("🤔🤔🤔")
        r = self.chat_request(self.messages)
        prompt_tokens = r.get('prompt_eval_count', 0)
        completion_tokens = r.get('eval_count', 0)
        total_tokens = prompt_tokens + completion_tokens
        if total_tokens > 10000:
            print(f"🤯 Is this too many tokens? 🤯 {total_tokens} - do we need to trim the chat history?")

        return str(r["message"]["content"]).strip()

    def large_input(self):
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

    def input_cmd(self):
        user_cmd = input("😎😕🤔: ")
        if user_cmd == "clear":
            print("🔥 cleared context 🔥")
            self.messages.clear()
            self._init_system_message()
            return self.input_cmd()
        if user_cmd == "exit":
            return "exit"

        if user_cmd in ["s", "show"]:
            self.print_chat_state()
            return self.input_cmd()

        if user_cmd in ["m", "multi", "multiline", "large", "start"]:
            print("😂 Ready for large content 🤪")
            user_cmd = self.large_input()

        return self.add_user_message(user_cmd)

    def add_user_message(self, message):
        d = {
            "role": "user",
            "content": message,
        }
        self.messages.append(d)
        print(f"🫠 echo:  {message}")
        return d

    def add_assistant_message(self, message):
        d = {
            "role": "assistant",
            "content": message,
        }
        self.messages.append(d)
        print(f"🤖 echo:  {message}")
        return d

    def handle_json_blocks(self, json_blocks):
        did_something = False

        for json_block in json_blocks:
            action, output = self.tools.execute_block(json_block)
            if output:
                out_message = (
                    f"Result of `{action}({list(json_block['parameters'].values())!r})`:\n\n{output}"
                )
                self.add_user_message(out_message)
                did_something = True

        return did_something

    def handle_tools(self, assistant_msg) -> bool:
        did_something = False
        python_results = self.tools.execute_python_blocks(assistant_msg)
        if python_results:
            all_results = "\n".join(python_results)
            self.add_user_message(all_results)
            did_something = True
        try:
            json_blocks = self.tools.parse_json_blocks(assistant_msg)
            if self.handle_json_blocks(json_blocks):
                did_something = True

        except InterfaceException as e:
            self.add_user_message(e.suggested_message)
            print(e.suggested_message)
            return True

        except Exception as e:
            uh_oh = f"A generic error occurred: {e}. What should we do next?"
            self.add_user_message(uh_oh)
            print(uh_oh)
            return True
        return did_something

    def print_chat_state(self):
        print(self.messages)

    def run(self, initial_user_message: str = None, max_idle_loops=10):
        print(f"Using sandbox: {self.sandbox}")
        print(f"Using model: {self.model}")
        print(f"Initial chat content:")
        self.print_chat_state()
        if initial_user_message:
            last_input = self.add_user_message(initial_user_message)
        else:
            last_input = self.input_cmd()
        last_output = None

        idle = 0
        while idle < max_idle_loops and last_input != "exit":
            last_output = self.assistant_response()

            if not last_output:
                print("🤯 No assistant response 🤯")
                return last_output

            idle = 0
            self.add_assistant_message(last_output)

            if self.handle_tools(last_output):
                continue

            last_input = self.input_cmd()
        return last_output
