class Graph:
    def __init__(self, vertices: set, edges: list[set]):
        self.__vertices = set(vertices)
        self.__edges = list(edges)
        # removing impossible edges:
        for edge in self.__edges.copy():
            if list(edge)[0] not in self.__vertices or list(edge)[1] not in self.__vertices:
                self.__edges.remove(edge)

    # adding vertex:
    def add_vertex(self, vertex):
        self.__vertices |= {vertex}

    # removing vertex with adjacent edges:
    def remove_vertex(self, vertex):
        self.__vertices -= {vertex}
        for edge in self.__edges.copy():
            if vertex in edge:
                self.__edges.remove(edge)

    # adding edge:
    def add_edge(self, edge):
        if list(edge)[0] in self.__vertices and list(edge)[1] in self.__vertices:
            self.__edges.append(edge)

    # removing edge:
    def remove_edge(self, edge):
        if edge in self.__edges:
            self.__edges.remove(edge)

    # finding neighbouring vertices of given vertex:
    def neighbours(self, vertex):
        __neighbours = []
        for edge in self.__edges:
            edge = list(edge)
            if edge[0] == vertex:
                __neighbours.append(edge[1])
            if edge[1] == vertex:
                __neighbours.append(edge[0])
        return __neighbours

    # function returns BFS iterator:
    def bfs(self, root):
        __bfs_iterator = BfsIterator(root, self.__vertices, self)
        return __bfs_iterator

    # function returns DFS iterator:
    def dfs(self, root):
        __dfs_iterator = DfsIterator(root, self.__vertices, self)
        return __dfs_iterator

    def __str__(self):
        return f"vertices: {self.__vertices}, edges: {self.__edges}"


class BfsIterator:
    def __init__(self, root, vertices, graph):
        self.__vertices = list(vertices)
        self.__order = list()  # final order of edges
        __status = dict()  # keeps track of visited edges
        __queue = list()
        for vertex in self.__vertices:
            __status[vertex] = 0
        __queue.append(root)
        while __queue:
            self.__order.append(__queue[0])
            __status[__queue[0]] = 1
            for vertex in graph.neighbours(__queue[0]):
                if __status[vertex] == 0:
                    __queue.append(vertex)
            __queue = __queue[1:]

    def __next__(self):
        try:
            return self.__order.pop(0)
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


class DfsIterator:
    def __init__(self, root, vertices, graph):
        self.__vertices = list(vertices)
        self.__order = list()
        __status = dict()
        __stack = list()
        for vertex in self.__vertices:
            __status[vertex] = 0
        __stack.append(root)
        while __stack:
            last = __stack.pop()
            __status[last] = 1
            self.__order.append(last)
            for vertex in graph.neighbours(last):
                if __status[vertex] == 0:
                    __stack.append(vertex)

    def __next__(self):
        try:
            return self.__order.pop(0)
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self


graph = Graph({1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
              [{1, 2}, {1, 7}, {1, 4}, {2, 5}, {3, 6}, {4, 3}, {4, 8}, {4, 9}, {4, 10}])
graph.add_vertex(11)
print(graph)
graph.remove_vertex(11)
print(graph)
graph.add_edge({10, 11})
print(graph)
graph.remove_edge({10, 11})
print(graph)
print(graph.neighbours(1))
print()

for vertex in graph.bfs(1):
    print(vertex)
print()

for vertex in graph.dfs(1):
    print(vertex)

graph = Graph({"Warszawa","Kraków", "Gdańsk", "Wrocław", "Poznań"},
              [{"Warszawa","Kraków"},{"Kraków", "Gdańsk"},{"Gdańsk","Wrocław"},{"Warszawa", "Lublin"}])
graph.add_vertex("Katowice")
print(graph)
graph.remove_vertex("Wrocław")
print(graph)
graph.add_edge({"Katowice", "Gdańsk"})
print(graph)
graph.remove_edge({"Kraków","Gdańsk"})
print(graph)
print(graph.neighbours("Kraków"))
print()

for vertex in graph.bfs("Kraków"):
    print(vertex)
print()

for vertex in graph.dfs("Kraków"):
    print(vertex)

