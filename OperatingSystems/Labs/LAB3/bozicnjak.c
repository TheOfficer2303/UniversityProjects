#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTEND

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>
#include <unistd.h>
#include <stdatomic.h>
#include <semaphore.h>
#include <time.h>
#include <sys/ipc.h>
#include <sys/shm.h>

int ID;

int* brojSobova;
int* brojPatuljaka;
sem_t* djedMraz;
sem_t* KO;
sem_t* konzultacije;
sem_t* sobovi;



void* djedica() {

   while (1) {
      printf("Djed spava...\n");
      sem_wait(djedMraz);
      sem_wait(KO);

      if (*brojSobova == 10 && *brojPatuljaka > 0) {
         sem_post(KO);
         printf("Djed: Ukrcavam poklone i raznosim...\n");
         sleep(2);    // ukrcaj_poklone_i_raznosi
         printf("Djed: Pokloni razneseni, šaljem sobove na godišnji...\n");
         sem_wait(KO);

         //povećaj semafor za 10
         for (size_t i = 0; i < 10; i++) {
            sem_post(sobovi);
         }

         *brojSobova = 0;
      }

      if (*brojSobova == 10) {
         sem_post(KO);
         printf("Djed: Svi sobovi su mi na broju! Hranim ih...\n");
         sleep(2);   //nahrani sobove
         printf("Djed: Sobovi su nahranjeni!\n");
         sem_wait(KO);
      }
      //ako je samo_tri_patuljka_pred_vratima 
      while (*brojPatuljaka >= 3) {
         sem_post(KO);
         printf("Djed: Riješavam problem trojice patuljaka...\n");
         sleep(2);
         sem_wait(KO);

         for (size_t i = 0; i < 3; i++) {
            sem_post(konzultacije);
         }

         *brojPatuljaka -= 3;
         printf("Djed: Problem riješen!\n");
         printf("Broj patuljaka nakon rješavanja: %d\n", *brojPatuljaka);
      }
      sem_post(KO);

   }
}

void* patuljak() {
   *brojPatuljaka += 1;
   printf("Ja sam %d. patuljak!\n", *brojPatuljaka);
   sem_wait(KO);
   
   // printf("Broj patuljaka: %d\n", *brojPatuljaka);

   if (*brojPatuljaka > 0 && *brojSobova == 10) {
      sem_post(djedMraz);
   }
   else if (*brojPatuljaka == 3) {
      printf("Zovemo djedicu!\n");
      sem_post(djedMraz);
   }
   sem_post(KO);
   sem_wait(konzultacije);
}

void* sob() {
   *brojSobova += 1;
   printf("Ja sam %d. sob\n", *brojSobova);
   sem_wait(KO);
   
   // printf("Broj sobova: %d\n", *brojSobova);

   if (*brojSobova == 10 && *brojPatuljaka > 0) { //za raznosenje poklona
      sem_post(djedMraz);
   }
   else if (*brojSobova == 10) { //za hranidbu sobova
      sem_post(djedMraz);
   }

   sem_post(KO);
   sem_wait(sobovi);
}

void kraj(int sig) {
   shmdt(djedMraz);
   shmctl(ID, IPC_RMID, NULL);

   sem_destroy(djedMraz);
   sem_destroy(KO);
   sem_destroy(konzultacije);
   sem_destroy(sobovi);
   exit(0);
   printf("GOTOVO!\n");

}


// SJEVERNI POL
int main(void) {
   sigset(SIGINT, kraj);
   sigset(SIGCHLD, SIG_IGN);

   ID = shmget(IPC_PRIVATE, sizeof(sem_t) * 4 + sizeof(int) * 2, 0600);
   // shmctl(ID, IPC_RMID, NULL);

   djedMraz = (sem_t*)shmat(ID, NULL, 0);
   KO = (sem_t*)(djedMraz + 1);
   konzultacije = (sem_t*)(KO + 1);
   sobovi = (sem_t*)(konzultacije + 1);

   brojPatuljaka = (int*)(sobovi + 1);
   brojSobova = (int*)(brojPatuljaka + 1);

   *brojPatuljaka = 0;
   *brojSobova = 0;

   sem_init(djedMraz, 1, 0);
   sem_init(KO, 1, 1);
   sem_init(konzultacije, 1, 3);
   sem_init(sobovi, 1, 10);

   int pid;
   switch (pid = fork()) {
   case -1:
      printf("Greška\n");
      exit(1);
      break;
   case 0:
      djedica();
      exit(0);
   default:
      break;

   }

   srand(time(0));
   
   while (1) {
      //svake 1-3 sekunde stvori soba ili patuljka
      int sleepTime = (rand() % (3 - 1 + 1)) + 1;
      sleep(sleepTime);
      int vjerojatnostPatuljka = (rand() % (100 - 0 + 1)) + 0;
      int vjerojatnostSoba = (rand() % (100 - 0 + 1)) + 0;


      if (vjerojatnostPatuljka > 50) {
         switch (pid = fork()) {
         case -1:
            printf("Greška!");
            break;
         case 0:
            patuljak();
            exit(0);
            break;
         default:
            break;
         }
      }

      if (vjerojatnostSoba > 50 && *brojSobova < 10) {
         switch (pid = fork()) {
         case -1:
            printf("Greška!");
            break;
         case 0:
            sob();
            exit(0);
            break;
         default:
            break;
         }
      }

   }


   
   wait(NULL);
   

   for (size_t i = 0; i < *brojPatuljaka; i++) {
      wait(NULL);
   }

   for (size_t i = 0; i < *brojSobova; i++) {
      wait(NULL);
   }

   return 0;
}


