"""Assembler for UVM variant 20, stage 2."""

import sys
import yaml


def mask(n):
    """Return bitmask with n ones."""
    return 2 ** n - 1


def asm_load_const(x):
    """Pack load_const into 3 bytes."""
    cmd = 22
    cmd |= (x & mask(18)) << 5
    return cmd.to_bytes(3, "little")


def asm_read_mem(x):
    """Pack read_mem into 2 bytes."""
    cmd = 4
    cmd |= (x & mask(9)) << 5
    return cmd.to_bytes(2, "little")


def asm_write_mem(x):
    """Pack write_mem into 4 bytes."""
    cmd = 17
    cmd |= (x & mask(24)) << 5
    return cmd.to_bytes(4, "little")


def asm_unary_minus():
    """Pack unary_minus into 1 byte."""
    return bytes([31])


def parse_arguments(argv):
    """Parse command line arguments."""
    if len(argv) < 3:
        return None, None, False
    src = argv[1]
    bin_path = argv[2]
    test_mode = len(argv) > 3 and argv[3] == "--test"
    return src, bin_path, test_mode


def to_intermediate(program):
    """Convert YAML program into list of tuples."""
    result = []
    for item in program:
        op = item["op"]
        if op == "load_const":
            result.append(("load_const", item["arg"]))
        if op == "read_mem":
            result.append(("read_mem", item["arg"]))
        if op == "write_mem":
            result.append(("write_mem", item["arg"]))
        if op == "unary_minus":
            result.append(("unary_minus", 0))
    return result


def assemble_to_bytes(intermediate):
    """Convert intermediate tuples to bytes."""
    data = b""
    for inst in intermediate:
        if inst[0] == "load_const":
            data += asm_load_const(inst[1])
        if inst[0] == "read_mem":
            data += asm_read_mem(inst[1])
        if inst[0] == "write_mem":
            data += asm_write_mem(inst[1])
        if inst[0] == "unary_minus":
            data += asm_unary_minus()
    return data


def practice():
    """Run tests from specification."""
    assert list(asm_load_const(543)) == [0xF6, 0x43, 0x00]
    assert list(asm_read_mem(244)) == [0x84, 0x1E]
    assert list(asm_write_mem(723)) == [0x71, 0x5A, 0x00, 0x00]
    assert list(asm_unary_minus()) == [0x1F]


def main(argv):
    """Entry point of the assembler."""
    src, bin_path, test_mode = parse_arguments(argv)
    if src is None:
        print("Usage: python uvm-asm.py <src> <bin> [--test]")
        return

    with open(src, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    program = data["program"]
    intermediate = to_intermediate(program)
    practice()

    bytecode = assemble_to_bytes(intermediate)

    with open(bin_path, "wb") as file:
        file.write(bytecode)

    if test_mode:
        print("Intermediate representation:")
        for item in intermediate:
            print(item)

    print(f"Assembled {len(intermediate)} commands")
    print(f"File size: {len(bytecode)} bytes")


if __name__ == "__main__":
    main(sys.argv)