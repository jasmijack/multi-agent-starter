# adapters/openai_adapter.py
import os
from typing import List, Dict, Any

def openai_llm(model: str | None = None, api_key: str | None = None):
    """
    Returns a callable LLM(messages, params) -> str.
    Safe for CI: does not import or create an SDK client until actually called.
    """

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        # Lazy import so CI without openai installed doesn't break unless this is actually used
        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError(
                "OpenAI SDK not available. Install it (e.g., `pip install openai>=2.3.0`) "
                "or avoid calling this adapter in CI."
            ) from e

        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY. Set it in your environment or pass api_key to openai_llm()."
            )

        client = OpenAI(api_key=key)
        model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        resp = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 512),
        )
        return (resp.choices[0].message.content or "").strip()

    return _llm
