This program simulates a Pushdown Automaton which accepts its input by final state.
For its definition it takes input like this:
1. row: all states
2. row: all symbols
3. row: acceptable states
4. row: initial state
5. row to end: transitions

1. row: input strings seperated with |. Symbols of every input string are separated with comma
2. row: States set separated with comma
3. redak: Input symbols set separated with comma
4. redak: Stack symbols set separated with comma
5. redak: Acceptable states set separated with comma
6. redak: Starting state
7. redak: Starting stack symbol
8. row and others: Transitions

Transition should look like this: currentState,inputSymbol,stackSymbol->newState,newStackSymbols
