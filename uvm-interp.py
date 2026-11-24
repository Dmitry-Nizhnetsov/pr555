"""Interpreter for UVM variant 20, stage 4."""

import sys
import xml.etree.ElementTree as ET


def mask(n):
    """Return bitmask with n ones."""
    return 2 ** n - 1


reg = 0
mem = [0] * 65536
pc = 0


def read_cmd(bytecode, pc):
    """Read command. Return (op, arg, size)."""
    b1 = bytecode[pc]
    op = b1 & 0b11111
    if op == 22:
        val = b1 | (bytecode[pc + 1] << 8) | (bytecode[pc + 2] << 16)
        return op, (val >> 5) & mask(18), 3
    if op == 4:
        val = b1 | (bytecode[pc + 1] << 8)
        return op, (val >> 5) & mask(9), 2
    if op == 17:
        val = b1 | (bytecode[pc + 1] << 8)
        val |= (bytecode[pc + 2] << 16)
        val |= (bytecode[pc + 3] << 24)
        return op, (val >> 5) & mask(24), 4
    if op == 31:
        return op, 0, 1
    return 0, 0, 1


def save_dump(memory, start, end, path):
    """Save memory range to XML."""
    root = ET.Element("memory")
    for i in range(start, end + 1):
        cell = ET.SubElement(root, "cell", address=str(i))
        cell.text = str(memory[i])
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def execute(bytecode):
    """Execute bytecode."""
    global reg, pc
    while pc < len(bytecode):
        op, arg, size = read_cmd(bytecode, pc)
        if op == 22:
            reg = arg
        if op == 4:
            reg = mem[reg + arg]
        if op == 17:
            mem[arg] = reg
        if op == 31:
            reg = -reg
        pc += size


def main(argv):
    """Entry point of the interpreter."""
    bin_path = "uvm-output.bin"
    dump_path = "uvm-dump.xml"
    start_addr = 0
    end_addr = 49
    if len(argv) > 3:
        bin_path = argv[1]
        dump_path = argv[2]
        start_addr = int(argv[3])
        end_addr = int(argv[4])

    with open(bin_path, "rb") as file:
        bytecode = file.read()

    execute(bytecode)
    save_dump(mem, start_addr, end_addr, dump_path)
    print(reg, mem[start_addr:end_addr + 1])


if __name__ == "__main__":
    main(sys.argv)