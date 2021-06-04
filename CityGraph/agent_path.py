import numpy as np
import pandas as pd
import networkx as nx
import geojson
from geojson import FeatureCollection, LineString, Feature
from networkx import NetworkXNoPath

from CityGraph.city_graph import CityGraph
from CityGraph.graph_tool import path_nodes_to_edges


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
        self.has_path = True
        self.find_path(source, target)
        self.weight = self.process_weight()

        # print(f'Path {agent_id}: {source_seg_id} -> {target_seg_id} = {self.weight}')

    def find_path(self, source, target):
        try:
            self.path_nodes = nx.dijkstra_path(self.graph.graph, source, target,
                                               weight=self.graph.out_indicator.norm_key)
            self.path_edges = path_nodes_to_edges(self.path_nodes)
        except NetworkXNoPath as e:
            self.path_nodes = None
            self.path_edges = None
            self.has_path = False
            print(f'## Cannot find a path for {self.agent_id}: {source} -> {target}')

    def process_weight(self):
        weight = 0
        # Compute weight if has edges
        if self.path_edges is not None:
            for edge in self.path_edges:
                weight += self.graph.graph.get_edge_data(edge[0], edge[1])[self.graph.out_indicator.norm_key]
        return weight

    def geojson_line(self):
        line = LineString(self.path_nodes)
        properties = {'agent_id': self.agent_id, 'edge_weight': self.weight}
        return Feature(geometry=line, properties=properties)


def create_agent_paths(city_graph, filepath, nrows=None):
    # Load start and end points
    df_agents = pd.read_csv(filepath, usecols=['device_id', 'start_ID_unique', 'end_ID_unique'], nrows=nrows)
    print(f'Loaded start end points agents ({len(df_agents)})')
    # Create agents paths
    f = lambda row: AgentPath(city_graph, row.device_id, int(row.start_ID_unique), int(row.end_ID_unique))
    agents_paths = df_agents.apply(f, axis=1).to_list()
    # filter not valid paths
    agents_paths = [apath for apath in agents_paths if apath.has_path]
    print(f'Computed agents paths ({len(agents_paths)})')
    return agents_paths


def save_agent_paths(agent_paths: [AgentPath], filepath):
    line_agent_paths = [apath.geojson_line() for apath in agent_paths]
    with open(filepath, 'w') as geojson_file:
        geojson.dump(obj=FeatureCollection(line_agent_paths), fp=geojson_file)
