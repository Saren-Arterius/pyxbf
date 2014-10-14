#!/usr/bin/env python3
from argparse import ArgumentParser

output = ""
ptrs = {0: 0}
ptr = 0
pos = 0
no_prompt = 0


def repr_dict(dict, highlight):
    s = "{"
    pos = 0
    l = len(dict)
    for key, value in dict.items():
        pos += 1
        if key == highlight:
            s += "({0}): ".format(repr(key))
        else:
            s += "{0}: ".format(repr(key))
        s += repr(value)
        if pos != l:
            s += ", "
    s += "}"
    return s


def handle_char():
    global ptrs, ptr, pos
    if chars[pos] == ".":
        return chr(ptrs[ptr])
    elif chars[pos] == ",":
        user_input = input()
        if len(user_input):
            ptrs[ptr] = ord(user_input[0])
    elif chars[pos] == ">":
        ptr += 1
        if ptr not in ptrs:
            ptrs[ptr] = 0
    elif chars[pos] == "<":
        ptr += -1
        if ptr not in ptrs:
            ptrs[ptr] = 0
    elif chars[pos] == "+":
        if ptr in ptrs:
            ptrs[ptr] += 1
        else:
            ptrs[ptr] = 1
    elif chars[pos] == "-":
        if ptr in ptrs:
            ptrs[ptr] -= 1
        else:
            ptrs[ptr] = -1
    elif chars[pos] == "[":
        if not ptrs[ptr]:
            for i in range(pos, len(chars)):
                if chars[i] == "]":
                    pos = i
                    break
    elif chars[pos] == "]":
        if ptrs[ptr]:
            for i in range(pos, 0, -1):
                if chars[i] == "[":
                    pos = i
                    break


if __name__ == "__main__":
    parser = ArgumentParser(description="Simple brainfuck interpreter.")
    parser.add_argument('--debug', '-d', action='store_true', help="Enable visual output.")
    parser.add_argument('--interactive', '-i', action='store_true', help="Enable interactive mode.")
    parser.add_argument('file', help="The brainfuck file.")
    args = parser.parse_args()
    chars = "".join([c for array in open(args.file).read() for c in array if c in "+-<>.,[]"])
    while pos < len(chars):
        result = handle_char()
        if args.debug:
            if result is not None:
                output += result
            print("{0}({1}){2} *(pos) = {3}".format(chars[0:pos] if pos != 0 else "", chars[pos],
                                                    chars[pos + 1:len(chars) - 1], pos))
            print("Pointers {{ptrs}} (ptr): {0}".format(repr_dict(ptrs, ptr)))
            print("Current output: \"{0}\"".format(output))
            print()
        elif result is not None:
            print(result, end="")
        if args.interactive:
            if no_prompt > 0:
                no_prompt -= 1
            else:
                print("Input an integer to take N steps further.")
                user_input = input("Exec: >>> ")
                try:
                    no_prompt = int(user_input)
                except ValueError:
                    try:
                        print("Output: ", end="")
                        exec(user_input)
                    except Exception as e:
                        if "EOF" not in repr(e):
                            print(e)
                    finally:
                        input()
                user_input = ""
                print()
        pos += 1
    if args.debug:
        print("End of program.")