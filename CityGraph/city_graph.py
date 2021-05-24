import geojson
import networkx as nx
import numpy as np
from geojson import FeatureCollection, LineString, Feature, GeoJSON, GeoJSONEncoder

from CityGraph.indicator import IndicatorGroup


class CityGraph:
    def __init__(self, graph: nx.Graph, indicator_groups: [IndicatorGroup], geo_graph=True):
        self.graph = graph
        self.indicator_groups = indicator_groups
        self.geo_graph = geo_graph
        self.pos = self.pos()
        self.compute_indicators()
        # EdgeType.set_agent_type_weights(self.graph)

    # TODO: need unit test
    def pos(self):
        for node in self.graph.nodes():
            if not (type(node) == tuple and type(node[0]) == float and type(node[1]) == float):
                # TODO: raise error
                is_geo = False
                break
        if self.geo_graph:
            return dict([(n, np.array(n)) for n in self.graph.nodes()])
        else:
            return nx.spring_layout(self.graph)

    def compute_indicators(self):
        # Iterate edges
        for u, v, d in self.graph.edges(data=True):
            # length = d['length']
            all_grp_sum_val = 0
            all_grp_sum_factors = 0
            # Iterate all group indicators
            for grp in self.indicator_groups:
                norm_grp = grp.compute_group_edge(d)
                # If the group has match some keys add the value and factor
                if norm_grp is not None:
                    all_grp_sum_val += norm_grp * grp.grp_factor
                    all_grp_sum_factors += grp.grp_factor

            # Compute all groups
            if all_grp_sum_factors > 0:
                # Normalize all groups indicator and save
                norm_all_grp = all_grp_sum_val / all_grp_sum_factors
                d['weight'] = norm_all_grp
            else:
                raise Exception(f'Cannot find any indicators for edge: {d}')

    def find_edge_by_attr(self, name, value):
        for u, v, attrs in self.graph.edges(data=True):
            if attrs.get(name) == value:
                return u, v
        return None, None

    def count_paths(self, paths):
        # Init npath to 0
        for _, _, d in self.graph.edges(data=True):
            d['npaths'] = 0

        # Increment npath
        for path in paths:
            for e in path.path_edges:
                self.graph.edges[e]['npaths'] += 1

    def save_geojson(self, filepath):
        # Iterate edges and convert to geojson lines
        geo_feats = []
        for u, v, d in self.graph.edges(data=True):
            line = LineString([u, v])
            geo_feats.append(Feature(geometry=line, properties=d))
        # Save geojson features
        with open(filepath, 'w') as geojson_file:
            geojson.dump(obj=FeatureCollection(geo_feats), fp=geojson_file)
