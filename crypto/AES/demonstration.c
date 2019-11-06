/*
   Created by cuprumtan on 2019-11-05.
*/


#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "AES.h"


uint8_t* key = "potatoandsausage";                                      /* 16 байт */
uint8_t* plain_text = "the quick brown fox jumps over the lazy dog";    /* любой длины */


/* Дополняет или урезает ключ до KEYLENGTH */
static uint8_t* EditKey(uint8_t* key) {
    uint8_t i;

    uint8_t* edited_key = (uint8_t*)malloc(KEYLENGTH*sizeof(uint8_t));

    for (i = 0; i < KEYLENGTH*sizeof(uint8_t); i ++)
        edited_key[i] = '0';

    for (i = 0; i < strlen(key) && i < strlen(edited_key); i++)
        edited_key[i] = key[i];

    return edited_key;
}


/* Дополняет исходный текст до длины, кратной BLOCKLENGTH */
static uint8_t* EditPlainText(uint8_t* plain_text) {
    uint8_t i;

    unsigned int length = strlen(plain_text);

    while (length % BLOCKLENGTH != 0)
    {
        length++;
    }

    uint8_t* edited_plain_text = (uint8_t*)malloc(length*sizeof(uint8_t));

    for (i = 0; i < length*sizeof(uint8_t); i ++)
        edited_plain_text[i] = '0';

    for (i = 0; i < strlen(plain_text) && i < length; i++)
    {
        edited_plain_text[i] = plain_text[i];
    }

    return edited_plain_text;
}


int main() {
    uint8_t i;

    printf("Демонстрация работы алгоритма AES128\n");
    printf("\n");

    printf("Исходный текст: "); printf(plain_text); printf("\n");
    keypress(0);
    printf("-------------------------------------------------------------------------------------------------------\n");
    uint8_t* new_key = EditKey(key);
    printf("        Ключ: "); printf(new_key); printf("\n");
    printf("  Ключ в HEX: "); print_hex(new_key, "              "); printf("\n");
    printf("\n");
    uint8_t* new_plain_text = EditPlainText(plain_text);
    printf("       Текст: "); printf(new_plain_text); printf("\n");
    printf(" Текст в HEX: "); print_hex(new_plain_text, "              "); printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");

    keypress(0);
    struct AES_context context_encrypt;
    AES_init_context(&context_encrypt, new_key);

    for (i = 0; i < (int)strlen(new_plain_text)/BLOCKLENGTH; i++)
    {
        printf("   |\n");
        printf("   [Блок %d]\n", i + 1);
        printf("   |\n");
        AES_encrypt(&context_encrypt, new_plain_text + (i * 16));
    }

    printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");
    printf("        Шифр: ");
    printf(new_plain_text); printf("\n");
    printf("  Шифр в HEX: ");
    print_hex(new_plain_text, "              "); printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");

    keypress(0);
    struct AES_context context_decrypt;
    AES_init_context(&context_decrypt, new_key);

    for (i = 0; i < (int)strlen(new_plain_text)/BLOCKLENGTH; i++)
    {
        printf("   |\n");
        printf("   [Блок %d]\n", i + 1);
        printf("   |\n");
        AES_decrypt(&context_decrypt, new_plain_text + (i * 16));
    }
    printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");
    printf("      Дешифр: ");
    printf(new_plain_text); printf("\n");
    printf("Дешифр в HEX: ");
    print_hex(new_plain_text, "              "); printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");
}
