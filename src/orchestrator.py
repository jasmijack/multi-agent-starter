from __future__ import annotations
from typing import Dict, Callable, List, Optional, Tuple
import time
from .core import Message, new_id
from .router import Router

class Orchestrator:
    def __init__(self, agents: Dict[str, any], router: Router,
                 max_turns: int = 8, wallclock_s: int = 30,
                 success_fn: Optional[Callable[[List[Message]], bool]] = None):
        self.agents = agents
        self.router = router
        self.max_turns = max_turns
        self.wallclock_s = wallclock_s
        self.success_fn = success_fn or (lambda msgs: any("final_answer:" in m.content.lower() for m in msgs))
        self.bus: List[Message] = []

    def post(self, msg: Message):
        self.bus.append(msg)

    def inbox_for(self, name: str) -> List[Message]:
        return [m for m in self.bus if m.recipient in (name, "all", "router")]

    def run(self, task_prompt: str) -> Tuple[List[Message], Optional[str]]:
        start = time.time()
        first = Message(id=new_id(), sender="user",
                        recipient=self.router.next_recipient(None),
                        content=task_prompt)
        self.post(first)

        last = None
        for _ in range(self.max_turns):
            if time.time() - start > self.wallclock_s:
                self.post(Message(id=new_id(), sender="system", recipient="all",
                                  content="Timeout reached", metadata={"stop": True}))
                break

            recipient = self.bus[-1].recipient
            if recipient == "stop":
                break
            if recipient not in self.agents:
                recipient = self.router.next_recipient(last)

            agent = self.agents[recipient]
            out = agent.step(self.inbox_for(agent.name))
            out.recipient = self.router.next_recipient(out)
            self.post(out)
            last = out

            if self.success_fn(self.bus):
                break

        final = next((m.content for m in reversed(self.bus) if "final_answer:" in m.content.lower()), None)
        if not final and self.bus:
            final = self.bus[-1].content
        return self.bus, final
