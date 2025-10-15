from .core import Message

class Router:
    def __init__(self, agent_order):
        self.agent_order = agent_order
        self.idx = 0

    def next_recipient(self, last_message: Message | None) -> str:
        if last_message and last_message.metadata.get("stop") is True:
            return "stop"
        name = self.agent_order[self.idx]
        self.idx = (self.idx + 1) % len(self.agent_order)
        return name
