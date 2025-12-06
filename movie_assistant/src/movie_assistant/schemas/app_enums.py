from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class ChatRole(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
