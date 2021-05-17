#include <stdio.h>
#include <stdlib.h>
#include <time.h>
char storage[50];

int findMinFreeSpace(int memory, int alloc) {
   int startingPoint = 0;
   int freeMemory = 0;
   char lastChar = storage[0];
   int j = 0;
   char startPoint[memory];
   int lengths[memory];

   for (size_t i = 0; i < memory; i++) {
      startPoint[i] = 0;
      lengths[i] = 0;
   }


   for (size_t i = 0; i < memory; i++) {
      if (storage[i] == 0x2D && lastChar == 0x2D) {

         freeMemory += 1;

      }
      else if (storage[i] == 0x2D && lastChar != 0x2D) {
         freeMemory = 1;

      }
      else if (storage[i] != 0x2D && freeMemory != 0) {
         startPoint[j] = i - freeMemory;
         lengths[j] = freeMemory;
         j += 1;
      }
      lastChar = storage[i];
   }

   startPoint[j] = memory - freeMemory;
   lengths[j] = freeMemory;

   int minLength = memory;
   for (size_t i = 0; i < (sizeof lengths / sizeof lengths[0]); i++) {
      if (lengths[i] < minLength && lengths[i] != 0 && lengths[i] >= alloc) {
         minLength = lengths[i];
         startingPoint = startPoint[i];
      }
   }


   return startingPoint;

}

int hasEnoughMemory(int memory, int alloc) {
   int freeMemory = 0;
   int maxFreeMemory = 0;
   char lastChar = storage[0];
   for (size_t i = 0; i < memory; i++) {
      if (storage[i] == 0x2D && lastChar == 0x2D) {
         freeMemory += 1;
         if (freeMemory > maxFreeMemory)
            maxFreeMemory = freeMemory;
      }
      else if (storage[i] == 0x2D && lastChar != 0x2D){
         freeMemory = 1;
      }
      lastChar = storage[i];
   }

   if (maxFreeMemory >= alloc) {
      return 1;
   }
   else {
      return 0;
   }
}

int hasRequest(int memory, char request) {
   for (size_t i = 0; i < memory; i++)
   {
      if (storage[i] == request) {
         return 1;
      }
   }

   return 0;

}

int main(int argc, char const* argv[]) {
   srand(time(NULL));
   int memory = atoi(argv[1]);
   storage[memory];

   for (size_t i = 0; i < memory; i++) {
      storage[i] = 0x2D;
      printf("%c", storage[i]);
   }

   printf("\n");

   char request = 'A';
   int lastFilled = 0;
   char key;

   while (1) {
      printf("Input key: ");
      scanf(" %c", &key);
      int randAlloc = (rand() % 6) + 1;

      switch (key) {
      case 0x5A:

         if (hasEnoughMemory(memory, randAlloc)) {
            lastFilled = findMinFreeSpace(memory, randAlloc);
         }
         else {
            printf("Request is bigger than free space. Free some space or try a smaller request!\n");
            break;
         }
         for (size_t i = lastFilled; i < randAlloc + lastFilled; i++) {
            storage[i] = request;
         }

         lastFilled += randAlloc;
         printf("New request %c for %d memory space.\n", request, randAlloc);
         request += 1;



         for (size_t i = 0; i < memory; i++){
            printf("%c", storage[i]);
         }
         printf("\n");
         break;
      case 0x4F:
         printf("Which request do you want to free?\n");
         char choice;
         scanf("%s", &choice);

         if (!hasRequest(memory, choice)) {
            printf("No such request to free!\n");
            break;
         }

         printf("Freeing request...\n");
         if (!hasEnoughMemory(memory, randAlloc)) {
            request += 1;
         }

         printf("%c\n", request);

         for (size_t i = 0; i < memory; i++) {
            if (storage[i] == choice) {
               storage[i] = 0x2D;
            }
         }

         for (size_t i = 0; i < memory; i++){
            printf("%c", storage[i]);
         }
         printf("\n");
         break;
      default:
         printf("Unknown input. Try again!\n");
         break;
      }

   }



   return 0;
}
