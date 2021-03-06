#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include "AES.h"


/* State - структура хранения одного блока данных */
typedef uint8_t state_t[4][4];

/* массив значений S-box */
static const uint8_t Sbox[256] = {
/*      0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F  */
/* 00 */0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
/* 10 */0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
/* 20 */0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
/* 30 */0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
/* 40 */0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
/* 50 */0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
/* 60 */0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
/* 70 */0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
/* 80 */0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
/* 90 */0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
/* A0 */0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
/* B0 */0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
/* C0 */0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
/* D0 */0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
/* E0 */0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
/* F0 */0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16};

/* массив значений InvS-box */
static const uint8_t InvSbox[256] = {
/*      0     1     2     3     4     5     6     7     8     9     A     B     C     D     E     F  */
/* 00 */0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
/* 10 */0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
/* 20 */0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
/* 30 */0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
/* 40 */0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
/* 50 */0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
/* 60 */0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
/* 70 */0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
/* 80 */0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
/* 90 */0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
/* A0 */0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
/* B0 */0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
/* C0 */0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
/* D0 */0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
/* E0 */0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
/* F0 */0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d};

/* массив значений RCon */
static const uint8_t RCon[11] = {
        0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36};


#define getSBoxValue(i) (Sbox[(i)])
#define getSBoxInvert(i) (InvSbox[(i)])


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


/* Печать строки в HEX */
void print_hex(uint8_t* string, uint8_t* delimiter)
{
    unsigned char i;

    for (i = 0; i < strlen(string); i++)
        if (i % 16 == 0 && i != 0) {
            printf("\n");
            printf(delimiter);
            printf("%.2X ", string[i]);
        } else {
            printf("%.2X ", string[i]);
        }
}


/* Печать state в HEX */
void print_state(state_t* state, uint8_t* delimiter)
{
    uint8_t i, j;

    for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
            printf("%.2X ", (*state)[i][j]);
        }
        printf("\n");
        printf(delimiter);
    }
}


/*
 Функция расширения ключа KeyExpansion

 Берет ключ шифрования К и выполняет операцию расширения ключа, чтобы создать набор данных для раундовых ключей.
 Расширенный ключ W содержит 4(10+1) слов - начальный ключ в 4 слова и по 4 слова расширенного ключа на каждый
 из 10 раундов. Расширенный ключ W состоит из слов (четыре байта на слово), обозначаемых ниже как wi, где i
 находится в диапазоне [0..44]. Полная длина расширенного ключа 1408 бит, по 128 бит на каждый раунд.

 Расширение ключа можно описать следующей последовательностью операций:
 1) Четыре слова ключа шифрования К копируются в первые четыре слова расширенного ключа W: wi = ki для i = 0, 1, 2, 3.
 2) Остальные слова расширенного ключа W для i = 4, 5, ..., 44 генерируются так:
    - если i кратно 4, то wi = SubWord(RotByte(wi-1)) XOR Rcon(i/4) XOR wi-4;
    - если i не кратно 4, то wi = wi-1 XOR wi-4.
*/
static void KeyExpansion(uint8_t* RoundKey, const uint8_t* Key)
{
    unsigned int i, j, k;
    uint8_t temp_word[4];

    /* Первые 4 слова расширенного ключа = первые четыре слова исходного ключа */
    for (i = 0; i < Nk; i++)
    {
        RoundKey[(i * 4) + 0] = Key[(i * 4) + 0];
        RoundKey[(i * 4) + 1] = Key[(i * 4) + 1];
        RoundKey[(i * 4) + 2] = Key[(i * 4) + 2];
        RoundKey[(i * 4) + 3] = Key[(i * 4) + 3];
    }

    /* Следующие Nr ключей получаем из предыдущих */
    for (i = Nk; i < Nb * (Nr + 1); i++)
    {
        /* получаем wi-1 слово */
        {
            k = (i - 1) * 4;
            temp_word[0]=RoundKey[k + 0];
            temp_word[1]=RoundKey[k + 1];
            temp_word[2]=RoundKey[k + 2];
            temp_word[3]=RoundKey[k + 3];
        }

        /* если i кратно 4, то применяем к wi-1 слову преобразование */
        if (i % Nk == 0)
        {
            /* Фцнкция создает смещение [a0,a1,a2,a3] -> [a1,a2,a3,a0]
               RotWord() */
            {
                const uint8_t temp_byte = temp_word[0];
                temp_word[0] = temp_word[1];
                temp_word[1] = temp_word[2];
                temp_word[2] = temp_word[3];
                temp_word[3] = temp_byte;
            }

            /* Функция для каждого байта слова применяет S-box
               Subword() */
            {
                temp_word[0] = getSBoxValue(temp_word[0]);
                temp_word[1] = getSBoxValue(temp_word[1]);
                temp_word[2] = getSBoxValue(temp_word[2]);
                temp_word[3] = getSBoxValue(temp_word[3]);
            }

            /* XOR с i/Nk членом Rcon */
            temp_word[0] = temp_word[0] ^ RCon[i / Nk];
        }

        j = i * 4;          /* индекс начала нового заполняемого слова */
        k = (i - Nk) * 4;   /* индекс начала wi-4 слова */

        /* wi-1 XOR wi-4 */
        RoundKey[j + 0] = temp_word[0] ^ RoundKey[k + 0];
        RoundKey[j + 1] = temp_word[1] ^ RoundKey[k + 1];
        RoundKey[j + 2] = temp_word[2] ^ RoundKey[k + 2];
        RoundKey[j + 3] = temp_word[3] ^ RoundKey[k + 3];
    }
}

