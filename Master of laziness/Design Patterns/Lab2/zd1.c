#include <stdio.h>
#include <string.h>

const void* mymax(const void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *)) {
  const void* max = base + size;
  const void* curr;

  for (size_t i = 0; i < nmemb; i++) {
    curr = base + (i * size);
    if (compar(curr, max)) {
      max = curr;
    }
  }

  return max;
}

int gt_int(const void* a, const void* b) {
  return *(int*)a > *(int*)b ? 1 : 0;
}

int gt_char(const void* a, const void* b) {
  return *(char*)a > *(char*)b;
}

int gt_str(const void* a, const void* b) {
  return strcmp(*(char**)a, (char**)b) > 0;
}

int main() {
  int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
  char arr_char[]="Suncana strana ulice";
  const char* arr_str[] = {"Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"};

  printf("%d\n", *(int*)mymax(arr_int, sizeof(arr_int) / sizeof(int), sizeof(int), gt_int));
  printf("%c\n", *(char*)mymax(arr_char, sizeof(arr_char) / sizeof(char), sizeof(char), gt_char));
  printf("%s\n", *(char**)mymax(arr_str, sizeof(arr_str) / sizeof(*arr_str), sizeof(char*), gt_str));
}
