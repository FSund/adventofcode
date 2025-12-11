import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List
from pathlib import Path
from typing import Dict, List, Set, Tuple
from pyvis.network import Network
from typing import Dict, List


def get_input(filename):
    script_dir = Path(__file__).parent
    lines = []
    with open(script_dir / filename) as file:
        for line in file:
            lines.append(line.strip("\n"))

    return lines


def visualize_graph_pyvis(graph: Dict[str, List[str]], output_file: str = "graph.html"):
    """
    Create an interactive graph with physics simulation.
    Opens in browser - very smooth and interactive.
    """
    net = Network(
        height="1200px", 
        width="100%", 
        directed=True, 
        notebook=False
    )
    
    # Add nodes and edges
    all_nodes = set(graph.keys())
    for neighbors in graph.values():
        all_nodes.update(neighbors)
    
    # Nodes to highlight
    # highlight_nodes = {"out", "you", "srv", "fft", "dac"}
    
    for node in all_nodes:
        if node in ["fft", "dac"]:
            net.add_node(node, label=node, color='red', size=25)
        elif node in ["srv", "you"]:
            net.add_node(node, label=node, color='orange', size=25)
        elif node == "out":
            net.add_node(node, label=node, color='green', size=25)
        else:
            net.add_node(node, label=node)
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            net.add_edge(node, neighbor)
    
    # Configure physics for smooth interaction
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "stabilization": {
          "iterations": 100
        },
        "barnesHut": {
          "gravitationalConstant": -8000,
          "springLength": 150
        }
      }
    }
    """)
    
    net.show(output_file, notebook=False)
    print(f"Graph saved to {output_file} - open in browser")


# Example usage
if __name__ == "__main__":
    lines = get_input("input.txt")

    graph = {}
    for line in lines:
        node, neighbors = [e.strip() for e in line.split(":")]
        neighbors = [e.strip() for e in neighbors.split(" ")]

        graph[node] = neighbors
    
    # visualize_graph(graph, "Example Directed Graph")

    visualize_graph_pyvis(graph)
