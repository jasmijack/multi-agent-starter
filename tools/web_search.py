import os
import requests
from typing import List, Dict, Any
from src.core import Tool

class WebSearch(Tool):
    """
    Simple web search tool. Supports Bing Web Search if BING_SEARCH_KEY is set.
    You can adapt to SerpAPI, Tavily, or another provider by changing _search().
    """
    def __init__(self):
        super().__init__("web_search", "Web search via provider API. Args: query: str, count: int=3")

    def __call__(self, query: str, count: int = 3) -> str:
        results = self._search(query, count)
        return "\n".join(f"- {r['name']}: {r['url']}" for r in results) if results else "No results."

    def _search(self, query: str, count: int) -> List[Dict[str, Any]]:
        key = os.getenv("BING_SEARCH_KEY")
        endpoint = os.getenv("BING_SEARCH_ENDPOINT", "https://api.bing.microsoft.com/v7.0/search")
        if not key:
            return [{"name": "Configure BING_SEARCH_KEY to enable real search", "url": "https://www.bing.com"}]
        headers = {"Ocp-Apim-Subscription-Key": key}
        params = {"q": query, "count": count}
        r = requests.get(endpoint, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        web_pages = data.get("webPages", {}).get("value", [])
        return [{"name": x.get("name", "result"), "url": x.get("url", "")} for x in web_pages[:count]]
