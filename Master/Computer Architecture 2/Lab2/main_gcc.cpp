#include <iostream>
#include <stdio.h>
#include <cstdlib>
#include <stdlib.h>

extern "C" int potprogram_asm(int);

int potprogram_c(int n) {
	int sum = 0;
	for (int i = 0; i < n; i++) {
		sum += i;
	}
	return sum;
}

int main() {
	std::cout << "ASM, n = 0: " << potprogram_asm(0) << std::endl;
	std::cout << "C++, n = 0: " << potprogram_c(0) << std::endl;

	std::cout << "ASM, n = 10: " << potprogram_asm(10) << std::endl;
	std::cout << "C++, n = 10: " << potprogram_c(10) << std::endl;

	std::cout << "ASM, n = 120: " << potprogram_asm(120) << std::endl;
	std::cout << "C++, n = 120: " << potprogram_c(120) << std::endl;

	std::cout << "ASM, n = -10: " << potprogram_asm(-10) << std::endl;
	std::cout << "C++, n = -10: " << potprogram_c(-10) << std::endl;
}