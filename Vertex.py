class Vertex:
    def __init__(self, name):
        # name : human-readable identifier of the vertex
        self.name = name
        # dictionary : vertex -> float, represents the weight on edge between two vertices
        self.distances_dictionary = dict()

    def __str__(self):
        return self.name + " : " + str(self.distances_dictionary.values())
