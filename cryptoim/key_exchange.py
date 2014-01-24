import random
from const import PRIMES

random = random.SystemRandom()
#Random generator useable for cryptography

def generate_random(limit_lo, limit_hi):
    return random.randint(limit_lo, limit_hi)

def prime_pick():
    rnd = generate_random(0, len(PRIMES))
    return PRIMES[rnd]

def base_pick():
    rnd = generate_random(1, 15)
    return rnd

def make_public_key(prime, base, p_number):
    pub_key = (base ** rnumber) % prime
    return pub_key

def make_private_key(prime, pub_key, p_number):
    private_key = (pub_key ** p_number) % prime
    return private_key
