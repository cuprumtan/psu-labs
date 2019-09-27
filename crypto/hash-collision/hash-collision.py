import hashlib

# входные строки
L = 'february'
R = 'sandwich'

# невидимый символ
invisible_symbol = ' '


def search_collision(L, R, size, invisible_symbol):
    counter = 1
    L_list = []
    R_list = []
    flag = False
    L_hash = ''
    R_hash = ''
    while not flag:
        L_hash = hashlib.md5(L.encode()).hexdigest()
        L_list.append(L_hash[0:size])
        R_hash = hashlib.md5(R.encode()).hexdigest()
        R_list.append(R_hash[0:size])
        for i in L_list:
            for j in R_list:
                if i == j:
                    flag = True
        L += invisible_symbol
        R += invisible_symbol
        counter += 1
        print('Итерация {}'.format(counter))
    return counter


number_of_iterations = search_collision(L, R, 2, invisible_symbol)
print(number_of_iterations)
