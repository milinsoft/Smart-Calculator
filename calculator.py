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
            else:
                print("Argumets must be integers!")