void AES_init_context(struct AES_context* context, const uint8_t* key)
{
    printf("\n");
    printf("AES:\n");
    printf("\n");
    printf("   Расширение ключа\n");
    printf("   |\n");
    printf("   |--- Исходный ключ в HEX\n");
    printf("   |    |\n");
    printf("   |    | ");
    print_hex(key, "   |    | ");
    printf("\n");
    printf("   |    |\n");
    printf("   |\n");
    keypress(0);

    printf("   |--- Расширенный ключ в HEX\n");
    KeyExpansion(context->RoundKey, key);
    printf("   |    |\n");
    printf("   |    | ");
    print_hex(context->RoundKey, "   |    | ");
    printf("\n");
    printf("   |    |\n");
    printf("   |\n");
    keypress(0);
}


/*
 В преобразовании AddRoundKey, раундовый ключ RK добавляется к state посредством побитового XOR каждого байта
 State с каждым байтом RoundKey.
*/
static void AddRoundKey(uint8_t round, state_t* state, const uint8_t* RoundKey)
{
    uint8_t i, j;

    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            (*state)[i][j] ^= RoundKey[(round * Nb * 4) + (i * Nb) + j];
        }
    }
}


/*
 SubBytes() обрабатывает каждый байт State, независимо производя нелинейную замену байтов, используя S-box.
 1. Байт Z преобразуется в шестнадцатеричную систему счисления - XYh, где X - старший разряд, Y - младший разряд.
    Если старшего разряда нет, он заменяется нулем.
 2. В S-box выбирается строка X и столбец Y.
 3. Значение Z' на пересечении строки X и столбца Y таблицы S-box используется как замена Z.
*/
static void SubBytes(state_t* state)
{
    uint8_t i, j;

    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            (*state)[j][i] = getSBoxValue((*state)[j][i]);
        }
    }
}


