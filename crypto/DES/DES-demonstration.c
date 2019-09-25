#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define MAXCHAR 256

struct DES_configs {
	char *plain_text;
	char *key_text;
} configs;

FILE *config_file;
char buffer[MAXCHAR];

extern int errno;

int main(int argc, char *argv[]){
	config_file = fopen("DES.conf", "r");
	if (config_file != NULL){
		while (fscanf(config_file, "%s", buffer) == 1){
			printf("%s\n", buffer);
			if (strcmp(buffer, "PLAIN_TEXT") == 0){
				fscanf(config_file, "%s", buffer);
				printf("%s\n", buffer);
				configs.plain_text = buffer;
				printf("%s\n", configs.plain_text);
			}
			if (strcmp(buffer, "KEY_TEXT") == 0){
				fscanf(config_file, "%s", buffer);
				printf("%s\n", buffer);
				configs.key_text = buffer;
				//printf("%s\n", configs.plain_text);
			}
		}		
		if (errno != 0){
			perror(argv[0]);
			exit(1);
		}
		exit(0);
	} else {
		printf("%s\n", "test");
		perror(argv[0]);
		exit(1);
	}
	fclose(config_file);
	printf("%s\n", configs.plain_text);
	printf("  KEY_TEXT: %s\n", configs.key_text);
}
