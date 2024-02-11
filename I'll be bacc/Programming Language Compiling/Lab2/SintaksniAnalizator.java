import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class SintaksniAnalizator {
    private static Queue<String> queue = new LinkedList<>();
    private static String input;
    private static String temp;
    private static StringBuilder toPrint = new StringBuilder();

    private static final List<String> programPrimijeni = Arrays.asList("IDN", "KR_ZA", "");

    private static final List<String> listaNaredbiPrimijeni1 = Arrays.asList("IDN", "KR_ZA");
    private static final List<String> listaNaredbiPrimijeni2 = Arrays.asList("KR_AZ", "");

    private static final List<String> naredbaPrimijeni1 = Collections.singletonList("IDN");
    private static final List<String> naredbaPrimijeni2 = Arrays.asList("KR_ZA", "");

    private static final List<String> pridruzivanjePrimijeni = Collections.singletonList("IDN");
    private static final List<String> petljaPrimijeni = Collections.singletonList("KR_ZA");

    private static final List<String> EPrimijeni = Arrays.asList("IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA");
    private static final List<String> TPrimijeni = Arrays.asList("IDN", "BROJ", "OP_PLUS", "OP_MINUS", "L_ZAGRADA");

    private static final List<String> EListaPrimijeni1 = Collections.singletonList("OP_PLUS");
    private static final List<String> EListaPrimijeni2 = Collections.singletonList("OP_MINUS");
    private static final List<String> EListaPrimijeni3 = Arrays.asList("IDN", "KR_ZA", "KR_DO", "KR_AZ", "D_ZAGRADA", "");

    private static final List<String> TListaPrimijeni1 = Collections.singletonList("OP_PUTA");
    private static final List<String> TListaPrimijeni2 = Collections.singletonList("OP_DIJELI");
    private static final List<String> TListaPrimijeni3 = Arrays.asList("IDN", "KR_ZA", "KR_DO", "KR_AZ", "OP_PLUS", "OP_MINUS", "D_ZAGRADA", "");

    private static final List<String> PPrimijeni1 = Arrays.asList("OP_PLUS");
    private static final List<String> PPrimijeni2 = Arrays.asList("OP_MINUS");
    private static final List<String> PPrimijeni3 = Arrays.asList("L_ZAGRADA");
    private static final List<String> PPrimijeni4 = Arrays.asList("IDN");
    private static final List<String> PPrimijeni5 = Arrays.asList("BROJ");

    public static void main(String[] args) throws IOException {
        String line = "";
//        Scanner sc = new Scanner(System.in);
//        while (sc.hasNextLine() && !(line = sc.nextLine()).equals("!")) {
//            queue.add(line);
//        }

        File file = new File("C:\\Users\\blazb\\Desktop\\zadatak.txt");
        Scanner sc = new Scanner(file);
        while (sc.hasNextLine()) {
            queue.add(sc.nextLine());
        }

        int indentation = 0;
        readInput();
        if (programPrimijeni.contains(input)) {
            append(indentation, "<program>\n");
            program(indentation);
        } else {
            exit();
        }
        FileWriter writer = new FileWriter("C:\\Users\\blazb\\Desktop\\moje.txt");
        writer.write(String.valueOf(toPrint.toString().trim()));
        writer.close();
        System.out.println(toPrint.toString().trim());

    }

    public static void program(int i) {
        isInListaNaredbi(i);
    }

    private static void isInListaNaredbi(int i) {
        if (listaNaredbiPrimijeni1.contains(input)) {
            listaNaredbi1(++i);
        } else if (listaNaredbiPrimijeni2.contains(input)) {
            listaNaredbi2(++i);
        }
    }

    private static void listaNaredbi1(int i) {
        append(i, "<lista_naredbi>\n");

        if (naredbaPrimijeni1.contains(input)) {
            naredba1(i+1);
            isInListaNaredbi(i);
        } else if (naredbaPrimijeni2.contains(input)) {
            naredba2(i+1);
            isInListaNaredbi(i);
        } else {
            readInput();
        }
    }



    private static void listaNaredbi2(int i) {
        append(i, "<lista_naredbi>\n");
        append(i+1, "$\n");

    }

    private static void naredba1(int i) {
        append(i, "<naredba>\n");

        if (pridruzivanjePrimijeni.contains(input)) {
            pridruzivanje(++i);
        }
    }



    private static void naredba2(int i) {
        append(i, "<naredba>\n");

        if (petljaPrimijeni.contains(input)) {
            petlja(++i);
        }
    }

    private static void pridruzivanje(int i) {
        append(i, "<naredba_pridruzivanja>\n");

        if (!input.equals("IDN")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (!input.equals("OP_PRIDRUZI")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(++i);
        } else {
            exit();
        }
    }

    private static void petlja(int i) {
        append(i, "<za_petlja>\n");

        if (!input.equals("KR_ZA")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (!input.equals("IDN")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (!input.equals("KR_OD")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(i+1);
        } else {
            exit();
        }

        if (!input.equals("KR_DO")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(i+1);
        }

        isInListaNaredbi(i);

        if (!input.equals("KR_AZ")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
    }


    private static void E(int i) {
        append(i, "<E>\n");
        if (TPrimijeni.contains(input)) {
            T(i+1);
        }

        isInELista(i);
    }


    private static void isInELista(int i) {
        if (EListaPrimijeni1.contains(input)) {
            ELista1(++i);
        } else if (EListaPrimijeni2.contains(input)) {
            ELista2(++i);
        } else if (EListaPrimijeni3.contains(input)) {
            ELista3(++i);
        } else {
            exit();
        }
    }

    private static void ELista1(int i) {
        append(i, "<E_lista>\n");

        if (!input.equals("OP_PLUS")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(++i);
        }
    }

    private static void ELista2(int i) {
        append(i, "<E_lista>\n");

        if (!input.equals("OP_MINUS")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(++i);
        }
    }

    private static void ELista3(int i) {
        append(i, "<E_lista>\n");
        append(i+1, "$\n");
    }

    private static void T(int i) {
        append(i, "<T>\n");
        isInP(i);

        isInTLista(i);
    }

    private static void isInTLista(int i) {
        if (TListaPrimijeni1.contains(input)) {
            TLista1(++i);
        } else if (TListaPrimijeni2.contains(input)) {
            TLista2(++i);
        } else if (TListaPrimijeni3.contains(input)) {
            TLista3(++i);
        } else {
            exit();
        }
    }

    private static void TLista1(int i) {
        append(i, "<T_lista>\n");

        if (!input.equals("OP_PUTA")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (TPrimijeni.contains(input)) {
            T(++i);
        }
    }

    private static void TLista2(int i) {
        append(i, "<T_lista>\n");

        if (!input.equals("OP_DIJELI")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (TPrimijeni.contains(input)) {
            T(++i);
        }
    }

    private static void TLista3(int i) {
        append(i, "<T_lista>\n");
        append(i+1, "$\n");
    }

    private static void isInP(int i) {
        if (PPrimijeni1.contains(input)) {
            P1(++i);
        } else if (PPrimijeni2.contains(input)) {
            P2(++i);
        } else if (PPrimijeni3.contains(input)) {
            P3(++i);
        } else if (PPrimijeni4.contains(input)) {
            P4(++i);
        } else if (PPrimijeni5.contains(input)) {
            P5(++i);
        }
    }

    private static void P1(int i) {
        append(i, "<P>\n");

        if (!input.equals("OP_PLUS")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        isInP(i);
    }

    private static void P2(int i) {
        append(i, "<P>\n");

        if (!input.equals("OP_MINUS")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        isInP(i);
    }

    private static void P3(int i) {
        append(i, "<P>\n");

        if (!input.equals("L_ZAGRADA")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
        if (EPrimijeni.contains(input)) {
            E(i+1);
        }

        if (!input.equals("D_ZAGRADA")) {
            exit();
        }
        append(i+1, temp + "\n");
        readInput();
    }

    private static void P4(int i) {
        append(i, "<P>\n");

        if (!input.equals("IDN")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
    }

    private static void P5(int i) {
        append(i, "<P>\n");

        if (!input.equals("BROJ")) {
            exit();
        }
        append(i+1, temp + "\n");

        readInput();
    }

    public static void append(int i, String s) {
        toPrint.append(" ".repeat(Math.max(0, i)));
        toPrint.append(s);
    }

    public static void readInput() {
        if (queue.size() > 0) {
            temp = queue.remove();
            input = temp.split(" ")[0];
        } else {
            temp = "";
            input = "";
        }

    }

    private static void exit() {
        if (!temp.equals("")) {
            System.out.println("err " + temp);
        } else {
            System.out.println("err kraj");
        }

        System.exit(0);
    }
}
