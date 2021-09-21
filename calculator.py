import re


def transform_expression(string) -> str:
    """Removing spaces"""
    string = "".join(string.split())

    if not re.match(r"[\w+\-]+$", string):
        """ add * and devisors"""
        """ add check that operators are not 1st and lst"""
        print("Invalid expression")
    elif len(string) == 1:
        return string
    else:
        args = []
        for arg in string:
            if re.match(r"[-]", arg):
                args.append("+" if len(arg) % 2 == 0 else "-")
            elif re.match(r"\+{2,}", arg):
                args.append("+")
            else:
                args.append(arg)
        return "".join(args)


def compute_expression(math_expression):
    math_expression = [element for element in math_expression]
    print(math_expression)



if __name__ == '__main__':
    while True:
        arguments_str = input()
        if arguments_str == "/exit":
            print("Bye!")
            exit()
        elif arguments_str == "/help":
            print("The program calculates a given expression")
        elif len(arguments_str) == 0:
            continue
        else:
            expression = transform_expression(arguments_str)
            print(eval(expression))  # this is a great build-in method to calculate the expression, but I need to try implement mine
            #compute_expression(expression)

