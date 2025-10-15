import os
from typing import List, Dict, Any
import anthropic

def anthropic_llm(model: str | None = None, api_key: str | None = None):
    client = anthropic.Client(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        # Convert OpenAI-style messages to Anthropic format
        system = ""
        user_turns = []
        for m in messages:
            if m["role"] == "system":
                system += m["content"] + "\n"
            elif m["role"] in ("user", "assistant"):
                user_turns.append({"role": m["role"], "content": m["content"]})
        # Build a single user prompt interleaving prior roles for simplicity
        content = "\n".join([f'{m["role"]}: {m["content"]}' for m in user_turns])
        resp = client.messages.create(
            model=model,
            max_tokens= params.get("max_tokens", 512),
            temperature=params.get("temperature", 0.2),
            system=system.strip(),
            messages=[{"role": "user", "content": content}]
        )
        # Anthropic returns a list of content blocks
        text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
        return text.strip()
    return _llm
