import math
import random
from collections import namedtuple
from copy import copy
from functools import wraps

PARAMS = set(['min_temperature', 'alpha', 'max_iterations'])

def get_params(args):
    if not args:
        return {}
    return {key: val for key, val in args.iteritems() if key in PARAMS}

Point = namedtuple("Point", ["name", "x", "y"])

def memo(f):
    cache = {}
    MAXSIZE = 100000
    @wraps(f)
    def wrapper(*args):
        if args not in cache:
            if len(cache) > MAXSIZE:
                cache.clear()
            cache[args] = f(*args)
        return cache[args]
    return wrapper

# A set of default methods for simulated annealing algorithm
@memo
def euclidean_distance(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def neighbor(solution):
    newsolution = copy(solution)
    while True:
        idx1, idx2 = random.randint(0, len(solution) - 1), random.randint(0, len(solution) - 1)
        if idx1 != idx2:
            break
    newsolution[idx1], newsolution[idx2] = newsolution[idx2], newsolution[idx1]
    return newsolution

def cost(solution, distance=euclidean_distance):
    total_cost = 0
    for i in xrange(len(solution) - 1):
        p1, p2 = solution[i], solution[i + 1]
        total_cost += distance(p1, p2)
    total_cost += distance(solution[-1], solution[0])
    return total_cost

def accept_probability(oldcost, newcost, temperature):
    if newcost < oldcost:
        return 1
    return math.exp((oldcost - newcost)/temperature)


def simulated_annealing(locations, distance_fn=euclidean_distance,
                        cost_fn=cost, accept_probability_fn=accept_probability,
                        neighbor_fn=neighbor, min_temperature=0.00001, alpha=0.90,
                        max_iterations=500):
    points = []
    for name, [x, y] in locations.iteritems():
        points.append(Point(name, x, y))
    
    curr_temperature = 1
    solution = points
    cost = cost_fn(solution, distance_fn)
    best_cost, best_solution = cost, solution
    while curr_temperature >= min_temperature:
        i = 0
        # Optimization: Run neigbor search a few times at same temperature
        while i < max_iterations:
            new_solution = neighbor_fn(solution)
            new_cost = cost_fn(new_solution)
            if new_cost < best_cost:
                best_cost, best_solution = new_cost, new_solution
            if accept_probability_fn(cost, new_cost, curr_temperature) >= random.random():
                solution = new_solution
                cost = new_cost
            i += 1
        curr_temperature = curr_temperature * alpha
        
    # Optimization in case local minima is found
    if best_cost < cost:
        cost, solution = best_cost, best_solution
    return {'items': [p.name for p in solution], 'cost': cost}
