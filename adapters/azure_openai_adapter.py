import os
from typing import List, Dict, Any
from openai import OpenAI

def azure_openai_llm(
    endpoint: str | None = None,         # https://<resource>.openai.azure.com
    api_key: str | None = None,
    deployment: str | None = None,       # your deployed chat model name
    api_version: str | None = None,      # e.g. 2024-08-01-preview
):
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_version = api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    if not all([endpoint, api_key, deployment]):
        raise ValueError("Set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_DEPLOYMENT")

    client = OpenAI(
        api_key=api_key,
        base_url=f"{endpoint}/openai/deployments/{deployment}",
        default_query={"api-version": api_version},
    )

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        resp = client.chat.completions.create(
            model=deployment,  # ignored by Azure when base_url targets a deployment
            messages=messages,
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 512),
        )
        return (resp.choices[0].message.content or "").strip()

    return _llm
