#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

int main() {
    FILE *file;
    char ch, prev;
    int charCount = 0, lineCount = 0;
    int isString = 0, isChar = 0;

    file = fopen("input.c", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    while ((ch = fgetc(file)) != EOF) {
        charCount++;

        if (ch == '\n') {
            lineCount++;
        }

        if (ch == '"' && prev != '\\') {
            isString = !isString;
        }

        if (ch == '\'' && prev != '\\') {
            isChar = !isChar;
        }

        if (ch == '#' && !isString && !isChar) {
            printf("Preprocessing directive found.\n");
        }

        if (ch == 'p' && !isString && !isChar) {
            char buffer[7];
            fgets(buffer, 7, file);
            if (strcmp(buffer, "rintf(") == 0) {
                ch = fgetc(file);
                if (ch == '"') {
                    printf("String found.\n");
                } else if (ch == '\'') {
                    printf("Character found.\n");
                }
            }
        }

        prev = ch;
    }

    printf("Character count: %d\n", charCount);
    printf("Line count: %d\n", lineCount);

    fclose(file);
    return 0;
}
