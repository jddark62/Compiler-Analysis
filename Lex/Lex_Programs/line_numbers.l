%{
int lineno=0;
%}
%option noyywrap
line .*\n
%%
{line} {printf("%d %s",lineno++,yytext);}
%%
int main(int argc, char* argv[]){
    extern FILE* yyin;
    yyin=fopen(argv[1],"r");
    yylex();
    return 0;
}