import sys
import os
import time
import argparse
import random
from progress import Progress  #Importing progress from progress.py

def load_graph(args):
    """Load graph from text file."""
    #Stores graph, nodes and edges
    graph = {}
    with args.datafile as f:
        for line in f:
            node, target = line.strip().split()
            #Create list if not already in graph
            if node not in graph:
                graph[node] = []
            graph[node].append(target)
    return graph

def build_adjacency_matrix(graph):
    """Convert graph to adjacency matrix."""
    #List all nodes in the graph
    nodes = list(graph.keys())
    #Map each node to an index for matrix representation
    node_indices = {node: i for i, node in enumerate(nodes)}
    #Initialize an adjacency matrix with zeros
    size = len(nodes)
    adjacency_matrix = [[0] * size for _ in range(size)]

    for node, targets in graph.items():
        row = node_indices[node]
        for target in targets:
            col = node_indices[target]
            adjacency_matrix[row][col] = 1  # Set edge to 1
    return adjacency_matrix

def build_edge_list(graph):
    """Convert graph to edge list."""
    #Initialize an edge list as a list of tuples
    edge_list = []
    for node, targets in graph.items():
        for target in targets:
            edge_list.append((node, target))
    return edge_list

def print_stats(graph):
    """Print number of nodes and edges in the graph."""
    #Initialises number of nodes as key in directory
    num_nodes = len(graph)
    #Initialises number of edges as total of all lengths of list
    num_edges = sum(len(targets) for targets in graph.values())
    # Print graph statistics
    print(f"Graph has {num_nodes} nodes and {num_edges} edges.")

def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation."""
    #Set hit counts for each of the nodes to 0
    hit_count = {node: 0 for node in graph}
    #Gets a list of all nodes in graph
    nodes = list(graph.keys())
    #Start random walker at random node
    current_node = random.choice(nodes)
    #Increase hit count per node
    hit_count[current_node] += 1

    #Take out the number of walk repetitions
    for _ in range(args.repeats):
        #If statement if node has no outgoing edges randomly pick another
        if not graph[current_node]:
            current_node = random.choice(nodes)
        else:
            #Else statment to randomly pick one of current nodes outgoing edges
            current_node = random.choice(graph[current_node])
        #Increase hit counter for current node
        hit_count[current_node] += 1

    total_hits = sum(hit_count.values())
    return {node: count / total_hits for node, count in hit_count.items()}

def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation."""
    #List of all nodes in graph
    nodes = list(graph.keys())
    #Total number of nodes in the graph
    num_nodes = len(nodes)
    node_prob = {node: 1 / num_nodes for node in nodes}

    #Complete specific number of iterations
    for _ in range(args.steps):
        #Initialize the next set of probabilities to zero
        next_prob = {node: 0 for node in nodes}
        for node, targets in graph.items():
            if targets:
                contribution = node_prob[node] / len(targets)
                for target in targets:
                    next_prob[target] += contribution
            else:
                contribution = node_prob[node] / num_nodes
                for target in nodes:
                    next_prob[target] += contribution
        #Update the probabilities for the next iteration
        node_prob = next_prob

    #Return the final probabilities
    return node_prob

#Command-line argument parsing
parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions for stochastic method")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps for distribution method")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")
parser.add_argument('--representation', choices=('list', 'matrix', 'edges'), default='list',
                    help="Select graph representation: list, matrix, or edge list")

if __name__ == '__main__':
    #Parse command-line arguments
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    #Load the graph from the specified file
    graph = load_graph(args)

    #Generate alternative representations if needed
    if args.representation == 'matrix':
        adjacency_matrix = build_adjacency_matrix(graph)
        print("Adjacency Matrix Representation:")
        for row in adjacency_matrix:
            print(row)
    elif args.representation == 'edges':
        edge_list = build_edge_list(graph)
        print("Edge List Representation:")
        print(edge_list)

    #Print graph statistics
    print_stats(graph)

    #Measure the time taken to calculate PageRank
    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    elapsed_time = stop - start

    #Sort the results by PageRank in descending order
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    #Display the top-ranked pages
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k, v in top[:args.number]))
    #Display the time taken for the calculation
    sys.stderr.write(f"Calculation took {elapsed_time:.2f} seconds.\n")
