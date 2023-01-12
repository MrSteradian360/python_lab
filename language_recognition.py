# based on: https://scikit-learn.org/stable/supervised_learning.html#supervised-learning,
# https://python-course.eu/machine-learning/natural-language-processing-classification.php?fbclid=IwAR2rNCuWXKEz5FNvlkV3oX1V6h5J71-zMoqwC42HKMrUQtDZ3jK7Jny2ysc

import os
import string

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier


def text2strings(filename, num_words):
    punct = dict.fromkeys(string.punctuation, '')
    with open(filename, encoding='ISO-8859-1') as file:
        lines = []
        while True:
            line = file.readline()
            if not line:
                break
            line = line.translate(str.maketrans(punct))
            line = line.lower()
            line = line.rstrip()
            line = line.split()
            lines += line
        strings = [' '.join(lines[i*num_words: (i + 1)*num_words]) for i in range((len(lines) + num_words - 1) // num_words)]
    return strings


def classify(n, length, classifier_type):
    os.listdir("lang")

    files = os.listdir("lang")
    labels = {name[:-4] for name in files if name.endswith(".txt")}
    labels = sorted(list(labels))
    # print(labels)

    data = []
    targets = []

    for name in files:
        if name.endswith(".txt"):
            lines = text2strings('lang/' + name, length)
            data.extend(lines)
            country = name[:-4]
            index = labels.index(country)
            targets += [index] * len(lines)

    res = train_test_split(data, targets,
                           test_size=0.2,
                           random_state=42)
    train_data, test_data, train_targets, test_targets = res

    count_vectorizer = CountVectorizer(analyzer='char_wb', ngram_range=(n, n))

    vectors = count_vectorizer.fit_transform(train_data)
    if classifier_type == 'MultinomialNB':
        classifier = MultinomialNB(alpha=.01)
    if classifier_type == 'MLP':
        classifier = MLPClassifier(alpha=1, max_iter=2)
    if classifier_type == 'DecisonTree':
        classifier = DecisionTreeClassifier(max_depth=100)

    classifier.fit(vectors, train_targets)

    vectors_test = count_vectorizer.transform(test_data)

    predictions = classifier.predict(vectors_test)

    precision = metrics.precision_score(test_targets, predictions, average='macro')
    accuracy = metrics.accuracy_score(test_targets,
                                      predictions)
    f1 = metrics.f1_score(test_targets,
                          predictions,
                          average='macro')
    recall = metrics.recall_score(test_targets, predictions, average='macro')

    print('precision: ', precision)
    print('accuracy score: ', accuracy)
    print('F1-score: ', f1)
    print('recall: ', recall)


for n_gram_length in [2, 3, 4]:
    for test_text_length in [5, 10, 20]:
        for classifier in ['MultinomialNB', 'MLP', 'DecisonTree']:
            print(n_gram_length, test_text_length, classifier)
            classify(n_gram_length, test_text_length, classifier)
            print()
