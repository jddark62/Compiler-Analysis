#include <iostream>
#include <regex>
#include <unordered_map>
#include <vector>

struct SymbolEntry {
	std::string assemblerStartAddr;
	std::string symbolAddr;
	std::string runtimeStartAddr;
	std::vector<std::string> referredIn;
};

std::unordered_map<std::string, SymbolEntry> symbolTable;

void addToSymbolTable(const std::string& symbol, const std::string& assemblerStartAddr, const std::string& symbolAddr, const std::string& runtimeStartAddr, const std::string& referredIn) {
	if (symbolTable.count(symbol) > 0) {
		SymbolEntry& entry = symbolTable[symbol];
		entry.runtimeStartAddr = runtimeStartAddr;
		entry.referredIn.push_back(referredIn);
	} else {
		SymbolEntry entry;
		entry.assemblerStartAddr = assemblerStartAddr;
		entry.symbolAddr = symbolAddr;
		entry.runtimeStartAddr = runtimeStartAddr;
		entry.referredIn.push_back(referredIn);
		symbolTable[symbol] = entry;
	}
}

void constructSymbolTable(const std::vector<std::string>& objectPrograms) {
	std::regex headerRegex(R"(H_(\w+)_(\w+)_(\w+))");
	std::regex definitionRegex(R"(D_(\w+)_(\w+)_(\w+)_(\w+)_(\w+)_(\w+))");
	std::regex referenceRegex(R"(R_(\w+)_(\w+))");
	std::regex endRegex(R"(E_(\w+))");

	for (const std::string& objectProgram : objectPrograms) {
		std::istringstream iss(objectProgram);
		std::string line;

		std::string programName;
		std::string assemblerStartAddr;
		std::string runtimeStartAddr;

		while (std::getline(iss, line)) {
			if (std::regex_match(line, headerRegex)) {
				std::smatch match;
				std::regex_search(line, match, headerRegex);
				programName = match[1];
				assemblerStartAddr = match[2];
				runtimeStartAddr = match[3];
			} else if (std::regex_match(line, definitionRegex)) {
				std::smatch match;
				std::regex_search(line, match, definitionRegex);
				std::string symbol = match[1];
				std::string symbolAddr = match[2];
				addToSymbolTable(symbol, assemblerStartAddr, symbolAddr, runtimeStartAddr, programName);
			} else if (std::regex_match(line, referenceRegex)) {
				std::smatch match;
				std::regex_search(line, match, referenceRegex);
				std::string referredSymbol = match[2];
				addToSymbolTable(referredSymbol, "", "", "", programName);
			} else if (std::regex_match(line, endRegex)) {
				break;
			}
		}
	}
}

void printSymbolTable() {
	std::cout << "Symbol\tAssembler starting address\tAddress of Symbol\tRuntime starting address\tAddress of Symbol Referred in\n";
	for (const auto& entry : symbolTable) {
		std::cout << entry.first << "\t" << entry.second.assemblerStartAddr << "\t\t\t" << entry.second.symbolAddr << "\t\t\t" << entry.second.runtimeStartAddr << "\t\t\t";
		if (entry.second.referredIn.empty()) {
			std::cout << "None";
		} else {
			for (const std::string& program : entry.second.referredIn) {
				std::cout << program << " ";
			}
		}
		std::cout << "\n";
	}
}

int main() {
	std::vector<std::string> objectPrograms = {
		"H_Prog1_001000_1E\nD_A1_1010_A2_101C_A3_1020\nR_B1_C1\nT_...........................\nM_.....................\nE_001000",
		"H_Prog2_001000_1E\nD_B1_101A_B2_101D_B3_1024\nR_A1_C3\nT_...........................\nM_.....................\nE_001000",
		"H_Prog3_001000_1E\nD_C1_2000_C2_201C_C3_2021\nR_A1_B1_B2\nT_...........................\nM_.....................\nE_001000"
	};

	constructSymbolTable(objectPrograms);
	printSymbolTable();

	return 0;
}
