This program simulates a Pushdown Automaton which accepts its input by final state.
For its definition it takes input like this:

1. row: input strings seperated with |. Symbols of every input string are separated with comma
2. row: States set separated with comma
3. row: Input symbols set separated with comma
4. row: Stack symbols set separated with comma
5. row: Acceptable states set separated with comma
6. row: Starting state
7. row: Starting stack symbol
8. row and others: Transitions

Transition should look like this: currentState,inputSymbol,stackSymbol->newState,newStackSymbols
