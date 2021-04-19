import java.util.*;

public class DFA {
    private Set<String> startingStates;
    private Set<String> symbolSet;
    private Set<String> acceptableStates;
    private Set<Set<String>> finalStatesSet;
    private String startingState;
    private Map<String, Map<String, String>> transitionList = new TreeMap<>();

    public Map<String, Map<String, String>> getTransitionList() {
        return transitionList;
    }

    public DFA() {
        this.readInput();
        Set<String> unreachableStates = getUnreachableStates();
        startingStates.removeAll(unreachableStates);
        acceptableStates.removeAll(unreachableStates);
        finalStatesSet = this.minimization();
        merge();
        print();

    }

    private void print() {
        //states
        System.out.print(String.join(",", startingStates));
        System.out.println();

        //symbols
        System.out.print(String.join(",", symbolSet));
        System.out.println();

        //acceptable states
        System.out.println(String.join(",", acceptableStates));

        //starting state
        System.out.println(startingState);

        //transitions
        List<String> printLines = new ArrayList<>();
        for (String symbol : transitionList.keySet()) {
            Map<String, String> transition = transitionList.get(symbol);
            for (String state : transition.keySet()) {
                printLines.add(state + "," + symbol + "->" + transition.get(state));
            }
        }
        Collections.sort(printLines);
        for (String lajna : printLines) {
            System.out.println(lajna);
        }
    }

    private void merge() {
        finalStatesSet.removeIf(Set::isEmpty);
        Set<String> leadingStates = new TreeSet<>();
        Set<String> notLeadingStates = new TreeSet<>(startingStates);


        for (Set<String> identicalStates : finalStatesSet) {
            List<String> identicalStatesList = new ArrayList<>(identicalStates);
            leadingStates.add(identicalStatesList.get(0));
        }
        notLeadingStates.removeAll(leadingStates);


        //intersection between starting states and leading ones, i.e. those which have stayed after
        // the minimization
        startingStates.retainAll(leadingStates);
        acceptableStates.retainAll(leadingStates);

        //removing identical states
        for (String symbol : symbolSet) {
            for (String state : notLeadingStates) {
                transitionList.get(symbol).remove(state);
            }
        }

        //replacing identical states with leading ones
        for (String state : leadingStates) {
            for (String symbol : symbolSet) {
                String newState = null;
                if (transitionList.get(symbol).containsKey(state)) {
                    if (!leadingStates.contains(transitionList.get(symbol).get(state))) {
                        newState = getLeadingState(finalStatesSet, transitionList.get(symbol).get(state));
                        transitionList.get(symbol).replace(state, newState);
                    }
                }
            }
        }

        //replacing acceptable states and startin state with the leading ones
        for (String state : acceptableStates) {
            if (!leadingStates.contains(state))
                state = getLeadingState(finalStatesSet, state);
        }
        if (!leadingStates.contains(startingState)) {
            startingState = getLeadingState(finalStatesSet, startingState);
        }

    }

    private String getLeadingState(Set<Set<String>> finalStatesSet, String oldState) {
        String ret = null;
        for (Set<String> identicalStates : finalStatesSet) {
            List<String> identicalStatesList = new ArrayList<>(identicalStates);
            if (identicalStates.contains(oldState)) {
                ret = identicalStatesList.get(0);
            }
        }
        return ret;
    }


