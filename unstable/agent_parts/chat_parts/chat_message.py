import datetime

from agent_parts.chat_parts.tool_request import ToolRequest


class ChatMessage:

    def __init__(self, message: str, role: str, thinking: str = None, nickname: str = None,
                 timestamp: datetime.datetime = None,
                 tool_calls: list[ToolRequest] = None,
                 pinned: bool = False):
        self.message = message
        self.thinking = thinking
        self.role = role
        self.timestamp = timestamp
        self.nickname = nickname or ''
        self.pinned = pinned
        self.tool_calls: list[ToolRequest] = tool_calls or []

    def __repr__(self):
        pinned_str = "[pinned]" if self.pinned else ""
        icon_str = "⚙️"
        if self.role == "assistant":
            icon_str = "🤖"
        elif self.role == "user":
            icon_str = "🫠"
        base_str = f"{icon_str}{self.nickname}{pinned_str}:{self.message}"
        if self.thinking:
            return f"{base_str}\n💭{self.thinking}💭"
        return base_str

    def __str__(self):
        return self.__repr__()

    def to_ollama_dict(self):
        d = {
            "role": self.role,
            "content": self.message,
        }
        return d
