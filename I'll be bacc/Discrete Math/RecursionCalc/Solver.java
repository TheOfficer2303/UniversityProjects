import java.util.ArrayList;

public class Solver {
    private double[][] matrix;
    private ArrayList<Double> solutions;


    public Solver(double[][] matrix) {
        this.matrix = matrix;
    }

    public void solve() {
        row(3, this.matrix);
        solutions = saveSolutions();
    }


    public static void row(int n, double[][] matrix) {   // dijeli matricu s vodećim članom kako bi dobili jedinice na dijagonali
        for (int i = 0; i < n; ++i) {
            double mainNum = matrix[i][i];
            if (mainNum != 0) {
                for (int j = 0; j < n + 1; j++) {
                    matrix[i][j] /= mainNum;
                }
            }
            column(n, matrix);
        }
    }

    public static void column(int n, double[][] matrix) {    //stupce s vodećim članom postavlja u nule
        for (int i = 0; i < n; i++) {              //moramo ici 2x po svakom retku kako bi izbjegli unistavanje vodećeg člana
            for (int j = 0; j < n; j++) {
                if (j != i) {                       //ovdje osiguravamo prethodni komentar
                    double mainNum = matrix[j][i];

                    for (int k = 0; k < n + 1; k++) {
                        matrix[j][k] -= mainNum * matrix[i][k];

                    }
                }
            }
        }
    }

    public ArrayList<Double> saveSolutions() {
        ArrayList<Double> ret = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
           ret.add(matrix[i][3]);
        }
        return ret;
    }

    public void printSolutions() {
        for (int i = 0; i < 3; i++) {
            System.out.println("λ" + (i + 1) + " = " + solutions.get(i));
        }
    }

    public ArrayList<Double> getSolutions() {
        return solutions;
    }

}
