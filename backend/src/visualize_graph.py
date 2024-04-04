import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

class VisualizeGraph:
    def __init__(self, graph, source, destinations):
        self.graph = graph
        self.source = source
        self.destinations = destinations

    def create_plot(self):
        # Generate positions for the nodes
        pos = nx.kamada_kawai_layout(self.graph)

        # Initialize a list to store node colors
        node_colors = []

        # Assign colors to nodes based on whether they are source nodes or destination nodes
        for node in self.graph.nodes():
            if node in self.source:
                node_colors.append('green')  # Color for source nodes
            elif node in self.destinations:
                node_colors.append('red')  # Color for destination nodes
            else:
                node_colors.append('lightblue')  # Default color

        # Draw the graph with specified node colors
        nx.draw(self.graph, pos, with_labels=True, node_size=800, node_color=node_colors, font_size=10, font_color='black')

        # Draw edge labels
        labels = nx.get_edge_attributes(self.graph, 'flow')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        # Add title
        plt.title("Evacuation Network")

        # Show the plot
        plt.show()
