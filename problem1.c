#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int countCharacters(FILE *file) {
    int count = 0;
    char ch;
    while ((ch = fgetc(file)) != EOF) {
        count++;
    }
    return count;
}

int countLines(FILE *file) {
    int count = 0;
    char ch;
    while ((ch = fgetc(file)) != EOF) {
        if (ch == '\n') {
            count++;
        }
    }
    return count;
}

int isKeyword(char *word) {
    char *keywords[] = {"auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern", "float", "for", "goto", "if", "int", "long", "register", "return", "short", "signed", "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"};
    int numKeywords = sizeof(keywords) / sizeof(keywords[0]);
    for (int i = 0; i < numKeywords; i++) {
        if (strcmp(word, keywords[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int isOperator(char ch) {
    char operators[] = "+-*/%=";
    int numOperators = sizeof(operators) / sizeof(operators[0]);
    for (int i = 0; i < numOperators; i++) {
        if (ch == operators[i]) {
            return 1;
        }
    }
    return 0;
}

int isIdentifier(char *word) {
    if (!isalpha(word[0]) && word[0] != '_') {
        return 0;
    }
    for (int i = 1; i < strlen(word); i++) {
        if (!isalnum(word[i]) && word[i] != '_') {
            return 0;
        }
    }
    return 1;
}

int isNumericConstant(char *word) {
    for (int i = 0; i < strlen(word); i++) {
        if (!isdigit(word[i])) {
            return 0;
        }
    }
    return 1;
}

int main() {
    FILE *file = fopen("/workspaces/Compiler-Analysis/problem1.c", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    int numCharacters = countCharacters(file);
    fseek(file, 0, SEEK_SET); // Reset file pointer to the beginning
    int numLines = countLines(file);
    fseek(file, 0, SEEK_SET); // Reset file pointer to the beginning

    char word[100];
    while (fscanf(file, "%s", word) != EOF) {
        if (isKeyword(word)) {
            printf("Keyword: %s\n", word);
        } else if (isOperator(word[0])) {
            printf("Operator: %s\n", word);
        } else if (isIdentifier(word)) {
            printf("Identifier: %s\n", word);
        } else if (isNumericConstant(word)) {
            printf("Numeric Constant: %s\n", word);
        } else {
            printf("Invalid token: %s\n", word);
        }
    }

    printf("Number of characters: %d\n", numCharacters);
    printf("Number of lines: %d\n", numLines);

    fclose(file);
    return 0;
}
