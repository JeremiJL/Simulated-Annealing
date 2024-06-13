from Converter import convert_adjacency_matrix_to_vertices
from Annealing import Annealing

vertices = convert_adjacency_matrix_to_vertices("./data/tsp_data_big.txt")
algorithm = Annealing(vertices,10,200)

print(algorithm.best_distance)






