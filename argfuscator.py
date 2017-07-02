#!/usr/bin/env python
import sys, re, random

__author__  = "Jeff White [karttoon] @noottrak"
__email__   = "karttoon@gmail.com"
__version__ = "1.0.0"
__date__    = "04MAR2017"

command = sys.argv[1]
command = command.replace("^","")

ps_args = {
    "command"           : {"args":2, "length":1},
    "encodedcommand"    : {"args":2, "length":2},
    "ec"                : {"args":2, "length":2}, # alias for encodedcommand
    "executionpolicy"   : {"args":2, "length":2},
    "ep"                : {"args":2, "length":2}, # alias for executionpolicy
    "file"              : {"args":2, "length":1},
    "inputformat"       : {"args":2, "length":1},
    "if"                : {"args":2, "length":2}, # alias for inputformat
    "mta"               : {"args":1, "length":1},
    "noexit"            : {"args":1, "length":3},
    "nologo"            : {"args":1, "length":3},
    "noninteractive"    : {"args":1, "length":3},
    "noprofile"         : {"args":1, "length":3},
    "outputformat"      : {"args":2, "length":1},
    "of"                : {"args":2, "length":2}, # alias for outputformat
    "psconsolefile"     : {"args":1, "length":1},
    "sta"               : {"args":1, "length":1},
    "version"           : {"args":1, "length":1},
    "windowstyle"       : {"args":2, "length":1}
}

def arg_randomize(arg, value):

    randomized_arg  = {}
    newVal          = [value]

    # Add aliases to list
    if value == "command":
        newVal.append("c")
    if value == "encodedcommand":
        newVal.append("ec")
        newVal.append("e")
    if value == "executionpolicy":
        newVal.append("ep")
    if value == "inputformat":
        newVal.append("if")
    if value == "outputformat":
        newVal.append("of")

    # Randomize length of command used for iterations
    if value in ps_args:
        argLength = random.randint(ps_args[arg]["length"],len(value))
    # Keep length for non-recognized commands and data
    else:
        argLength = len(value)

    # Determine whether to inject carets
    caretCheck = random.randrange(2)

    # If injecting carets, build list with regular character and then caret-prepended character
    for letter in value:
        randomized_arg[letter] = [letter]
        if caretCheck == 1 and arg != "command":
            randomized_arg[letter].append("^" + letter)

    # Generate up-to 5000 variants (only relevant for caret injection) and build string
    counter = 0
    while counter < 5000:
        stringGen = value[0]
        for letter in value[1:argLength]:
            stringGen += randomized_arg[letter][random.randrange(len(randomized_arg[letter]))]
        if stringGen not in newVal:
            newVal.append(stringGen)
        counter += 1

    # Randomize case on encodedcommand but not B64 data
    if (arg == "encodedcommand" or arg == "ec") and (value != "encodedcommand" or value != "ec"):
        return ''.join(newVal[random.randrange(len(newVal))])
    # Otherwise always randomize command and, if applicable, variable
    else:
        return ''.join(random.choice((str.upper, str.lower))(letter) for letter in newVal[random.randrange(len(newVal))])

# Take provided "powershell.exe" format as first entry in list
command_args = [command.split(" ")[0]]

# If not using an argument with a quoted variable
if "\"" not in command:
    [command_args.append(value) for value in command.split(" -")[1:]]
# Otherwise check for commands which use quotes, such-as "command", and then attempt to parse arguments
else:
    # Strip out arguments with quoted variables
    for value in re.findall("\-[a-zA-Z]+ \".+\"", command):
        command_args.append(value[1:])
    # Remove the quoted variable and then parse regularly
    for value in command_args:
        value = re.escape(value)
        command = re.sub("-" + value, "", command)
        command = command.replace("  ", " ")
    [command_args.append(value) for value in command.split(" -")[1:]]

new_command = []
holder = ""  # This variable will hold "command" arguments so that it can be appended to list as subsequent variables may not come after

for value in command_args[1:]: # Parse everything past initial "powershell.exe" in list

    f_flag      = 0
    new_value   = ""

    # EncodedCommand can be shortened even further so this modifies it to catch
    if re.search("^[eE] [a-zA-Z0-9]", value):
        value = re.sub("^[eE] ", "encodedcommand ", value)

    # Command can be shortened even further so this modifies it to catch
    if re.search("^[cC] [\"\']", value):
        value = re.sub("^[cC] ", "command ", value)

    for arg in ps_args:

        arg_length = len(arg)

        # Since we don't know what format we'll receive arguments in, we start with max length and slowly reduce until finding match
        while arg_length >= ps_args[arg]["length"] and f_flag == 0:

            # Found match
            if re.search("^" + arg[0:arg_length], value, re.IGNORECASE):
                # Randomize argument
                new_value += ("-" + arg_randomize(arg, arg))

                # Check if argument is standalone or has a variable with it - if so, randomize variable too
                if ps_args[arg]["args"] == 2:
                    new_value += (" " + arg_randomize(arg, " ".join(value.split(" ")[1:])))

                if arg == "command":
                    holder = new_value

                f_flag = 1

            # Decrement command and keep processing
            else:
                if arg_length >= ps_args[arg]["length"]:
                    arg_length -= 1

    # If for whatever reason, like new PS version and new commands or typo in provided argument, notify user unable to parse
    if f_flag == 0 and value != command_args[0]:
        print "[!] Unable to match argument: %s" % value

    # Append randomized variable to list unless it's "command", which MUST come last in the returned string for PS to process correctly
    if new_value != "" and new_value != holder:
        new_command.append(new_value)

# Shuffle around variables
random.shuffle(new_command)

# Append "command" argument to now randomized (string+location) argument list
if holder != "":
    new_command.append(holder)

# Finally randomize provided value, eg "powershell.exe" and print result
print "\n%s\n" % (arg_randomize("N/A", command_args[0]) + " " + " ".join(new_command))



