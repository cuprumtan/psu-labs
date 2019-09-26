import binascii
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


def char_to_binary(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
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


def print_as_table(content, delimiter):
    for i in range(64):
        if i % 8 == 0:
            print(delimiter, end='')
        if content[i] // 10 > 0:
            print('{} '.format(content[i]), end='')
        else:
            print('0{} '.format(content[i]), end='')


def output():
    global plain_text_binary_ro
    global key_text_binary_ro
    global plain_text_binary_rw
    global key_text_binary_rw
    print('PSU, 2019')
    print('DES algorithm demonstration\n')
    print('Input data:')
    print('------------------------')
    print('| Plain text: ' + plain_text_char + ' |')
    print('| Key text:   ' + key_text_char + '  |')
    print('------------------------\n')
    plain_text_binary_ro = char_to_binary(plain_text_char)
    key_text_binary_ro = char_to_binary(key_text_char)
    print('DES')
    print('|')
    print('|--- Binary input')
    print('|    |')
    print('|    | Plain text: ' + ''.join(str(x) for x in plain_text_binary_ro))
    print('|    | Key text:   ' + ''.join(str(x) for x in key_text_binary_ro))
    print('|')
    print('|--- IP')
    print('|    |')
    print('|    | IP table:')
    print('|    | ', end='')
    print_as_table(IP_table, '\n|    | ')
    print('\n|    |')
    print('|    | IP result for plain text:')
    print('|    | ', end='')
    plain_text_binary_rw = permute(plain_text_binary_ro, IP_table)
    print_as_table(plain_text_binary_rw, '\n|    | ')
    print('\n|')
    print('|--- Key generating')
    print('|    |')
    print('|    |--- Adding parity bits')
    print('|    |    |')
    key_text_binary_rw = add_parity_bits(key_text_binary_ro)
    print('|    |    | ' + ''.join(str(x) for x in key_text_binary_rw))
    print('|    |')
    print('|    |--- Key permutation')
    print('|    |    |')
    print('|    |    | Permutation table:')
    print('|    |    |', end='')
    print_as_table(KP_table, '\n|    |    | ')
    print('\n|    |    |')
    print('|    |    | IP result for plain text:')
    print('|    |    | ', end='')
    key_text_binary_rw = permute(key_text_binary_rw, KP_table)
    print_as_table(key_text_binary_rw, '\n|    |    | ')
    print('\n|    |    |')
    C0 = define_C0(key_text_binary_rw)
    print('|    |    | C0 = ' + ''.join(str(x) for x in C0))
    D0 = define_D0(key_text_binary_rw)
    print('|    |    | D0 = ' + ''.join(str(x) for x in D0))
    print('|    |    | ')
    print('|    | ')
    print('|    |--- Generating keys:')
    print('|    |    |')
    print('|    |    |')

output()

# Сети вт: эволюция 10 Base, 100 Base, Гигабитные соединения (в общем)
