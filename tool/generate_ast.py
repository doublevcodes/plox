from io import TextIOWrapper
from pathlib import Path
import sys

def indent_write(indent_level: int, file: TextIOWrapper, string: str):
    file.write(f"{'    ' * indent_level}{string}")

def define_type(writer: TextIOWrapper, base_name: str, class_name: str, fields: str):
    indent_write(0, writer, f"class {class_name}({base_name}):\n")
    writer.write("\n")
    indent_write(1, writer, f"def __init__(self, {fields}) -> None:\n")
    for attr in fields.split(","):
        indent_write(2, writer, f"self.{attr.strip()} = {attr.strip().split(':')[0]}\n")
    indent_write(1, writer, f"def accept(self, visitor: Visitor):\n        return visitor.visit{class_name, base_name}\n\n\n")

def define_visitor(writer: TextIOWrapper, base_name: str, types: list[str]):
    writer.write("class Visitor(ABC):\n")
    for type_ in types:
        type_name = type_.split(":")[0].strip()
        indent_write(1, writer, f"@abstractmethod\n    def visit{type_name}{base_name}({base_name.lower()}: {type_name}):\n        pass\n\n")
    writer.write("\n")

def define_imports(writer: TextIOWrapper):
    writer.write("from __future__ import annotations\n\nfrom abc import ABC, abstractmethod\nfrom plox.scan import Token\n\n\n")

def define_ast(output_dir: str, base_name: str, types: list[str]):
    path = Path(f"{output_dir}/ast.py")
    with open(path, "w") as writer:
        define_imports(writer)
        define_visitor(writer, base_name, types)
        writer.write(f"class {base_name}(ABC):\n    pass\n")
        indent_write(1, writer, "@abstractmethod\n    def accept(self, visitor: Visitor):\n        pass\n\n\n")
        for type_ in types:
            class_name: str = type_.split(":")[0].strip()
            fields: str = ':'.join(type_.split(":")[1:]).strip()
            define_type(
                writer,
                base_name,
                class_name,
                fields
            )

def main(*args: tuple[str]):
    if len(args) != 1:
        print("Usage: generate_ast <output_director>")
        sys.exit(64)
    output_dir = args[0]
    define_ast(
        output_dir,
        "Expr",
        [
            "Binary   : left: Expr, operator: Token, right: Expr",
            "Grouping : expression: Expr",
            "Literal  : value: object",
            "Unary    : operator: Token, right: Expr"
        ]
    )

if __name__ == "__main__":
    main(sys.argv[1:][0])