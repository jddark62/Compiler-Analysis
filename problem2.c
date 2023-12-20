#include <stdio.h>
#include <string.h>

#define MAX_LINE_LENGTH 100

typedef struct {
    char name[MAX_LINE_LENGTH];
    char value[MAX_LINE_LENGTH];
} Macro;

Macro macros[MAX_LINE_LENGTH];
int num_macros = 0;

void preprocessFile(FILE* inputFile, FILE* outputFile) {
    char line[MAX_LINE_LENGTH];

    // Read and store macro definitions
    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        if (strncmp(line, "#define", 7) == 0) {
            char* macroName = strtok(line + 7, " \t\n");
            char* macroValue = strtok(NULL, "\n");
            strcpy(macros[num_macros].name, macroName);
            strcpy(macros[num_macros].value, macroValue);
            num_macros++;
        }
    }

    // Preprocess the code
    rewind(inputFile);
    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        // Replace macros
        for (int i = 0; i < num_macros; i++) {
            char* macroPos = strstr(line, macros[i].name);
            while (macroPos != NULL) {
                strncpy(macroPos, macros[i].value, strlen(macros[i].value));
                macroPos = strstr(line, macros[i].name);
            }
        }

        // Write preprocessed line to output file
        fputs(line, outputFile);
    }
}

int main() {
    FILE* inputFile = fopen("input.c", "r");
    FILE* outputFile = fopen("output.c", "w");

    if (inputFile == NULL || outputFile == NULL) {
        printf("Error opening files.\n");
        return 1;
    }

    preprocessFile(inputFile, outputFile);

    fclose(inputFile);
    fclose(outputFile);

    return 0;
}

