%{
#include <stdio.h>
#include <string.h>

#define MAX_LENGTH 100
char smallest_word[MAX_LENGTH];
char longest_word[MAX_LENGTH];
int smallest_length = MAX_LENGTH;
int longest_length = 0;
%}
%option noyywrap
%%
[a-zA-Z]+ {
    int length = strlen(yytext);
    if (length < smallest_length) {
        smallest_length = length;
        strcpy(smallest_word, yytext);
    }
    if (length > longest_length) {
        longest_length = length;
        strcpy(longest_word, yytext);
    }
}
. ;

%%

int main(int argc, char * argv[]) {
    extern FILE* yyin;
    yyin = fopen(argv[1], "r");
    yylex();
    printf("Smallest word: %s\n", smallest_word);
    printf("Longest word: %s\n", longest_word);
    return 0;
}