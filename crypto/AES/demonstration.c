/*
   Created by cuprumtan on 2019-11-05.
*/


#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "AES.h"


uint8_t* key = "potatoandsausage";                                      /* 16 байт */
uint8_t* plain_text = "the quick brown fox jumps over the lazy dog";    /* любой длины */

/* Печать строки в HEX */
static void print_hex(uint8_t* string)
{
    unsigned char i;

    for (i = 0; i < BLOCKLENGTH; i++)
        printf("%.2X ", string[i]);
    printf("\n");
}


int main() {
    printf("Демонстрация работы алгоритма AES128\n");
}
