This program simulates a Pushdown Automaton which accepts its input by final state.
For its definition it takes input like this:
1st row: input strings seperated with |. Symbols of every input string are separated with comma
2nd row: States set separated with comma
3rd row: Input symbols set separated with comma
4th row: Stack symbols set separated with comma
5th row: Acceptable states set separated with comma
6th row: Starting state
7th row: Starting stack symbol
8th row and others: Transitions

Transition should look like this: currentState,inputSymbol,stackSymbol->newState,newStackSymbols
