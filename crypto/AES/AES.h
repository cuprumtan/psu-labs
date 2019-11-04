/*
   Created by cuprumtan on 2019-11-04.
*/

#include <stdint.h>

#ifndef AES_H
#define AES_H

#define BLOCKLENGTH 16      /* длина блока данных в байтах */
#define KEYLENGTH 16        /* длина ключа в байтах */
#define KEYEXPSIZE 176      /* длина расширенного ключа в байтах */
#define WORDLENGTH 4        /* длина слова в байтах */
#define Nb 4                /* количество слов в одном блоке */
#define Nk 4                /* количество слов в ключе */
#define Nr 10               /* количество раундов */

struct AES_context
{
    uint8_t RoundKey[KEYEXPSIZE];
};

void AES_init_context(struct AES_context* context, const uint8_t* key);
void AES_encrypt(const struct AES_context* context, uint8_t* buffer);
void AES_decrypt(const struct AES_context* context, uint8_t* buffer);

#endif
