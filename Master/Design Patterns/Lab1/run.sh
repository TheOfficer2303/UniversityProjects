gcc --target=i386 -fno-asynchronous-unwind-tables -S -masm=intel -S proba.c

gcc -arch=pentium -fno-asynchronous-unwind-tables -S -masm=intel -S proba.c
