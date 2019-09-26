import binascii
import numpy
import yaml

# read configs
with open('DES.yml', 'r') as file:
    config = yaml.load(file)

plain_text_char = config['plain_text']['value']
key_text_char = config['key_text']['value']
plain_text_binary_ro = []
key_text_binary_ro = []
plain_text_binary_rw = []
key_text_binary_rw = []

# initial permutation
IP_table = [58, 50, 42, 34, 26, 18, 10,  2,
            60, 52, 44, 36, 28, 20, 12,  4,
            62, 54, 46, 38, 30, 22, 14,  6,
            64, 56, 48, 40, 32, 24, 16,  8,
            57, 49, 41, 33, 25, 17,  9,  1,
            59, 51, 43, 35, 27, 19, 11,  3,
            61, 53, 45, 37, 29, 21, 13,  5,
            63, 55, 47, 39, 31, 23, 15,  7]

KP_table = [57, 49, 41, 33, 25, 17,  9,  8,
             1, 58, 50, 42, 34, 26, 18, 16,
            10,  2, 59, 51, 43, 35, 27, 24,
            19, 11,  3, 60, 52, 44, 36, 32,
            63, 55, 47, 39, 31, 23, 15, 40,
             7, 62, 54, 46, 38, 30, 22, 48,
            14,  6, 61, 53, 45, 37, 29, 56,
            21, 13,  5, 28, 20, 12,  4, 64]


key_table = [14, 17, 11, 24,  1,  5,  3, 28,
             15,  6, 21, 10, 23, 19, 12,  4,
             26,  8, 16,  7, 27, 20, 13,  2,
             41, 52, 31, 37, 47, 55, 30, 40,
             51, 45, 33, 48, 44, 49, 39, 56,
             34, 53, 46, 42, 50, 36, 29, 32]

key_shift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

E_table = [32,  1,  2,  3,  4,  5,  4,  5,
            6,  7,  8,  9,  8,  9, 10, 11,
           12, 13, 12, 13, 14, 15, 16, 17,
           16, 17, 18, 19, 20, 21, 20, 21,
           22, 23, 24, 25, 24, 25, 26, 27,
           28, 29, 28, 29, 30, 31, 32,  1]

S_blocks = [
    [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
      0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
      4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
     15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13],
    
    [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
      3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
      0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
     13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9],
    
    [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
     13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
     13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
      1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12],
    
    [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
     13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
     10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
      3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14],
    
    [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
     14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
      4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
     11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5, 3],
    
    [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
     10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
      9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13,  11, 6,
      4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13],
    
    [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
     13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
      1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
      6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12],
    
    [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
      1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
      7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
      2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11]
    ]


