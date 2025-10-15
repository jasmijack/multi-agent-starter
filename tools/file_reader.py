from pathlib import Path
from typing import Optional
from src.core import Tool

class FileReader(Tool):
    """
    Reads text content of a local file path.
    Args: path: str, max_chars: int=2000
    """
    def __init__(self):
        super().__init__("file_reader", "Read text from a local file path.")
    def __call__(self, path: str, max_chars: int = 2000, encoding: Optional[str] = "utf-8") -> str:
        p = Path(path)
        if not p.exists() or not p.is_file():
            return f"File not found: {path}"
        text = p.read_text(encoding=encoding)
        if len(text) > max_chars:
            return text[:max_chars] + "... [truncated]"
        return text
