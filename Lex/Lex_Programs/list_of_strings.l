%{
#include <stdio.h>
%}
%option noyywrap
%%
\"[^\"\n]*\"   { printf("String: %s\n", yytext); }
\'[^\'\n]*\'   { printf("Character: %s\n", yytext); }
.              ;
%%

int main(int argc, char * argv[]) {
    extern FILE* yyin;
    yyin = fopen(argv[1], "r");
    yylex();
    return 0;
}