/*
 Каждая строка сдивгается влево на количество байт, равное номеру строки.
*/
static void ShiftRows(state_t* state)
{
    uint8_t temp_byte;

    /* смещение 1 строки */
    temp_byte = (*state)[0][1];
    (*state)[0][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[3][1];
    (*state)[3][1] = temp_byte;

    /* смещение 2 строки */
    temp_byte = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = temp_byte;
    temp_byte = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = temp_byte;

    /* смещение 3 строки */
    temp_byte = (*state)[0][3];
    (*state)[0][3] = (*state)[3][3];
    (*state)[3][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[1][3];
    (*state)[1][3] = temp_byte;
}


/*
 Обрабатывает State по колонкам, трактуя каждую из них как полином третьей степени.
 Над этими полиномами производится умножение в GF(2^8) по модулю x^4+1 на фиксированный многочлен c(x)=3x^3+x^2+x+2.
 Процесс умножения полиномов эквивалентен матричному умножению:
  __ __     __            __     ____
 | S'0 | = | 02  03  01  01 |   | S0 |
 | S'1 | = | 01  02  03  01 |   | S1 |
 | S'2 | = | 01  01  02  03 | * | S2 |
 | S'3 | = | 03  01  01  02 |   | S3 |
 |__ __|   |__            __|   |____|

 В результате такого умножения, байты столбца c {S0, S1, S2, S3} заменяются, соответственно, на байты:
 S'0 = (2 * S0) XOR (3 * S1) XOR S2 XOR S3
 S'1 = S0 XOR (2 * S1) XOR (3 * S2) XOR S3
 S'2 = S0 XOR S1 XOR (2 * S2) XOR (3 * S3)
 S'3 = (3 * S0) XOR S1 XOR S2 XOR (2 * S3)
*/

static uint8_t xtime(uint8_t x)
{
    return ((x<<1) ^ (((x>>7) & 1) * 0x1b));
}


static void MixColumns(state_t* state)
{
    uint8_t i;
    uint8_t Tmp, Tm, t;

    for (i = 0; i < 4; i++)
    {
        t   = (*state)[i][0];
        Tmp = (*state)[i][0] ^ (*state)[i][1] ^ (*state)[i][2] ^ (*state)[i][3];
        Tm  = (*state)[i][0] ^ (*state)[i][1]; Tm = xtime(Tm);  (*state)[i][0] ^= Tm ^ Tmp;
        Tm  = (*state)[i][1] ^ (*state)[i][2]; Tm = xtime(Tm);  (*state)[i][1] ^= Tm ^ Tmp;
        Tm  = (*state)[i][2] ^ (*state)[i][3]; Tm = xtime(Tm);  (*state)[i][2] ^= Tm ^ Tmp;
        Tm  = (*state)[i][3] ^ t;              Tm = xtime(Tm);  (*state)[i][3] ^= Tm ^ Tmp;
    }
}


/* Умножение в GF(2^8) */
static uint8_t Multiply(uint8_t x, uint8_t y)
{
    return (((y & 1) * x) ^
            ((y>>1 & 1) * xtime(x)) ^
            ((y>>2 & 1) * xtime(xtime(x))) ^
            ((y>>3 & 1) * xtime(xtime(xtime(x)))) ^
            ((y>>4 & 1) * xtime(xtime(xtime(xtime(x))))));
}


static void InvMixColumns(state_t* state)
{
    int i;
    uint8_t a, b, c, d;

    for (i = 0; i < 4; i++)
    {
        a = (*state)[i][0];
        b = (*state)[i][1];
        c = (*state)[i][2];
        d = (*state)[i][3];

        (*state)[i][0] = Multiply(a, 0x0e) ^ Multiply(b, 0x0b) ^ Multiply(c, 0x0d) ^ Multiply(d, 0x09);
        (*state)[i][1] = Multiply(a, 0x09) ^ Multiply(b, 0x0e) ^ Multiply(c, 0x0b) ^ Multiply(d, 0x0d);
        (*state)[i][2] = Multiply(a, 0x0d) ^ Multiply(b, 0x09) ^ Multiply(c, 0x0e) ^ Multiply(d, 0x0b);
        (*state)[i][3] = Multiply(a, 0x0b) ^ Multiply(b, 0x0d) ^ Multiply(c, 0x09) ^ Multiply(d, 0x0e);
    }
}


/*
 Инвертированная функция SubBytes для дешифрования.
*/
static void InvSubBytes(state_t* state)
{
    uint8_t i, j;

    for (i = 0; i < 4; i++)
    {
        for (j = 0; j < 4; j++)
        {
            (*state)[j][i] = getSBoxInvert((*state)[j][i]);
        }
    }
}


/*
 Инвертированная функция ShiftRows для дешифрования.
*/
static void InvShiftRows(state_t* state)
{
    uint8_t temp_byte;

    /* смещение 1 строки */
    temp_byte = (*state)[3][1];
    (*state)[3][1] = (*state)[2][1];
    (*state)[2][1] = (*state)[1][1];
    (*state)[1][1] = (*state)[0][1];
    (*state)[0][1] = temp_byte;

    /* смещение 2 строки */
    temp_byte = (*state)[0][2];
    (*state)[0][2] = (*state)[2][2];
    (*state)[2][2] = temp_byte;
    temp_byte = (*state)[1][2];
    (*state)[1][2] = (*state)[3][2];
    (*state)[3][2] = temp_byte;

    /* смещение 3 строки */
    temp_byte = (*state)[0][3];
    (*state)[0][3] = (*state)[1][3];
    (*state)[1][3] = (*state)[2][3];
    (*state)[2][3] = (*state)[3][3];
    (*state)[3][3] = temp_byte;
}


/* функция шифрования блока */
static void Cipher(state_t* state, const uint8_t* RoundKey)
{
    uint8_t round = 0;

    printf("   |\n");
    printf("   |--- Раунды\n");
    printf("   |    |\n");
    printf("   |    |--- [Раунд 0]\n");
    printf("   |    |    |\n");
    printf("   |    |    |--- Исходый State\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |\n");

    printf("   |    |    |--- AddRoundKey\n");

    /* Добавление первого раундового ключа */
    AddRoundKey(0, state, RoundKey);

    printf("   |    |    |    |\n");
    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |\n");
    printf("   |    |\n");

    /* Выполнение Nr раундов начиная с 1 и до Nr-1 */
    for (round = 1; round < Nr; round++)
    {
        printf("   |    |--- Раунд %d\n", round);
        printf("   |    |    |\n");
        printf("   |    |    |--- SubBytes\n");
        printf("   |    |    |    |\n");

        SubBytes(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- ShiftRows\n");
        printf("   |    |    |    |\n");

        ShiftRows(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- MixColumns\n");
        printf("   |    |    |    |\n");

        MixColumns(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- AddRoundKey\n");
        printf("   |    |    |    |\n");

        AddRoundKey(round, state, RoundKey);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");
        printf("   |    |\n");
    }

    printf("   |    |--- Раунд %d\n", round);
    printf("   |    |    |\n");

    /* Раунд Nr */
    printf("   |    |    |--- SubBytes\n");
    printf("   |    |    |    |\n");

    SubBytes(state);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");


    printf("   |    |    |--- ShiftRows\n");
    printf("   |    |    |    |\n");

    ShiftRows(state);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");


    printf("   |    |    |--- AddRoundkey\n");
    printf("   |    |    |    |\n");

    AddRoundKey(Nr, state, RoundKey);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");

    keypress(0);
}


/* функция дешифрования блока */
static void InvCipher(state_t* state, const uint8_t* RoundKey)
{
    uint8_t round = 0;

    printf("   |\n");
    printf("   |--- Раунды\n");
    printf("   |    |\n");
    printf("   |    |--- [Раунд 11]\n");
    printf("   |    |    |\n");
    printf("   |    |    |--- Исходый State\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |\n");

    printf("   |    |    |--- AddRoundKey\n");

    /* Добавление первого раундового ключа */
    AddRoundKey(Nr, state, RoundKey);

    printf("   |    |    |    |\n");
    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |    |\n");
    printf("   |    |    |\n");
    printf("   |    |\n");

    /* Выполнение Nr раундов начиная с Nr-1 и до 1 */
    for (round = (Nr - 1); round > 0; --round)
    {
        printf("   |    |--- Раунд %d\n", round + 1);
        printf("   |    |    |\n");
        printf("   |    |    |--- InvShiftRows\n");
        printf("   |    |    |    |\n");

        InvShiftRows(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- InvSubBytes\n");
        printf("   |    |    |    |\n");

        InvSubBytes(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- AddRoundKey\n");
        printf("   |    |    |    |\n");

        AddRoundKey(round, state, RoundKey);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");


        printf("   |    |    |--- InvMixColumns\n");
        printf("   |    |    |    |\n");

        InvMixColumns(state);

        printf("   |    |    |    | ");
        print_state(state, "   |    |    |    | "); printf("\n");
        printf("   |    |    |\n");
    }

    printf("   |    |--- Раунд %d\n", round + 1);
    printf("   |    |    |\n");

    /* Раунд 1 */
    printf("   |    |    |--- InvShiftRows\n");
    printf("   |    |    |    |\n");

    InvShiftRows(state);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");


    printf("   |    |    |--- InvSubBytes\n");
    printf("   |    |    |    |\n");

    InvSubBytes(state);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");


    printf("   |    |    |--- AddRoundKey\n");
    printf("   |    |    |    |\n");

    AddRoundKey(0, state, RoundKey);

    printf("   |    |    |    | ");
    print_state(state, "   |    |    |    | "); printf("\n");
    printf("   |    |    |\n");

    keypress(0);
}


/* функция шифрования текста */
void AES_encrypt(const struct AES_context* context, uint8_t* buffer)
{
    Cipher((state_t*)buffer, context->RoundKey);
}


/* функция дешифрования текста */
void AES_decrypt(const struct AES_context* context, uint8_t* buffer)
{
    InvCipher((state_t*)buffer, context->RoundKey);
}

