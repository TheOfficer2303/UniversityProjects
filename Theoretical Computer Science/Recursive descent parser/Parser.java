import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class Parser {
    private static Queue<Character> queue = new LinkedList<>();
    private static String input;

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        String line = scanner.nextLine();

        for (int i = 0; i < line.length(); i++) {
            queue.add(line.charAt(i));
        }

        readInput();
        S();

        if (!input.equals(" ")) {
            stop("\nNE\n");
        } else {
            System.out.print("\nDA\n");
        }
    }

    private static void S() {
        System.out.print("S");

        switch (input) {
            case "a":
                readInput();
                A();
                B();
                break;

            case "b":
                readInput();
                B();
                A();
                break;
            case " ":
                stop("\nDA\n");
                break;
            default:
                stop("\nNE\n");
                break;
        }
    }

    private static void A() {
        System.out.print("A");

        switch (input) {
            case "b":
                readInput();
                C();
                break;

            case "a":
                readInput();
                break;
            default:
                stop("\nNE\n");
                break;
        }
    }

    private static void B() {
        System.out.print("B");

        if (input.equals("c")) {
            readInput();
            if (!input.equals("c")) {
                stop("\nNE\n");
            }

            readInput();
            S();

            if (!input.equals("b")) {
                stop("\nNE\n");
            }
            readInput();

            if (!input.equals("c")) {
                stop("\nNE\n");
            }

            readInput();
        }
    }

    private static void C() {
        System.out.print("C");
        A();
        A();
    }

    private static void readInput() {
        if (queue.size() > 0) {
            input = queue.remove().toString();
        } else {
            input = " ";
        }
    }

    private static void stop(String s) {
        System.out.print(s);
        System.exit(1);
    }
}
