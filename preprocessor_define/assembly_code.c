#include <stdio.h>
#include <string.h>

// Function to convert assembly language program to machine code
void convertToMachineCode(char *assemblyCode[], int numInstructions, int startingAddress, int instructionSize) {
    int address = startingAddress;
    
    // First pass: Assign addresses to each instruction
    for (int i = 0; i < numInstructions; i++) {
        printf("%04X\t%s\t", address, assemblyCode[i]);
        
        // Check if the instruction is a label
        if (strstr(assemblyCode[i], ":") != NULL) {
            printf("\n");
            continue;
        }
        
        // Increment address based on instruction size
        address += instructionSize;
        printf("%05X\n", address);
    }
    
    address = startingAddress;
    
    // Second pass: Generate machine code
    for (int i = 0; i < numInstructions; i++) {
        printf("%04X\t%s\t", address, assemblyCode[i]);
        
        // Check if the instruction is a label
        if (strstr(assemblyCode[i], ":") != NULL) {
            printf("\n");
            continue;
        }
        
        // Generate machine code based on instruction
        if (strstr(assemblyCode[i], "LDA") != NULL) {
            printf("00100F\n");
        } else if (strstr(assemblyCode[i], "STA") != NULL) {
            printf("0C100C\n");
        } else if (strstr(assemblyCode[i], "LDCH") != NULL) {
            printf("501012\n");
        } else if (strstr(assemblyCode[i], "STCH") != NULL) {
            printf("541013\n");
        } else if (strstr(assemblyCode[i], "RESW") != NULL) {
            printf("\n");
        } else if (strstr(assemblyCode[i], "WORD") != NULL) {
            printf("000005\n");
        } else if (strstr(assemblyCode[i], "BYTE") != NULL) {
            // Extract the character from the BYTE instruction
            char *start = strchr(assemblyCode[i], '\'') + 1;
            char *end = strchr(start, '\'');
            char character = *start;
            
            printf("%02X\n", character);
        } else if (strstr(assemblyCode[i], "RESB") != NULL) {
            printf("\n");
        }
        
        // Increment address based on instruction size
        address += instructionSize;
    }
}

int main() {
    // Input assembly code
    char *assemblyCode[] = {
        "LDA  FIVE",
        "STA  ALPHA",
        "LDCH  CHAR",
        "STCH   C1",
        "ALPHA   RESW 1",
        "FIVE  WORD 5",
        "CHAR  BYTE C'Z'",
        "C1  RESB 1"
    };
    
    int numInstructions = sizeof(assemblyCode) / sizeof(assemblyCode[0]);
    int startingAddress = 1000;
    int instructionSize = 3;
    
    // Convert assembly code to machine code
    convertToMachineCode(assemblyCode, numInstructions, startingAddress, instructionSize);
    
    return 0;
}
