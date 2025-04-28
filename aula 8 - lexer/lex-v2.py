from rich import print
import re
from typing import cast, Iterator
from dataclasses import dataclass

exemplos_corretos = ["aAa 42", "aa bbAB #foo\naaa", "aaabbbaaa 54.9"]
exemplos_incorretos = ["ccc", "a b c", "a c b"]

PATTERNS = {
    "COMMENT": r"#[^\n]*",
    "INT": r"0|[1-9][0-9]*",
    "FLOAT": r"0|[1-9][0-9]*\.[0-9]+",
    "WA": r"[aA]+",
    "WB": r"[bB]+",
    "WS": r"\s+",
    #IMPORTANTE! esse deve ser o ultimo padrao para capturar oq os outros padroes nao capturam
    "ERROR": r".",
}

GROUPS = (f"(?P<{name}>{regex})" for name, regex in PATTERNS.items())
REGEX = "|".join(GROUPS)
LEXER = re.compile(REGEX)

@dataclass
class Token:
        kind: str
        word: str

def tokenizer(src: str) -> Iterator[Token]:
    IGNORE = ("WS", "COMMENT")
    
    for msg in LEXER.finditer(src):
        kind = cast(str, msg.lastgroup)
        word = msg.group(0)
        
        if kind == "ERROR":
            raise SyntaxError(msg)
        if kind in IGNORE:
            continue
        
        yield Token(kind, word)
    
if __name__ == "__main__":
    print("[blue bold]CORRETOS")
    for src in exemplos_corretos:
        tokens = list(tokenizer(src))
        print(f"{src =}")
        print(f"{tokens =}\n")
    
    print("[red bold]INCORRETOS")
    for src in exemplos_incorretos:
        try:
            tokens = list(tokenizer(src))
        except SyntaxError:
            print(f"{src =} OK!\n")
        else:
            print(f"{src =}")
            print(f"{tokens =}\n")