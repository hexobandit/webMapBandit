# 
# 
#   WebMapBandit is a tool that maps GET, POST, and other HTTP requests made by a website by processing .har (HTTP Archive) files. 
#   It visualizes the network of requests using different layouts and an adjustable URL depth representation.
#
#


############ THINGS TO CHANGE IN HERE BUDDY ############

har_file_path = 'name-of-the-har-file.har' 
depth_limit = 0  # Link depth 
graph_layout = "neato" # 'dot' neato, twopi, circo, fdp, sfdp, patchwork, osage

############ THINGS TO CHANGE IN HERE BUDDY ############


import json

def parse_har_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        har_data = json.load(file)

    # Get the starting point from the 'pages' section
    starting_point = har_data['log']['pages'][0]['title']  # First page's title is the URL

    entries = har_data['log']['entries']
    connections = []
    url_sequence = []

    for entry in entries:
        url = entry['request']['url']
        method = entry['request']['method']
        connections.append((url, method))
        url_sequence.append(url) 

    return connections, starting_point, url_sequence

from urllib.parse import urlparse

############

def get_url_depth(url, depth_limit):
    parsed_url = urlparse(url)
    
    # Combine subdomain and domain (netloc)
    domain = parsed_url.netloc

    # Split the path by '/' and limit the depth
    path_parts = parsed_url.path.strip('/').split('/')[:depth_limit]

    # Reconstruct the URL with depth limit
    depth_url = f"{domain}/{'/'.join(path_parts)}"
    
    return depth_url

############

import networkx as nx
import matplotlib.pyplot as plt

def create_graph(connections, depth_limit, starting_point):
    graph = nx.DiGraph()

    # Add the starting point node
    root = get_url_depth(starting_point, depth_limit)
    graph.add_node(root)
    graph.nodes[root]['method'] = 'START'

    # Add the rest of the nodes and edges
    for url, method in connections:
        node = get_url_depth(url, depth_limit)
        graph.add_node(node)
        graph.nodes[node]['method'] = method
        graph.add_edge(root, node, method=method)  # Connect the root to each URL
        root = node  # Continue connecting in sequence

    return graph

############

import textwrap

def wrap_node_labels(graph, width=20):
    labels = {}
    for node in graph.nodes():
        labels[node] = "\n".join(textwrap.wrap(node, width=width))
    return labels

def draw_cascade_graph(graph, starting_point, url_sequence):
    # Use Graphviz to create a cascade layout
    pos = nx.nx_agraph.graphviz_layout(graph, prog=graph_layout, args='-Granksep=8')  # args='-Granksep=5' doesnt really do anything
    
    plt.figure(figsize=(16, 9))  # Set the figure size to 16:9 ratio
    
    # Draw starting node
    starting_node = get_url_depth(starting_point, depth_limit)
    nx.draw_networkx_nodes(graph, pos, nodelist=[starting_node], node_size=5000, node_color='orange')
    
    # Draw nodes and edges
    nx.draw_networkx_nodes(graph, pos, node_size=200, node_color='lightgrey')
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), arrowstyle='->')
    
    # Wrap node labels to multiple lines if necessary
    wrapped_labels = wrap_node_labels(graph) 
    
    # Draw node labels with adjusted font size
    nx.draw_networkx_labels(graph, pos, labels=wrapped_labels, font_size=8, font_weight='bold')

    # Display all HTTP methods on the edges (GET, POST, PUT, DELETE, etc.)
    edge_labels = {(u, v): d['method'] for u, v, d in graph.edges(data=True)}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)

    plt.margins(x=0.1, y=0.1)

    plt.show()

    # # Print the URLs in order from top to bottom
    # print("\nURLs in order of appearance:")
    # for index, url in enumerate(url_sequence):
    #     print(f"{index + 1}. {url}")

############

connections, starting_point, url_sequence = parse_har_file(har_file_path)  
graph = create_graph(connections, depth_limit, starting_point) 
draw_cascade_graph(graph, starting_point, url_sequence)

############ 

# Summary of Layouts:

# 	•	dot: Hierarchical layout (default for directional graphs).
# 	•	neato: Force-directed layout for general graphs.
# 	•	fdp: Force-directed layout optimized for larger graphs.
# 	•	sfdp: Scalable version of fdp for very large graphs.
# 	•	twopi: Radial layout with concentric circles.
# 	•	circo: Circular layout, good for cyclic graphs.
# 	•	patchwork: Grid/tiling layout, compact and rectangular.
# 	•	osage: Clustered layout for grouped nodes.
