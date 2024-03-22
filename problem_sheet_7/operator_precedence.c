#include<stdio.h>
#include<string.h>

char *input;
int i=0;

char lasthandle[6],stack[50],handles[][5]={")E(","E*E","E+E","i","E^E"};
//(E) becomes )E( when pushed to stack

int top=0,l;
// top points to the position of the topmost element in the stack
// l is the length of the input string
char prec[9][9]={

                            /*input*/

            /*stack    +    -   *   /   ^   i   (   )   $  */

            /*  + */  '>', '>','<','<','<','<','<','>','>',

            /*  - */  '>', '>','<','<','<','<','<','>','>',

            /*  * */  '>', '>','>','>','<','<','<','>','>',

            /*  / */  '>', '>','>','>','<','<','<','>','>',

            /*  ^ */  '>', '>','>','>','<','<','<','>','>',

            /*  i */  '>', '>','>','>','>','e','e','>','>',

            /*  ( */  '<', '<','<','<','<','<','<','>','e',

            /*  ) */  '>', '>','>','>','>','e','e','>','>',

            /*  $ */  '<', '<','<','<','<','<','<','<','>',

                };

// getindex()
// This function is used to get the index of the input character
// It returns the index of the input character based on the following order:
// +,-,*,/,^,i,(,),$
// This function is called to get the index of the input character and the stack top character

int getindex(char c)
{
switch(c)
    {
    case '+':return 0;
    case '-':return 1;
    case '*':return 2;
    case '/':return 3;
    case '^':return 4;
    case 'i':return 5;
    case '(':return 6;
    case ')':return 7;
    case '$':return 8;
    }
}

// shift()
// This function is used to shift the input string to the stack
// It increments the top and i values and copies the input character to the stack
// It also appends a null character to the end of the stack
// This function is called when the precedence of the input character is less than the precedence of the stack top character
int shift()
{
stack[++top]=*(input+i++);
stack[top+1]='\0';
}

//reduce()
//This function is used to reduce the contents of the stack to E, if possible
//It checks for the presence of any of the handles in the stack top
//If a handle is found, it is replaced by E
//The function returns 1 if a reduction has been done, else it returns 0
int reduce()
{
int i,len,found,t;
for(i=0;i<5;i++)//selecting handles
    {
    len=strlen(handles[i]);
    if(stack[top]==handles[i][0]&&top+1>=len)
        {
        found=1;
        for(t=0;t<len;t++)
            {
            if(stack[top-t]!=handles[i][t])
                {
                found=0;
                break;
                }
            }
        if(found==1)
            {
            stack[top-t+1]='E';
            top=top-t+1; // E is pushed
            strcpy(lasthandle,handles[i]); // to display the handle which is replaced
            stack[top+1]='\0'; 
            return 1;//successful reduction
            }
        }
   }
return 0;
}



void dispstack()
{
int j;
for(j=0;j<=top;j++)
    printf("%c",stack[j]);
}



void dispinput()
{
int j;
for(j=i;j<l;j++)
    printf("%c",*(input+j));
}



void main()
{
int j;

input=(char*)malloc(50*sizeof(char));
printf("\nEnter the string\n");
scanf("%s",input);
input=strcat(input,"$");
l=strlen(input);
strcpy(stack,"$");
printf("\nSTACK\tINPUT\tACTION");
while(i<=l)
	{
	shift();
	printf("\n");
	dispstack();
	printf("\t");
	dispinput();
	printf("\tShift");
    // if the precedence of the input character is less than the precedence of the stack top characteri+(ii)
	if(prec[getindex(stack[top])][getindex(input[i])]=='>')
		{
		while(reduce())
			{
			printf("\n");
			dispstack();
			printf("\t");
			dispinput();
			printf("\tReduced: E->%s",lasthandle);
			}
		}
	}

if(strcmp(stack,"$E$")==0)
    printf("\nAccepted;");
else
    printf("\nNot Accepted;");
}