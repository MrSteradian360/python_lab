def build(*patterns):
    # building trie
    # trie is stored as a dict where key is node index and value is another dict whose keys are strings
    # containing chars from previous edges and one edge ahead, values of inside dict are next nodes to visit;
    # when there are no thick edges coming out from node it is denoted as '$' at the end of string;
    # '#' in keys of inside dict denotes accepting state; '*' denotes joker; '' denotes faillink
    trie = {}
    biggest_num = 0  # helps to keep track of new nodes on different branches
    for pattern in patterns:
        current_num = 0
        for idx, char in enumerate(pattern):
            prefix = pattern[:idx + 1]
            if current_num in trie:
                # deleting unnecessary items (when one pattern contains other):
                if None in trie[current_num].values():
                    del trie[current_num][
                        (list(trie[current_num].keys())[list(trie[current_num].values()).index(None)])]
                connections = trie[current_num]
                # creating new nodes:
                if prefix not in connections:
                    connections[prefix] = biggest_num + 1
                    trie[current_num] = connections
                    biggest_num += 1
                    current_num = biggest_num
                else:
                    current_num += 1
            # creating new nodes:
            else:
                trie[current_num] = {prefix: current_num + 1}
                current_num += 1
                biggest_num += 1
        # creating accepting states (and denoting those which end with no thick edges coming out):
        if current_num not in trie:
            trie[current_num] = {prefix + "$": None}
        trie[current_num] |= {'#': "accept"}

    # backwards trie
    # gives us info about previous nodes and what string is coming into given node:
    backwards = {}
    for vertex in trie:
        if list(trie[vertex].values())[0] is not None:
            for key in trie[vertex]:
                if key != '#':
                    backwards[trie[vertex][key]] = (key, vertex)

    # adding faillinks to chilren of root:
    for edge in trie[0].copy():
        trie[trie[0][edge]] |= {'': 0}

    # adding 'joker':
    trie[0] |= {'*': 0}

    # adding faillinks to deeper vertices:
    # sorting trie based on length of keys of inside dict (guarantees that faillinks will be set in right order):
    trie_sorted = {key: value for key, value in sorted(trie.items(), key=lambda item: len(list(item[1].keys())[0]))}
    for vertex in trie_sorted:
        # adding faillinks to levels deeper than second:
        if len(list(trie_sorted[vertex].keys())[0]) > 2:
            label, parent = backwards[vertex]
            label = label[-1]  # char incoming to current node
            fail = trie.copy()[trie.copy()[parent]['']]
            done = False
            while not done:
                for key in fail.keys():
                    if key not in ['', '*'] and key[-1] == label:
                        vertex2 = fail[key]
                        trie[vertex] |= {'': vertex2}
                        done = True
                        break
                    # adding faillink incoming to zero node:
                    elif key == '*':
                        trie[vertex] |= {'': 0}
                        done = True
                        break
                # travelling back through faillink:
                if not done:
                    fail = trie.copy()[fail['']]
    return trie


# travelling through trie:
def search(trie, text):
    i = 0
    appearance_list = []
    idx = 0
    # checking chars from text:
    while idx < len(text):
        for key in trie[i].keys():
            # thick vertices:
            if key not in ['', '*', '#'] and key[-1] == text[idx]:
                i = trie[i][key]
                # checking if states before weren't accepting
                idx1 = idx + 1
                j = i
                while True:
                    if '' in trie[j].keys():
                        if '#' in trie[j].keys():
                            for key in trie[j].keys():
                                if key not in ['', '#', '*']:
                                    length = len(key)
                            appearance_list.append(idx1 - (length - 1))
                        j = trie[j]['']
                    else:
                        break
                break
            # faillinks:
            elif key == '':
                i = trie[i][key]
                idx -= 1  # guarantees staying on the same char
            # take no action on joker:
            elif key == '*':
                pass
        idx += 1

    return appearance_list


def main():
    trie = build('abc', 'aab', 'cba')
    print(trie)
    print(search(trie, "aaabc"))


if __name__ == "__main__":
    main()
