from Data_set import *
from Graph import *


class ID3:
    def __init__(self):
        self.decision_tree = None

    def id3(self, D: DataSet, D_parent: DataSet, X, y):
        label = D.feature_names[-1]
        if len(D.data) == 0:
            v = D_parent.most_common_label
            leaf = Leaf(v)
            return leaf

        v = D.most_common_label

        feature_index = list(D.feature_values).index(label)
        Dy_v = filter_data_set(D, feature_index, v, "label")
        if len(X) == 0 or D == Dy_v:
            leaf = Leaf(v)
            return leaf

        x = get_most_discriminitive_feature(D, X)
        subtrees = []
        for v in D.feature_values[x]:
            feature_index = list(D.feature_values).index(x)
            Dx_v = filter_data_set(D, feature_index, v)
            if x in X:
                X.remove(x)
            t = self.id3(Dx_v, D, X, y)
            subtrees.append((v, t))
            X.append(x)
        return Node(x, subtrees)

    def fit(self, train_dataset: DataSet):
        self.decision_tree = self.id3(train_dataset, train_dataset, train_dataset.feature_names[:-1], train_dataset.feature_names[-1])

    def predict(self, train_dataset: DataSet, test_dataset: DataSet):
        predictions = []
        for line in test_dataset.data:
            node = self.decision_tree
            parent_feature_index = None
            while True:
                if isinstance(node, Leaf):
                    predictions.append(node.value)
                    break

                feature_index = test_dataset.feature_names.index(node.value)

                node = find_next_node(line, feature_index, node)
                if not node:
                    if parent_feature_index is not None:
                        Dx_v = filter_data_set(train_dataset, parent_feature_index, parent_feature)
                        predictions.append(Dx_v.most_common_label)
                        break
                    else:
                        predictions.append(train_dataset.most_common_label)
                        break
                parent_feature_index = feature_index
                parent_feature = line[0][feature_index]

        self.print_predictions(predictions)
        self.confusion_matrix(predictions, test_dataset)

    def confusion_matrix(self, predictions, test_dataset):
        possible_predictions = list(sorted(set(predictions)))
        matrix_len = len(possible_predictions)
        matrix = [[0 for x in range(matrix_len)] for y in range(matrix_len)]
        for k, line in enumerate(test_dataset.data):
            actual = line[1]
            prediction = predictions[k]
            i = possible_predictions.index(actual)
            j = possible_predictions.index(prediction)
            matrix[i][j] += 1

        actuals = sum(matrix[i][i] for i in range(matrix_len))
        total = len(test_dataset.data)
        accuracy = "{:.5f}".format(actuals/total)
        print_matrix_and_accuracy(matrix, accuracy)

    def print_branches(self):
        print('[BRANCHES]:')
        to_leaf(self.decision_tree, 1, [])

    def print_predictions(self, predictions):
        print(f"[PREDICTIONS]: {' '.join(predictions)}")


def print_matrix_and_accuracy(matrix, accuracy):
    print(f"[ACCURACY]: {accuracy}")
    print('[CONFUSION_MATRIX]:')
    for row in matrix:
        for column in row:
            print(column, end=" ")
        print()


def find_next_node(line, feature_index, node):
    for i, branch in enumerate(node.tree):
        if branch[0] == line[0][feature_index]:
            return branch[1]


def to_leaf(node, depth, lista):
    if isinstance(node, Leaf):
        print(' '.join(lista) + f" {node.value}")
        if len(lista) > 0:
            lista.pop()
        return

    for branch in node.tree:
        lista.append(f"{depth}:{node.value}={branch[0]}")
        to_leaf(branch[1], depth+1, lista)

    if len(lista) > 0:
        lista.pop()

