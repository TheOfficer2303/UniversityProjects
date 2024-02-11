import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Recursion2 {
    private int n;
    private double[] input;
    private ArrayList<Double> solutions;
    private double[] conds;

    public Recursion2(int n, double[] input, int[] conds, ArrayList<Double> solutions) {
        this.n = n;
        this.conds = new double[n + 1];
        this.input = input;
        this.solutions = solutions;
        for (int i = 0; i < conds.length; i++) {
            this.conds[i] = conds[i];
        }
    }

    public double recurrence(int n) {
        if (n == 0) {
            return  conds[0];
        } else if (n == 1) {
            return  conds[1];
        } else if (n == 2) {
            return  conds[2];
        } else {
            conds[n] = solutions.get(0) * recurrence(n - 1) + solutions.get(1) * recurrence(n - 2) +
                    solutions.get(2) * recurrence(n - 3);

            return conds[n];
        }

    }
}


