import re


def transform_expression(string) -> str:
    """Removing spaces"""
    string = "".join(string.split())

    """single argument case"""
    if re.search(r"[-+]?\d+$", string):
        return string
    elif re.search(r"(([-+]?\d+)[-|\+|\*|\/](\d+$))", string):
        args = []
        for arg in string:
            if re.match(r"[-]", arg):
                args.append("+" if len(arg) % 2 == 0 else "-")
            elif re.match(r"\+{2,}", arg):
                args.append("+")
            else:
                args.append(arg)
        args = "".join(args)
        return args
    else:
        print("Invalid expression")



def handle_command(command):
    if command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("The program calculates a given expression")
    else:
        print("Unknown command")



def compute_expression(math_expression):
    math_expression = [element for element in math_expression]
    print(math_expression)



if __name__ == '__main__':
    while True:
        arguments_str = input()
        if arguments_str.startswith("/"):
            handle_command(arguments_str)
        elif len(arguments_str) == 0:
            continue
        else:
            if not arguments_str[-1].isnumeric():
                print("Invalid expression")
            else:
                expression = transform_expression(arguments_str)
                print(eval(expression))  # this is a great build-in method to calculate the expression, but I need to try implement mine
                #compute_expression(expression)
