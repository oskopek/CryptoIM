# Fibonacci numbers module

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a+b

def fib2(n): # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

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
