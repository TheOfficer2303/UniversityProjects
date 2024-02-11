#include <stdio.h>

class CoolClass {
public:
  virtual void set(int x){x_=x;};
  virtual int get(){return x_;};
private:
  int x_;
};

class PlainOldClass {
public:
  void set(int x){x_=x;};
  int get(){return x_;};
private:
  int x_;
};

int main(int argc, char const *argv[])
{
  printf("%d\n", sizeof(CoolClass));
  printf("%d", sizeof(PlainOldClass));
  return 0;
}
