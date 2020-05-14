from itertools import combinations
from math import gcd
import random


class RSAEncryption:
    def __init__(self):
        pass

    # проверка на простое число
    def is_prime(self, x):
        if x <= 1:
            return False
        for i in range(2, x - 1):
            if x % i == 0:
                return False
        return True

    # генерация случайного числа от 1000 до 5000
    def generate_prime(self):
        while True:
            self.number = random.randint(1000, 5000)
            if self.is_prime(self.number):
                return self.number

    # n = p * q
    def n(self, p, q):
        return p*q

    # функция Эйлера
    def euler(self, p, q):
        return (p-1)*(q-1)

    # открытая экспонента e
    def euclid(self, a, b):
        while b != 0:
            return gcd(b, a % b)
        else:
            return a

    # проверка на взоимнопростые числа
    def is_coprime(self, list):
        for number, phi in combinations(list, 2):
            if self.euclid(number, phi) == 1:
                return True
        return False

    # секретная экспонента d
    def egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, y, x = self.egcd(b % a, a)
            return gcd, x-(b//a)*y, y

    def modular_exponentiation(self, x, n, m):
        return pow(x, n, m)

    def encrypt(self, plain_text, private_key, phi):
        c = self.modular_exponentiation(plain_text, private_key, phi)
        return c


class RSADecryption:
    def __init__(self):
        pass

    def modular_exponentiation(self, x, n, m):
        return pow(x, n, m)

    def decrypt(self, cipher_text, public_key, phi):
        p = self.modular_exponentiation(cipher_text, public_key, phi)
        return p
