#include <stdint.h>



#ifndef AES_H
#define AES_H



// define encryption mode

#ifndef EBC
  #define EBC 1
#endif

#ifndef CCB
  #define CCB 1
#endif

#ifndef CTR
  #define CTR 1
#endif

#define AES128 1
// #define AES192 1
// #define AES256 1



//define AES parameters
// Nb		number of words in block
// Nk		number of words in key
// Nr		number of rounds
// KEYLENGTH	key length in bytes
// KEYEXPSIZE	number of words in expanded key

// block length in bytes
#define BLOCKLENGTH 16

// AES main parameters

#define Nb 4

#if defined(AES256) && (AES256 == 1)
	#define KEYLENGTH 32
	#define KEYEXPSIZE 240
	#define Nk 8
	#define Nr 14
#elif defined(AES192) && (AES192 == 1)
	#define KEYLENGTH 24
	#define KEYEXPSIZE 208
	#define Nk 6
	#define 12
#else
	#define KEYLENGTH 16
	#define KEYEXPSIZE 176
	#define Nk 4
	#define Nr 10
#endif



// AES structure

struct AES_context
{
	uint8_t RoundKey[KEYEXPSIZE];
#if (defined(CBC) && (CBC == 1)) || (defined(CTR) && (CTR == 1))
	uint8_t InitVector[BLOCKLENGTH];
#endif
};



// AES functions

void AES_init_context();
