import string


def n_most_common_words(file, n):
    with open(file, encoding='utf-8', mode='r') as text:
        count_dict = {}  # key = word; value = number of appearances
        while True:
            line = text.readline()
            if not line:
                break
            line = line.translate(str.maketrans('', '', string.punctuation))  # removing punctuation
            line = line.lower()
            line = line.split()
            for word in line:
                if word in count_dict:
                    count_dict[word] += 1
                else:
                    count_dict[word] = 1
        count = list(sorted(count_dict.items(), key=lambda item: item[1], reverse=True))  # sorting by descending value
        n_words = [i[0] for i in count[:n]]
        # adding words with equal no of appearances as the last one
        for word in count[n:]:
            if word[1] == count[n-1][1]:
                n_words.append(word[0])

        return n_words


print(n_most_common_words('potop.txt', 10))