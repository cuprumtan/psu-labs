#include <stdint.h>
#include <string.h>
#include "streebog.h"


/* функция подстановки из pi */
void S(uint8_t *state)
{
    uint8_t i;

    for(i = 0; i < 64; i++)
    {
        state[i] = pi[state[i]];
    }
}


// функция подстановки из tau
void P(uint8_t *state)
{
    uint8_t i, t[64] = {};

    for(i = 0; i < 64; i++)
    {
        t[i] = state[tau[i]];
    }

    memcpy(state, t, 64);
}


/* функция умножения вектора state на бинарную матрицу A */
void L(uint8_t *state)
{
    uint64_t v = 0;
    uint8_t i, j, k;

    for (i = 0; i < 8; i++)
    {
        v = 0;
        for(k = 0; k < 8; k++)
        {
            for(j = 0; j < 8; j++)
            {
                if ((state[i * 8 + k] & (1<<(7 - j))) != 0)
                    v ^= A[k * 8 + j];
            }
        }
        for(k = 0; k < 8; k++)
        {
            state[i * 8 + k] = (v & ((uint64_t)0xFF << (7 - k) * 8)) >> (7 - k) * 8;
        }
    }
}


// функция XOR с элементом массива C
void XORC(const void *a, const void *b, void *c)
{
    uint8_t i;
    const uint64_t *A = a, *B = b;
    uint64_t *C = c;

    for(i = 0; i < 8; i++)
    {
        C[i] = A[i] ^ B[i];
    }
}


// функция KeySchedule(K, i)
// формирует временный ключ на каждом раунде функции E(K, m)
void KeySchedule(uint8_t *K, uint8_t i)
{
    XORC(K, C[i], K);
    S(K);
    P(K);
    L(K);
}


// функция E(K, m)
void E(uint8_t *K, const uint8_t *m, uint8_t *state)
{
    uint8_t i;

    memcpy(K, K, 64);

    XORC(m, K, state);

    for(i = 0; i < 12; i++)
    {
        S(state);
        P(state);
        L(state);
        KeySchedule(K, i);
        XORC(state, K, state);
    }
}


// функция сжатия gN(N, m, h)
void gN(const uint8_t *N, const uint8_t *m, uint8_t *h)
{
    uint8_t t[64], K[64];

    XORC(N, h, K);
    S(K);
    P(K);
    L(K);
    E(K, m, t);
    XORC(t, h, t);
    XORC(t, m, h);
}


// функция для вычисления mod 2^512
void MOD2512(const uint8_t *a, const uint8_t *b, uint8_t *c)
{
    int i, t;

    for(i = 63; i >= 0; i--)
    {
        t = a[i] + b[i] + (t >> 8);
        c[i] = t & 0xFF;
    }
}



// функция хеширования
void hash_func(uint8_t *IV, const uint8_t *message, uint64_t length, uint8_t *out)
{
    uint8_t v512[64] = {0x00}; v512[62] = 0x02;
    uint8_t v0[64] = {0x00};
    uint8_t Sigma[64] = {0x00};
    uint8_t N[64] = {0x00};
    uint8_t m[64], *hash = IV;
    uint64_t len = length;

    while (len >= 512)
    {
        memcpy(m, message + len/8 - 63 - ((len & 0x7) == 0 ), 64);

        gN(N, hash, m);
        MOD2512(N, v512, N);
        MOD2512(Sigma, m, Sigma);
        len -= 512;
    }

}
