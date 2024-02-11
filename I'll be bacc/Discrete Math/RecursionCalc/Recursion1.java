import java.util.ArrayList;
import java.util.Arrays;

public class Recursion1 {
    private int n;
    private double[] input;
    private ArrayList<Double> solutions;

    public Recursion1(int n, double[] input, ArrayList<Double> solutions) {
        this.n = n;
        this.input = Arrays.copyOf(input, input.length);
        this.solutions = solutions;
        for (int i = 0; i < this.input.length; i++) {
            this.input[i] = Math.pow(this.input[i], n);
        }
    }

    public double getNumber() {
        double number;
        number = solutions.get(0) * this.input[0] + solutions.get(1) * this.input[1] + solutions.get(2) * this.input[2];
        return number;
    }
}
