import datetime

from agent_parts.chat_parts.tool_request import ToolRequest


class ChatMessage:

    def __init__(self, message: str, role: str, thinking: str = None, nickname: str = None,
                 timestamp: datetime.datetime = None,
                 tool_calls: list[ToolRequest] = None,
                 pinned: bool = False, raw=None):
        self.message = message
        self.thinking = thinking
        self.role = role
        self.timestamp = timestamp
        self.nickname = nickname or ''
        self.pinned = pinned
        self.raw = raw
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
            base_str += f"\n💭{self.thinking}💭"
        for t in self.tool_calls:
            base_str += f"\n🔧{t}🔧"
        if self.raw:
            base_str += f"\n{self.raw}"
        return base_str

    def __str__(self):
        return self.__repr__()

    def to_ollama_dict(self):
        if self.raw:
            return self.raw
        d = {
            "role": self.role,
            "content": self.message,
            "thinking": self.thinking,
        }
        return d
