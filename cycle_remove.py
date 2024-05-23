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

def generate_lp_string(num_vertices, edges):
    edge_set = set((i, j) for (i, j, w) in edges)
    lp_str = ""
    
    for (i, j, _) in edges:
        lp_str += f"var x_{i}_{j}, binary;\n"

    lp_str += "minimize obj: " + " + ".join([f"{w}*x_{i}_{j}" for (i, j, w) in edges]) + ";\n"
    
    lp_str += "s.t.\n"
    
    # cyklus délky 3
    for i in range(num_vertices):
        for j in range(num_vertices):
            for k in range(num_vertices):
                if i != j and j != k and k != i:
                    if (i, j) in edge_set and (j, k) in edge_set and (k, i) in edge_set:
                        lp_str += f" c3_{i}_{j}_{k}: x_{i}_{j} + x_{j}_{k} + x_{k}_{i} >= 1;\n"
    
    # cyklus délky 4
    for i in range(num_vertices):
        for j in range(num_vertices):
            for k in range(num_vertices):
                for l in range(num_vertices):
                    if len(set([i, j, k, l])) == 4:
                        if (i, j) in edge_set and (j, k) in edge_set and (k, l) in edge_set and (l, i) in edge_set:
                            lp_str += f" c4_{i}_{j}_{k}_{l}: x_{i}_{j} + x_{j}_{k} + x_{k}_{l} + x_{l}_{i} >= 1;\n"
    
    lp_str += "solve;\n"
    lp_str += "end;\n"
    
    return lp_str

def main(input_file):
    num_vertices, edges = read_graph(input_file)
    if not edges:
        print("#OUTPUT: 0")
        print("#OUTPUT END")
        return
    lp_string = generate_lp_string(num_vertices, edges)
    
    out_file = "out.txt"
    print(lp_string, file=open(out_file, "w"))


file_name = input("zadejte název souboru: ")
if file_name:
    main(file_name)

