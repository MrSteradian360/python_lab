import numpy as np

np.set_printoptions(suppress=True)


class KNNClassifier:
    def __init__(self, k, metric):
        self.k = k
        self.metric = metric
        self.test_set = []
        self.true_values = []

    def train(self, true_values: list, *observations: list[float]):
        self.true_values = list(true_values)
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


knn_classifier1 = KNNClassifier(2, 'taxi')
knn_classifier1.train(['kaczka', 'pies', 'kaczka'], [0, 9, 9], [9, 8, 10], [0, 1, 2])
print(knn_classifier1.predict([3, 4, 5], [1, 4, 6], [0, 0, 0], [9, 8, 9]))
