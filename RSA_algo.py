import random
import math
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    prime = random.randint(min_val, max_val)
    while not is_prime(prime):
        prime = random.randint(min_val, max_val)
    return prime

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Modular inverse (private key) doesn't exist")



def generate_keys():
    p = generate_prime(100, 300)
    q = generate_prime(100, 300)
    while p == q:
        q = generate_prime(100, 300)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 3
    while math.gcd(e, phi) != 1:
        e += 2
    d = mod_inverse(e, phi)
    return (n, e), (n, d)

def rsa_encrypt(message, key):
    n, e = key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

def rsa_decrypt(encrypted_message, key):
    n, d = key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message