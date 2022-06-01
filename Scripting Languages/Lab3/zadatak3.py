import argparse
import os
import re
import sys
from typing import Tuple, Dict


def print_scores(students_dict: Dict[str, Tuple[str, str]], scores_dict: Dict[Tuple[str, str], str]) -> None:
    print("{:15s}{:40s}{:8s}{:8s}{:8s}".format("JMBAG", "Prezime, Ime", "L1", "L2", "L3"))

    for jmbag, first_and_last_name in students_dict.items():
        first_name, last_name = first_and_last_name

        print("{:15s}{:40s}{:8s}{:8s}{:8s}".format(
            jmbag,
            "{}, {}".format(last_name, first_name),
            "{:.1f}".format(float(scores_dict[(jmbag, "LAB1")])) if (jmbag, "LAB1") in scores_dict else "-",
            "{:.1f}".format(float(scores_dict[(jmbag, "LAB2")])) if (jmbag, "LAB2") in scores_dict else "-",
            "{:.1f}".format(float(scores_dict[(jmbag, "LAB3")])) if (jmbag, "LAB3") in scores_dict else "-"
        ))


def read_file_in_directory(directory: str) -> (Dict[str, Tuple[str, str]], Dict[Tuple[str, str], str]):
    file_names = os.listdir(directory)
    students_dict = {}
    scores_dict = {}

    for file_name in file_names:
        file_path = "{}/{}".format(directory, file_name)

        if file_name == "studenti.txt":
            with open(file_path, "r") as students_file:
                for line in students_file:
                    jmbag, first_name, last_name = line.strip().split(" ")
                    students_dict[jmbag] = (first_name, last_name)

            continue

        with open(file_path, "r") as students_file:
            result = re.search(r"LAB_(\d+)_g\d+.txt", file_name, flags=re.I)
            lab_index = result.group(1).lstrip("0")
            lab_name = "{}{}".format("LAB", lab_index)

            for line in students_file:
                jmbag, score = line.strip().split(" ")
                if (jmbag, lab_name) in scores_dict:
                    print("WARNING: Student {} already has score for {}".format(jmbag, lab_name))
                scores_dict[(jmbag, lab_name)] = score

    return students_dict, scores_dict


def main():
    directory = sys.argv[2]
    students_dict, scores_dict = read_file_in_directory(directory)
    print_scores(students_dict, scores_dict)


if __name__ == "__main__":
    main()
