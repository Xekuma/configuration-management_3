import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

REG_COUNT = 128
MEM_SIZE = 1 << 17
WORD_MASK = 0xFFFFFFFF
CMD_SIZES = {25: 6, 62: 3, 63: 4, 21: 4}


@dataclass(frozen=True)
class Instruction:
    a: int
    b: int
    c: int


def parse_range(raw: str) -> tuple[int, int]:
    parts = raw.split(":")
    if len(parts) != 2:
        raise ValueError(
            f"Неверный формат диапазона '{raw}', ожидается start:end"
        )
    start, end = int(parts[0]), int(parts[1])
    if not (0 <= start <= end < MEM_SIZE):
        raise ValueError(
            f"Диапазон {start}:{end} вне [0, {MEM_SIZE - 1}]"
        )
    return start, end


def decode_at(code: bytes, pc: int) -> tuple[Instruction, int]:
    opcode = code[pc] & 0x3F
    size = CMD_SIZES.get(opcode)
    if size is None:
        raise ValueError(f"Неизвестный код операции A={opcode} (pc={pc})")
    if pc + size > len(code):
        raise ValueError(f"Обрыв команды A={opcode} по смещению {pc}")

    word = int.from_bytes(code[pc : pc + size], "little")
    if opcode == 25:
        b = (word >> 6) & ((1 << 28) - 1)
        c = (word >> 34) & 0x7F
    elif opcode == 62:
        b = (word >> 6) & 0x7F
        c = (word >> 13) & 0x7F
    elif opcode == 63:
        b = (word >> 6) & ((1 << 17) - 1)
        c = (word >> 23) & 0x7F
    else:
        b = (word >> 6) & 0x7F
        c = (word >> 13) & ((1 << 17) - 1)
    return Instruction(opcode, b, c), pc + size


def execute_step(
    instr: Instruction, regs: list[int], mem: list[int]
) -> None:
    if instr.a == 25:
        regs[instr.c] = instr.b
    elif instr.a == 62:
        addr = regs[instr.c]
        if not (0 <= addr < MEM_SIZE):
            raise IndexError(f"Адрес памяти вне диапазона: {addr}")
        regs[instr.b] = mem[addr]
    elif instr.a == 63:
        mem[instr.b] = regs[instr.c]
    elif instr.a == 21:
        regs[instr.b] = ~mem[instr.c] & WORD_MASK
    else:
        raise ValueError(f"Неподдерживаемая команда A={instr.a}")


def run_vm(code: bytes) -> tuple[list[int], list[int]]:
    regs = [0] * REG_COUNT
    mem = [0] * MEM_SIZE
    pc = 0
    while pc < len(code):
        instr, pc = decode_at(code, pc)
        execute_step(instr, regs, mem)
    return regs, mem


def save_xml_dump(
    mem: list[int], start: int, end: int, dump_path: Path
) -> None:
    root = ET.Element(
        "memory_dump", {"start": str(start), "end": str(end)}
    )
    for addr in range(start, end + 1):
        cell = ET.SubElement(root, "cell", {"address": str(addr)})
        cell.text = str(mem[addr])

    ET.indent(root, space="  ")
    dump_path.parent.mkdir(parents=True, exist_ok=True)
    tree = ET.ElementTree(root)
    tree.write(dump_path, encoding="utf-8", xml_declaration=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Интерпретатор УВМ (вариант №4)."
    )
    parser.add_argument(
        "binary_file", type=Path, help="Бинарный файл программы"
    )
    parser.add_argument(
        "dump_file", type=Path, help="Путь к XML-файлу дампа памяти"
    )
    parser.add_argument(
        "mem_range", type=str, help="Диапазон адресов памяти (start:end)"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        start, end = parse_range(args.mem_range)
        code = args.binary_file.read_bytes()
        _, mem = run_vm(code)
        save_xml_dump(mem, start, end, args.dump_file)
    except (OSError, ValueError, IndexError) as exc:
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 1

    print(f"Дамп памяти [{start}:{end}] сохранен в {args.dump_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())