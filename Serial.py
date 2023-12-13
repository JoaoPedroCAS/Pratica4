"""
IMPORTS
time: Permite medir o tempo de execução, utilizado na comparação da estrutura paralelo e serial
networkx: Usado para gerar grafos aleatórios
random: seleciona um nó inicial aleatório para o algoritmo BFS
queue: Implementa a FIFO
"""
import networkx as nx
import random
import queue
import time

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
SERIAL BFS
executa a (BFS) em um grafo sequencialmente.
bfs_queue: Uma fila para identificar nós a serem visitados.
visitados: um conjunto para identificar os nós visitados.
Inicia a partir do start_node especificado e explora vizinhos iterativamente, 
adicionando vizinhos não visitados à fila e marcando-os como visitados.
"""
def serial_bfs(graph, start_node):
    bfs_queue = queue.Queue()
    visited = set()

    bfs_queue.put(start_node)
    visited.add(start_node)

    while not bfs_queue.empty():
        current_node = bfs_queue.get()

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                bfs_queue.put(neighbor)
               '' visited.add(neighbor)

    return visited

"""
MAIN
num_nodes e avg_degree: Define parâmetros para o grafo.
enorme_graph: Gera um grafo aleatório.
start_node: Especifica o nó inicial para BFS.
start_time: registra a hora de início.
resultado: chama a função serial BFS no grafo enorme.
Imprime o resultado do BFS e o tempo de execução.
"""
if __name__ == "__main__":
    start_time = time.time()
    # Define the number of nodes and average degree for the huge graph
    num_nodes = 10000  # Adjust this value for a larger or smaller graph
    avg_degree = 100

    # Generate a huge graph
    huge_graph = generate_huge_graph(num_nodes, avg_degree)

    # Specify the starting node for BFS
    start_node = 0

    # Measure the execution time of serial BFS
    
    result = serial_bfs(huge_graph, start_node)
    

    # Print the result and execution time
    print("Serial BFS Result:", result)
    end_time = time.time()
    print("Execution Time:", end_time - start_time, "seconds")
