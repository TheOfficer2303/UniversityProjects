from Data_set import *
from Graph import *
from ID3 import *
import sys


def read_training_set(file_name):
    file = open(file_name)
    data = file.readlines()
    fn = data.pop(0).split(",")
    feature_names = [s.strip() for s in fn]

    features = tuple()
    possible_feature_values = dict()
    data_set_list = list()

    for line in data:
        words = line.split(",")
        features = (words[:-1], words[-1].strip())
        data_set_list.append(features)

        for i, word in enumerate(words):
            if len(possible_feature_values) != len(words):
                possible_feature_values[feature_names[i]] = set()

            possible_feature_values[feature_names[i]].add(word.strip())

    data_set = DataSet(data_set_list, possible_feature_values, feature_names)
    return data_set


def main():
    # train_file_name = "D:\\FAKS\\3. god\\UUI\\Labosi\\lab3py\\volleyball.csv"
    # train_data_set = read_training_set(train_file_name)
    # test_file_name = "D:\\FAKS\\3. god\\UUI\\Labosi\\lab3py\\volleyball_test.csv"
    # test_data_set = read_training_set(test_file_name)

    train_file_name = sys.argv[1]
    train_data_set = read_training_set(train_file_name)
    test_file_name = sys.argv[2]
    test_data_set = read_training_set(test_file_name)

    model = ID3()
    model.fit(train_data_set)
    model.print_branches()
    model.predict(train_data_set, test_data_set)


if __name__ == '__main__':
    main()
