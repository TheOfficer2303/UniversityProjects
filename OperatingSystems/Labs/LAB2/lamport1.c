#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>
#include <stdatomic.h>

atomic_int a;
atomic_int n;
atomic_int BROJ_ITERACIJA, * BROJ, * ULAZ;

int max(atomic_int* p, atomic_int n) {
   atomic_int maxBroj, i;
   maxBroj = 0;
   for (i = 0; i < n; ++i) {
      if (*(p + i) > maxBroj)
         maxBroj = *(p + i);
   }
   return maxBroj;
}



void* dretva(void* rbr) {
   int i;
   atomic_int* id = rbr;
  

   for (int k = 0; k < BROJ_ITERACIJA; k++) {
      //ulaz u KO
      ULAZ[*id] = 1;
      BROJ[*id] = max(BROJ, n) + 1;
      ULAZ[*id] = 0;

      for (size_t j = 0; j < n; j++) {
         while (ULAZ[j] != 0);
         while (BROJ[j] != 0 && (BROJ[j] < BROJ[*id] || (BROJ[j] == BROJ[*id] && j < *id)));
      }

      a += 1;  //kritični odsječak

      //izlaz iz KO
      BROJ[*id] = 0;
   }

   return NULL;
}




int main(int argc, char const* argv[]) {
   a = 0;

   if (argc != 3) {
      printf("Korištenje: ./lamport.out broj_dretvi broj_uvećanja\n");
      exit(1);
   }

   n = atoi(argv[1]);
   BROJ_ITERACIJA = atoi(argv[2]);
   pthread_t t[n];

   ULAZ = (atomic_int*)malloc((n) * sizeof(atomic_int));
   atomic_int* id = (atomic_int*)malloc((n) * sizeof(atomic_int));
   BROJ = (atomic_int*)malloc(n * sizeof(atomic_int));

   for (int i = 0; i < n; i++) {
      ULAZ[i] = 0;
      BROJ[i] = 0;
      
   }

   for (size_t i = 0; i < n; i++) {
      id[i] = (i);
      if (pthread_create(&t[i], NULL, dretva, &id[i])) {
         printf("Ne mogu stvoriti dretvu!");
         exit(1);
      }
   }

   for (int j = 0; j < n; j++) {
      pthread_join(t[j], NULL);
   }
   
   printf("A=%d\n", a);

   return 0;
}
