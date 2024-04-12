%{
%}
%option noyywrap
comment1 \/\/.*
comment2 \/\*(.*\n.*)+\*\/
%%
{comment1} {printf("%s",yytext);}
{comment2} {printf("%s",yytext);}
. ;
%%
int main(int argc, char* argv[]){
    extern FILE* yyin;
    yyin=fopen(argv[1],"r");
    yylex();
    return 0;
}