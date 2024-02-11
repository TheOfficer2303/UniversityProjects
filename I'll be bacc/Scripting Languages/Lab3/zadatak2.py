import argparse
import sys


def print_hypotheses(hypotheses):
    print("Hyp#Q10#Q20#Q30#Q40#Q50#Q60#Q70#Q80#Q90")

    for hypothesis_number, hypothesis in enumerate(hypotheses, start=1):
        quantiles = [str(hypothesis[(int(x / 10 * len(hypothesis))) - 1]) for x in range(1, 10)]

        print("{:03d}#{}".format(hypothesis_number, "#".join(quantiles)))


def read_hypotheses_from_file(file_path):
    with open(file_path, "r") as file:
        hypotheses = []

        for line in file:
            hypothesis = sorted(float(x) for x in line.strip().split(" "))
            hypotheses.append(hypothesis)

    return hypotheses


def main():
    if len(sys.argv) != 2:
        print("Wrong number of parameters")
        exit(0)
    hypotheses_file = sys.argv[1]
    hypotheses = read_hypotheses_from_file(hypotheses_file)
    print_hypotheses(hypotheses)


if __name__ == "__main__":
    main()
