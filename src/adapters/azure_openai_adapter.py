import os
from typing import List, Dict, Any
from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential

def azure_openai_llm(
    endpoint: str | None = None,
    deployment: str | None = None,
    api_key: str | None = None,
    api_version: str | None = None,
):
    endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = deployment or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
    api_version = api_version or os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

    client = OpenAIClient(endpoint=endpoint, credential=AzureKeyCredential(api_key), api_version=api_version)

    def _llm(messages: List[Dict[str, str]], params: Dict[str, Any]) -> str:
        resp = client.chat.completions.create(
            model=deployment,
            messages=messages,
            temperature=params.get("temperature", 0.2),
            max_tokens=params.get("max_tokens", 512),
        )
        return (resp.choices[0].message.content or "").strip()
    return _llm
