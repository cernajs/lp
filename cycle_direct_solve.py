import pulp

def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    header = lines[0].strip().split()
    num_vertices = int(header[2])
    num_edges = int(header[3][:-1])
    
    edges = []
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) >= 5:
            start = int(parts[0])
            end = int(parts[2])
            weight = int(parts[4][:-1])
            edges.append((start, end, weight))
        
    return num_vertices, edges

def solve_ilp(num_vertices, edges):
    prob = pulp.LpProblem("minedge", pulp.LpMinimize)
    
    x = {}
    for (i, j, w) in edges:
        x[(i, j)] = pulp.LpVariable(f"x_{i}_{j}", cat='Binary')
    

    prob += pulp.lpSum(w * x[(i, j)] for (i, j, w) in edges)
    

    for i in range(num_vertices):
        for j in range(num_vertices):
            for k in range(num_vertices):
                if i != j and j != k and k != i:
                    if (i, j) in x and (j, k) in x and (k, i) in x:
                        prob += x[(i, j)] + x[(j, k)] + x[(k, i)] >= 1
    

    for i in range(num_vertices):
        for j in range(num_vertices):
            for k in range(num_vertices):
                for l in range(num_vertices):
                    if len(set([i, j, k, l])) == 4:
                        if (i, j) in x and (j, k) in x and (k, l) in x and (l, i) in x:
                            prob += x[(i, j)] + x[(j, k)] + x[(k, l)] + x[(l, i)] >= 1

    prob.solve()
    
    removed_edges = [(i, j) for (i, j) in x if pulp.value(x[(i, j)]) > 0.5]
    total_weight = sum(w for (i, j, w) in edges if (i, j) in removed_edges)
    
    return total_weight, removed_edges

def main(input_file):
    num_vertices, edges = read_graph(input_file)
    if not edges:
        print("#OUTPUT: 0")
        print("#OUTPUT END")
        return
    total_weight, removed_edges = solve_ilp(num_vertices, edges)
    
    print("#OUTPUT:", total_weight)
    for (i, j) in removed_edges:
        print(f"{i} --> {j}")
    print("#OUTPUT END")


file_name = input("zadejte název souboru: ")
if file_name:
    main(file_name)

