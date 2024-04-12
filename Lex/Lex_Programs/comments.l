%{
#include <stdio.h>
int nested_comment_flag = 0;
%}
%option noyywrap
%%
"#"[^"\n]*                               { printf("Single-line preprocessor directive: %s\n", yytext); }
"#"(.|\n)*"#"                            { printf("Multi-line preprocessor directive: %s\n", yytext); }
"/*"                                     { nested_comment_flag = 1; }
"/*"(.|\n)*"*/"                          { if (nested_comment_flag) { printf("Nested comment: %s\n", yytext); } }
"//"(.|\n)*                              { printf("Single-line comment: %s\n", yytext); }
.                                        ;
%%

int main(int argc, char * argv[]) {
    extern FILE* yyin;
    yyin = fopen(argv[1], "r");
    yylex();
    return 0;
}