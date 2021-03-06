import re, sys, os

# string represent hack comment format
comment_regex = "\\s*//"

# regex to check if string has inline comment
inline_comment_regex = re.compile(comment_regex)

# regex to check if string is comment line
comment_format = re.compile("^" + comment_regex)

# assembly code for saving last 2 values from stack
GET_VALUES = "@SP\nM=M-1\n@SP\nA=M\nD=M\n@R13\nM=D\n@SP\nM=M-1\n@SP\nA=M\n" \
             "D=M\n@R14\nM=D\n"

# assembly code for assign the return value into the stack
ASSIGN_RETURN_VAL = "(TRUE$$)\n@SP\nA=M\nM=-1\n@END$$\n0;JMP\n(FALSE$$)\n" \
           "@SP\nA=M\nM=0\n(END$$)\n@SP\nM=M+1\n"

# assembly code for compare between 2 saved values
LT_CHECK = "@R13\nD=M\n@POSITIVE$$\nD;JGE\n@R14\nD=M\n@COMPARE_SAME_SIGN$$\nD" \
           ";JLT\n@FALSE$$\n0;JMP\n(" \
           "POSITIVE$$)\n@R14\nD=M\n@COMPARE_SAME_SIGN$$\nD;JGE\n@TRUE$$\n0;JMP\n" \
           "(COMPARE_SAME_SIGN$$)\n@R13\nD=M\n@R14\nD=D-M\n@TRUE$$\nD;JGT\n" \
           "@FALSE$$\n0;JMP\n"

EQ_CHECK = "@R14\nD=M\n@POSITIVE$$\nD;JGE\n@R13\nD=M\n@COMPARE_SAME_SIGN$$\n" \
           "D;JLT\n@FALSE$$\n0;JMP\n(" \
           "POSITIVE$$)\n@R13\nD=M\n@COMPARE_SAME_SIGN$$\nD;JGE\n@FALSE$$\n0;JMP\n" \
           "(COMPARE_SAME_SIGN$$)\n@R14\nD=M\n@R13\nD=D-M\n@TRUE$$\nD;JEQ\n@FALSE$$\n" \
           "0;JMP\n"

GT_CHECK = "@R14\nD=M\n@POSITIVE$$\nD;JGE\n@R13\nD=M\n@COMPARE_SAME_SIGN$$\nD;JLT\n" \
           "@FALSE$$\n0;JMP\n(POSITIVE$$)\n@R13\nD=M\n@COMPARE_SAME_SIGN$$\nD;JGE\n" \
           "@TRUE$$\n0;JMP\n(COMPARE_SAME_SIGN$$)\n@R14\nD=M\n@R13\nD=D-M\n@TRUE$$\n" \
           "D;JGT\n@FALSE$$\n0;JMP\n"

# assembly name for each segment
segment_symbol = {"local": "LCL\n", "argument": "ARG\n", "this": "THIS\n",
                  "that": "THAT\n"}

# assembly command for each binary command
binary_command = {"add": "D=D+M\n", "sub": "D=D-M\n", "and": "D=D&M\n",
                  "or": "D=D|M\n"}

# assembly command for each unary command
unary_command = {"not": "D=!D\n", "neg": "D=-D\n"}

# assembly command for each compare command
compare_command = {"gt": GT_CHECK, "lt": LT_CHECK, "eq": EQ_CHECK}

# the name of last declared function
lastfunc = ""

# counters to the return calls and compare calls
compare_counter = 0
return_counter = 0


# push assembler code  --------------------------------------------------------

PUSH_TO_STACK = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"  # *SP=D ; SP++


# pop assembler code   --------------------------------------------------------

POP_TEMP = "D=A\n@5\nD=D+A\n@SP\nM=M-1\n@R13\nM=D\n@SP\nA=M\nD=M\n@R13\nA=M" \
           "\nM=D\n"

POP_FROM_STACK = "@SP\nM=M-1\nA=M\nD=M\n"     # SP--; D=*SP


# functions -------------------------------------------------------------------

# assembly code for saving function frame
SAVE_FUNCTION_FRAME = "D=A\n" + PUSH_TO_STACK + "@LCL\nD=M\n" + PUSH_TO_STACK + "@ARG" \
                "\nD=M\n" + PUSH_TO_STACK + "@THIS\nD=M\n" + PUSH_TO_STACK +\
                "@THAT\nD=M\n" + PUSH_TO_STACK + "@SP\nD=M\n@5\nD=D-A\n"

