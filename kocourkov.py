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


def generate_lp_model(num_vertices, edges):
    model = []

    model.append(f"set V := 0..{num_vertices-1};")
    model.append(f"set E := {{ {', '.join(f'({i},{j})' for i, j in edges)} }};")
    model.append(f"param M := {num_vertices};")

    model.append("var x{i in V, k in 0..M-1} binary;")
    model.append("var y{k in 0..M-1} binary;")

    model.append("minimize TotalParties: sum{k in 0..M-1} y[k];")

    # jedna strana na vrchol
    for i in range(num_vertices):
        model.append(f"s.t. assign_{i}: sum{{k in 0..M-1}} x[{i},k] = 1;")

    # pouze použité strany
    for i in range(num_vertices):
        for k in range(num_vertices):
            model.append(f"s.t. use_{i}_{k}: x[{i},{k}] <= y[{k}];")

    # ve stejné straně pouze pokud je hrana
    for v1 in range(num_vertices):
        for v2 in range(v1 + 1, num_vertices):
            if (v1, v2) not in edges and (v2, v1) not in edges:
                for i in range(num_vertices):
                    model.append(f"s.t. no_edge_{v1}_{v2}_{i}: x[{v1},{i}] + x[{v2},{i}] <= 1;")

    return "\n".join(model)

def main(input_file):
    out_file = "out.txt"
    num_vertices, edges = read_graph(input_file)
    lp_model = generate_lp_model(num_vertices, edges)
    print(lp_model, file=open(out_file, "w"))


file_name = input("zadejte název souboru: ")
if file_name:
    main(file_name)
