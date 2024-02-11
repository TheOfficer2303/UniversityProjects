This program simulates recursive descent parser for the following grammar:

S → aAB | bBA

A → bC | a

B → ccSbc | ϵ

C → AA

It prints "DA" on the end of the program if the input string is in a language defined by that grammar.
Otherwise it will print "NE".
