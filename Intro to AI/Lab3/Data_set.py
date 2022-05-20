import math


class DataSet:
    def __init__(self, data, feature_values, feature_names):
        self.freq = dict()
        self.most_common_label = ""
        self.mdf = ""
        self.data = data
        self.feature_values = feature_values
        self.feature_names = feature_names
        self.get_frequency_of_classes()
        self.get_most_common_label()

    def __eq__(self, other):
        if isinstance(other, DataSet):
            return self.data == other.data
        return False

    def get_number_of_classes(self):
        fv_len = len(self.feature_values)
        return len(list(self.feature_values.values())[fv_len - 1])

    def get_classes_values(self):
        fv_len = len(self.feature_values)
        return sorted(list(self.feature_values.values())[fv_len - 1])

    def get_frequency_of_classes(self):
        freq = dict()

        for value in sorted(self.feature_values[self.feature_names[-1]]):
            freq[value] = 0

        for line in self.data:
            for value in freq.keys():
                if line[1] == value:
                    freq[value] += 1

        self.freq = freq

    def get_most_common_label(self):
        self.most_common_label = max(self.freq, key=self.freq.get)


def get_most_discriminitive_feature(data_set, feature_names):
    max_ig = 0
    max_feature = feature_names[0]
    for name in feature_names:
        ig = calculate_ig(data_set, name)
        if ig > max_ig:
            max_ig = ig
            max_feature = name

    return max_feature


def calculate_entropy(data_set):
    data_size = len(data_set.data)
    sum = 0

    for value in data_set.freq.keys():
        value_freq = data_set.freq[value]
        if data_size == 0:
            return 0
        sample = value_freq / data_size
        log = 0
        if sample != 0:
            log = math.log2(sample)
        sum -= sample * log

    return sum


def filter_data_set(data_set, feature_index, value, by="feature"):
    data_set_list = list()

    if by == "label":
        for line in data_set.data:
            if line[1] == value:
                data_set_list.append(line)
    else:
        for line in data_set.data:
            if line[0][feature_index] == value:
                data_set_list.append(line)

    return DataSet(data_set_list, data_set.feature_values, data_set.feature_names)


def calculate_ig(data_set: DataSet, feature):
    feature_index = list(data_set.feature_values).index(feature)

    entropy = calculate_entropy(data_set)
    sum = 0

    for value in data_set.feature_values[feature]:
        filtered_data_set = filter_data_set(data_set, feature_index, value)
        entropy_filtered_set = calculate_entropy(filtered_data_set)
        sum += (len(filtered_data_set.data) / len(data_set.data)) * entropy_filtered_set

    ig = entropy - sum
    return ig
