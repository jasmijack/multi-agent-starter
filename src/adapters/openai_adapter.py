import os
from typing import List, Dict, Any
from openai import OpenAI

def openai_llm(model: str | None = None, api_key: str | None = None):
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 512),
        )
        return (resp.choices[0].message.content or "").strip()
    return _llm
