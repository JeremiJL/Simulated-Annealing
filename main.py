from Converter import convert_adjacency_matrix_to_vertices
from Annealing import Annealing, compute_distance


def display_results(alg):
    print("Every evaluated sequence:")
    for sequence in alg.searched_paths:
        for vertex in sequence:
            print(vertex.name, end=", ")
        print("")

    print("\nLocally optimal sequence:")
    for vertex in alg.best_path:
        print(vertex.name, end=", ")

    print("\n\nThe distance of the locally optimal sequence:")
    print(alg.best_distance)

    print("\nThe distance of random sequence for comparison:")
    print(compute_distance(alg.random_order()))


# INITIALIZE THE ALGORITHM
vertices = convert_adjacency_matrix_to_vertices("./data/tsp_data_big.txt")

# max freeze dependent on data size
max_freeze = len(vertices)
# initial temperature dependent on data size
initial_temperature = 5 * len(vertices)

algorithm = Annealing(vertices, 50, 50, 2)
display_results(algorithm)

