import random


# функция для поиска обратного по модулю числа
def inverse_mod(A, N):
    T = 0
    R = 0
    if A < 0:
        return N - inverse_mod(-A, N)
    T, newt = 0, 1
    R, newr = N, A
    while newr != 0:
        int_value = R // newr
        T, newt = newt, T - int_value * newt
        R, newr = newr, R - int_value * newr
    if R > 1:
        return -1
    if T < 0:
        T = T + N
    return T


# класс написан с помощью pygost
class GOST3410Curve(object):
    def __init__(self, p, q, a, b, x, y, e=None, d=None):
        self.p = p
        self.q = q
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.e = e
        self.d = d

    def pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def __add__(self, other):
        tx = 0
        ty = 0
        t = 0
        if self.x == other.x and self.y == other.y:
            t = ((3 * self.x * self.x + self.a) * inverse_mod(2 * self.y, self.p)) % self.p
        else:
            tx = self.pos(other.x - self.x) % self.p
            ty = self.pos(other.y - self.y) % self.p
            t = (ty * inverse_mod(tx, self.p)) % self.p
        tx = self.pos(t * t - self.x - other.x) % self.p
        ty = self.pos(t * (self.x - tx) - self.y) % self.p
        return GOST3410Curve(self.p, self.q, self.a, self.b, tx, ty)

    def __rmul__(self, other):
        p_result = GOST3410Curve(self.p, self.q, self.a, self.b, self.x, self.y)
        temp = GOST3410Curve(self.p, self.q, self.a, self.b, self.x, self.y)
        x = other - 1
        while x != 0:
            if x % 2 != 0:
                p_result += temp
                x -= 1
            x //= 2
            temp = temp + temp
        return p_result

    def exp(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        if degree == 0:
            raise ValueError(">> Некорректное значение степени")
        degree -= 1
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty

    def st(self):
        if self.e is None or self.d is None:
            raise ValueError(">> Не скрученная кривая Эдвардса")
        if self._st is not None:
            return self._st
        self._st = (
            self.pos(self.e - self.d) * inverse_mod(4, self.p) % self.p,
            (self.e + self.d) * inverse_mod(6, self.p) % self.p,
        )
        return self._st

    def generate_keys(self):
        d = random.randint(1, self.q - 1)
        q_point = d * self
        return d, q_point


# функция для генерации публичного ключа
def public_key(curve, prv):
    return curve.exp(prv)


# функция для вычисления подписи
def sign(curve, message, private_key, k=0):
    e = message % curve.q
    if e == 0:
        e = 1
    if k == 0:
        k = random.randint(1, curve.q - 1)
    r, s = 0, 0
    while r == 0 or s == 0:
        c_point = k * curve
        r = c_point.x % curve.q
        s = (r * private_key + k * e) % curve.q
    return r, s


# функция подтверждения
def verify(curve, message, sign, public_key):
    r1, s1 = sign
    if r1 <= 0 or r1 >= curve.q or s1 <= 0 or s1 >= curve.q:
        return False
    e = message % curve.q
    if e == 0:
        e = 1
    nu = inverse_mod(e, curve.q)
    z1 = (sign[1] * nu) % curve.q
    z2 = (-sign[0] * nu) % curve.q
    c_point = z1 * curve + z2 * public_key
    r = c_point.x % curve.q
    if r == sign[0]:
        return True
    return False





