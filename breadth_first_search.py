import pandas as pd
import queue


# The function initializes and returns open
def init_open():
    return queue.Queue()


# The function inserts s into open
def insert_to_open(open_list, s):  # Should be implemented according to the open list data
    open_list.put(s)


# The function returns the best node in open (according to the search algorithm)
def get_best(open_list):
    return open_list.get()


def is_valid_location(x, y, grid):
    return 0 <= y < len(grid) and 0 <= x < len(grid[y]) and not grid[x, y] == "@"


def try_appeand_location(x, y, grid, s_location, neighbors):
    if is_valid_location(x, y, grid):
        neighbors.append((x, y, s_location))


# The function returns neighboring locations of s_location
def get_neighbors(grid, s_location):
    neighbors = []
    try_appeand_location(s_location[0] + 1, s_location[1], grid, s_location, neighbors)
    try_appeand_location(s_location[0] - 1, s_location[1], grid, s_location, neighbors)
    try_appeand_location(s_location[0], s_location[1] + 1, grid, s_location, neighbors)
    try_appeand_location(s_location[0], s_location[1] - 1, grid, s_location, neighbors)
    return neighbors


def distance_to_root(s):
    x = 0
    while s[2]:
        s = s[2]
        x += 1
    return x


# The function returns whether n_location should be generated (checks in open_list)
# removes a node from open_list if needed 
def check_for_duplicates_open(n_location, s, open_list):
    bool_flag = False
    new = queue.Queue()
    while not open_list.empty():
        x = open_list.get()
        if is_goal(x, n_location):
            bool_flag = True
            if distance_to_root(x[2]) > distance_to_root(s):
                bool_flag = True
                break
            new.put(x)
            break
        new.put(x)
    while not new.empty():
        open_list.put(new.get())
    # if bool_flag:
    #     insert_to_open(open_list, s)
    return bool_flag


# The function returns whether n_location should be generated (checks in closed_list)
# removes a node from closed_list if needed  
def check_for_duplicates_close(n_location, s, closed_list):
    return n_location in closed_list
    # for x in closed_list.keys():
    #     if is_goal(x, n_location):
    #         if distance_to_root(x[2]) > distance_to_root(s):
    #             return False
    # return True


# The function returns whether or not s_location is the goal location
def is_goal(s_location, goal_location):
    return s_location[0] == goal_location[0] and s_location[1] == goal_location[1]


# Locations are tuples of (x, y)
def bfs(grid, start_location, goal_location):
    # State = (x, y, s_prev)
    # Start_state = (x_0, y_0, False)
    open_list = init_open()
    closed_list = {}

    # Mark the source node as
    # visited and enqueue it
    start = (start_location[0], start_location[1], False)
    insert_to_open(open_list, start)

    while not open_list.empty():
        # Dequeue a vertex from
        # queue and print it
        s = get_best(open_list)
        # print(s, end=" ")
        s_location = (s[0], s[1])
        if s_location in closed_list:
            continue
        if is_goal(s_location, goal_location):
            print("The number of states visited by BFS:", len(closed_list))
            return s
        neighbors = get_neighbors(grid, s_location)
        for n_location in neighbors:
            if check_for_duplicates_open(n_location, s, open_list) or check_for_duplicates_close(n_location, s,
                                                                                                 closed_list):
                continue
            n = (n_location[0], n_location[1], s)
            insert_to_open(open_list, n)
        closed_list[s_location] = s


def print_route(s):
    while s:
        print(s[0], s[1])
        s = s[3]


def get_route(s):
    route = []
    while s:
        s_location = (s[0], s[1])
        route.append(s_location)
        s = s[2]
    route.reverse()
    return route


def print_grid_route(route, grid):
    for location in route:
        grid[location] = 'x'
    print(pd.DataFrame(grid))
