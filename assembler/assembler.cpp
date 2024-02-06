#include <iostream>
#include <unordered_map>
#include <sstream>

std::unordered_map<std::string, std::string> symbolTable;

std::string convertToMachineCode(const std::string& opcode, const std::string& operand) {
    std::stringstream machineCode;
    if (opcode == "LDA") {
        machineCode << "00";
    } else if (opcode == "STA") {
        machineCode << "0C";
    } else if (opcode == "LDCH") {
        machineCode << "50";
    } else if (opcode == "STCH") {
        machineCode << "54";
    }
    
    if (symbolTable.find(operand) != symbolTable.end()) {
        machineCode << symbolTable[operand];
    } else {
        machineCode << operand;
    }
    
    return machineCode.str();
}

// first pass: addresses 
// second pass: machine code
// machine code should be in hex
// do not ask for input, give input as a string

int main(){
    // give input as:
    /*
    	LDA FIVE
	STA ALPHA
	LDCH CHAR
	STCH C1
ALPHA RESW 1
FIVE WORD 5
CHAR BYTE C’Z’
C1 RESB 1*/
    std:: string input = "LDA FIVE\nSTA ALPHA\nLDCH CHAR\nSTCH C1\nALPHA RESW 1\nFIVE WORD 5\nCHAR BYTE C’Z’\nC1 RESB 1";
    std::stringstream ss(input);
    std::string line;
    // starting address is 1000
    int locctr = 1000;
    while (getline(ss, line)) {
        std::stringstream ss2(line);
        std::string opcode, operand;
        ss2 >> opcode >> operand;
        if (opcode == "RESW") {
            symbolTable[operand] = std::to_string(locctr);
            locctr += 3;
        } else if (opcode == "RESB") {
            symbolTable[operand] = std::to_string(locctr);
            locctr += 1;
        } else if (opcode == "WORD") {
            symbolTable[operand] = std::to_string(locctr);
            locctr += 3;
        } else if (opcode == "BYTE") {
            symbolTable[operand] = std::to_string(locctr);
            locctr += 1;
        } else {
            symbolTable[operand] = std::to_string(locctr);
            locctr += 3;
        }
    }
    
    ss = std::stringstream(input);
    // output should be of this format:
    /*
    1000 LDA FIVE 00100F
    1003 STA ALPHA 0C100C
    ..
    1012 CHAR BYTE C’Z’ Hex of ‘Z’
    1013 C1 RESB 1
    */
    while (getline(ss, line)) {
        std::stringstream ss2(line);
        std::string opcode, operand;
        ss2 >> opcode >> operand;
        std::cout << symbolTable[operand] << " " << opcode << " " << operand << " " << convertToMachineCode(opcode, operand) << std::endl;
    }
}

