import re


def transform_expression(lst) -> list:
    args = []
    for arg in lst:
        if arg.strip("-").isdigit():
            args.append(int(arg))
        elif re.match(r"-{2}", arg):
            args.append("+")
        elif re.match(r"-{3}", arg):
            args.append("-")
        elif re.match(r"\+{2,}", arg):
            args.append("+")
        else:
            args.append(arg)
    return args


if __name__ == '__main__':
    while True:
        arguments_str = input()
        try:
            arguments_list = [int(x) for x in arguments_str.split()]
            print(sum(arguments_list)) if len(arguments_str) > 0 else ""
        except ValueError:
            if arguments_str == "/exit":
                print("Bye!")
                exit()
            elif arguments_str == "/help":
                print("The program calculates the sum of numbers"
                      "bla bla bla")
            else:
                print("Argumets must be integers!")


# try to remove all "+" from the expression and
# if there is a munis before armument - make it negative
# sum all
