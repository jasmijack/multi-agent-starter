from src.core import Message, Memory

def test_memory_roundtrip():
    mem = Memory(max_items=2)
    mem.add({"a": 1})
    mem.add({"b": 2})
    mem.add({"c": 3})
    assert len(mem.store) == 2
    assert mem.recall()[0]["b"] == 2
