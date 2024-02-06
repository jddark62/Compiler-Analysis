// assign addresses during first pass
/*
LDA loads the accumulator with the number of the associated variable
o STA moves accumulator content to the associated variable
o LDCH and STCH are similar to LDA and STA but used for a character
o RESW reserves a word (3 bytes)
o WORD reserves a word and assigns 5 to it

o BYTE reserves a byte and assigns ‘Z’ to it
o RESB reserves a byte*/

// assign addresses during first pass
// example:
/*
Input:
LDA FIVE
STA ALPHA
LDCH CHAR
STCH C1
ALPHA RESW 1
FIVE WORD 5
CHAR BYTE C’Z’
C1

Desired output:
Output: Assuming starting address as 1000 and each instruction needs 3 bytes (machine
code) inside main memory. Read each instruction twice. During first read, assign
addresses and during second read, generate machine code.
1000 LDA FIVE 00100F
1003 STA ALPHA 0C100C
1006 LDCH CHAR 501012
1009 STCH C1 541013
100C ALPHA RESW 1
100F FIVE WORD 5 000005
1012 CHAR BYTE C’Z’ Hex of ‘Z’
1013 C1 RESB 1
*/

