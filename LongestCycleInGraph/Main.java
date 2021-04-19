import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) throws FileNotFoundException {
        Scanner sc = new Scanner(System.in);

        System.out.println("Complete name of input file: ");
        String input = sc.nextLine();
        int[][] matrix = Graph2.readMatrix(input);


        Graph2 G = new Graph2(matrix.length, matrix);
        System.out.println("All edges:");
        G.printEdges();

        for (int v = 1; v <= matrix.length; v++) {
            G.search(new ArrayList<>(Arrays.asList(v)));
        }

        System.out.println("All cycles:");
        G.printCycles();

        System.out.println("Longest cycle length: " + G.getMaxCycleLength());
    }
}
