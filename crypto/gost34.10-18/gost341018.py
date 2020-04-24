import gost341118 as streebog


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







