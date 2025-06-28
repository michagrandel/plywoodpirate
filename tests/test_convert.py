from plywoodpirate.buildins.convert import to_string

def test_convert():
    class CustomObject:
        def __repr__(self):
            return "bar"
    foo = CustomObject()
    values = {
        foo: "bar",
        "foobar": "foobar",
        1: "1",
        1.1: "1.1",
        None: "None",
    }
    for value, expected in values.items():
        converted = to_string(value)
        assert converted == expected, f"Expected {expected}, got {converted}"
        assert type(converted) is str, f"Expected string, got {type(converted)}"

    b = True
    converted = to_string(b)
    assert converted == "True", f"Expected {b}, got {converted}"
    assert type(converted) is str, f"Expected string, got {type(converted)}"
    
    l = [1, 2, 3]
    converted = to_string(l)
    assert converted == "[1, 2, 3]", f"Expected {l}, got {converted}"
    assert type(converted) is str, f"Expected string, got {type(converted)}"
    
    dic = {'a': 1, 'b': 2}
    converted = to_string(dic)
    assert converted == "{'a': 1, 'b': 2}", f"Expected {dic}, got {converted}"
    assert type(converted) is str, f"Expected string, got {type(converted)}"
    
    s = (1, 2, 3)
    converted = to_string(s)
    assert converted == "(1, 2, 3)", f"Expected {s}, got {converted}"
    assert type(converted) is str, f"Expected string, got {type(converted)}"
        
