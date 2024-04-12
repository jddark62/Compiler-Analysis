%{
%}
%option noyywrap
email [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}
%%
{email} {printf("\nEmail ID is correct");}
. {printf("\nEmail ID: %s is incorrect !!", yytext);}
%%
int main(){
    yylex();
    return 0;
}