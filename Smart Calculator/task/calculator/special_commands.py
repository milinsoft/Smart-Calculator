class SpecialCommand:
    HELP = """
The program calculates a given expression.
1. Acceptable math expressions: '+', '-', '/', '*', '^'
2. Additional functionality: you can use braces'( )' and variables.
3. Variables are case-sensetive, 'a' and 'A' is not the same, and can contain only latin letters.
4. To assign a variable use the syntax like: a = 1
"""

    @staticmethod
    def execute(command):
        if command == "/exit":
            print("Bye!")
            exit()
        elif command == "/help":
            print(SpecialCommand.HELP)
        else:
            print("Unknown command")
