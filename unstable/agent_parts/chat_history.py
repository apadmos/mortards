import datetime

from agent_parts.chat_message import ChatMessage


class ChatHistory:

    def __init__(self):
        self._messages = []
        self._pinned_messages = []
        self.clear()

    def add_message(self, message: ChatMessage):
        if not message.timestamp:
            message.timestamp = datetime.datetime.now()
        self._messages.append(message)

    def add_user_message(self, content:str, pinned:bool=False):
        self.add_message(ChatMessage(content, role="user", pinned=pinned))

    def add_assistant_message(self, content:str, thinking:str=None, pinned:bool=False):
        self.add_message(ChatMessage(content, role="assistant", thinking=thinking,  pinned=pinned))

    def add_system_message(self, content:str, pinned:bool=True):
        self.add_message(ChatMessage(content, role="system", pinned=pinned))

    def get_messages(self):
        c = self._pinned_messages + self._messages
        return c

    def clear(self, include_pinned:bool=False):
        self._messages = []
        if include_pinned:
            self._pinned_messages = []


    def replace_all(self, message: ChatMessage, include_pinned:bool=False):
        self.clear(include_pinned=include_pinned)
        self.add_message(message)

    def remove_last(self, count: int = 1):
        if count <= 0 or not self._messages:
            return
        self._messages = self._messages[:-count]

    def replace_last(self, message: ChatMessage, count: int = 1):
        self.remove_last(count)
        self.add_message(message)