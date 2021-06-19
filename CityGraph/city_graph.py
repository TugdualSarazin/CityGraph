import geopandas
import networkx as nx
import numpy as np
import pandas as pd
from shapely.geometry import LineString

from CityGraph.indicator.indicator10 import Indicator10, denormalize10
from CityGraph.indicator.indicator_group import IndicatorGroup


class CityGraph:
    npaths_key = 'npaths'

    def __init__(self, graph: nx.Graph,
                 in_indicators: [IndicatorGroup], out_indicator: Indicator10,
                 health_indicators: [IndicatorGroup],
                 geo_graph=True):
        self.graph = graph
        self.in_indicators = in_indicators
        self.out_indicator = out_indicator
        self.health_indicators = health_indicators
        self.geo_graph = geo_graph
        self.pos = self.pos()
        self.compute_indicators()

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
            all_grp_sum_val = 0
            all_grp_sum_factors = 0
            # Iterate all in group indicators
            for grp in self.in_indicators:
                norm_grp = grp.compute_group_edge(d)
                # If the group has match some keys add the value and factor
                if norm_grp is not None:
                    all_grp_sum_val += norm_grp * grp.grp_factor
                    all_grp_sum_factors += grp.grp_factor

            # Iterate all health group indicators
            #for grp in self.health_indicators:
            #    grp.compute_group_edge(d)

            # Compute all groups
            if all_grp_sum_factors > 0:
                # Normalize all groups indicator and write as edge property
                norm_all_grp = all_grp_sum_val / all_grp_sum_factors
                d[self.out_indicator.norm_key] = norm_all_grp
                d[self.out_indicator.key] = denormalize10(norm_all_grp)
            else:
                raise Exception(f'Cannot find any indicators for edge: {d}')

    def find_edge_by_attr(self, name, value):
        for u, v, attrs in self.graph.edges(data=True):
            if attrs.get(name) == value:
                return u, v
        return None, None

    def count_paths(self, paths):
        # Init all npaths to 0
        for _, _, d in self.graph.edges(data=True):
            d[self.npaths_key] = 0

        # Increment npaths
        for path in paths:
            for e in path.path_edges:
                self.graph.edges[e][self.npaths_key] += 1

    def save_geojson(self, filepath,
                     save_out_indic=True,
                     save_npaths=True,
                     save_grp_indic=True,
                     save_leaf_indic=True,
                     save_health_grp_indic=True,
                     save_health_leaf_indic=True,
                     with_normalize=False,
                     add_attributes=[]):
        # Define output keys
        output_keys = []
        output_keys += add_attributes

        # Add output indicator key
        if save_out_indic:
            output_keys.append(self.out_indicator.key)
            if with_normalize:
                output_keys.append(self.out_indicator.norm_key)

        # Add npaths key
        if save_npaths:
            output_keys.append(self.npaths_key)

        # Add input group indicators and leaf indicators
        for grp_indic in self.in_indicators:
            # Group indic key
            if save_grp_indic:
                output_keys.append(grp_indic.key)
                if with_normalize:
                    output_keys.append(grp_indic.norm_key)

            for indic in grp_indic.indicators:
                # Leaf indic key
                if save_leaf_indic:
                    output_keys.append(indic.key)
                    if with_normalize:
                        output_keys.append(indic.norm_key)

        # Add input health group indicators and health leaf indicators
        for health_grp_indic in self.health_indicators:
            # Group health indic key
            if save_health_grp_indic:
                output_keys.append(health_grp_indic.key)
                if with_normalize:
                    output_keys.append(health_grp_indic.norm_key)

            for health_indic in health_grp_indic.indicators:
                # Leaf indic key
                if save_health_leaf_indic:
                    output_keys.append(health_indic.key)
                    if with_normalize:
                        output_keys.append(health_indic.norm_key)

        # Iterate edges and convert to geojson lines
        geo_feats = []

        for u, v, d in self.graph.edges(data=True):
            # Add data filtered by key
            out_data = {k: v for k, v in d.items() if k in output_keys}
            # Add the geometry line
            out_data['geometry'] = LineString([u, v])
            geo_feats.append(out_data)

        # Convert to geopandas with crs=EPSG:25831
        gdf = geopandas.GeoDataFrame(pd.DataFrame(geo_feats), crs=25831)
        # Convert it to EPSG:4326
        gdf = gdf.to_crs(4326)
        # Save it as a GeoJson
        gdf.to_file(filepath, driver='GeoJSON')

        return gdf