def char_to_binary(content, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(content.encode(encoding, errors)), 16))[2:]
    return [int(x) for x in list(bits.zfill(8 * ((len(bits) + 7) // 8)))]


def permute(content, reference):
    return [int(content[x-1]) for x in reference]


def add_parity_bits(content):
    result = []
    count = 0
    for i in range(56):
        if (count + 1) % 8 == 0:
            if (sum(content[i-7:i]) % 2 == 0):
                result.append(1)
                count += 1
            else:
                result.append(0)
                count += 1
        result.append(content[i])
        count += 1
    if sum(content[56-7:56]) % 2 == 0:
        result.append(1)
    else:
        result.append(0)
    return [int(x) for x in result]


def define_C0(content):
    result = []
    for i in range(32):
        if (i + 1) % 8 != 0:
            result.append(content[i])
    return [int(x) for x in result]


def define_D0(content):
    result = []
    for i in range(32, 64):
        if (i + 1) % 8 != 0:
            result.append(content[i])
    return [int(x) for x in result]


def shift(content, step):
    return list(numpy.roll(content, -int(step)))


def generate_keys(C0, D0):
    keys = []
    for i in range(16):
        shifted_C0 = shift(C0, key_shift[i])
        shifted_D0 = shift(D0, key_shift[i])
        common_vector = shifted_C0 + shifted_D0
        round_key = permute(common_vector, key_table)
        keys.append(round_key)
        C0 = shifted_C0
        D0 = shifted_D0
    return keys


def round_function(content, round, keys):
    E = permute(content + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], E_table)
    xor = numpy.bitwise_xor(E, keys[round])
    B_blocks = []
    for i in range(0, 42, 6):
        B_blocks.append(xor[i:i + 6])
    B_blocks_S = []
    


def encrypt(content, keys):
    L = content[0:32]
    R = content[32:64]
    l_new = []
    R_new = []
    for i in range(16):
        L_new = R
        R_new = numpy.bitwise_xor(round_function(R, i), L)


def print_as_table(content, delimiter):
    for i in range(64):
        if i % 8 == 0:
            print(delimiter, end='')
        if content[i] // 10 > 0:
            print(' '.format(content[i]), end='')
        else:
            print('0 '.format(content[i]), end='')


def output():
    global plain_text_binary_ro
    global key_text_binary_ro
    global plain_text_binary_rw
    global key_text_binary_rw
    print('PSU, 2019')
    print('DES algorithm demonstration\n')
    print('Входные данные:')
    print('----------------------------')
    print('| Исходный текст: ' + plain_text_char + ' |')
    print('| Ключ:           ' + key_text_char + '  |')
    print('----------------------------\n')
    input()
    plain_text_binary_ro = char_to_binary(plain_text_char)
    key_text_binary_ro = char_to_binary(key_text_char)
    print('DES')
    print('|')
    print('|--- Двоичное представление')
    print('|    |')
    print('|    | Исходный текст: ' + ''.join(str(x) for x in plain_text_binary_ro))
    print('|    | Ключ:           ' + ''.join(str(x) for x in key_text_binary_ro))
    print('|')
    input('|')
    print('|--- Генерация ключей')
    print('|    |')
    print('|    |--- Добавление битов четности')
    print('|    |    |')
    key_text_binary_rw = add_parity_bits(key_text_binary_ro)
    print('|    |    | ' + ''.join(str(x) for x in key_text_binary_rw))
    input('|    |')
    print('|    |--- Начальная перестановка ключа')
    print('|    |    |')
    print('|    |    | Таблица перестановки:')
    print('|    |    |', end='')
    print_as_table(KP_table, '\n|    |    | ')
    print('\n|    |    |')
    print('|    |    | Результат применения таблицы перестановки к ключу:')
    print('|    |    | ', end='')
    key_text_binary_rw = permute(key_text_binary_rw, KP_table)
    print_as_table(key_text_binary_rw, '\n|    |    | ')
    print('\n|    |    |')
    C0 = define_C0(key_text_binary_rw)
    print('|    |    | Вектор C0 = ' + ''.join(str(x) for x in C0))
    D0 = define_D0(key_text_binary_rw)
    print('|    |    | Вектор D0 = ' + ''.join(str(x) for x in D0))
    print('|    |    |')
    input('|    |    |')
    print('|    |    |--- Ключи:')
    print('|    |    |    |')
    keys = generate_keys(C0, D0)
    for i in range(16):
        if i // 10 > 0 or i == 9:
            print('|    |    |    | K_ = '.format((i + 1), ''.join(str(x) for x in keys[i])))
        else:
            print('|    |    |    | K_ =  '.format((i + 1), ''.join(str(x) for x in keys[i])))
    print('|')
    input('|')
    print('|--- IP')
    print('|    |')
    print('|    | Таблица IP:')
    print('|    | ', end='')
    print_as_table(IP_table, '\n|    | ')
    print('\n|    |')
    print('|    | Результат применения таблицы IP к исходному тексту:')
    print('|    | ', end='')
    plain_text_binary_rw = permute(plain_text_binary_ro, IP_table)
    print_as_table(plain_text_binary_rw, '\n|    | ')
    print('\n|')
            
output()

# Сети вт: эволюция 10 Base, 100 Base, Гигабитные соединения (в общем)
