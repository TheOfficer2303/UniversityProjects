#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef char const* (*PTRFUN)();

struct Animal {
  struct AnimalFunctions* vtable;
  char const* name;
};

struct AnimalFunctions {
  PTRFUN menu;
  PTRFUN greet;
};

struct Animal2Functions {
  PTRFUN menu;
  PTRFUN greet;
  PTRFUN moves;
};

char const* birdMoves(void){
  return "im moving!";
}

char const* birdGreet(void){
  return "kre!";
}

char const* birdMenu(void){
  return "kukce";
}

char const* dogGreet(void){
  return "vau!";
}

char const* dogMenu(void){
  return "kuhanu govedinu";
}

char const* catGreet(void){
  return "mijau!";
}

char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

struct AnimalFunctions dogFunctions = {
  &dogMenu,
  &dogGreet
};

struct AnimalFunctions catFunctions = {
  &catMenu,
  &catGreet
};

struct Animal2Functions birdFunctions = {
  &birdMenu,
  &birdGreet,
  &birdMoves
};

void animalPrintGreeting(struct Animal* animal) {
  printf("%s pozdravlja: %s\n", animal->name, animal->vtable->greet());
}

void animalPrintMenu(struct Animal* animal) {
  printf("%s voli: %s\n", animal->name, animal->vtable->menu());
}

void constructDog(struct Animal* dog, char const* name) {
  dog->vtable = &dogFunctions;
  dog->name = name;
}

void constructBird(struct Animal* bird, char const* name) {
  bird->vtable = &birdFunctions;
  bird->name = name;
}

void constructCat(struct Animal* cat, char const* name) {
  cat->vtable = &catFunctions;
  cat->name = name;
}

struct Animal* createDog(char const* name) {
  struct Animal* dog = malloc(sizeof(struct Animal));

  constructDog(dog, name);

  return dog;
}

struct Animal* createBird(char const* name) {
  struct Animal* bird = malloc(sizeof(struct Animal));

  constructBird(bird, name);

  return bird;
}

struct Animal* createCat(char const* name) {
  struct Animal* cat = malloc(sizeof(struct Animal));

  constructCat(cat, name);

  return cat;
}

void testAnimals(void){
  struct Animal* p1 = createDog("Hamlet");
  struct Animal* p2 = createCat("Ofelija");
  struct Animal* p3 = createDog("Polonije");
  struct Animal* p4 = createBird("Ptica");

  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);
  animalPrintGreeting(p4);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);
  animalPrintMenu(p4);

  free(p1);
  free(p3);
}

struct Animal* createNDogs(int n) {
  struct Animal* dogs = malloc(n * sizeof(struct Animal));
  char* name;
  strcpy(name, "Jedan od N pasa");

  for (int i = 0; i < n; i++) {
    constructDog(&dogs[i], name);
  }

  return dogs;
}

struct Animal testHeapAndStack() {
  struct Animal dog;
  dog.name = "Pas 1";
  dog.vtable = &dogFunctions;

  return dog;
}

int main(int argc, char const *argv[]) {
  testAnimals();

  int n = 4;
  struct Animal* dogs = createNDogs(n);
  for (int i = 0; i < n; i++) {
    animalPrintGreeting(&dogs[i]);
    animalPrintMenu(&dogs[i]);
  }
  free(dogs);
  printf("\n");

  struct Animal dog = testHeapAndStack();

  struct Animal cat;
  constructCat(&cat, "Macak 1");

  animalPrintGreeting(&dog);
  animalPrintGreeting(&cat);

  animalPrintMenu(&dog);
  animalPrintMenu(&cat);

  return 0;
}
