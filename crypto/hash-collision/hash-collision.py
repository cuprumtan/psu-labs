import hashlib
import random
import string


# функция генерации байтовой строки
def generate_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


# функция поиска коллизии
def search_collision(L, R, size, invisible_symbol=' '):
    counter = 1
    L_list = []
    R_list = []
    flag = False
    L_hash = ''
    R_hash = ''
    while not flag:
        L_hash = hashlib.sha256(L.encode()).hexdigest()
        L_list.append(L_hash[0:size])
        R_hash = hashlib.sha256(R.encode()).hexdigest()
        R_list.append(R_hash[0:size])
        for i in L_list:
            for j in R_list:
                if i == j:
                    flag = True
        L += invisible_symbol
        R += invisible_symbol
        counter += 1
    return counter


# функция поиска среднего количества итераций
def get_avg():
    sum = 0
    for i in range(5):
        L = generate_string()
        R = generate_string()
        sum += search_collision(L, R, 2)
    avg = sum / 5
    return avg


avg = get_avg()
print('Хеш: md5; среднее количество итераций для получения коллизии II рода = ', avg)
    
