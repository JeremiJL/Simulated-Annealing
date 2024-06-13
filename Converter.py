from Vertex import Vertex


def convert_adjacency_matrix_to_vertices(file):
    vertices = []
    lines = []
    # move data from file to array
    with open(file, 'r') as f:
        for line in f:
            lines.append(line)
    # create empty vertices
    for i in range(0, len(lines)):
        vertices.append(Vertex(name="Vertex " + str(i)))
    # assign distance dictionaries to created vertices
    for line, i in zip(lines, range(0, len(lines))):
        current = vertices[i]
        distances = str(line).split(" ")
        for distance, j in zip(distances, range(0, len(lines))):
            current.distances_dictionary[vertices[j]] = int(str(distance).strip())
    return vertices
