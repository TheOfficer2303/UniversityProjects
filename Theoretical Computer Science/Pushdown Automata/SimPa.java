import java.util.*;

public class SimPa {
    public static void main(String[] args) {
        DPA dpa = new DPA();
    }
}


class DPA {
    private List<String> inputStrings;
    List<List<String>> inputString = new ArrayList<>();
    private Set<String> states;
    private Set<String> symbols;
    private List<String> stackSymbols;
    private Set<String> acceptableStates;
    private String startingState;
    private char startingStackSymbol;
    //    private List<String> stack;
    private Map<String, String> transitions = new HashMap<>();


    DPA() {
        scanInput();
        calculate();
    }

    private void scanInput() {
        //input strings
        Scanner scanner = new Scanner(System.in);
        inputStrings = new ArrayList<>(Arrays.asList(scanner.nextLine().split("\\|")));

        for (String string : inputStrings) {
            inputString.add(Arrays.asList(string.split(",")));
        }

        //states
        String line = scanner.nextLine();
        states = new TreeSet<>(Arrays.asList(line.split(",")));

        //symbols
        line = scanner.nextLine();
        symbols = new TreeSet<>(Arrays.asList(line.split(",")));

        //stack symbols
        line = scanner.nextLine();
        stackSymbols = new ArrayList<>(Arrays.asList(line.split(",")));

        //acceptable states
        line = scanner.nextLine();
        acceptableStates = new TreeSet<>(Arrays.asList(line.split(",")));

        //starting state
        startingState = scanner.nextLine();

        //starting stack symbol
        startingStackSymbol = scanner.nextLine().charAt(0);

        //transitions
        while (scanner.hasNextLine() && !(line = scanner.nextLine()).isEmpty()) {
            String[] splitted = line.split("->");
            String key = splitted[0];
            String value = splitted[1];
            transitions.put(key, value);
        }
    }

    private void calculate() {
        String currentState = startingState;
        StringBuilder output = new StringBuilder(currentState + "#");
        output.append(startingStackSymbol);
        Stack<Character> pdaStack = new Stack<>();
        pdaStack.push(startingStackSymbol);

        outer:
        for (List<String> substring : inputString) {
            for (String symbol : substring) {
                if (!pdaStack.isEmpty()) {
                    currentState = checkEpsilon(currentState, output, pdaStack);
                    if (pdaStack.isEmpty()) {
                        output.append("|fail|0");
                        System.out.println(output);
                        currentState = startingState;
                        output = new StringBuilder(currentState + "#");
                        output.append(startingStackSymbol);
                        pdaStack.clear();
                        pdaStack.add(startingStackSymbol);
                        continue outer;
                    }
                } else {
                    output.append("|fail|0");
                    System.out.println(output);
                    currentState = startingState;
                    output = new StringBuilder(currentState + "#");
                    output.append(startingStackSymbol);
                    pdaStack.clear();
                    pdaStack.add(startingStackSymbol);
                    continue outer;
                }

                String stackTop = pdaStack.pop().toString();
                String transKey = currentState + "," + symbol + "," + stackTop;

                if (transitions.containsKey(transKey)) {
                    currentState = transitions.get(transKey).split(",")[0];


                    stackTop = transitions.get(transKey).split(",")[1];

                    StringBuilder temp = new StringBuilder(stackTop).reverse();
                    for (int i = 0; i < temp.length(); i++) {
                        if (temp.toString().equals("$"))
                            continue;
                        pdaStack.push(temp.charAt(i));

                    }

                    stackTop = pdaStack.peek().toString();

                    if (!pdaStack.isEmpty()) {
                        output.append("|" + currentState + "#");
                        for (int i = pdaStack.size() - 1; i >= 0; i--) {
                            output.append(pdaStack.get(i));
                        }

                    } else {
                        output.append("|" + currentState + "#$");
                    }

                } else {
                    output.append("|fail|0");
                    System.out.println(output);
                    currentState = startingState;
                    output = new StringBuilder(currentState + "#");
                    output.append(startingStackSymbol);
                    pdaStack.clear();
                    pdaStack.add(startingStackSymbol);
                    continue outer;
                }

                if (!pdaStack.isEmpty() && !acceptableStates.contains(currentState))
                    currentState = checkEpsilon(currentState, output, pdaStack);
            }
            if (acceptableStates.contains(currentState)) {
                output.append("|1");
            } else {
                output.append("|0");

            }
            System.out.println(output);
            currentState = startingState;
            output = new StringBuilder(currentState + "#");
            output.append(startingStackSymbol);
            pdaStack.clear();
            pdaStack.add(startingStackSymbol);
        }


    }


    private String checkEpsilon(String currentState, StringBuilder output, Stack<Character> pdaStack) {
        String firstCurState = currentState;
        String stackTop = pdaStack.peek().toString();
        String firstStackTop = stackTop;
        String transKey = currentState + ",$," + stackTop;

        if (transitions.containsKey(transKey)) {
            pdaStack.pop();
            currentState = transitions.get(transKey).split(",")[0];


            stackTop = transitions.get(transKey).split(",")[1];


            StringBuilder temp = new StringBuilder(stackTop).reverse();
            for (int i = 0; i < temp.length(); i++) {
                if (temp.toString().equals("$")) {
                    continue;
                }
                pdaStack.push(temp.charAt(i));
            }





            if (!pdaStack.isEmpty()) {
                stackTop = pdaStack.peek().toString();
                output.append("|" + currentState + "#");
                for (int i = pdaStack.size() - 1; i >= 0; i--) {
                    output.append(pdaStack.get(i));
                }


            } else {
                output.append("|" + currentState + "#$");
            }

            if (!pdaStack.isEmpty() && (!currentState.equals(firstCurState) || !firstStackTop.equals(stackTop)) && !acceptableStates.contains(currentState))
                currentState = checkEpsilon(currentState, output, pdaStack);

        } else {
            return currentState;
        }

        return currentState;


    }


}
