import datetime
class ChatMessage:

    def __init__(self, message: str, role: str, timestamp: datetime.datetime = None, pinned:bool=False):
        self.message = message
        self.role = role
        self.timestamp = timestamp
        self.pinned = pinned

    def __repr__(self):
        pinned_str = "[pinned]" if self.pinned else ""
        icon_str = "⚙️"
        if self.role == "assistant":
            icon_str = "🤖"
        elif self.role == "user":
            icon_str = "🫠"
        return f"{icon_str}{pinned_str}:{self.message}"

