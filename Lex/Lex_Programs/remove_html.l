%{
#include <stdio.h>
%}
%option noyywrap
htmlTag <[^>]+>
%%
{htmlTag} {fprintf(yyout, " ");}
. {fprintf(yyout, yytext);};
%%

int main(int argc, char *argv[]) {
    extern FILE* yyin;
    extern FILE* yyout;
    yyin = fopen(argv[1],"r");
    yyout = fopen("output.txt", "w");
    yylex();

    return 0;
}
