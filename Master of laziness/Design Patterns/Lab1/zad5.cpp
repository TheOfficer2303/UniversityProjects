#include <cstdint>
#include <iostream>
using namespace std;

class B {
   public:
    virtual int prva() = 0;
    virtual int druga(int) = 0;
};

class D : public B {
   public:
    virtual int prva() {
        return 42;
    }
    virtual int druga(int x) {
        return prva() + x;
    }
};

typedef int (*PFUN1)(B*);
typedef int (*PFUN2)(B*, int);

void printReturnValues(B* pb) {
    size_t *vTable = *(size_t**) pb;

    PFUN1 fun1 = ((PFUN1) vTable[0]);
    PFUN2 fun2 = ((PFUN2) vTable[1]);

    printf("%d\n", fun1(pb));
    printf("%d\n", fun2(pb, 10));
}

int main(void) {
    D* pb = new D();
    printReturnValues(pb);
}
