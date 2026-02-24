import re
import math
from collections import defaultdict

from tree_sitter import Language, Parser
import tree_sitter_rust as rust_language


RUST = Language(rust_language.language())
PARSER = Parser(RUST)


RUST_KEYWORDS = {
    "as","break","const","continue","crate","else","enum","extern","false","fn","for","if","impl",
    "in","let","loop","match","mod","move","mut","pub","ref","return","self","Self","static","struct",
    "super","trait","true","type","unsafe","use","where","while","async","await","dyn"
}

RUST_OPERATORS = {
    "+", "-", "*", "/", "%", "<<", ">>", "&", "|", "^", "!", "&&", "||",
    "==", "!=", "<", "<=", ">", ">=", "=", "+=", "-=", "*=", "/=", "%=",
    "->", "::", ".", "..", "..=", "?", "@", ":"
}

RUST_TYPES = {
    "i8", "i16", "i32", "i64", "i128", "isize",
    "u8", "u16", "u32", "u64", "u128", "usize",
    "f32", "f64",
    "bool",
    "char",
    "str",
    "String"
}

IDENT_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')
NUMBER_RE = re.compile(r'^[0-9][0-9_]*([.][0-9_]+)?$')


class HalsteadRust:
    def __init__(self, source_bytes):
        self.source = source_bytes
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)
        self.function_calls = set()

    def classify_token(self, token, node_type=None):
        token = token.strip()
        if not token:
            return None
        
        if token in RUST_TYPES:
            return None
        
        
        
        if token in self.function_calls:
            return None

        
        if token in ("{", "}"):
            return ("op", "{}")
        
        if token == "if":
            return("op", "if...else")
        
        if token == "else":
            return None

        if token in RUST_OPERATORS or token in RUST_KEYWORDS:
            return ("op", token)

        if IDENT_RE.match(token):
            return ("operand", token)

        if NUMBER_RE.match(token):
            return ("operand", token)

        if token.startswith('"') or token.startswith("'"):
            return ("operand", token)

        return None

    def visit(self, node):
        if node.type == "call_expression":
            function_node = node.child_by_field_name("function")
            if function_node:
                name = self.source[function_node.start_byte:function_node.end_byte].decode("utf8", errors="ignore")
                self.operators["вызов функции"] += 1
                self.function_calls.add(name)
            for child in node.children:
                self.visit(child)
            return

        # Макрос
        if node.type == "macro_invocation":
            macro_node = node.child_by_field_name("macro")
            if macro_node:
                name = self.source[macro_node.start_byte:macro_node.end_byte].decode("utf8", errors="ignore")
                self.operators["вызов функции"] += 1
                self.function_calls.add(name)
            for child in node.children:
                self.visit(child)
            return
        
        if node.child_count == 0:
            text = self.source[node.start_byte:node.end_byte].decode("utf8", errors="ignore")
            result = self.classify_token(text, node.type)
            if result:
                kind, value = result
                if kind == "op":
                    self.operators[value] += 1
                else:
                    self.operands[value] += 1
        else:
            for child in node.children:
                self.visit(child)


def compute_halstead(code_text):
    source_bytes = code_text.encode("utf8")
    tree = PARSER.parse(source_bytes)
    root = tree.root_node

    analyzer = HalsteadRust(source_bytes)
    analyzer.visit(root)

    unique_operators = len(analyzer.operators)
    unique_operands = len(analyzer.operands)
    total_operators = sum(analyzer.operators.values())
    total_operands = sum(analyzer.operands.values())

    vocabulary = unique_operators + unique_operands
    length = total_operators + total_operands
    volume = round(length * math.log2(vocabulary), 5) if vocabulary > 0 else 0

    metrics = {
        "η1 (уникальные операторы)": unique_operators,
        "η2 (уникальные операнды)": unique_operands,
        "N1 (всего операторов)": total_operators,
        "N2 (всего операндов)": total_operands,
        "Словарь программы": vocabulary,
        "Длина программы": length,
        "Объем программы": volume,
    }

    return metrics, analyzer.operators, analyzer.operands


