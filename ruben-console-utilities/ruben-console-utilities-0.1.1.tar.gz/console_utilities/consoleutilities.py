def input_int(prompt):
    input_valid = False
    while not input_valid:
        try:
            number = int(input(prompt))
            input_valid = True
            return number
        except ValueError as e:
            print("Integers only! ({0})".format(e))


def input_float(prompt):
    input_valid = False
    while not input_valid:
        try:
            number = float(input(prompt))
            input_valid = True
            return number
        except ValueError as e:
            print("Real numbers only! ({0})".format(e))


def input_option_char(valid_options, prompt="Choose option: "):
    option = ""
    input_valid = False
    while not input_valid:
        option = input(prompt).lower()
        for valid_option in valid_options:
            if option == valid_option:
                input_valid = True
                break
        if not input_valid:
            print("Invalid option!")
    return option


def input_option_int(options, prompt="Choose option: "):
    for i in range(0, len(options)):
        print("  {0}: {1}".format(i, options[i]))
    while True:
        option = input_int(prompt)
        if 0 <= option < len(options):
            break
        else:
            print("Invalid option!")
    return option


def input_y_or_n(prompt):
    return input(prompt).lower() == "y"
