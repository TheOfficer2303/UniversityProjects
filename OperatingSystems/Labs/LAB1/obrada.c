#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTEND

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <math.h>

#define N 6

int OZNAKA_CEKANJA[N];
int PRIORITET[N];
int TEKUCI_PRIORITET;

int sig[] = {SIGUSR1, SIGUSR2, SIGBUS, SIGILL, SIGINT };
int flag = 0;

void zabrani_prekide() {
   for (size_t i = 0; i < 5; i++) {
      sighold(sig[i]);
   }
}

void dozvoli_prekide() {
   for (size_t i = 0; i < 5; i++) {
      sigrelse(sig[i]);
   }
}

void obrada_signala(int i) {
   flag = 1;
   const int SIZE = 6;
   char ispis[] = { '-', '-', '-', '-', '-', '-' };
   ispis[i] = 'P';
   printf("\n");
   for (size_t j = 0; j < SIZE; j++) {
      printf("%c ", ispis[j]);

   }
   printf("\n");

   for (int j = 1; j <= 5; j++) {
      sleep(1);
      ispis[i] = j + '0';
      for (size_t k = 0; k < SIZE; k++) {
         printf("%c ", ispis[k]);

      }
      printf("\n");
   }

   ispis[i] = 'K';
   for (size_t j = 0; j < SIZE; j++) {
      printf("%c ", ispis[j]);

   }
   printf("\n");
   flag = 0;
}

void prekidna_rutina(int sig) {
   int n = -1;
   zabrani_prekide();

   switch (sig) {
   case SIGUSR1:
      n = 1;
      if (flag == 1) {
         printf("\n- X - - - -\n");
      }
      else {
         printf("\n- X - - - -");
      }
      break;
   case SIGUSR2:
      n = 2;
      if (flag == 1) {
         printf("\n- - X - - -\n");
      }
      else {
         printf("\n- - X - - -");
      }
      break;

   case SIGBUS:
      n = 3;
      if (flag == 1) {
         printf("\n- - - X - -\n");
      }
      else {
         printf("\n- - - X - -");
      }
      break;

   case SIGILL:
      n = 4;
      if (flag == 1) {
         printf("\n- - - - X -\n");
      }
      else {
         printf("\n- - - - X -");
      }
      break;

   case SIGINT:
      n = 5;
      if (flag == 1) {
         printf("\n- - - - - X\n");
      }
      else {
         printf("\n- - - - - X");
      }
      break;
   }

   OZNAKA_CEKANJA[n] += 1;

   int max_prioritet;
   do {
      max_prioritet = 0;
      for (size_t i = TEKUCI_PRIORITET + 1; i < N; i++) {
         if (OZNAKA_CEKANJA[i] != 0)
            max_prioritet = i;
      }

      if (max_prioritet > 0) {
         OZNAKA_CEKANJA[max_prioritet] -= 1;
         PRIORITET[max_prioritet] = TEKUCI_PRIORITET;
         TEKUCI_PRIORITET = max_prioritet;
         dozvoli_prekide();
         obrada_signala(max_prioritet);
         zabrani_prekide();
         TEKUCI_PRIORITET = PRIORITET[max_prioritet];
         
      }
   } while (max_prioritet > 0);
}

int main(void) {
   TEKUCI_PRIORITET = 0;
   OZNAKA_CEKANJA[0] = 1;
   sigset(SIGUSR1, prekidna_rutina);
   sigset(SIGUSR2, prekidna_rutina);
   sigset(SIGBUS, prekidna_rutina);
   sigset(SIGILL, prekidna_rutina);
   sigset(SIGINT, prekidna_rutina);


   printf("Proces obrade prekida, PID=%d\n", getpid());
   printf("G 1 2 3 4 5\n");
   printf("------------------------------\n");

   const int SIZE = 5;
   char ispis[] = { '-', '-', '-', '-', '-' };

   for (int j = 1; j <= 25; j++) {
      sleep(1);
      printf("%d ", j);
      for (size_t k = 0; k < SIZE; k++) {
         printf("%c ", ispis[k]);
      }
      printf("\n");

   }

   return 0;
}