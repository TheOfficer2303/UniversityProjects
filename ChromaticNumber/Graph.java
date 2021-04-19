import java.util.*;

public class Graph {
    private final int size;
    private final int[][] matrix;

    private ArrayList<Integer>[] adjacencyVerteces;
    private int[] colors;
    private Set<Integer> colored = new TreeSet<>();                  // obojani vrhovi

    public int[] getColors() {
        return colors;
    }

    public int getSize() {
        return size;
    }

    public Set<Integer> getColored() {
        return colored;
    }

    Graph(int v, int matrix[][]) {
        size = v;
        colors = new int[v];
        adjacencyVerteces = new ArrayList[size];
        this.matrix = matrix;

        for (int i = 0; i < v; i++) {
            adjacencyVerteces[i] = new ArrayList<Integer>();
        }

    }

    public void makeAdjacency() {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix.length; j++) {
                if (matrix[i][j] == 1) {
                    adjacencyVerteces[i].add(j);
                }
            }
        }
    }

    public void findChromaticNumber(int v) {

        if (colored.size() == size) {
            return;
        }

        if (!colored.contains(v)) {
            colors[v] = 1;
            colored.add(v);
        }

        for (int adjVert : adjacencyVerteces[v]) {
            Set<Integer> unavailableColors = new TreeSet<>();
            if (!colored.contains(adjVert)) {

                for (int adjVert2 : adjacencyVerteces[adjVert]) {
                    unavailableColors.add(colors[adjVert2]);
                }

                for (int j = 1; j <= this.size; j++) {
                    if (!unavailableColors.contains(j)) {
                        colors[adjVert] = j;
                        colored.add(adjVert);
                        break;
                    }
                }
            }
        }

        for (int adjVert: adjacencyVerteces[v]) {
            if (adjVert != v) {
                for (int adjVert2 : adjacencyVerteces[adjVert]) {
                    if (!colored.contains(adjVert2)) {
                        findChromaticNumber(adjVert);
                    }
                }
            }
        }
    }

 public static int largest(int[] arr) {
        int i;

        int max = arr[0];

        for (i = 1; i < arr.length; i++)
            if (arr[i] > max)
                max = arr[i];

        return max;
    }
}

