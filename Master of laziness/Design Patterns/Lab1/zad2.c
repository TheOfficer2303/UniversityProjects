#include <stdio.h>
#include <stdlib.h>

typedef double (*PTRFUN)();

struct UnaryFunction {
  struct UnaryFunctionTable* vtable;
  int lower_bound;
  int upper_bound;
};

struct UnaryFunctionTable {
  PTRFUN value_at;
  PTRFUN negative_value_at;
};

double negative_value_at(double x, struct UnaryFunction* uf) {
  return uf->vtable->value_at(x, uf) * -1;
}

void tabulate(struct UnaryFunction* uf) {
  for(int x = uf->lower_bound; x <= uf->upper_bound; x++) {
    double value = uf->vtable->value_at((double)x, uf);
    printf("f(%d)=%lf\n", x, value);
  }
}

int same_functions_for_ints(struct UnaryFunction *f1, struct UnaryFunction *f2, double tolerance) {
  if(f1->lower_bound != f2->lower_bound) return 0;
  if(f1->upper_bound != f2->upper_bound) return 0;

  for(int x = f1->lower_bound; x <= f1->upper_bound; x++) {
    double delta = f1->vtable->value_at((double)x, f1) - f2->vtable->value_at((double)x, f2);
    if(delta < 0) delta = -delta;
    if(delta > tolerance) return 0;
  }

  return 1;
}

struct UnaryFunctionTable unaryFunctionTable = {
    NULL,
    &negative_value_at,
};


void constructUnaryFunction(struct UnaryFunction* fn, int lower_bound, int upper_bound, struct UnaryFunctionTable* vtable) {
    fn->lower_bound = lower_bound;
    fn->upper_bound = upper_bound;
    fn->vtable = vtable;
}

struct UnaryFunction* createUnaryFunction(int lower_bound, int upper_bound) {
    struct UnaryFunction* fn = malloc(sizeof(struct UnaryFunction));

    constructUnaryFunction(fn, lower_bound, upper_bound, &unaryFunctionTable);

    return fn;
}

//LINEAR
struct Linear {
  struct UnaryFunctionTable* vtable;
  int lower_bound;
  int upper_bound;
  double a;
  double b;
};

struct LinearTable {
  PTRFUN linear_value_at;
  PTRFUN negative_value_at;
};

double linear_value_at(double x, struct Linear* linear) {
    return linear->a * x + linear->b;
}

struct UnaryFunctionTable linearFunctionTable = {
  &linear_value_at,
  &negative_value_at
};

struct Linear* createLinear(int lb, int ub, double a, double b) {
  struct Linear* linear = malloc(sizeof(struct Linear));

  constructUnaryFunction((struct UnaryFunction*) linear, lb, ub, &linearFunctionTable);
  linear->a = a;
  linear->b = b;

  return linear;
}
//END LINEAR

//SQUARE
struct Square {
  struct UnaryFunctionTable* vtable;
  int lower_bound;
  int upper_bound;
};

struct SquareTable {
  PTRFUN square_value_at;
  PTRFUN negative_value_at;
};

double square_value_at(double x, struct Square* square) {
  return x*x;
}

struct UnaryFunctionTable squareFunctionTable = {
  &square_value_at,
  &negative_value_at
};

struct Square* createSquare(int lb, int ub) {
  struct Square* square = malloc(sizeof(struct Square));

  constructUnaryFunction((struct UnaryFunction*) square, lb, ub, &squareFunctionTable);

  return square;
}
//END SQUARE

int main(int argc, char const *argv[]) {
    struct Square* f1 = createSquare(-2, 2);
    tabulate((struct UnaryFunction*)f1);

    struct Linear* f2 = createLinear(-2, 2, 5, -2);
    tabulate((struct UnaryFunction*)f2);

    printf("f1==f2: %s\n", same_functions_for_ints((struct UnaryFunction*)f1, (struct UnaryFunction*)f2, 1E-6) == 1 ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", f2->vtable->negative_value_at(1.0, f2));

    free(f1);
    free(f2);

    return 0;
}
