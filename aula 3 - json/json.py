from typing import Any

def json(src:str) -> Any:
    chars = list(reversed(src)) 
    
    return read_value(chars)

def ws(chars:list[str]):
    while chars and chars[-1] in "\n\t\r":
        chars.pop()

def read_literal(lit:str, chars:list[str], value):
    for c in lit:
        if c!=chars.pop():
            raise SyntaxError
    return value

def read_number(chars: list[str]):
    ns = []
    while chars and chars[-1] in "0123456789":
        n = chars.pop()
        ns.append(n)
    return int("".join(ns))

def read_string(chars: list[str]) -> str:
    if chars.pop() != '"':
        raise SyntaxError
    parts = []
    while (c := chars.pop()) != '"':
        parts.append(c)
    return "".join(parts)

def read_array(chars: list[str]) -> list:
    if chars.pop() != "[":
        raise SyntaxError
    
    ws(chars)
    if chars[-1] == "]":
        chars.pop()
        return []
    
    values = []
    while True:
        value = read_value(chars)
        values.append(value)
        c = chars.pop()
        if c == ",":
            continue
        elif c == "]":
            break
        else:
            raise SyntaxError
    
    return values         
    
def read_value(chars):
    ws(chars)
    
    match chars[-1]:
        case "t":
            value = read_literal("true",chars, True)
        case "f":
            value = read_literal("false",chars, False)
        case "n":
            value = read_literal("null",chars, None)
        case "{":
            value = read_object(chars)
        case "[":
            value = read_array(chars)
        case '"':
            value = read_string(chars)
        case "-":
            chars.pop()
            value = read_number(chars)
        case c if c.isdigit() :
            value = read_number(chars)
        case _:
            raise SyntaxError
    ws(chars)
    return value
    

if __name__ == "__main__":
    print(json("null"))
    print(json("42")+1)
    print(json('"Leticia"'))
    print(json('["Leticia", 1, "compiladores", [1, 2, 3]]'))