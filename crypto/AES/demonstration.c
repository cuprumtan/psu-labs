/*
   Created by cuprumtan on 2019-11-05.
*/


#include <stdint.h>
#include <stdio.h>
#include "AES.h"


/* Печать строки в HEX */
static void print_hex(uint8_t* string)
{
    unsigned char i;

    for (i = 0; i < BLOCKLENGTH; i++)
        printf("%.2x", string[i]);
    printf("\n");
}


int main() {
    printf("Демонстрация работы алгоритма AES128\n");
}
