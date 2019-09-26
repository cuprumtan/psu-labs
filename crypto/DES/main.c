#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

#define MAXCHAR 256

struct DES_configs {
    char plain_text_buffer[MAXCHAR];
    char key_text_buffer[MAXCHAR];
} configs;


FILE *config_file;
char buffer[MAXCHAR];

extern int errno;

void
read_config (int argc, char *argv[])
{
    config_file = fopen("../DES.conf", "r");
    if (config_file != NULL){
        while (fscanf(config_file, "%s", buffer) == 1) {
            if (strcmp(buffer, "PLAIN_TEXT") == 0) {
                fscanf(config_file, "%s", buffer);
                memcpy(configs.plain_text_buffer, buffer, 256);
            }
            if (strcmp(buffer, "KEY_TEXT") == 0) {
                fscanf(config_file, "%s", buffer);
                memcpy(configs.key_text_buffer, buffer, 256);
            }
        }
        if (errno != 0) {
            perror(argv[0]);
            exit(1);
        }
        fclose(config_file);
        /* exit(0); */
    } else {
        perror(argv[0]);
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    read_config(argc, argv);
    printf("PSU, 2019\n");
    printf("DES algorithm demonstration\n");
    printf("\n");
    printf("Input data:\n");
    printf("------------------------\n");
    printf("| Plain text: %s |\n", configs.plain_text_buffer);
    printf("| Key text:   %s  |\n", configs.key_text_buffer);
    printf("------------------------\n");
}
