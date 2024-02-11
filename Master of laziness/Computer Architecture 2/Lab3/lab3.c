/*
OS: Ubuntu 22 (VM VirtualBox na Windows 10)
model name	: Intel(R) Core(TM) i5-8300H CPU @ 2.30GHz
f = 2.3 GHz

L1
s1 = 64 KB (32KB instrukcije + 32KB podaci)
b1 = 64 b

L2
s2 = 256 KB
b1 = 64 b

L3
s3 = 8 MB
b1 = 64 b
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <malloc.h>

#define S1 32768
#define B1 64
#define S2 262144
#define B2 64
#define S3 8388608
#define B3 64
#define DELTA 8

void init(char *a, int size) {
    for(int i = 0; i < size; i++) {
        a[i] = 0;
    }
}

void A(char* buffer, int size) {
    for (int i = 0; i < size; i++) {
        buffer[i] += 1;
    }
}

void B(char* buffer, int size) {
    for (int i = 0; i < size; i += DELTA * B1) {
        buffer[i] += 1;
    }
}

void C(char* buffer, int size) {
    for (int i = 0; i < size; i += B2) {
        buffer[i] += 1;
    }
}

void D(char* buffer, int size) {
    for (int i = 0; i < size; i += B3) {
        buffer[i] += 1;
    }
}

double L1_benchmark() {
    int i, j;
    double start, stop, duration, bandwidth;
    
    start = clock();
    int size = S1;

    char *buffer = (char *)malloc(size * sizeof(char));
    init(buffer, size);

    for (i = 0; i < 10000; i++) {
        A(buffer, size);
    }

    stop = clock();
    free(buffer);

    duration = (stop - start) / CLOCKS_PER_SEC;
    bandwidth = 10000 * size / duration / S1;
    return bandwidth;
}

double L2_benchmark() {
    int i, j;
    double start, stop, duration, bandwidth;
    
    start = clock();
    int size = DELTA * 2 * S1;

    char *buffer = (char *)malloc(size * sizeof(char));
    init(buffer, size);

    for (i = 0; i < 10000; i++) {
        B(buffer, size);
    }

    stop = clock();
    free(buffer);

    duration = (stop - start) / CLOCKS_PER_SEC;
    bandwidth = 10000 * size / B1 / duration / (1 << 18);
    return bandwidth;
}

double L3_benchmark() {
    int i, j;
    double start, stop, duration, bandwidth;
    
    start = clock();
    int size = 2 * S2;

    char *buffer = (char *)malloc(size * sizeof(char));
    init(buffer, size);

    for (i = 0; i < 10000; i++) {
        C(buffer, size);
    }

    stop = clock(); 
    free(buffer);
    
    duration = (stop - start) / CLOCKS_PER_SEC;
    bandwidth = 10000 * size / B2 / duration / (1 << 18);
    return bandwidth;
}

double RAM_benchmark() {
    int i, j;
    double start, stop, duration, bandwidth;
    
    start = clock();
    int size = 2 * S3;

    char *buffer = (char *)malloc(size * sizeof(char));
    init(buffer, size);

    for (i = 0; i < 10000; i++) {
        D(buffer, size);
    }

    free(buffer);
    stop = clock(); 
    duration = (stop - start) / CLOCKS_PER_SEC;
    bandwidth = 10000 * size / B3 / duration / (1 << 18);
    return bandwidth;
}

int main(void) {
    double tL1, tL2, tL3, tRAM;

    tL1 = L1_benchmark();
    printf("Propusnost L1: %f\n", tL1);

    tL2 = L2_benchmark();
    printf("Propusnost L2: %f\n", tL2);

    tL3 = L3_benchmark();
    printf("Propusnost L3: %f\n", tL3);

    tRAM = RAM_benchmark();
    printf("Propusnost RAM: %f\n", tRAM);

    printf("L2/L1 = %f\n", tL2 / tL1);
    printf("L3/L2 = %f\n", tL3 / tL2);
	printf("RAM/L3 = %f\n", tRAM/ tL2);

    return 0;
}