# assembly code for restore function frame
RESTORE_FUNCTION_FRAME = "@endFrame\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n@endFrame\n" \
                         "M=M-1\nD=M\nA=M\nD=M\n@THIS\nM=D\n@endFrame\nM=M-1\n" \
                         "A=M\nD=M\n@ARG\nM=D\n@endFrame\nM=M-1\nA=M\nD=M\n" \
                         "@LCL\nM=D\n"

# assembly code for return action
RETURN_FROM_FUNCTION = "@LCL\nD=M\n@endFrame\nM=D\n@endFrame\nD=M\n@5\nD=D-A" \
                       "\nA=D\nD=M\n@retAddr\nM=D\n@retAddr\nM=D\n" + \
                       POP_FROM_STACK + \
                       "@ARG\nA=M\nM=D\n@ARG\nD=M+1\n@SP\nM=D\n" + \
                       RESTORE_FUNCTION_FRAME + "@retAddr\nA=M\n0;JMP\n"


def push(line, file_name):
    """
    A function that gets a vm push line and returns its asm translation
    :param line: is a vm line
    :param file_name: is a vm file the line is in
    :return: line asm translation
    """
    asm_trans = ""
    commands = line.split()
    segment = commands[1]
    i = commands[2]

    if segment in segment_symbol:
        asm_trans = "@" + segment_symbol[segment] + "D=M\n@" + i + "\n" + \
               "D=D+A\nA=D\nD=M\n"

    if segment == "constant":                         # line = push constant i
        asm_trans = "@" + commands[2] + "\nD=A\n"

    if segment == "static":                           # line = push static i
        asm_trans = "@" + file_name + commands[2] + "\n" + "D=M\n"

    if segment == "temp":                             # line = push temp i
        asm_trans = "@" + commands[2] + "\n" + "D=A\n@5\nD=D+A\nA=D\nD=M\n"

    if segment == "pointer":                          # line = push pointer i
        if i == "0":
            asm_trans = "@THIS\nD=M\n"
        else:
            asm_trans = "@THAT\nD=M\n"

    return asm_trans + PUSH_TO_STACK


def pop(line, file_name):
    """
    A function that gets a vm pop line and returns its asm translation
    :param line: is a vm line
    :param file_name: is a vm file the line is in
    :return: line asm translation
    """
    commands = line.split()
    segment = commands[1]
    i = commands[2]

    if segment in segment_symbol:
        return "@" + segment_symbol[segment] + "D=M\n@" + i + "\n" + \
               "D=D+A\n@R13\nM=D\n" + POP_FROM_STACK + "@R13\nA=M\nM=D\n"

    if segment == "static":                              # line = pop static i
        return POP_FROM_STACK + "@" + file_name + i + "\nM=D\n"

    if segment == "temp":                                # line = pop temp i
        return "@" + i + "\n" + POP_TEMP

    if segment == "pointer":                             # line = pop pointer i
        if i == "0":
            return POP_FROM_STACK + "@THIS\nM=D\n"
        else:
            return POP_FROM_STACK + "@THAT\nM=D\n"


def labels(line, line_type):              ######################  new ex8
    """
    A function that gets a line and returns a label or a jump to a label
    :param line:  is the line to translate
    :param line_type:  is the line type
    :return:  an assembler translation of line
    """
    global lastfunc
    commands = line.split()

    if line_type == "l":
        return "(" + lastfunc + "$" + commands[1] + ")\n"

    if line_type == "g":
        return "@" + lastfunc + "$" + commands[1] + "\n" + "0;JMP\n"

    if line_type == "i":
        return POP_FROM_STACK + "@" + lastfunc + "$" + commands[1] + \
                              "\nD;JNE\n"


def translate(line, file_name):
    """
     A function that translate a vm line into an assembler commands
    :param line: a line of vm code
    :param file_name: the name of the file line is in
    :return: ASSEMBLY CODE OF LINE
    """
    global lastfunc
    translated_line = "// " + line + "\n"   # inserting a comment - the vm line

    if line.startswith("push"):
        return translated_line + push(line, file_name)

    if line.startswith("pop"):
        return translated_line + pop(line, file_name)

    if line in binary_command:
        return translated_line + POP_FROM_STACK + "@R14\nM=D\n" + \
               POP_FROM_STACK + "@R14\n" + binary_command[line] + \
               PUSH_TO_STACK

    if line in unary_command:
        return translated_line + POP_FROM_STACK + unary_command[line] + \
                PUSH_TO_STACK

    if line in compare_command:
        return translated_line + GET_VALUES + compare_command[line] + \
               ASSIGN_RETURN_VAL

