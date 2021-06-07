import sys

if len(sys.argv) != 2:
    print("Usage: python3 Alice.py <inputfilename>")
    sys.exit()

# Here is how you open a file whose name is given as the first argument
f = open(sys.argv[1])

# Read in size of grid.
grid_size = int(f.readline())


def solve_maze():
    move_count = 0                      # Smallest number of steps to reach goal
    bfs_queue = []                      # The Queue for Breadth First Search
    num_curr_level = 1                  # Number of nodes at this distance level from start node
    num_next_level = [0]                # Number of nodes at next distance level from start node
    step_size = 1                       # Default step size
    parents = {}                        # Hash table for keeping track of nodes and their parents in BFS
    reached_goal = False                # Boolean flag for if we reached our goal node yet
    # We get our start node's location
    row = int(f.readline())
    col = int(f.readline())
    start = (row, col, step_size)

    # We read in info from our text representation of the maze
    graph = []
    for line in f:
        row_nodes = line.split()
        graph.append(row_nodes)

    # We need a map to keep track of the nodes we visited at certain step sizes so we know when a graph is a 'dead-end'
    visited_map = []
    for i in range(0, grid_size):
        row = []
        for j in range(0, grid_size):
            row.append([])
        visited_map.append(row)

    bfs_queue.append(start)             # Add our start node to our BFS Queue
    curr_node = start
    visited_map[start[0]][start[1]].append(step_size)
    while len(bfs_queue) > 0:
        curr_node = bfs_queue.pop(0)
        # If we reached our goal node, by properties of BFS, this is the shortest path and we're done!
        if graph[curr_node[0]][curr_node[1]] == "G":
            reached_goal = True
            break

        # Get our destinations from the branching node
        get_destinations(curr_node, curr_node[2], graph, visited_map, bfs_queue, parents, num_next_level)
        num_curr_level = num_curr_level - 1

        # If we have no more nodes to analyze at this distance, move to the next level
        if num_curr_level == 0:
            num_curr_level = num_next_level[0]
            num_next_level = [0]
            move_count = move_count + 1

    if reached_goal:
        final_path = []
        path_node = (curr_node[0], curr_node[1], curr_node[2])

        # Unravel the path we took to get to the goal node
        for i in range(0, move_count):
            final_path.insert(0, path_node)
            path_node = parents[path_node]
        final_path.insert(0, start)

        # All of the following is just reformatting our list to present cardinal directions rather than coordinates
        directional_path = []
        for i in range(0, move_count):
            if final_path[i][0] < final_path[i + 1][0] and final_path[i][1] == final_path[i + 1][1]:
                directional_path.append(("S", final_path[i + 1][2]))
            elif final_path[i][0] > final_path[i + 1][0] and final_path[i][1] == final_path[i + 1][1]:
                directional_path.append(("N", final_path[i + 1][2]))
            elif final_path[i][0] == final_path[i + 1][0] and final_path[i][1] < final_path[i + 1][1]:
                directional_path.append(("E", final_path[i + 1][2]))
            elif final_path[i][0] == final_path[i + 1][0] and final_path[i][1] > final_path[i + 1][1]:
                directional_path.append(("W", final_path[i + 1][2]))
            elif final_path[i][0] < final_path[i + 1][0] and final_path[i][1] < final_path[i + 1][1]:
                directional_path.append(("SE", final_path[i + 1][2]))
            elif final_path[i][0] < final_path[i + 1][0] and final_path[i][1] > final_path[i + 1][1]:
                directional_path.append(("SW", final_path[i + 1][2]))
            elif final_path[i][0] > final_path[i + 1][0] and final_path[i][1] < final_path[i + 1][1]:
                directional_path.append(("NE", final_path[i + 1][2]))
            elif final_path[i][0] > final_path[i + 1][0] and final_path[i][1] > final_path[i + 1][1]:
                directional_path.append(("NW", final_path[i + 1][2]))

        # Output desired output
        print("Steps taken: " + str(move_count))
        print(directional_path)
    else:
        print("There is no solution to the maze")
    return


def get_destinations(node: tuple, step: int, graph: list, visited: list,
                     queue: list, parents: dict, next_level: list) -> None:
    """
    For a given maze 'graph', we enqueue to 'path' the valid destinations from 'node' with a step size 'step'.
    We update our 'visited' map, 'parent' hash table, and increment value in 'next_level' per valid destination found.
    """
    colour_and_directions = graph[node[0]][node[1]].split("-")

    # If arrows are red, increase step_size by 1; if yellow, decrease step_size by 1
    if int(colour_and_directions[0]) == 1:
        step = step + 1
    elif int(colour_and_directions[0]) == 2:
        step = step - 1

    # Get destination based on the direction given by the text representation
    for direction in colour_and_directions[1:]:
        if direction == "N":
            destination = (node[0] - step, node[1], step)
        elif direction == "S":
            destination = (node[0] + step, node[1], step)
        elif direction == "E":
            destination = (node[0], node[1] + step, step)
        elif direction == "W":
            destination = (node[0], node[1] - step, step)
        elif direction == "NW":
            destination = (node[0] - step, node[1] - step, step)
        elif direction == "NE":
            destination = (node[0] - step, node[1] + step, step)
        elif direction == "SW":
            destination = (node[0] + step, node[1] - step, step)
        elif direction == "SE":
            destination = (node[0] + step, node[1] + step, step)
        else:
            destination = (-1, -1, step)
        # If coordinates are out of bounds, disregard the destination
        if destination[0] < 0 or destination[0] >= grid_size or destination[1] < 0 or destination[1] >= grid_size:
            continue
        if step in visited[destination[0]][destination[1]]:
            continue

        # Here we have passed the checks above, so:
        queue.append(destination)                             # Append this destination to our BFS Queue
        parents[destination] = node                           # Set destination's parent node accordingly
        visited[destination[0]][destination[1]].append(step)  # Update the visited map,
        next_level[0] = next_level[0] + 1                     # Increment to indicate a new node at next distance level


if __name__ == '__main__':
    solve_maze()
