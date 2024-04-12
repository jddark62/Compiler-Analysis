%{
int printCount=0;
%}
%option noyywrap
printStatement printf
%%
{printStatement} {printCount++;}
. ;
%%
int main(int argc, char* argv[]){
    extern FILE* yyin;
    yyin=fopen(argv[1],"r");
    yylex();
    printf("\nOccurence of printf word: %d", printCount);
    return 0;
}