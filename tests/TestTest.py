# A failing test
def testFail():
    assert False

# A passing test
def testPass():
    pass

# A tests that throws an error
def testError():
    int("lol")

# A test generator
def test_evens():
    for i in range(0, 5):
        yield check_even, i, i*2

# A test generator checker
def check_even(n, nn):
    assert n % 2 == 0 or nn % 2 == 0