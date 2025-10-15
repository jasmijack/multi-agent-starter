import os
from typing import List, Dict, Any
from anthropic import Anthropic

def anthropic_llm(model: str | None = None, api_key: str | None = None):
    client = Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
    model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        system = "\n".join(m["content"] for m in messages if m["role"] == "system").strip()
        convo = [m for m in messages if m["role"] in ("user", "assistant")]
        user_content = "\n".join(f'{m["role"]}: {m["content"]}' for m in convo)

        resp = client.messages.create(
            model=model,
            system=system or None,
            max_tokens=params.get("max_tokens", 512),
            temperature=params.get("temperature", 0.2),
            messages=[{"role": "user", "content": user_content}],
        )
        text = "".join(block.text for block in resp.content if getattr(block, "type", "") == "text")
        return text.strip()

    return _llm
