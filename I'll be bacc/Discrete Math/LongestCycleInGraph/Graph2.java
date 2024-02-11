import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;

public class Graph2 {
    private int size;
    private TreeSet<Integer> adj[];
    private ArrayList<ArrayList<Integer>> edges = new ArrayList<>();
    ArrayList<ArrayList<Integer>> cycles = new ArrayList<>();
    private int maxCycleLength = 0;

    Graph2(int v, int matrix[][]) {
        size = v;
        adj = new TreeSet[v];

        for (int i = 0; i < v; ++i) {
            adj[i] = new TreeSet<>();
        }
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                if (matrix[i][j] == 1) {
                    addEdge(i, j);
                }
            }
        }
    }


    public void addEdge(int i, int j) {
        List<Integer> edge = Arrays.asList(i + 1, j + 1);
        Collections.sort(edge);

        if (edges.isEmpty()) {
            edges.add(new ArrayList<>(edge));
            return;
        }

        for (var e : edges) {
            if (e.get(0) == (edge.get(0)) && e.get(1) == (edge.get(1))) {
                return;
            }
        }
        edges.add(new ArrayList<>(edge));
    }

    public void printCycles() {
        for (var c : cycles) {
            System.out.println(c);
        }
    }

    public int getMaxCycleLength() {
        return maxCycleLength;
    }

    public void printEdges() {
        for (var e : edges) {
            System.out.println(e);
        }
    }

    public void search(ArrayList<Integer> list) {
        int start = list.get(0);

        for (var e : edges) {
            int v1 = e.get(0);
            int v2 = e.get(1);

            if (e.contains(start)) {
                int next;
                if (v1 != start)
                    next = v1;
                else {
                    next = v2;
                }

                if (!list.contains(next)) {
                    ArrayList<Integer> sublist = new ArrayList<>(list);
                    sublist.add(0, next);
                    search(sublist);
                } else if (list.size() > 2 && list.get(list.size() - 1) == next) {
                    cycles.add(list);

                    if(list.size() > maxCycleLength) maxCycleLength = list.size();
                }
            }

        }
    }


    public static int[][] readMatrix(String input) throws FileNotFoundException {
        ArrayList<ArrayList<Integer>> a = new ArrayList<ArrayList<Integer>>();
        ArrayList<Integer> col = new ArrayList<>();

        Scanner sc = new Scanner((new FileReader(input)));
        int n = Integer.parseInt(sc.nextLine());
        sc.nextLine();
        int[][] myArray = new int[n][n];
        while (sc.hasNextLine()) {
            for (int i = 0; i < myArray.length; i++) {
                String[] line = sc.nextLine().trim().split(" ");
                for (int j = 0; j < line.length; j++) {
                    myArray[i][j] = Integer.parseInt(line[j]);
                }
            }
        }
        return myArray;
    }




}

