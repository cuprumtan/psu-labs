/*
   Created by cuprumtan on 2019-11-05.
*/


#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include "AES.h"


uint8_t* key = "potatoandsausage";                                      /* 16 байт */
uint8_t* plain_text = "the quick brown fox jumps over the lazy dog";    /* любой длины */


/* сон до нажатия клавиши */
int keypress(unsigned char echo)
{
    struct termios savedState, newState;
    int c;

    if (-1 == tcgetattr(STDIN_FILENO, &savedState))
    {
        return EOF;     /* error on tcgetattr */
    }

    newState = savedState;

    if ((echo = !echo))
    {
        echo = ECHO;    /* echo bit to disable echo */
    }

    /* disable canonical input and disable echo.  set minimal input to 1. */
    newState.c_lflag &= ~(echo | ICANON);
    newState.c_cc[VMIN] = 1;

    if (-1 == tcsetattr(STDIN_FILENO, TCSANOW, &newState))
    {
        return EOF;     /* error on tcsetattr */
    }

    c = getchar();      /* block (withot spinning) until we get a keypress */

    /* restore the saved state */
    if (-1 == tcsetattr(STDIN_FILENO, TCSANOW, &savedState))
    {
        return EOF;     /* error on tcsetattr */
    }

    return c;
}


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


/* Печать строки в HEX */
static void print_hex(uint8_t* string)
{
    unsigned char i;

    for (i = 0; i < strlen(string); i++)
        printf("%.2X ", string[i]);
}


int main() {
    printf("Демонстрация работы алгоритма AES128\n");
    printf("\n");

    printf("Исходный текст: "); printf(plain_text); printf("\n");
    keypress(0);
    printf("-------------------------------------------------------------------------------------------------------\n");
    uint8_t* new_key = EditKey(key);
    printf("        Ключ: "); printf(new_key); printf("\n");
    printf("  Ключ в HEX: "); print_hex(new_key); printf("\n");
    printf("\n");
    uint8_t* new_plain_text = EditPlainText(plain_text);
    printf("       Текст: "); printf(new_plain_text); printf("\n");
    printf(" Текст в HEX: "); print_hex(new_plain_text); printf("\n");
    printf("-------------------------------------------------------------------------------------------------------\n");

    printf("ciphertext:\n");

    uint8_t i;

    struct AES_context context;
    AES_init_context(&context, new_key);

    for (i = 0; i < 4; ++i)
    {
        AES_encrypt(&context, new_plain_text + (i * 16));
        print_hex(new_plain_text + (i * 16));
    }
    printf("\n");
}
