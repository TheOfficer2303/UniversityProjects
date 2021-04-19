import java.io.FileNotFoundException;
import java.io.FileReader;
import java.util.*;

public class Main {

    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(System.in);

        System.out.println("Unesite naziv datoteke:");
        String input = sc.nextLine();

        int[][] matrix = null;
        List<Integer> bestWay = new ArrayList<>();


        matrix = readMatrix(input);

        for (int i = 0; i < matrix.length; i++) {
            Graph G = new Graph(matrix.length, matrix);
            G.makeAdjacency();

            for (int j = i; j < G.getSize() + i; j++) {
                if (j >= G.getSize()) {
                    j -= G.getSize();
                }
                G.findChromaticNumber(j);
                if (G.getColored().size() == G.getSize()) {

                    bestWay.add(Graph.largest(G.getColors()));
                    break;

                }
            }
            matrix = readMatrix(input);
        }

        System.out.println(Collections.min(bestWay));
    }
    
    

    public static int[][] readMatrix(String input) throws FileNotFoundException {
        ArrayList<ArrayList<Integer>> a = new ArrayList<>();
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
