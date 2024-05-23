import pulp

def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    header = lines[0].strip().split()
    num_vertices = int(header[1])
    num_edges = int(header[2][:-1])

    edges = []
    for line in lines[1:]:
        parts = line.strip().split()
        if len(parts) == 3 and parts[1] == '--':
            start = int(parts[0])
            end = int(parts[2])
            edges.append((start, end))

    return num_vertices, edges

def solve_political_party_problem(num_vertices, edges):
    max_colors = num_vertices
    model = pulp.LpProblem("Political_Party_Problem", pulp.LpMinimize)

    y = pulp.LpVariable.dicts("color_used", range(max_colors), cat='Binary')
    x = pulp.LpVariable.dicts("vertex_color", (range(num_vertices), range(max_colors)), cat='Binary')

    model += pulp.lpSum(y[i] for i in range(max_colors))

    for v in range(num_vertices):
        model += pulp.lpSum(x[v][i] for i in range(max_colors)) == 1

    for v1 in range(num_vertices):
        for v2 in range(v1 + 1, num_vertices):
            if (v1, v2) not in edges and (v2, v1) not in edges:
                for i in range(max_colors):
                    model += x[v1][i] + x[v2][i] <= 1


    for i in range(max_colors):
        for v in range(num_vertices):
            model += x[v][i] <= y[i]


    model.solve()

    vertex_colors = [-1] * num_vertices
    num_used_colors = sum(y[i].varValue for i in range(max_colors))

    for v in range(num_vertices):
        for i in range(max_colors):
            if x[v][i].varValue == 1:
                vertex_colors[v] = i

    return int(num_used_colors), vertex_colors

def main(input_file):
    num_vertices, edges = read_graph(input_file)
    num_parties, vertex_colors = solve_political_party_problem(num_vertices, edges)

    print("#OUTPUT: {}".format(num_parties))
    for v in range(num_vertices):
        print("v_{}: {}".format(v, vertex_colors[v]))
    print("#OUTPUT END")


file_name = input("zadejte název souboru: ")
if file_name:
    main(file_name)