################################################################ex8   todo

    if line.startswith("label"):
        return translated_line + labels(line, "l")

    if line.startswith("goto"):
        return translated_line + labels(line, "g")

    if line.startswith("if-goto"):
        return translated_line + labels(line, "i")

    if line == "return":
        return translated_line + RETURN_FROM_FUNCTION

    if line.startswith("function"):
        line = line.split()
        lastfunc = line[1]
        return translated_line + "(" + lastfunc + ")\n" + "@" + line[2] +\
               "\nD=A\n(LOOP$$)\n@END$$\nD;JEQ\nD=D-1\n@SP\nA=M\nM=0" \
                "\n@SP\nM=M+1\n@LOOP$$\n0;JMP\n(END$$)\n"

    if line.startswith("call"):
        line = line.split()
        return "@" + lastfunc + "$ret.%%\n" + SAVE_FUNCTION_FRAME + "@" + \
               line[2] + "\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@"\
               + line[1] + "\n0;JMP\n(" + lastfunc + "$ret.%%)\n"


def parser(file):
    """
    A function that parses over all vm file lines and returns only the commands.
    :param file: is a file object
    :return: a list of all vm commands only.
    """
    lines = [""]
    line = file.readline()
    while line != "":

        if line.isspace() or re.match(comment_format, line):
            # if true, this line is empty \ comment  - continue
            line = file.readline()
            continue

        if (re.search(inline_comment_regex, line)):
            # clears inline comments from line
            line = re.split(inline_comment_regex, line)[0]

        line = line.strip("\n")
        line = line.strip("\r")
        lines.append(line)              # add the actual instruction to lines array and go to next line
        line = file.readline()          # next line

    return lines


def add_bootstrap(dir_name):
    """
    initilaze the stack pointer address and another systematic issues
    :param dir_name: the name of the directory or file
    :return: string represent the bootstrap code in assembly
    """
    bootstrap = "@256\nD=A\n@SP\nM=D\n"
    bootstrap += translate("call Sys.init 0", dir_name)
    bootstrap = bootstrap.replace("$ret.%%", "")
    return bootstrap


def virtual_machine(file, file_name):
    """
    translate the given file from virtual machine language to hack
    :param file: virtual machine language file
    :param file_name: virtual machine language file name to name static variables
    :return: hack code file
    """

    lines = parser(file)

    assembler_rep = ""
    global compare_counter
    global return_counter

    for line in lines:

        if line == "":
            continue

        translated_ins = translate(line, file_name)

        if "$$" in translated_ins:

            translated_ins = translated_ins.replace("$$", str(compare_counter))
            compare_counter += 1

        if "%%" in translated_ins:
            translated_ins = translated_ins.replace("%%", str(return_counter))
            return_counter += 1

        assembler_rep = assembler_rep + translated_ins

    return assembler_rep


def main(file_path):
    """
    :param file_path: is the input path
    :return: a translated vm file
    """
    global lastfunc
    if os.path.isdir(file_path):          # if a directory - convert all files
        dir_name = os.path.basename(file_path)
        output_file = open(file_path + "//" + dir_name + ".asm", "w")
        lastfunc = dir_name
        output_file.write(add_bootstrap(dir_name))
        for file in os.listdir(file_path):
            if file.endswith(".vm"):
                file = open(file_path + "//" + file, "r")
                file_name = os.path.basename(file.name)[:-2]
                lastfunc = file_name
                output_file.write(virtual_machine(file, file_name))
        output_file.close()
    else:                                        # is an file - convert to asm
        file = open(file_path, "r")
        output_file = open(file_path[:-2] + "asm", "w")
        file_name = file.name[:-2]
        lastfunc = file_name
        output_file.write(add_bootstrap(file_name))
        output_file.write(virtual_machine(file, file_name))
        output_file.close()


# running VM

if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
        main(path)
    else:
        print('wrong input')
