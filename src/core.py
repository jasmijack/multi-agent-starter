from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import json
import uuid

# messaging
@dataclass
class Message:
    id: str
    sender: str
    recipient: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

def new_id(prefix: str = "msg") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"

# tools
class Tool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def __call__(self, **kwargs) -> Any:
        ...

# memory
class Memory:
    def __init__(self, max_items: int = 1000):
        self.max_items = max_items
        self.store: List[Dict[str, Any]] = []

    def add(self, item: Dict[str, Any]) -> None:
        self.store.append(item)
        if len(self.store) > self.max_items:
            self.store.pop(0)

    def recall(self, query: Optional[str] = None, k: int = 10) -> List[Dict[str, Any]]:
        if not query:
            return self.store[-k:]
        q = query.lower()
        hits = [x for x in self.store if q in json.dumps(x).lower()]
        return hits[-k:]
