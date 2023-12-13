"""
IMPORTS
mpi4py - Fornece funcionalidade MPI (Message Passing Interface) para processamento paralelo
time: Permite medir o tempo de execução, utilizado na comparação da estrutura paralelo e serial
networkx: Usado para gerar grafos aleatórios
random: seleciona um nó inicial aleatório para o algoritmo BFS
"""
from mpi4py import MPI
import time
import networkx as nx
import random

"""
GENERATE HUGE GRAPH
Cria um grafo aleatório usando o modelo Erdos-Renyi com um número especificado de nós
(num_nodes) e grau médio (avg_degree).
O grafo é representado como uma lista de adjacências (adj_list), onde cada nó mapeia para uma lista de seus 
vizinhos.
"""
def generate_huge_graph(num_nodes, avg_degree):
    graph = nx.erdos_renyi_graph(num_nodes, avg_degree / (num_nodes - 1))
    adj_list = {node: list(graph.neighbors(node)) for node in graph.nodes()}
    return adj_list

"""
PARALLEL BFS
executa uma BFS em um grafo em paralelo usando MPI.

Inicialização MPI: comm, rank e tamanho são obtidos para determinar a classificação do processo e o número
total de processos, decidi ir aumentando esse valor, até chegar em 10 processos.

Particionamento de subgrafos: O grafo é dividido em subgrafos com base na classificação do processo.

subgraph_size: Tamanho de cada subgrafo.
subgraph_start e subgraph_end: Definem o intervalo de nós atribuídos ao processo atual.
BFS local: cada processo explora seu subgrafo usando BFS, começando no start_node especificado.

local_visited: definido para identificar nós visitados localmente.
MPI Gather: Todos os processos reúnem seus conjuntos locais visitados no processo raiz (rank 0).

all_visited: Lista contendo conjuntos locais visitados de todos os processos.
Atualização do Conjunto Global: O processo raiz atualiza um conjunto visitado global (global_visited)
mesclando todos os conjuntos visitados locais.

Valores de retorno: o processo raiz retorna o conjunto global visitado, enquanto outros processos retornam 
um conjunto vazio.
"""
def parallel_bfs(graph, start_node):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size() 
    print(size)

    subgraph_size = len(graph) // size
    subgraph_start = rank * subgraph_size
    subgraph_end = (rank + 1) * subgraph_size

    local_visited = set()

    if start_node in range(subgraph_start, subgraph_end):
        local_visited.add(start_node)

    for current_node in range(subgraph_start, subgraph_end):
        if current_node in local_visited:
            for neighbor in graph[current_node]:
                if neighbor not in local_visited:
                    local_visited.add(neighbor)

    all_visited = comm.gather(local_visited, root=0)

    if rank == 0:
        global_visited = set()
        for visited_set in all_visited:
            global_visited.update(visited_set)
        return global_visited
    else:
        return set()
    
"""
MAIN
num_nodes_huge e avg_degree_huge: Defina os parâmetros para o grafo.
huge_graph: Gera um grafo aleatório.
start_node_huge: Escolha um nó inicial aleatório para BFS.
result_huge: Chame a função BFS paralela no grafo.
Imprime o resultado no processo raiz junto com o tempo de execução.
"""
if __name__ == "__main__":
    start_time = time.time()

    # Define the number of nodes and average degree for the huge graph
    num_nodes_huge = 10000
    avg_degree_huge = 100

    # Generate the huge graph
    huge_graph = generate_huge_graph(num_nodes_huge, avg_degree_huge)

    # Specify the starting node for BFS
    start_node_huge = random.randint(0, num_nodes_huge - 1)

    # Call the parallel BFS function on the huge graph
    result_huge = parallel_bfs(huge_graph, start_node_huge)

    # Print the result at the root process
    #if MPI.COMM_WORLD.Get_rank() == 0:
        #print("Parallel BFS Result (Huge Graph):", result_huge)
    
    end_time = time.time()
    print("Execution Time:", end_time - start_time, "seconds")
