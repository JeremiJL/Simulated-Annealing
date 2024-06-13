import math
import random
from random import shuffle


def convert_into_cycle(sequence):
    return list(sequence).append(sequence[0])


def generate_neighbourhood(neighbour):
    # list of all neighbours of given sequence
    neighbours_list = []
    # swap any element on 'k' position with element on 'k+1' position
    for k in range(-1, len(neighbour) - 1):
        new = neighbour[:]
        tmp = new[k]
        new[k] = new[k + 1]
        new[k + 1] = tmp
        # add to neighbours list
        neighbours_list.append(new)
    # return neighbourhood
    return neighbours_list


def compute_distance(sequence):
    # total distance
    distance = 0
    # sum distances between element with index 'i' and 'i+1'
    for i in range(-1, len(sequence) - 1):
        start = sequence[i]
        end = sequence[i + 1]
        distance += start.distances_dictionary[end]
    return distance


def pick_random_neighbour(neighbourhood):
    index = random.randint(0, len(neighbourhood) - 1)
    return neighbourhood[index]


def should_swap_neighbour(current_distance, neighbour_distance, temperature):
    # assuming that neighbour_distance is greater than current_distance, because
    # otherwise we should pick smaller distance instantly
    # temperature starts from some positive number and decreases to 0 after each iteration
    benchmark = math.exp(-(neighbour_distance - current_distance) / temperature)
    rand = random.random()
    return rand < benchmark





class Annealing:
    def __init__(self, vertices_list, max_freeze, initial_temperature, temperature_divisor):
        # list of vertices (corresponding to cities in tsp problem)
        self.vertices_list = vertices_list
        # best path
        self.best_path = []
        # searched paths
        self.searched_paths = []
        # best path summed distance
        self.best_distance = None
        # hyperparameter that determines how quickly should algorithm give
        # up the search for local optimum - the number of iteration that have not changed for any neighbour
        self.max_freeze = max_freeze
        # hyperparameter - initial temperature
        self.initial_temperature = initial_temperature
        # hyperparameter - determines the rate how quickly the temperature decreases towards 0
        if temperature_divisor <= 1:
            raise ValueError("Temperature divisor has to be greater than 1")
        self.temperature_divisor = temperature_divisor

        # start the algorithm
        self.search()

    def search(self):
        # assign the randomly chosen sequence as initial path
        current_path = self.random_order()
        current_distance = compute_distance(current_path)
        # assign best distance and best path to initial, random choice as first step
        self.best_path = current_path
        self.best_distance = compute_distance(self.best_path)

        # keep count of iterations during which the current sequence have not changed
        freeze_count = 0
        # start with initial temperature
        temperature = self.initial_temperature
        # iteratively find local best
        while freeze_count < self.max_freeze or self.lower_temperature(temperature) == 0:

            # compute neighbourhood of current best path under evaluation
            neighbourhood = generate_neighbourhood(current_path)
            random_neighbour = pick_random_neighbour(neighbourhood)
            random_neighbour_distance = compute_distance(random_neighbour)
            # save random neighbour to searched neighbours history
            self.searched_paths.append(random_neighbour)

            # swap the currently evaluated sequence if neighbour has better value of cost function
            # also update the best known value so far
            if random_neighbour_distance < self.best_distance:
                current_path = self.best_path = random_neighbour
                current_distance = self.best_distance = random_neighbour_distance
                # refresh freeze count
                freeze_count = 0
            # swap the currently evaluated sequence with neighbour with some probability dependent on temperature

            elif should_swap_neighbour(current_distance, random_neighbour_distance, temperature):
                current_path = random_neighbour
                current_distance = random_neighbour_distance
                # refresh freeze count
                freeze_count = 0
            else:
                # we increment freeze count, as no swap was performed during this iteration
                freeze_count += 1
            # lower temperature at the end of the iteration
            temperature = self.lower_temperature(temperature)

    def lower_temperature(self, temperature):
        return temperature / self.temperature_divisor

    def random_order(self):
        shuffled = self.vertices_list[:]
        shuffle(shuffled)
        return shuffled
