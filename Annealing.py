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


def lower_temperature(temperature):
    return temperature / 2


class Annealing:
    def __init__(self, vertices_list, max_freeze, initial_temperature):
        # list of vertices (corresponding to cities in tsp problem)
        self.vertices_list = vertices_list
        # best path
        self.current_path = []
        # searched paths
        self.searched_paths = []
        # best path summed distance
        self.best_distance = None
        # hyperparameter that determines how quickly should algorithm give
        # up the search for local optimum - the number of iteration that have not changed for any neighbour
        self.max_freeze = max_freeze
        # hyperparameter - initial temperature
        self.initial_temperature = initial_temperature

        # start the algorithm
        self.search()

    def search(self):
        # assign best distance and best path to initial, random choice as first step
        self.current_path = self.random_order()
        self.best_distance = compute_distance(self.current_path)

        # keep count of iterations during which the current sequence have not changed
        freeze_count = 0
        # start with initial temperature
        temperature = self.initial_temperature
        # iteratively find local best
        while freeze_count < self.max_freeze:
            # compute neighbourhood of current best path under evaluation
            neighbourhood = generate_neighbourhood(self.current_path)
            random_neighbour = pick_random_neighbour(neighbourhood)
            random_neighbour_distance = compute_distance(random_neighbour)
            # save random neighbour to searched neighbours history
            self.searched_paths.append(random_neighbour)
            # swap if neighbour has better value of cost function
            # or the probability function based on temperature returns True
            # uses lazy evaluation
            if (random_neighbour_distance < self.best_distance or
                    should_swap_neighbour(self.best_distance, random_neighbour_distance, temperature)):
                # we swap current best path for the new best one
                self.current_path = random_neighbour
                self.best_distance = random_neighbour_distance
                # we refresh freeze count
                freeze_count = 0
            else:
                # we increment freeze count, as no swap was performed during this iteration
                freeze_count += 1
            # lower temperature at the end of the iteration
            temperature = lower_temperature(temperature)

    def random_order(self):
        shuffled = self.vertices_list[:]
        shuffle(shuffled)
        return shuffled
