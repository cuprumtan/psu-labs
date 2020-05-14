from RSA import *
import sys


def generate_public_keypair():
    rsa_encryption = RSAEncryption()

    key_p = rsa_encryption.generate_prime()
    key_q = rsa_encryption.generate_prime()

    while key_q == key_p:
        key_q = rsa_encryption.generate_prime()

    if rsa_encryption.is_prime(key_p):
        pass
    else:
        print("\nОШИБКА p - не простое число\n")
        sys.exit(1)

    if rsa_encryption.is_prime(key_q):
        pass
    else:
        print("\nОШИБКА q - не простое число\n")
        sys.exit(1)

    key_n = rsa_encryption.n(key_p, key_q)

    phi_n = rsa_encryption.euler(key_p, key_q)

    coprime_list = []

    for i in range(2, phi_n):
        if rsa_encryption.is_coprime([i, phi_n]):
            coprime_list.append(i)

    key_e = coprime_list[random.randint(0, len(coprime_list) - 1)]

    if gcd(key_e, phi_n) == 1:
        pass
    else:
        print("\nОШИБКА E - не взаимнопростое число с phi(n)\n")
        sys.exit(1)

    _, key_d, _ = rsa_encryption.egcd(key_e, phi_n)

    while key_e == key_d:
        key_e = coprime_list[random.randint(0, len(coprime_list) - 1)]
        _, key_d, _ = rsa_encryption.egcd(key_e, phi_n)

    if key_d < 0:
        key_d = key_d % phi_n

    if gcd(key_d, phi_n) == 1:
        pass
    else:
        print("\nОШИБКА D - не взаимнопростое число с phi(n)\n")
        sys.exit(1)

    public_key = (key_e, key_n)
    private_key = (key_d, key_n)

    return public_key, private_key


def generateNonce(length=2):
    nonce = int(''.join([str(random.randint(0, 9)) for i in range(length)]))
    return nonce
