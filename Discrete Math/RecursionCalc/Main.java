import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        double[] input = solutionsInput(sc);
        int[] conds = conditionsInput(sc);

        int n = nInput(sc);

        solveByFormula(n, input, conds);
        solveByRecurrences(n, input, conds);
    }

    public static void solveByRecurrences(int n, double[] input, int[] conds) {
        double[][] matrix = generateEquation2(input);

        Solver solver = new Solver(matrix);
        solver.solve();

        ArrayList<Double> solutions = solver.getSolutions();

        Recursion2 recursion2 = new Recursion2(n, input, conds, solutions);
        System.out.printf("Vrijednost n-tog clana niza iz rekurzije: %.2f\n", recursion2.recurrence(n));
//        System.out.println(" " +  recursion2.recurrence(n));
    }

    public static void solveByFormula(int n, double[] input, int[] conds) {
        double[][] matrix = generateEquation1(input, conds);

        Solver solver = new Solver(matrix);
        solver.solve();

        ArrayList<Double> solutions = solver.getSolutions();

        Recursion1 recursion1 = new Recursion1(n, input, solutions);
        System.out.printf("Vrijednost n-tog clana niza pomocu formule: %.2f\n", recursion1.getNumber());
//        System.out.println("Vrijednost n-tog clana niza pomocu formule: " +  recursion1.getNumber());
    }

    public static double[][] generateEquation1(double[] input, int[] conds) {
        double[][] matrix = new double[3][4];

        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3 + 1; j++) {
                if (j != 3) {
                    matrix[i][j] = Math.pow(input[j], i);
                } else {
                    matrix[i][j] = conds[i];
                }
            }
        }

        return matrix;
    }

    public static double[][] generateEquation2(double[] input) {
        double[][] matrix;

        matrix = new double[][]{{Math.pow(input[0], 2), Math.pow(input[0], 1), Math.pow(input[0], 0), Math.pow(input[0], 3)}, {Math.pow(input[1], 2), Math.pow(input[1], 1), Math.pow(input[1], 0), Math.pow(input[1], 3)},
                {Math.pow(input[2], 2), Math.pow(input[2], 1), Math.pow(input[2], 0), Math.pow(input[2], 3)}
        };

        return matrix;
    }


    public static double[] solutionsInput(Scanner sc) {
        double[] ret = new double[3];
        String[] card = new String[]{"prvo", "drugo", "trece"};

        for (int i = 0; i < 3; i++) {
            System.out.print("Unesite " + card[i] +  " rjesenje x1 karakteristicne jednadzbe: ");
            ret[i] = sc.nextDouble();
        }

        return ret;
    }

    public static int[] conditionsInput(Scanner sc) {
        int[] ret = new int[3];
        String[] card = new String[]{"nultog", "prvog", "drugog"};

        for (int i = 0; i < 3; i++) {
            System.out.print("Unesite vrijednost " + card[i] +  " clana niza: ");
            ret[i] = sc.nextInt();
        }

        return ret;
    }

    public static int nInput(Scanner sc) {
        System.out.print("Unesite redni broj n trazenog clana niza: ");
        return sc.nextInt();
    }
}
