#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTENDED

#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <sys/time.h>
#include <math.h>

unsigned long broj = 100000001;
unsigned long zadnji = 100000001;
int pauza = 0;

void prekini() {
   printf("zadnji prost = %lu\n", zadnji);
   exit(0);
}

void ispis() {
   printf("zadnji prost = %lu\n", zadnji);
}

void postavi_pauzu() {
   if (pauza == 0) {
      printf("  zaustavljam\n");
   } else {
      printf("  nastavljam\n");
   }

   pauza = 1 - pauza;
   
}

void postavi_timer() {
   struct itimerval t;

   sigset(SIGALRM, ispis);

   t.it_value.tv_sec = 1;
   t.it_value.tv_usec = 0;

   t.it_interval.tv_sec = 5;
   t.it_interval.tv_usec = 0;

   setitimer(ITIMER_REAL, &t, NULL);

}

int prost(int broj) {
   if (broj % 2 == 0) return 0;

   int max = sqrt(broj);
   for (size_t i = 3; i <= max; i += 2) {
      if (broj % i == 0) return 0;
   }

   return 1;
}

int main(void) {

   sigset(SIGTERM, prekini);
   sigset(SIGINT, postavi_pauzu);

   postavi_timer();

   while (1) {
      if (prost(broj)) {
         zadnji = broj;
      }
      ++broj;
      while (pauza == 1) {
         pause();
      }
   }
   return 0;
}