    private Set<Set<String>> minimization() {
        //partitioning on acceptable and non acceptable states
        Set<Set<String>> newGroups = new HashSet<>();

        Set<String> nonAcceptableStates = new TreeSet<>(startingStates);
        Set<String> helpAcceptable = new TreeSet<>(acceptableStates);

        nonAcceptableStates.removeAll(helpAcceptable);

        newGroups.add(helpAcceptable);
        newGroups.add(nonAcceptableStates);

        while (true) {
            ArrayList<Set<String>> newGroupsList = new ArrayList<>(newGroups);
            newGroups.clear();
            for (Set<String> group : newGroupsList) {
                Set<Set<String>> statePairs = makePairs(group);
                Set<String> nextGroup = new HashSet<>();

                for (Set<String> statePair : statePairs) {
                    int index1 = 0, index2 = 0;
                    List<String> statePairList = new ArrayList<>(statePair);
                    for (String symbol : symbolSet) {
                        String nextState1 = transitionList.get(symbol).get(statePairList.get(0));
                        String nextState2 = transitionList.get(symbol).get(statePairList.get(1));
                        for (int i = 0; i < newGroupsList.size(); i++) {
                            boolean set1 = false, set2 = false;
                            if (newGroupsList.get(i).contains(nextState1)) {
                                index1 = i;
                                set1 = true;
                            }
                            if (newGroupsList.get(i).contains(nextState2)) {
                                index2 = i;
                                set2 = true;
                            }
                            if (set1 && set2) break;
                        }
                        if (index1 != index2) {
                            nextGroup.add(statePairList.get(0));
                        }
                    }
                }
                if (!nextGroup.isEmpty())
                    newGroups.add(nextGroup);
                group.removeAll(nextGroup);
                newGroups.add(group);
            }
            Set<Set<String>> newest = new HashSet<>(newGroupsList);
            if (newGroups.equals(newest)) {
                break;
            }

        }
        return newGroups;
    }

    public Set<Set<String>> makePairs(Set<String> grupa) {
        Set<Set<String>> statePairs = new HashSet<>();

        for (String state1 : grupa) {
            for (String state2 : grupa) {
                Set<String> pair = new TreeSet<>();
                pair.add(state1);
                pair.add(state2);
                if (pair.size() == 2)
                    statePairs.add(pair);
            }
        }
        return statePairs;
    }


    public Set<String> getUnreachableStates() {
        Set<String> reachableStates = new TreeSet<>();
        Set<String> temp1 = new TreeSet<>();
        Set<String> temp2 = new TreeSet<>();
        Set<String> visited = new TreeSet<>();

        reachableStates.add(startingState);
        temp1.add(startingState);
        visited.add(startingState);


        while (true) {
            for (String state : temp1) {
                for (String symbol : symbolSet) {
                    String nextState = transitionList.get(symbol).get(state);
                    if (!visited.contains(nextState))
                        temp2.add(nextState);
                    visited.add(nextState);
                }
            }

            if (temp1.equals(temp2)) {
                break;
            } else {
                Set<String> addingList = new TreeSet<>(temp2);
                reachableStates.addAll(addingList);
                temp1 = new TreeSet<>(temp2);
                temp2.clear();
            }
        }

        Set<String> unreachableStates = new TreeSet<>(startingStates);
        unreachableStates.removeAll(reachableStates);

        //removing unreachable states from transition list
        for (String symbol : symbolSet) {
            for (String state : unreachableStates) {
                transitionList.get(symbol).remove(state);
            }
        }
        return unreachableStates;
    }


    public void readInput() {
        Scanner scanner = new Scanner(System.in);
        //states
        String line = scanner.nextLine();
        this.startingStates = new TreeSet<>(Arrays.asList(line.split(",")));

        //symbols
        line = scanner.nextLine();
        this.symbolSet = new TreeSet<>(Arrays.asList(line.split(",")));

        //acceptable states
        line = scanner.nextLine();
        this.acceptableStates = new TreeSet<>(Arrays.asList(line.split(",")));

        //starting state
        this.startingState = scanner.nextLine();

        //transitions
        this.transitionList = new TreeMap<>();

        while (scanner.hasNextLine() && !(line = scanner.nextLine()).isEmpty()) {

            String currentState = line.substring(0, line.indexOf(","));
            String symbol = line.substring(line.indexOf(",") + 1, line.indexOf("->"));
            String nextState = line.substring(line.indexOf(">") + 1);
            Map<String, String> transition = new TreeMap<>();

            if (transitionList.containsKey(symbol)) {
                transition = transitionList.get(symbol);
            }

            transition.put(currentState, nextState);
            transitionList.put(symbol, transition);
        }
    }

}
