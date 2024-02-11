#include <iostream>
#include <list>
#include <set>
#include <vector>

template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred) {
  Iterator max = first;
  Iterator curr = ++max;

  while (curr != last) {
    if (pred(curr, max)) {
      max = curr;
    }

    curr++;
  }

  return max;
}

int gt_int(const int* a, const int* b) {
    return *a > *b;
}

int gt_char(const char* a, const char* b) {
    return *a > *b;
}

int gt_str(const char** a, const char** b) {
    return strcmp(*a, *b) > 0;
}


int main(){
  int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
  char arr_char[] = "Suncana strana ulice";
  const char* arr_str[] = {"Gle", "malu", "vocku", "poslije", "kise", "Puna", "je", "kapi", "pa", "ih", "njise"};


  const int* maxint = mymax(&arr_int[0], &arr_int[sizeof(arr_int)/sizeof(*arr_int)], gt_int);
  const char* maxchar = mymax(&arr_char[0], &arr_char[sizeof(arr_char)/sizeof(*arr_char)], gt_char);
  const char** max_cstring = mymax(&arr_str[0], &arr_str[sizeof(arr_str)/sizeof(*arr_str)], gt_str);

  std::cout <<*maxint <<"\n";
  std::cout <<*maxchar <<"\n";
  std::cout <<*max_cstring <<"\n";
}
