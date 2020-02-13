# --------------------------------------------------------------------------------------------
# Метод восхождения к вершине
# 1. Сгенерировать на основе нашего алфавита рандомный ключ-родитель, вычислить для него chi.
#    chi - Хи - значение, показывающее похожесть полученного текста на текст на английском языке.
#    Для анализа взят датасет 4-грамм из книги "Война и мир" на английском языке (4-грамма, ее количество в книге).
# 2. Выполнить перестановку двух букв в ключе, вычислить новый Хи и сравнить с текущим.
#    Если Хи выше, то сделать новый ключ ключом-родителем и продолжить поиск.
# --------------------------------------------------------------------------------------------

from pycipher import SimpleSubstitution as SimpleSub
import random
import re
from ngram_chi import ngram_chi
fitness = ngram_chi('english_quadgrams.txt') # файл со статистикой встречаемости 4-грамм в английском языке


cipher_text = 'Pvhvobg jvvep jvwa nl, csofwx jrfmr Qboafw Vcvw pascfvc rfp xobqqbo, ovhfvjvc arv nyyep yw vafisvaav, bwc ovbc hyobmfyspgl arv nyyep arba mbsxra rfp zbwml.  Yz rfp yjw mgbpp rv pbj wyarfwx.  Arv xfogp yz arv Gyasp Mgsn jywcvovc jrba rbc nvmyqv yz rfq bwc jyoofvc Dfq jfar'
#with open('cipher.txt', 'r') as file:
#    cipher_text = file.read().replace('\n', '')
#cipher_text = re.sub('[^A-Z]', '', cipher_text.upper())

max_key = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
max_chi = -99e9

parent_key = max_key[:]
parent_chi = max_chi

print("Шифр простой замены")
max_iterations = input("Максимальное количество итераций: ")
iterations = 0

while iterations < int(max_iterations):
    iterations = iterations + 1
    random.shuffle(parent_key)
    decipher_text = SimpleSub(parent_key).decipher(cipher_text)
    parent_chi = fitness.chi(decipher_text)
    count = 0
    while count < 1000:
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        child_key = parent_key[:]

        child_key[a], child_key[b] = child_key[b], child_key[a]
        decipher_text = SimpleSub(child_key).decipher(cipher_text)
        child_chi = fitness.chi(decipher_text)

        if child_chi > parent_chi:
            parent_chi = child_chi
            parent_key = child_key[:]
            count = 0
        count = count + 1

    if parent_chi > max_chi:
        max_chi, max_key = parent_chi, parent_key[:]
        print('\nЛучший результат:', max_chi, ', итерация', iterations)
        ss = SimpleSub(max_key)
        print('     гипотетический ключ: ' + ''.join(max_key))
        print('    гипотетический текст: ' + ss.decipher(cipher_text))
