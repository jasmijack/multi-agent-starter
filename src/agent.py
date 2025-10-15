from __future__ import annotations
from typing import Dict, Any, List, Optional, Callable
import json

from .core import Message, new_id, Tool, Memory
from tools.calculator import Calculator

LLMFn = Callable[[List[Dict[str, str]], Dict[str, Any]], str]


class Agent:
    def __init__(
        self,
        name: str,
        system_prompt: str,
        llm: LLMFn,
        tools: Optional[List[Tool]] = None,
        memory: Optional[Memory] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = llm
        self.tools = {t.name: t for t in (tools or [])}
        self.memory = memory or Memory()
        self.params = params or {"temperature": 0.2}

    def call_llm(self, messages: List[Dict[str, str]]) -> str:
        return self.llm(messages, self.params)

    def tool_call(self, name: str, **kwargs) -> str:
        if name not in self.tools:
            raise ValueError(f"Tool not found: {name}")
        return str(self.tools[name](**kwargs))

    def step(self, inbox: List[Message]) -> Message:
        # Build chat context
        chat = [{"role": "system", "content": self.system_prompt}]
        for m in inbox[-8:]:
            role = "user" if m.sender != self.name else "assistant"
            chat.append({"role": role, "content": f"{m.sender}: {m.content}"})

        reply = self.call_llm(chat)
        self.memory.add({"type": "reply", "agent": self.name, "text": reply})

        # Optional JSON tool protocol: {"tool":"calculator","args":{"expr":"7*6"}}
        tool_out: Optional[str] = None
        try:
            s = reply.strip()
            if s.startswith("{") and s.endswith("}"):
                obj = json.loads(s)
                if "tool" in obj and "args" in obj:
                    tool_out = self.tool_call(obj["tool"], **obj["args"])
        except Exception as e:
            tool_out = f"Tool error: {e}"

        if tool_out is None:
            content = reply
        else:
            # Include tool result and ensure a final_answer is present
            content = f"{reply}\n\ntool result: {tool_out}"
            if "final_answer" not in reply.lower():
                content += f"\nfinal_answer: {tool_out}"

        return Message(
            id=new_id(),
            sender=self.name,
            recipient="router",
            content=content,
            metadata={"type": "agent_update"},
        )


def make_researcher(llm: LLMFn) -> Agent:
    prompt = (
        "You are Researcher. Produce concise, factual notes. "
        "If arithmetic is needed, emit a JSON tool call like "
        '{"tool":"calculator","args":{"expr":"7*6"}} then include the result. '
        "When solved, add the line 'final_answer: <text>'."
    )
    return Agent("Researcher", prompt, llm, tools=[Calculator()])


def make_critic(llm: LLMFn) -> Agent:
    prompt = (
        "You are Critic. Review the latest result, point out gaps, and suggest fixes. "
        "If acceptable, say 'Looks good. final_answer: <concise answer>'."
    )
    return Agent("Critic", prompt, llm)
