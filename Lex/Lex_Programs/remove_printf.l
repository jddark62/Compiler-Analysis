%{
%}
%option noyywrap
printStatement printf
%%
{printStatement} {fprintf(yyout,"");}
. {fprintf(yyout,"%s", yytext);};
%%
int main(int argc, char* argv[]){
    extern FILE* yyin;
    extern FILE* yyout;
    yyin=fopen(argv[1],"r");
    yyout=fopen("output.txt","w");
    yylex();
    fclose(yyin);
    fclose(yyout);
    return 0;
}