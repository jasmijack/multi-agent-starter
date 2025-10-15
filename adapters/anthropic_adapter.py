# adapters/anthropic_adapter.py
import os
from typing import List, Dict, Any

def anthropic_llm(model: str | None = None, api_key: str | None = None):
    """
    Returns a callable LLM(messages, params) -> str.
    CI-safe: no Anthropic import or client creation until the function is actually called.
    """

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        # Lazy import so test environments without the SDK don't fail unless used
        try:
            from anthropic import Anthropic
        except Exception as e:
            raise RuntimeError(
                "Anthropic SDK not available. Install it (e.g., `pip install anthropic>=0.70.0`) "
                "or avoid calling this adapter in CI."
            ) from e

        key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "Missing ANTHROPIC_API_KEY. Set it in your environment or pass api_key to anthropic_llm()."
            )

        client = Anthropic(api_key=key)
        model_name = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")

        # Fold OpenAI-style history into a single user turn + optional system
        system_text = "\n".join(m["content"] for m in messages if m["role"] == "system").strip()
        convo = [m for m in messages if m["role"] in ("user", "assistant")]
        user_content_text = "\n".join(f'{m["role"]}: {m["content"]}' for m in convo).strip()

        # Some SDK versions accept str, others prefer blocks. Use blocks for compatibility.
        user_blocks = [{"type": "text", "text": user_content_text or " "}]  # non-empty

        resp = client.messages.create(
            model=model_name,
            system=system_text or None,
            max_tokens=params.get("max_tokens", 512),
            temperature=params.get("temperature", 0.2),
            messages=[{"role": "user", "content": user_blocks}],
        )

        # Anthropic returns a list of content blocks; collect text safely
        try:
            blocks = getattr(resp, "content", []) or []
            text = "".join(getattr(b, "text", "") for b in blocks if getattr(b, "type", "") == "text").strip()
            return text
        except Exception:
            # Fallback: best-effort string
            return str(resp)

    return _llm
