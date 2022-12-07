import string


def n_most_common_words(file, n):  # przesłonięcie symbolu wbudowanego; przydałaby się jakaś dekompozycja
    if n > 0:
        with open(file, encoding='utf-8', mode='r') as text:
            count_dict = {}  # key = word; value = number of appearances  # polecam collections.Counter
            punct = dict.fromkeys(string.punctuation, ' ')
            while True:
                line = text.readline()
                if not line:
                    break
                line = line.translate(str.maketrans(punct))  # replacing punctuation with spaces  # nie lepiej argument tej metody obliczyć raz przed pętlą?
                line = line.lower()
                line = line.split()
                for word in line:
                    if word in count_dict:
                        count_dict[word] += 1
                    else:
                        count_dict[word] = 1
            count = list(   # sorted zawsze zwraca listę
                sorted(count_dict.items(), key=lambda item: item[1], reverse=True))  # sorting by descending value  # można też operator.itemgetter(1)
            n_words = [i[0] for i in count[:n]]
            # adding words with equal no of appearances as the last one
            for word in count[n:]:
                if word[1] == count[n - 1][1]:
                    n_words.append(word[0])

            return n_words  # to zadanie nieprzypadkowo jest po laboratorium o generatorach
    else:
        raise ValueError("Number must be positive")


print(n_most_common_words('potop.txt', 10))
