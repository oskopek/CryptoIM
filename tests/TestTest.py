def testFail():
    assert False

def testPass():
    pass

def testError():
    int("lol")

def test_evens():
    for i in range(0, 5):
        yield check_even, i, i*2

def check_even(n, nn):
    assert n % 2 == 0 or nn % 2 == 0