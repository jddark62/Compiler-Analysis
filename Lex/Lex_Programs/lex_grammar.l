%{
#include <stdio.h>
%}
%option noyywrap
%%
[0-9]+                             { printf("Integer: %s\n", yytext); }
[0-9]+[Uu]?[Ll]?                    { printf("Integer with modifiers: %s\n", yytext); }
[0-9]*\.[0-9]+[FfLl]?               { printf("Float: %s\n", yytext); }
[0-9]+\.[0-9]*[Ee][+\-]?[0-9]+[Ff]? { printf("Scientific notation float: %s\n", yytext); }
0[Xx][0-9A-Fa-f]+                   { printf("Hexadecimal: %s\n", yytext); }
0[Xx][0-9A-Fa-f]+[Uu]?[Ll]?        { printf("Hexadecimal with modifiers: %s\n", yytext); }
.                                   ;
%%

int main(int argc, char * argv[]) {
    extern FILE* yyin;
    yyin = fopen(argv[1], "r");
    yylex();
    return 0;
}
