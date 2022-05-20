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
    train_file_name = sys.argv[1]
    train_data_set = read_training_set(train_file_name)
    test_file_name = sys.argv[2]
    test_data_set = read_training_set(test_file_name)
    if len(sys.argv) == 4:
        max_depth = int(sys.argv[3])
    else:
        max_depth = sys.maxsize

    model = ID3()
    model.fit(train_data_set, max_depth)
    model.print_branches()
    model.predict(train_data_set, test_data_set)


if __name__ == '__main__':
    main()
