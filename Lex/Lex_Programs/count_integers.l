%{
#include <stdio.h>
int int_count = 0;
int float_count = 0;
%}
%option noyywrap
%%
[0-9]+                      { int_count++; }
[0-9]+"."[0-9]+             { float_count++; }
.                           ;
%%

int main(int argc, char *argv[]) {
    yyin = fopen(argv[1],"r");
    yylex();

    printf("Number of integers: %d\n", int_count);
    printf("Number of floats: %d\n", float_count);

    return 0;
}
