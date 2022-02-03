import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class LeksickiAnalizator {
    public static void main(String[] args) throws IOException {
        File file = new File("C:\\Users\\blazb\\Desktop\\zadatak.txt");

        Scanner scanner = new Scanner(file);
        int noOfRow = 1;
        StringBuilder print = new StringBuilder();

        String input = "";

        while (scanner.hasNextLine()) {
            input = scanner.nextLine();
            String[] inputChars = input.split("");

            int index = 0;
            while (index < inputChars.length && inputChars[index].equals(" ")) {
                ++index;
            }
            input = input.substring(index);

            if (input.isBlank() || input.startsWith("//")) {
                ++noOfRow;
                continue;
            }
            String toAppend = analyze(input, noOfRow);
            print.append(toAppend);

            ++noOfRow;
        }
        FileWriter writer = new FileWriter("C:\\Users\\blazb\\Desktop\\moje.txt");
        writer.write(String.valueOf(print));
        writer.close();
        System.out.println(print);
    }

    private static String analyze(String stringForCheck, int noOfRow) {
        String[] op = {"+", "-", "*", "/", "=", "(", ")"};
        String[] kw = {"za", "az", "od", "do"};
        List<String> operators = Arrays.asList(op);
        List<String> keywords = Arrays.asList(kw);

        StringBuilder retPrint = new StringBuilder();

        String[] splitted = stringForCheck.split("");
        int index = 0;

        while (index < splitted.length) {
            String toAppend = "";
            if (Character.isLetter(splitted[index].toCharArray()[0])) {
                toAppend += splitted[index];
                ++index;
                while (index < splitted.length && !operators.contains(splitted[index]) && !splitted[index].equals(" ")) {
                    toAppend += splitted[index];
                    ++index;
                }
                if (index < splitted.length && splitted[index].equals(" ")) {
                    ++index;
                }
                if (keywords.contains(toAppend)) {
                    retPrint.append(detectKeyword(toAppend, noOfRow));
                } else {
                    retPrint.append("IDN ").append(noOfRow).append(" ").append(toAppend.trim()).append("\n");
                }


            } else if (Character.isDigit(splitted[index].toCharArray()[0])) {
                toAppend += splitted[index];
                ++index;
                while (index < splitted.length && Character.isDigit(splitted[index].toCharArray()[0])) {
                    toAppend += splitted[index];
                    ++index;
                }
                retPrint.append("BROJ ").append(noOfRow).append(" ").append(toAppend.trim()).append("\n");
            } else if (operators.contains(splitted[index])) {
                if ((index + 1) < splitted.length &&  splitted[index].equals("/")) {
                    if (splitted[index + 1].equals("/")) {
                        break;
                    }
                }
                retPrint.append(detectOperator(splitted[index], noOfRow));
                ++index;
            } else {
                ++index;
            }
        }

        return retPrint.toString();
    }

    private static StringBuilder detectKeyword(String keyword, int noOfRow) {
        StringBuilder retPrint = new StringBuilder();

        String toAppend = "KR_" + keyword.toUpperCase() + " ";
        return retPrint.append(toAppend).append(noOfRow).append(" ").append(keyword).append("\n");

    }

    private static StringBuilder detectOperator(String operator, int noOfRow) {
        StringBuilder retPrint = new StringBuilder();
        Map<String, String> operators = new HashMap<>();
        operators.put("+", "OP_PLUS ");
        operators.put("-", "OP_MINUS ");
        operators.put("*", "OP_PUTA ");
        operators.put("/", "OP_DIJELI ");
        operators.put(")", "D_ZAGRADA ");
        operators.put("(", "L_ZAGRADA ");

        return retPrint.append(operators.get(operator)).append(noOfRow).append(" ").append(operator).append("\n");
    }
}
