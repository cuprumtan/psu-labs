#include <stdint.h>
#include <string.h>
#include "streebog.h"


/* функция подстановки из pi */
void S(uint8_t *state)
{
    uint8_t i = 0;

    for(i = 0; i < 64; i++)
    {
        state[i] = pi[state[i]];
    }
}


// функция подстановки из tau
void P(unsigned char *state)
{
    uint8_t i = 0;
    uint8_t t[64] = {};

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
    uint8_t i = 0, j = 0, k = 0;

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

