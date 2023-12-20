#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1000
#define MAX_MACRO_NAME_LENGTH 100
#define MAX_MACRO_VALUE_LENGTH 100

typedef struct {
    char name[MAX_MACRO_NAME_LENGTH];
    char value[MAX_MACRO_VALUE_LENGTH];
} Macro;

Macro macros[100];
int numMacros = 0;

void addMacro(const char* name, const char* value) {
    if (numMacros >= 100) {
        printf("Maximum number of macros exceeded.\n");
        exit(1);
    }
    strcpy(macros[numMacros].name, name);
    strcpy(macros[numMacros].value, value);
    numMacros++;
}

char* replaceMacros(const char* line) {
    char* result = malloc(MAX_LINE_LENGTH);
    strcpy(result, line);

    for (int i = 0; i < numMacros; i++) {
        char* pos = strstr(result, macros[i].name);
        while (pos != NULL) {
            int nameLength = strlen(macros[i].name);
            int valueLength = strlen(macros[i].value);
            int diff = valueLength - nameLength;

            if (diff >= 0) {
                memmove(pos + valueLength, pos + nameLength, strlen(pos + nameLength) + 1);
                memcpy(pos, macros[i].value, valueLength);
            } else {
                memmove(pos + valueLength, pos + nameLength, strlen(pos + nameLength) + 1);
                memcpy(pos, macros[i].value, nameLength + diff);
            }

            pos = strstr(pos + valueLength, macros[i].name);
        }
    }

    return result;
}

int main() {
    FILE* inputFile = fopen("/workspaces/Compiler-Analysis/preprocessor.c", "r");
    FILE* outputFile = fopen("/workspaces/Compiler-Analysis/preprocessed.c", "w");

    if (inputFile == NULL || outputFile == NULL) {
        printf("Failed to open files.\n");
        return 1;
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        char* preprocessedLine = replaceMacros(line);
        fputs(preprocessedLine, outputFile);
        free(preprocessedLine);
    }

    fclose(inputFile);
    fclose(outputFile);

    printf("Preprocessing completed.\n");

    return 0;
}