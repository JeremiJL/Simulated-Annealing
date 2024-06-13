from Converter import convert_adjacency_matrix_to_vertices
from Annealing import Annealing


def display_results(alg):
    print("Every evaluated sequence:")
    for sequence in alg.searched_paths:
        for vertex in sequence:
            print(vertex.name, end=", ")
        print("")

    print("\nLocally optimal sequence:")
    for vertex in alg.current_path:
        print(vertex.name, end=", ")

    print("\n\nThe distance of the locally optimal sequence:")
    print(alg.best_distance)


# INITIALIZE THE ALGORITHM
vertices = convert_adjacency_matrix_to_vertices("./data/tsp_data_big.txt")

# max freeze dependent on data size
max_freeze = len(vertices)
# initial temperature dependent on data size
initial_temperature = 5 * len(vertices)

algorithm = Annealing(vertices, 30, 200)
display_results(algorithm)
