# Цель - заполучить мастер-ключ K. Для этого необходимо найти K1 || K2.
# Условия - возможность обнуления регистров устройства шифрования, возможность подавать открытые тексты и получать
# зашифрованные тексты.
#
# Механизм:
#   Для нахождения i-ого байта ключа K1 можно вносить ошибку в i-ый байт обрабатываемого блока,
#   после его прохождения через S-блок, перебирая различные входные сообщения до тех пор, пока не получим ошибку,
#   не повлекшую изменений,то есть C = C'.
#   Соответствующий байт до попадания в S-блок был равен S^(−1)(0).
#   Следовательно, i-й байт K1 можно найти как K1[i] = P[i] XOR S^(-1)(0).
#   Аналогинчым обарзом на втором раунде вычисляется ключ K2.


from pygost.gost3412 import GOST3412Kuznechik
from pygost.gost3412 import lp, strxor, PIinv, Linv


master_key = [x for x in range(32)]
plain_text = [0 for x in range(16)]
kuznyechik = GOST3412Kuznechik(master_key)


# функция для взлома ключа
def hack_key(rounds):
    result = [0 for x in range(16)]
    for i in range(16):
        # для каждого байта существует 2^8 = 256 возможных значений
        for j in range(256):
            plain_text[i] = j
            temp_text = plain_text
            # проводим необходимое количество раундов до начала атаки
            for round in range(rounds):
                temp_text = lp(bytearray(strxor(kuznyechik.ks[round], temp_text)))
            # атака
            temp_text = bytearray(strxor(kuznyechik.ks[rounds], temp_text))
            temp_text[i] = 0
            temp_text = lp(temp_text)
            # завершаем цикл шифрования
            for round in range(rounds + 1, 9):
                temp_text = lp(bytearray(strxor(kuznyechik.ks[round], temp_text)))
            temp_text = strxor(kuznyechik.ks[9], temp_text)
            # сравниваем "оригинальный" и полученный во время атаки зашифрованные тексты
            if temp_text == GOST3412Kuznechik.encrypt(kuznyechik, plain_text):
                if rounds == 0:
                    result[i] = plain_text[i] ^ PIinv[0]
                if rounds == 1:
                    result[i] = lp(bytearray(strxor(kuznyechik.ks[0], temp_text)))[i] ^ PIinv[0]
    return result


K0 = hack_key(0)
K1 = hack_key(1)
new_master_key = K0 + K1

print('Оригинальнй мастер-ключ: ', master_key)
print(' Полученный мастер-ключ: ', new_master_key)
if master_key == new_master_key:
    print('    ---> hacked')
else:
    print('    ---> failed')
