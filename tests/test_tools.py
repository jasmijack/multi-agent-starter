from tools.calculator import Calculator
from tools.file_reader import FileReader
import tempfile, pathlib

def test_calculator():
    calc = Calculator()
    assert calc(expr="7*6") == "42"

def test_file_reader_roundtrip():
    fr = FileReader()
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "x.txt"
        p.write_text("hello")
        out = fr(path=str(p))
        assert "hello" in out
