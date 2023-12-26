#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1000
#define MAX_MACROS 100

typedef struct {
    char* name;
    char* definition;
} Macro;

Macro macros[MAX_MACROS];
int num_macros = 0;

void add_macro(const char* name, const char* definition) {
    macros[num_macros].name = malloc(strlen(name) + 1);
    strcpy(macros[num_macros].name, name);

    macros[num_macros].definition = malloc(strlen(definition) + 1);
    strcpy(macros[num_macros].definition, definition);

    num_macros++;
}

char* find_macro(const char* name) {
    for (int i = 0; i < num_macros; i++) {
        if (strcmp(macros[i].name, name) == 0) {
            return macros[i].definition;
        }
    }
    return NULL;
}

void preprocess_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file: %s\n", filename);
        return;
    }

    char line[MAX_LINE_LENGTH];
    char processed_line[MAX_LINE_LENGTH];
    int line_number = 1;

    while (fgets(line, sizeof(line), file)) {
        char* macro_start = strstr(line, "#define");
        if (macro_start != NULL) {
            char* macro_name_start = macro_start + strlen("#define");
            char* macro_name_end = strchr(macro_name_start, ' ');
            if (macro_name_end != NULL) {
                *macro_name_end = '\0';
                char* macro_definition_start = macro_name_end + 1;
                char* macro_definition_end = strchr(macro_definition_start, '\n');
                if (macro_definition_end != NULL) {
                    *macro_definition_end = '\0';
                    add_macro(macro_name_start, macro_definition_start);
                }
            }
        } else {
            int processed_line_length = 0;
            char* token = strtok(line, " ");
            while (token != NULL) {
                char* macro_definition = find_macro(token);
                if (macro_definition != NULL) {
                    int macro_definition_length = strlen(macro_definition);
                    memmove(processed_line + processed_line_length, macro_definition, macro_definition_length);
                    processed_line_length += macro_definition_length;
                } else {
                    int token_length = strlen(token);
                    memcpy(processed_line + processed_line_length, token, token_length);
                    processed_line_length += token_length;
                }
                token = strtok(NULL, " ");
                if (token != NULL) {
                    processed_line[processed_line_length++] = ' ';
                }
            }
            processed_line[processed_line_length] = '\0';
            printf("%s", processed_line);
        }

        line_number++;
    }

    fclose(file);
}

int main() {
    preprocess_file("input.c");
    return 0;
}
