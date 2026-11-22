import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

MAX_REG = (1 << 7) - 1
MAX_MEM = (1 << 17) - 1
MAX_CONST = (1 << 28) - 1

RE_LOAD = re.compile(
    r"^reg\[\s*(\d+)\s*\]\s*=\s*(0x[0-9a-fA-F]+|\d+)$"
)
RE_READ = re.compile(
    r"^reg\[\s*(\d+)\s*\]\s*=\s*mem\[\s*reg\[\s*(\d+)\s*\]\s*\]$"
)
RE_WRITE = re.compile(
    r"^mem\[\s*(\d+)\s*\]\s*=\s*reg\[\s*(\d+)\s*\]$"
)
RE_NOT = re.compile(
    r"^reg\[\s*(\d+)\s*\]\s*=\s*~\s*mem\[\s*(\d+)\s*\]$"
)


@dataclass(frozen=True)
class Instruction:
    a: int
    b: int
    c: int


def check_range(name: str, val: int, limit: int, line_no: int) -> None:
    if not (0 <= val <= limit):
        msg = (
            f"Строка {line_no}: {name}={val} "
            f"вне диапазона [0, {limit}]"
        )
        raise ValueError(msg)


def parse_line(raw_line: str, line_no: int) -> Instruction | None:
    line = raw_line.split("#", 1)[0].strip()
    if not line:
        return None

    if match := RE_LOAD.match(line):
        c, b = int(match.group(1), 10), int(match.group(2), 0)
        check_range("B", b, MAX_CONST, line_no)
        check_range("C", c, MAX_REG, line_no)
        return Instruction(25, b, c)

    if match := RE_READ.match(line):
        b, c = int(match.group(1), 10), int(match.group(2), 10)
        check_range("B", b, MAX_REG, line_no)
        check_range("C", c, MAX_REG, line_no)
        return Instruction(62, b, c)

    if match := RE_WRITE.match(line):
        b, c = int(match.group(1), 10), int(match.group(2), 10)
        check_range("B", b, MAX_MEM, line_no)
        check_range("C", c, MAX_REG, line_no)
        return Instruction(63, b, c)

    if match := RE_NOT.match(line):
        b, c = int(match.group(1), 10), int(match.group(2), 10)
        check_range("B", b, MAX_REG, line_no)
        check_range("C", c, MAX_MEM, line_no)
        return Instruction(21, b, c)

    raise SyntaxError(f"Строка {line_no}: ошибка синтаксиса: '{line}'")


def assemble_to_ir(source_text: str) -> list[Instruction]:
    ir: list[Instruction] = []
    for line_no, raw_line in enumerate(source_text.splitlines(), 1):
        instr = parse_line(raw_line, line_no)
        if instr is not None:
            ir.append(instr)
    return ir


def encode_instruction(instr: Instruction) -> bytes:
    a, b, c = instr.a, instr.b, instr.c
    if a == 25:
        word = a | (b << 6) | (c << 34)
        return word.to_bytes(6, "little")
    if a == 62:
        word = a | (b << 6) | (c << 13)
        return word.to_bytes(3, "little")
    if a == 63:
        word = a | (b << 6) | (c << 23)
        return word.to_bytes(4, "little")
    if a == 21:
        word = a | (b << 6) | (c << 13)
        return word.to_bytes(4, "little")
    raise ValueError(f"Неизвестный код операции: A={a}")


def encode_program(ir: list[Instruction]) -> list[bytes]:
    return [encode_instruction(instr) for instr in ir]


def format_bytes(data: bytes) -> str:
    return ", ".join(f"0x{byte:02X}" for byte in data)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ассемблер УВМ (вариант №4)."
    )
    parser.add_argument(
        "input_file", type=Path, help="Исходный файл программы"
    )
    parser.add_argument(
        "output_file", type=Path, help="Выходной двоичный файл"
    )
    parser.add_argument(
        "-t", "--test", action="store_true", help="Режим тестирования"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        source = args.input_file.read_text(encoding="utf-8")
        ir = assemble_to_ir(source)
        encoded = encode_program(ir)
        args.output_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_file.write_bytes(b"".join(encoded))
    except (OSError, SyntaxError, ValueError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    print(f"Ассемблировано команд: {len(ir)}")
    if args.test:
        for cmd_bytes in encoded:
            print(format_bytes(cmd_bytes))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())