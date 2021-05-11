#define _XOPEN_SOURCE
#define _XOPEN_SOURCE_EXTEND

#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>


char filozofi[5] = {'0', '0', '0', '0', '0'};
char vilica[5] = {1, 1, 1, 1, 1};
pthread_mutex_t monitor;
pthread_cond_t red[5];

void ispisStanja() {
    for (size_t i = 0; i < 5; i++) {
        printf("%c ", filozofi[i]);
    }
    printf("\n");

}

void jesti(int n) {
    pthread_mutex_lock(&monitor);
    filozofi[n] = 'o';
    while (vilica[n] == 0 || vilica[(n + 1) % 5] == 0) {
        pthread_cond_wait(&red[n], &monitor);
    }
    vilica[n] = 0;
    vilica[(n + 1) % 5] = 0;
    filozofi[n] = 'X';
    ispisStanja();      
    pthread_mutex_unlock(&monitor);

    sleep(2); //hranidba

    pthread_mutex_lock(&monitor);
    filozofi[n] = 'O';
    vilica[n] = 1;
    vilica[(n + 1) % 5] = 1;
    pthread_cond_signal(&red[(n - 1) % 5]);
    pthread_cond_signal(&red[(n + 1) % 5]);
    ispisStanja();
    pthread_mutex_unlock(&monitor);
}

void *filozof(void *rbr) {
    int n = *((int *) rbr);
   
    while (1) {
        srand(time(0));
        int slucVrijeme = (rand() % (3 - 1 + 1)) + 1;
        sleep(slucVrijeme); //misliti
        jesti(n);
    }
}


int main(int argc, char const *argv[]) {
    int brojFilozofa = 5;
    pthread_mutex_init(&monitor, NULL);
    for (size_t i = 0; i < brojFilozofa; i++) {
        pthread_cond_init(&red[i], NULL);
    }

    pthread_t t[brojFilozofa];
    int broj[brojFilozofa];

    for (size_t i = 0; i < brojFilozofa; i++) {
        broj[i] = i;
        pthread_create(&t[i], NULL, filozof, &broj[i]);
    }

    for (size_t i = 0; i < brojFilozofa; i++) {
        pthread_join(t[i], NULL);
    }

    pthread_mutex_destroy(&monitor);
    for (size_t i = 0; i < brojFilozofa; i++)
    {
        pthread_cond_destroy(&red[i]);
    }
    
    
    

    return 0;
}
