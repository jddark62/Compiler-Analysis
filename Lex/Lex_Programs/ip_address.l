%{
#include <stdio.h>
#include <string.h>
%}
%option noyywrap
%%
[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}    { 
    printf("Valid IP Address: %s\n", yytext);
    char first_octet[4];
    strncpy(first_octet, yytext, 3);
    first_octet[3] = '\0';
    int octet = atoi(first_octet);
    if (octet >= 1 && octet <= 126) {
        printf("Class: A\n");
    } else if (octet >= 128 && octet <= 191) {
        printf("Class: B\n");
    } else if (octet >= 192 && octet <= 223) {
        printf("Class: C\n");
    } else if (octet >= 224 && octet <= 239) {
        printf("Class: D\n");
    } else if (octet >= 240 && octet <= 255) {
        printf("Class: E\n");
    }
}
[a-zA-Z]+   { printf("Invalid IP Address: %s\n", yytext); }
.   ;
%%

int main() {
    yylex();
    return 0;
}
