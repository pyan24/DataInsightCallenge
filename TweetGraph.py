import re
import json
import networkx as nx
import itertools

# Create a graph object G
G = nx.Graph()
# Calculate average_degree
class GetAveDegree():
    def __init__(self , text_list , created_time):
        self.textlist = text_list
        self.createdtime = created_time

    def TweetAveDegree(self):
        # Build graph and calculate graph's average_degree

        # Add nodes
        G.add_nodes_from(self.textlist,time = self.createdtime)

        # Get edges list
        edges = []
        for b in itertools.combinations(self.textlist,2):
            edges.append(b)

        # Add edges
        G.add_edges_from(edges,time =self.createdtime)

        # Calculate average_degree
        degrees = G.degree()
        sum_of_edges = sum(degrees.values())
        # Average_degree = Sum of edges degree / total number of nodes
        average_degree = sum_of_edges/G.number_of_nodes()
        return average_degree


