import sys
from queue import PriorityQueue
import time

algorithm = ''
file_path = ''
heuristic_path = ''
start = ''
end = []
adjacency_list = {}
heuristic_map = {}


def printToFormat(algorithm, found_solution, states, path, total_cost):
    path_to_print = ' => '.join(str(x) for x in path)
    print(f"# {algorithm}\n"
          f"[FOUND_SOLUTION]: {found_solution}\n"
          f"[STATES_VISITED]: {states}\n"
          f"[PATH_LENGTH]: {len(path)}\n"
          f"[TOTAL_COST]: {float(total_cost)}\n"
          f"[PATH]: {path_to_print}")


def myFunc(e):
    return e[0]


def checkIfConsistent():
    consistent = True
    for node in adjacency_list:
        for neighbour in adjacency_list[node]:
            if not neighbour:
                break
            neighbour_vertex = neighbour.split(',')[0]
            neighbour_cost = neighbour.split(',')[1]
            result = f'h({node}) <= h({neighbour_vertex}) + c: {float(heuristic_map[node])} <= {float(heuristic_map[neighbour_vertex])} + {float(neighbour_cost)}'
            if float(heuristic_map[node]) <= (float(heuristic_map[neighbour_vertex]) + float(neighbour_cost)):
                print(f'[CONDITION]: [OK] {result}')
            else:
                print(f'[CONDITION]: [ERR] {result}')
                consistent = False

    if consistent:
        print("[CONCLUSION]: Heuristic is consistent.")
    else:
        print("[CONCLUSION]: Heuristic is not consistent.")


def checkIfOptimistic():
    optimistic = True
    for node in heuristic_map:
        path, _, _ = ucs(adjacency_list, node, end)
        result = f'h({node}) <= h*: {float(heuristic_map[node])} <= {float(path[0])}'
        if float(path[0]) >= float(heuristic_map[node]):
            print(f'[CONDITION]: [OK] {result}')
        else:
            print(f'[CONDITION]: [ERR] {result}')
            optimistic = False

    if optimistic:
        print("[CONCLUSION]: Heuristic is optimistic.")
    else:
        print("[CONCLUSION]: Heuristic is not optimistic.")


def astar(graph_to_search, start, end):
    global heuristic_map
    queue = PriorityQueue()
    queue.put((0, [start + ',0']))
    visited = []

    open = list()
    open.append((0, [start + ',0']))

    # zbog neucinkovitosti implementacije, izvrsavanje while petlje ograniceno je na 5 sekundi
    time_duration = 5
    time_start = time.time()
    while len(open) != 0 and (time.time() < time_start + time_duration):
        continue_outer = False
        path = open[0]
        open.remove(open[0])

        vertex = path[-1][-1].split(',')[0]
        vertex_cost = path[-1][-1].split(',')[1]

        if vertex in end:
            while True:
                a = queue.get()
                b = a[1][1]
                if b in end:
                    return a, len(visited), 'yes'

        visited.append(path)

        for neighbour in graph_to_search.get(vertex, []):
            for m in (visited + open):
                if m[-1][-1].split(',')[0] == neighbour.split(',')[0]:
                    if float(m[-1][-1].split(',')[1]) < (float(neighbour.split(',')[1]) + float(vertex_cost)):
                        continue_outer = True
                        break
                    else:
                        if m in visited:
                            visited.remove(m)
                        if m in open:
                            open.remove(m)

            if continue_outer:
                continue_outer = False
                continue

            h = float(heuristic_map[neighbour.split(',')[0]])
            cost = float(neighbour.split(',')[1]) + float(path[1][0].split(',')[1])

            new_path = list(path[1])
            tempPath = neighbour.split(',')[0]
            new_path.append(tempPath)

            queue.put((-cost, new_path))

            open.append((h + cost, [tempPath + ',' + str(cost)]))
            open.sort(key=myFunc)

    return None, None, 'no'


def ucs(graph_to_search, start, end):
    queue = PriorityQueue()
    queue.put((0, [start]))
    visited = set()

    while not queue.empty():
        path = queue.get()
        vertex = path[-1][-1]

        if end.__contains__(vertex):
            return path, len(visited), 'yes'
        elif vertex not in visited:
            for neighbour in graph_to_search.get(vertex, []):
                new_path = list(path[1])
                neighbour_vertex = neighbour.split(',')[0]
                new_path.append(neighbour_vertex)
                neighbour_cost = neighbour.split(',')[1]
                cost = float(neighbour_cost) + path[0]

                queue.put((cost, new_path))
            visited.add(vertex)
    return None, None, 'no'


def bfs(graph_to_search, start, end):
    queue = [[start]]
    visited = set()
    total_cost = 0

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if end.__contains__(vertex):
            return path, len(visited), total_cost, 'yes'

        elif vertex not in visited:
            for current_neighbour in graph_to_search.get(vertex, []):
                new_path = list(path)
                new_path.append(current_neighbour.split(',')[0])
                total_cost += float(current_neighbour.split(',')[1])
                queue.append(new_path)

            visited.add(vertex)
    return None, None, None, 'no'


def read_file():
    file = open(file_path, 'r')
    data = file.readlines()

    for i in range(len(data) - 1):
        if data[i].startswith('#'):
            data.remove(data[i])

    global start, end
    start, end = data[0].strip(), data[1].strip().split(' ')

    for i in range(2, len(data)):
        split_line = data[i].split(':')
        adjacency_list[split_line[0]] = split_line[1].strip().split(' ')


def read_heuristic():
    file = open(heuristic_path, 'r')
    data = file.readlines()

    for i in range(0, len(data)):
        split_line = data[i].split(': ')
        heuristic_map[split_line[0]] = split_line[1].strip()


def main():
    global algorithm, file_path, heuristic_path

    opt_cons_flag = ''
    for i in range(len(sys.argv)):
        if sys.argv[i] == '--alg':
            algorithm = sys.argv[i + 1]
        elif sys.argv[i] == '--ss':
            file_path = sys.argv[i + 1]
        elif sys.argv[i] == '--h':
            heuristic_path = sys.argv[i + 1]
        elif sys.argv[i] == '--check-optimistic':
            opt_cons_flag = 'optimistic'
        elif sys.argv[i] == '--check-consistent':
            opt_cons_flag = 'consistent'

    read_file()

    if algorithm == 'bfs':
        path, states_visited, total_cost, found = bfs(adjacency_list, start, end)
        if path is None:
            print('[FOUND_SOLUTION]: ', found)
            exit(1)
        printToFormat('BFS', found, states_visited, path, total_cost)

    elif algorithm == 'ucs':
        path, states_visited, found = ucs(adjacency_list, start, end)
        if path is None:
            print('[FOUND_SOLUTION]: ', found)
            exit(1)
        printToFormat('UCS', found, states_visited, path[1], path[0])

    elif algorithm == 'astar':
        read_heuristic()
        path, states_visited, found = astar(adjacency_list, start, end)
        if path is None:
            print('[FOUND_SOLUTION]: ', found)
            exit(1)
        printToFormat(f'A-STAR {heuristic_path}', found, states_visited, path, -path[0])

    elif opt_cons_flag == 'optimistic':
        read_heuristic()
        checkIfOptimistic()

    elif opt_cons_flag == 'consistent':
        read_heuristic()
        checkIfConsistent()


if __name__ == '__main__':
    main()
