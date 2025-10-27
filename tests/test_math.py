from tools.math import smart_math

def test_smart_math_basic():
    result = smart_math.run("2 + 2")
    assert result == 4

def test_smart_math_complex():
    result = smart_math.run("(10 + 5) * 2")
    assert result == 30
