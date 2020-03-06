key = 'keytext'
plain_text = 'plaintext'


def RC4(key):
    key_length = len(key)
    S = [x for x in range(256)]
    # начальное заполнение S-box
    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % key_length])) % 256
        S[i], S[j] = S[j], S[i]
    # генерация случайных 8-битовых слов
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K
    #return K


keys = RC4(key)

for symbol in plain_text:
    print('{:02x} '.format(ord(symbol) ^ keys.__next__()), end='')
