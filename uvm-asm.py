"""Assembler for UVM variant 20, stage 1."""

import sys
import yaml


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

    if test_mode:
        print("Intermediate representation:")
        for item in intermediate:
            print(item)


if __name__ == "__main__":
    main(sys.argv)