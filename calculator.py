# write your code here
a, b = input().split()


def summarize(arg1, arg2):
    try:
        sum_result = int(arg1) + int(arg2)
    except ValueError:
        print("Argumets must be integers!")
    return sum_result
        

if __name__ == '__main__':
    print(summarize(a, b))
    
