# Fibonacci numbers module

def fib3(n): # return Fibonacci properly
    result = []
    prev, num = 0, 1

    for i in range (0, n):
        result.append(num)
        tmp = prev
        prev = num
        num += tmp

    return result


if __name__ == "__main__":
    import sys
    print fib3(int(sys.argv[1]))
