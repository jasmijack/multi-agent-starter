# pip install openai
from typing import List, Dict, Any
from openai import OpenAI

def openai_llm(model: str, api_key: str):
    client = OpenAI(api_key=api_key)

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 512),
        )
        return resp.choices[0].message.content.strip()
    return _llm
