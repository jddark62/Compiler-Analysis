%{
#include <stdio.h>
#include <string.h>
%}
%option noyywrap
%%
([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}    { 
    printf("Valid MAC Address: %s\n", yytext); 
    char manufacturer[10];
    strncpy(manufacturer, yytext, 8);
    printf("\nManufacturer: %s", manufacturer);
}
[a-zA-Z0-9]+                           { printf("Invalid MAC Address: %s\n", yytext); }
.                                      ;
%%

int main() {
    yylex();
    return 0;
}
