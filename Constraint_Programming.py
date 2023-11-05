# Method 2: Constraint Programming
from ortools.sat.python import cp_model

def scaling(f):
    if isinstance(f, str):
        f = float(f)
    return int(f*1000000000)

def print_solution_graph(prev_list:list):
    pass

def solve():
    # Create the linear solver with the GLOP backend
    model = cp_model.CpModel()
    if not model:
        return
    
    n, D = map(int, input().split())
    D = scaling(D)
    d = []
    for i in range(n):
        d.append(list(map(scaling, input().split())))
    c = []
    for i in range(n):
        c.append(list(map(int, input().split())))

    # Create variables which contain the previous transmitter
    prev = [None]
    for i in range(1, n):
        prev.append(model.NewIntVar(0, n-1, f'prev{i}'))
        model.Add(prev[i] != i)
    # Create variables which contain the time to transmit to location i
    times = []
    for i in range(n):
        times.append(model.NewIntVar(0, D, f'times{i}'))
    model.Add(times[0] == 0)

    # Create variables which contain the expression prev[i] == j
    chosen = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            chosen[i].append(model.NewIntVar(0, 1, f'chosen{i}{j}'))

    for i in range(1, n):
        for j in range(0, n):
            if j != i:
                b = model.NewBoolVar(f'b{i}{j}')
                model.Add(prev[i] == j).OnlyEnforceIf(b)
                model.Add(prev[i] != j).OnlyEnforceIf(b.Not())
                model.Add(times[i] == times[j] + d[j][i]).OnlyEnforceIf(b)
                model.Add(chosen[j][i] == 1).OnlyEnforceIf(b)
                model.Add(chosen[j][i] == 0).OnlyEnforceIf(b.Not())



    objective = sum([c[i][j]*chosen[i][j] for j in range(n) for i in range(n)])
    model.Minimize(objective)
    # weighted_objective = sum(sum(obj[i][j]*C[i][j] for j in range(n)) for i in range(n))
    # model.Minimize(weighted_objective)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print(f'The minimized objective value is: {solver.ObjectiveValue()}')
        for i in range(1, n):
            print(solver.Value(prev[i]), end=' ')
            print(c[solver.Value(prev[i])][i])
        print()
    else:
        print(status)

if __name__ == "__main__":
    solve()

