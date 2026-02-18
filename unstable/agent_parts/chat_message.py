import datetime
class ChatMessage:

    def __init__(self, message: str, role: str, thinking:str=None, nickname:str=None, timestamp: datetime.datetime = None, pinned:bool=False):
        self.message = message
        self.thinking = thinking
        self.role = role
        self.timestamp = timestamp
        self.nickname = nickname or ''
        self.pinned = pinned

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
        return {
            "role": self.role,
            "content": self.message,
        }
