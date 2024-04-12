%{
#include <stdio.h>
%}
%option noyywrap
%%
[a-zA-Z]    { 
                int shifted = (yytext[0] - 'A' + 3) % 26 + 'A'; // Shifts the letter by three positions, wrapping around at Z
                printf("%c", shifted); 
            }
.           { printf("%s", yytext); } // Print other characters as is
%%

int main(int argc, char * argv[]) {
    extern FILE* yyin;
    yyin = fopen(argv[1], "r");
    yylex();
    return 0;
}
