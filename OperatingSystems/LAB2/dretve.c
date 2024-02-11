#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
int a;
int BROJ_ITERACIJA;

void *dretva(void *rbr) {
   int i, *broj = rbr;
   for (i = 0; i < BROJ_ITERACIJA; i++) {
      a += 1;
   }
   return NULL;
}

int main(int argc, char const *argv[]) {
   a = 0;

   if (argc != 3) {
      printf("Korištenje: ./dretve.out broj_dretvi broj_uvećanja\n");
      exit(1);
   }
   int BROJ_DRETVI = atoi (argv[1]);
   BROJ_ITERACIJA = atoi (argv[2]);

   pthread_t t[BROJ_DRETVI];
   int BR[BROJ_DRETVI];


   for (int i = 0; i < BROJ_DRETVI; i++) {
      BR[i] = i;
      if (pthread_create(&t[i], NULL, dretva, &BR[i])) {
         printf("Bezi bre!");
         exit(1);
      }
   }

   for (int j = 0; j < BROJ_DRETVI; j++) {
      pthread_join(t[j], NULL);
   }
   
   
   printf("A=%d\n", a);
   
   return 0;
}
