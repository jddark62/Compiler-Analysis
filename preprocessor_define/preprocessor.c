#include <stdio.h>
#include <string.h>

#define MAX_LINE_LENGTH 1000
#define MAX_MACRO_NAME_LENGTH 100
#define MAX_MACRO_VALUE_LENGTH 100

// structure to store macro name and value
typedef struct {
    char name[MAX_MACRO_NAME_LENGTH];
    char value[MAX_MACRO_VALUE_LENGTH];
} Macro;

Macro macros[MAX_LINE_LENGTH];
int numMacros = 0;

// preprocesses the given file and saves the processed output to a file
void preprocessFile(const char* inputFilePath, const char* outputFilePath) {
    FILE* inputFile = fopen(inputFilePath, "r");
    if (inputFile == NULL) {
        printf("Error opening file: %s\n", inputFilePath);
        return;
    }

    FILE* outputFile = fopen(outputFilePath, "w");
    if (outputFile == NULL) {
        printf("Error opening file: %s\n", outputFilePath);
        fclose(inputFile);
        return;
    }

    char line[MAX_LINE_LENGTH];
    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        if (line[0] == '#') {
            char directive[MAX_MACRO_NAME_LENGTH];
            char macroName[MAX_MACRO_NAME_LENGTH];
            char macroValue[MAX_MACRO_VALUE_LENGTH];
            // sscanf is used instead of strtok because the macro value may contain spaces
            sscanf(line, "#%s %s %s", directive, macroName, macroValue);

            if (strcmp(directive, "define") == 0) {
                Macro macro;
                strcpy(macro.name, macroName);
                strcpy(macro.value, macroValue);
                macros[numMacros++] = macro;
            }
        } else { // line is not a preprocessor directive
            char processedLine[MAX_LINE_LENGTH];
            // processedLine is initialized with line because processedLine may be shorter than line
            strcpy(processedLine, line);
            for (int i = 0; i < numMacros; i++) {
                Macro macro = macros[i];
                // strstr is used instead of strtok because the macro name may occur multiple times in the line
                char* macroOccurrence = strstr(processedLine, macro.name);
                while (macroOccurrence != NULL) {
                    int macroLength = strlen(macro.name);
                    int valueLength = strlen(macro.value);
                    int remainingLength = strlen(macroOccurrence + macroLength);
                    // memmove is used instead of strncpy because the destination and source strings may overlap
                    memmove(macroOccurrence + valueLength, macroOccurrence + macroLength, remainingLength + 1);
                    memcpy(macroOccurrence, macro.value, valueLength);
                    macroOccurrence = strstr(macroOccurrence + valueLength, macro.name);
                }
            }
            // fprintf is used to print the processed line to the output file
            fprintf(outputFile, "%s", processedLine);
        }
    }

    fclose(inputFile);
    fclose(outputFile);
}

int main() {
    preprocessFile("input.c", "output.c");
    return 0;
}

