class TrieWithoutFaillinks:
    trie = {}

    def __init__(self, *patterns):
        self.patterns = patterns

    def build(self):
        # building trie
        # trie is stored as a dict where key is node index and value is another dict whose keys are strings
        # containing chars from previous edges and one edge ahead, values of inside dict are next nodes to visit;
        # when there are no thick edges coming out from node it is denoted as '$' at the end of string;
        # '#' in keys of inside dict denotes accepting state; '*' denotes joker; '' denotes faillink
        biggest_num = 0  # helps to keep track of new nodes on different branches
        for pattern in self.patterns:
            current_num = 0
            for idx, char in enumerate(pattern):
                prefix = pattern[:idx + 1]
                if current_num in self.trie:
                    # deleting unnecessary items (when one pattern contains other):
                    if None in self.trie[current_num].values():
                        del self.trie[current_num][
                            (list(self.trie[current_num].keys())[list(self.trie[current_num].values()).index(None)])]
                    connections = self.trie[current_num]
                    # creating new nodes:
                    if prefix not in connections:
                        connections[prefix] = biggest_num + 1
                        self.trie[current_num] = connections
                        biggest_num += 1
                        current_num = biggest_num
                    else:
                        current_num += 1
                # creating new nodes:
                else:
                    self.trie[current_num] = {prefix: current_num + 1}
                    current_num += 1
                    biggest_num += 1
            # creating accepting states (and denoting those which end with no thick edges coming out):
            if current_num not in self.trie:
                self.trie[current_num] = {prefix + "$": None}
            self.trie[current_num] |= {'#': "accept"}
        return self.trie

    def __repr__(self):
        return str(self.trie)


# backwards trie
# gives us info about previous nodes and what string is coming into given node:
class BackwardsTrie:
    backwards = {}

    def __init__(self, trie):
        self.trie = trie

    def build(self):
        for vertex in self.trie:
            if list(self.trie[vertex].values())[0] is not None:
                for key in self.trie[vertex]:
                    if key != '#':
                        self.backwards[self.trie[vertex][key]] = (key, vertex)
        return self.backwards

    def __repr__(self):
        return str(self.backwards)


class Trie:
    trie = {}

    def __init__(self, trie_without_faillinks, backwards_trie):
        self.trie = trie_without_faillinks
        self.backwards = backwards_trie

    def add_faillinks(self):
        # adding faillinks to chilren of root:
        for edge in self.trie[0].copy():
            self.trie[self.trie[0][edge]] |= {'': 0}

        # adding 'joker':
        self.trie[0] |= {'*': 0}

        # adding faillinks to deeper vertices:
        # sorting trie based on length of keys of inside dict (guarantees that faillinks will be set in right order):
        trie_sorted = {key: value for key, value in
                       sorted(self.trie.items(), key=lambda item: len(list(item[1].keys())[0]))}
        for vertex in trie_sorted:
            # adding faillinks to levels deeper than second:
            if len(list(trie_sorted[vertex].keys())[0]) > 2:
                label, parent = self.backwards[vertex]
                label = label[-1]  # char incoming to current node
                fail = self.trie.copy()[self.trie.copy()[parent]['']]
                done = False
                while not done:
                    for key in fail.keys():
                        if key not in ['', '*'] and key[-1] == label:
                            vertex2 = fail[key]
                            self.trie[vertex] |= {'': vertex2}
                            done = True
                            break
                        # adding faillink incoming to zero node:
                        elif key == '*':
                            self.trie[vertex] |= {'': 0}
                            done = True
                            break
                    # travelling back through faillink:
                    if not done:
                        fail = self.trie.copy()[fail['']]
        return self.trie

    # travelling through trie:
    def search(self, text):
        current_node = 0
        appearance_list = []
        idx = 0
        # checking chars from text:
        while idx < len(text):
            for key in self.trie[current_node].keys():
                # thick vertices:
                if key not in ['', '*', '#'] and key[-1] == text[idx]:
                    current_node = self.trie[current_node][key]
                    # checking if states before weren't accepting
                    idx1 = idx + 1
                    node = current_node
                    while True:
                        if '' in self.trie[node].keys():
                            if '#' in self.trie[node].keys():
                                for key in self.trie[node].keys():
                                    if key not in ['', '#', '*']:
                                        length = len(key)
                                appearance_list.append(idx1 - (length - 1))
                            node = self.trie[node]['']
                        else:
                            break
                    break
                # faillinks:
                elif key == '':
                    current_node = self.trie[current_node][key]
                    idx -= 1  # guarantees staying on the same char
                # take no action on joker:
                elif key == '*':
                    pass
            idx += 1
        return appearance_list

    def __repr__(self):
        return str(self.trie)


basic_trie = TrieWithoutFaillinks('abc', 'aab', 'cba')
basic_trie.build()
print(basic_trie)
backwards_trie = BackwardsTrie(basic_trie.trie)
backwards_trie.build()
print(backwards_trie)
final_trie = Trie(basic_trie.trie, backwards_trie.backwards)
final_trie.add_faillinks()
print(final_trie)
print(final_trie.search("aaabc"))
