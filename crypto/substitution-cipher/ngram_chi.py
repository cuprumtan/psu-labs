# --------------------------------------------------------------------------------------------
# 1. Собирается словарь из N-грамм ngrams вида N-грамма: количество ее появлений;
#    L - длина N-граммы, N - общее количество N-грамм
# 2. Для каждой N-граммы вычисляется ее логарифмическая вероятность: p = log10(count(N-грамма)/N),
#    где count(N-грамма) - количество появлений текущей N-граммы.
# 3. Общее Хи для текста формируется как сумма логарифмических вероятностей N-грамм этого текста.
# --------------------------------------------------------------------------------------------

from math import log10


class ngram_chi(object):
    def __init__(self, ngramfile, sep=' '):

        self.ngrams = {}
        for line in open(ngramfile):
            key, count = line.split(sep)
            self.ngrams[key] = int(count)
        self.L = len(key)
        self.N = sum(self.ngrams.values())
        
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key])/self.N)
        self.floor = log10(0.01/self.N)

    def chi(self, text):
        chi = 0
        ngrams = self.ngrams.__getitem__
        for i in range(len(text) - self.L + 1):
            if text[i:i+self.L] in self.ngrams:
                chi += ngrams(text[i:i+self.L])
            else:
                chi += self.floor
        return chi
