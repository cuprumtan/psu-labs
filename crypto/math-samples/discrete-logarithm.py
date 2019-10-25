import math


# (x^y)%p in O(log y)
def pow_mod(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1  # y = y/2
        x = (x * x) % p
    return res


# возвращает -1, если ответа нет
def discrete_logarithm(a, b, m):
    n = int(math.sqrt(m) + 1)
    value = [0] * m
    for i in range(n, 0, -1):
        value[pow_mod(a, i * n, m)] = i
    for j in range(n):
        cur = (pow_mod(a, j, m) * b) % m
        if value[cur]:
            ans = value[cur] * n - j
            if ans < m:
                return ans
    return -1


# b = a^x (mod m)
# b = a^(np - q) (mod m)
# (a, m) =1 --> ba^q = a^(np) (mod m)
# найти p b q такие, что f_1(p) = f_2(q)

a = 15
b = 46
m = 53

print(discrete_logarithm(a, b, m))
