#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTENDED

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <stdbool.h>

int pid = 0;

void prekidna_rutina(int signal) {
    kill(pid, SIGKILL);
    exit(0);
}


int main(int argc, char *argv[]) {
    srand(time(NULL));
    pid = atoi(argv[1]);
    sigset(SIGINT, prekidna_rutina);

    // Generiranje signala nasumicno izabranog iz polja
    // svake 4 sekunde
    int signali[] = {SIGBUS, SIGILL, SIGHUP, SIGSEGV};
    while(true) {
        int rnd = rand() % 4;
        kill(pid, signali[rnd]);
        printf("SIGNAL KOD - %d\n", signali[rnd]);
        sleep(4);
    }
}
