import math
import random
from bird import MOVES, Bird
from tree import Node, Tree

SENSORS_COUNT = 40
SENSOR_DEGREE = 2 * math.pi / SENSORS_COUNT
BIRDS_COUNT = 50
CYCLES = 200
ARENA_SIZE = 100
FORESIGHT_DEPTH = 4

SEED = 0
random.seed(SEED)

output = ""
birds = [Bird(
    random.random() * ARENA_SIZE,
    random.random() * ARENA_SIZE,
    random.random()
) for _ in range(BIRDS_COUNT)]


def computeVisualDisk(currentBird, futureLocation, depth):
    data = [0 for _ in range(SENSORS_COUNT)]
    for bird in birds:
        if bird == currentBird:
            continue

        x = futureLocation.x
        y = futureLocation.y

        expectedLocation = bird.forward(depth)
        x1 = expectedLocation.x
        y1 = expectedLocation.y
        degree = math.atan(abs((y1 - y))/abs((x1 - x)))

        if x1 < x and y1 >= y:
            degree = math.pi - degree
        if x1 < x and y1 < y:
            degree = math.pi + degree
        if x1 >= x and y1 < y:
            degree = 2 * math.pi - degree

        data[math.floor(degree / SENSOR_DEGREE)] = 1

    return ''.join(str(e) for e in data)


def collides(futureLocation, currentBird,  depth):
    for bird in birds:
        if bird == currentBird:
            continue
        if bird.collides(futureLocation, depth):
            return True
    return False


def computeSearchTree(current_node, currentBird, depth):
    if depth == FORESIGHT_DEPTH:
        return

    for move in MOVES:
        futureLocation = currentBird.foreseeMove(
            move,
            currentBird.location if depth == 0 else current_node.value[0]
        )
        if not collides(futureLocation, currentBird, depth + 1):
            disk = computeVisualDisk(currentBird, futureLocation, depth + 1)
            child = Node([futureLocation, disk], depth + 1)
            current_node.children.append(child)
            computeSearchTree(child, currentBird, depth + 1)


def getFutures(move_root, futures):
    futures.add(move_root.value[1])
    for child in move_root.children:
        getFutures(child, futures)


def choseFuture(root):
    print("Choosing")
    maximum_futures = -1
    vals = []

    for move_root in root.children:
        futures = set()
        getFutures(move_root, futures)
        count = len(futures)
        maximum_futures = max(count, maximum_futures)
        vals.append(count)
        print("Posible Futures", count)

    print("Maximum Futures", maximum_futures)
    possibleIds = []
    for i in range(len(vals)):
        if vals[i] == maximum_futures:
            possibleIds.append(i)

    return random.choice(possibleIds)

# Main time loop
for cycle in range(CYCLES):
    currentBird = 0
    print("Cycle", cycle)

    # For each bird, we create a brand new search tree
    # The tree holds all of the possible combinations moves that the bird can make 
    # The tree also stores each posssible future location's Visual Disk
    # After computing the tree, we choose the move that maximises the number of unique future Visual Disks
    # We then update the location of the bird, based on the move we chose
    for bird in birds:
        search_tree = Tree(bird)
        computeSearchTree(search_tree.root, bird, 0)
        chosen_future = choseFuture(search_tree.root)
        bird.setLocation(search_tree.root.children[chosen_future].value[0])
        output += bird.format() + "\n"
        currentBird += 1

outputFile = open("output.txt", "a")
outputFile.write(output)
outputFile.close()
