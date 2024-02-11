#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/shm.h>
int* a;
int ID;
int BROJ_ITERACIJA;

void* proces() {
   for (size_t i = 0; i < BROJ_ITERACIJA; i++) {
      *a += 1;
   }
}

void brisi() {
   shmdt(a);
   shmctl(ID, IPC_RMID, NULL);
   exit(0);
}

int main(int argc, char const* argv[]) {
   int i, pid;

   //broj procesa i iteracija
   if (argc != 3) {
      printf("Korištenje: ./procesi.out broj_dretvi broj_uvećanja\n");
      exit(1);
   }
   int broj_procesa = atoi(argv[1]);
   BROJ_ITERACIJA = atoi(argv[2]);

   //rezerviranje zajednickog spremnika
   ID = shmget(IPC_PRIVATE, sizeof(int), 0600);
   if (ID == -1) {
      printf("Nema memorije\n"),
         exit(1);
   }

   //inicijalizacija u zajednickom spremniku
   a = (int*)shmat(ID, NULL, 0);
   *a = 0;

   for (i = 0; i < broj_procesa; i++) {
      switch (pid = fork()) {
      case -1:
         printf("R: Ne mogu stvoriti novi proces!\n");
         exit(1);
      case 0:
         proces();
         exit(0);
      default:
         break;
      }
   }

   for (i = 0; i < broj_procesa; i++)
      wait(NULL);

   printf("A = %d\n", *a);
   brisi();
   return 0;
}
