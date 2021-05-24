import networkx as nx
from geojson import LineString, Feature

from CityGraph.city_graph import CityGraph
from CityGraph.graph_tool import path_nodes_to_edges
import numpy as np


class AgentPath:
    EDGE_ID_KEY = 'ID_unique'
    G = None
    agent_id = None
    path_edges = None
    weight = None
    color = None

    def __init__(self, graph: CityGraph, agent_id, source_seg_id, target_seg_id, color=None):

        # Save attributes
        self.graph = graph
        self.agent_id = agent_id
        if color:
            self.color = color
        else:
            self.color = np.random.rand(3).tolist()

        # Find source and target
        source, _ = graph.find_edge_by_attr(AgentPath.EDGE_ID_KEY, source_seg_id)
        if not source:
            raise Exception(f'Cannot find edge for source {AgentPath.EDGE_ID_KEY}[{agent_id}]')

        _, target = graph.find_edge_by_attr(AgentPath.EDGE_ID_KEY, target_seg_id)
        if not target:
            raise Exception(f'Cannot find edge for target {AgentPath.EDGE_ID_KEY}[{agent_id}]')

        # Process path
        self.find_path(source, target)
        self.weight = self.process_weight()

        print(f'Path {agent_id}: {source_seg_id} -> {target_seg_id} = {self.weight}')

    def find_path(self, source, target):
        self.path_nodes = nx.dijkstra_path(self.graph.graph, source, target, weight='weight')
        self.path_edges = path_nodes_to_edges(self.path_nodes)

    def process_weight(self):
        weight = 0
        for edge in self.path_edges:
            weight += self.graph.graph.get_edge_data(edge[0], edge[1])['weight']
        return weight

    def geojson_line(self):
        line = LineString(self.path_nodes)
        properties = {'agent_id': self.agent_id, 'weight': self.weight}
        return Feature(geometry=line, properties=properties)

