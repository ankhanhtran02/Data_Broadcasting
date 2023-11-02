import sys

# def inp():
#     n, D = map(int,input().split()) 
#     time_matrix = [] # ma trận thời gian truyền tin từ u -> v
#     for _ in range(n):
#         time_matrix.append([float(x) for x in sys.stdin.readline().split()])
#     cost_matrix = [] # ma trận chi phí giữa từng đường truyền, đối xứng vì c(u,v) = c(v,u)
#     for _ in range(n):
#         cost_matrix.append([float(x) for x in sys.stdin.readline().split()])
#     return n, D, time_matrix, cost_matrix

def inp2():
    with open('test.txt','r') as f:
        n, D = map(int,f.readline().split()) 
        time_matrix = [] # ma trận thời gian truyền tin từ u -> v
        for _ in range(n):
            time_matrix.append([float(x) for x in f.readline().split()])
        cost_matrix = [] # ma trận chi phí giữa từng đường truyền, đối xứng vì c(u,v) = c(v,u)
        for _ in range(n):
            cost_matrix.append([float(x) for x in f.readline().split()])
        return n, D, time_matrix, cost_matrix

class Node:
    def __init__(self, ID):
        self.ID = ID
        self.parent: Node = None
        self.children = []
        self.neighbors = []
        self.visited = False
        self.total_time = 0 # thời gian từ root tới node hiện tại

# def solve(cur_node,time_matrix,D):
#     cur_node.neighbors.sort(key = lambda candidate: time_matrix[cur_node.ID][candidate.ID])
#     for candidate in cur_node.neighbors:
#         if not candidate.visited and cur_node.total_time + time_matrix[cur_node.ID][candidate.ID] <= D:
#             cur_node.children.append(candidate)                  
#             candidate.total_time = cur_node.total_time + time_matrix[cur_node.ID][candidate.ID]
#             candidate.parent = cur_node
#             candidate.visited = True
#     for node in cur_node.children:
#         solve(node,time_matrix,D)

def solve(root, time_matrix, D):
    stack = [root]
    while stack:
        cur_node = stack.pop()
        cur_node.neighbors.sort(key=lambda candidate: time_matrix[cur_node.ID][candidate.ID])
        for candidate in cur_node.neighbors:
            if not candidate.visited and cur_node.total_time + time_matrix[cur_node.ID][candidate.ID] <= D:
                cur_node.children.append(candidate)
                candidate.total_time = cur_node.total_time + time_matrix[cur_node.ID][candidate.ID]
                candidate.parent = cur_node
                candidate.visited = True
                stack.append(candidate)

n, D, time_matrix, cost_matrix = inp2()

nodes = [Node(i) for i in range(n)]
for node in nodes:
    node.neighbors = [nodes[i] for i in range(n) if i!= node.ID]
root = nodes[0]
root.visited=True

solve(root,time_matrix,D)

total = 0
for node in nodes:
	for child in node.children:
		total += cost_matrix[node.ID][child.ID]
		print(f'{node.ID} -> {child.ID}, cost = {cost_matrix[node.ID][child.ID]}')
		
print(f'total cost = {total}')





