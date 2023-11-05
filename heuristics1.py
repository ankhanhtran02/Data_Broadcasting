import sys

def inp():
    n, D = map(int,input().split()) # n: number of nodes in the network, including the root; D: time constraint
    time_matrix = [] # a matrix consisting of the time a data package is broadcasted from u to v
    for _ in range(n):
        time_matrix.append([float(x) for x in sys.stdin.readline().split()])
    cost_matrix = [] # a matrix consisting of the cost to rent each edge from u to v, denoted by c(u,v). It's symmetric since c(u,v) = c(v,u)
    for _ in range(n):
        cost_matrix.append([float(x) for x in sys.stdin.readline().split()])
    return n, D, time_matrix, cost_matrix

def inp2(filename):
    with open(filename,'r') as f:
        n, D = map(int,f.readline().split()) # n: number of nodes in the network, including the root; D: time constraint
        time_matrix = [] # a matrix consisting of the time a data package is broadcasted from u to v
        for _ in range(n):
            time_matrix.append([float(x) for x in f.readline().split()])
        cost_matrix = [] # a matrix consisting of the cost to rent each edge from u to v, denoted by c(u,v). It's symmetric since c(u,v) = c(v,u)
        for _ in range(n):
            cost_matrix.append([float(x) for x in f.readline().split()])
        return n, D, time_matrix, cost_matrix

class Node:
    def __init__(self, ID):
        self.ID = ID
        self.parent = None
        self.children = [] # list of nodes right after
        self.neighbors = [] # list of nodes that the current node can go to, in this case 
        self.visited = False
        self.total_time = 0 # total time from the root to the node

def solve(root, time_matrix, cost_matrix, D):
    stack = [root]
    while stack:
        cur_node = stack.pop()
        cur_node.neighbors.sort(key=lambda candidate: cost_matrix[cur_node.ID][candidate.ID])
        for candidate in cur_node.neighbors:
            if (not candidate.visited) and (cur_node.total_time + time_matrix[cur_node.ID][candidate.ID] <= D):
                cur_node.children.append(candidate)
                candidate.total_time = cur_node.total_time + time_matrix[cur_node.ID][candidate.ID]
                candidate.parent = cur_node
                candidate.visited = True
                stack.append(candidate)

def print_solution(filename):
    n, D, time_matrix, cost_matrix = inp2(filename) 
    nodes = [Node(i) for i in range(n)]
    for node in nodes:
        node.neighbors = [nodes[i] for i in range(n) if i!= node.ID]
    root = nodes[0]
    root.visited=True

    solve(root,time_matrix,cost_matrix,D)

    # print(f'{filename}: ',end='')
    print(n)
    total = 0
    counts = 0
    for node in nodes:
        for child in node.children:
                counts += 1
                total += cost_matrix[node.ID][child.ID]
                print(f'{node.ID} {child.ID}')
                # print(f'{node.ID} -> {child.ID}, cost = {cost_matrix[node.ID][child.ID]}')
    # count_left = n-1-counts
    # print(f'total cost = {total}', end = ', ')
    # print(f'number of nodes unconnected = {count_left}')

def export_solution(input,output):
    with open(output,'w') as f:    
        n, D, time_matrix, cost_matrix = inp2(input) 

        nodes = [Node(i) for i in range(n)]
        for node in nodes:
            node.neighbors = [nodes[i] for i in range(n) if i!= node.ID]
        root = nodes[0]
        root.visited=True

        solve(root,time_matrix,cost_matrix,D)

        f.write(f'{n}\n')
        total = 0
        counts = 0
        for node in nodes:
            for child in node.children:
                    counts += 1
                    total += cost_matrix[node.ID][child.ID]
                    f.write(f'{node.ID} {child.ID}\n')
        # count_left = n-1-counts

filename = input() # insert name of input file
print_solution(filename)

