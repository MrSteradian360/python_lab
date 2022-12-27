import numpy as np

np.set_printoptions(suppress=True)


class KNNClassifier:
    def __init__(self, k, metric):
        self.k = k
        self.metric = metric
        self.test_set = []
        self.true_values = []

    def train(self, true_values: list, *observations: list[float]):
        self.true_values += list(true_values)
        self.test_set += list(observations)

    def predict(self, *observations: list[float]):
        test_set = np.array(self.test_set)
        true_values = np.array(self.true_values)
        observations = np.array(observations)
        results_array = []
        for observation in observations:
            if self.metric == 'euclidean':
                distance = np.sqrt(np.sum(np.square(test_set - observation), axis=1))
            if self.metric == 'taxi':
                distance = np.sum(np.absolute(test_set - observation), axis=1)
            if self.metric == 'maximum':
                distance = np.max(np.absolute(test_set - observation), axis=1)
            if self.metric == 'cosine':
                distance = np.sum(test_set * observation, axis=1) / \
                           (np.sqrt(np.sum(test_set * test_set, axis=1)) *
                            np.sqrt(np.sum(observation * observation)))

            k_neighbour_distance = np.partition(distance, kth=self.k - 1)[self.k - 1]
            nearest_neighbours = true_values[distance <= k_neighbour_distance]
            unique, counts = np.unique(nearest_neighbours, return_counts=True)
            result = max(list(zip(counts, unique)))[1]
            results_array.append(result)
        return results_array


knn_classifier_0 = KNNClassifier(3, 'cosine')
knn_classifier_0.train(['kaczka', 'pies', 'kaczka', 'pies', 'pies'], [0, 9, 9], [9, 8, 10], [0, 1, 2], [0, 4, 5],
                       [9, 5, 1])
print(knn_classifier_0.predict([3, 4, 5], [1, 4, 6], [4, 5, 0], [3, 8, 9], [4.5, 3, 4]))


def evaluation(received, true):
    received = np.array(received)
    true = np.array(true)
    tp = np.sum(np.logical_and(received == 1., true == 1.))
    tn = np.sum(np.logical_and(received == 0., true == 0.))
    fp = np.sum(np.logical_and(received == 1., true == 0.))
    fn = np.sum(np.logical_and(received == 0., true == 1.))

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = (2 * precision * recall) / (precision + recall)

    return accuracy, precision, recall, f1


knn_classifier_1 = KNNClassifier(3, 'taxi')
knn_classifier_2 = KNNClassifier(5, 'maximum')
knn_classifier_3 = KNNClassifier(7, 'euclidean')

with open('dataset') as data:
    lines = data.readlines()
    vector = []
    labels = []
    for line in lines:
        data_list = list(map(float, line.split()))
        vector.append(data_list[:-1])
        labels.append(data_list[-1])

    knn_classifier_1.train(labels[:int(0.7 * len(labels))], *vector[:int(0.7 * len(labels))])
    knn_classifier_2.train(labels[:int(0.7 * len(labels))], *vector[:int(0.7 * len(labels))])
    knn_classifier_3.train(labels[:int(0.7 * len(labels))], *vector[:int(0.7 * len(labels))])

    p1 = knn_classifier_1.predict(*vector[int(0.7 * len(labels)):])
    p2 = knn_classifier_2.predict(*vector[int(0.7 * len(labels)):])
    p3 = knn_classifier_3.predict(*vector[int(0.7 * len(labels)):])

    print(evaluation(p1, labels[int(0.7 * len(labels)):]))
    print(evaluation(p2, labels[int(0.7 * len(labels)):]))
    print(evaluation(p3, labels[int(0.7 * len(labels)):]))
