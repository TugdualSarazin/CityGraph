import os

import pandas as pd

from CityGraph.agent_path_tools import create_agent_paths, save_agent_paths
from CityGraph.city_graph import CityGraph
from CityGraph.graph_tool import load_graph
from CityGraph.trajectory.nearest_semgent_ids import NearestSegmentIds


class Simulation:
    root_path = os.getcwd()+'/../'
    name = None
    network_fp_shp = None
    agents_seg_ids_fp_csv = None
    agent_paths_fp_geojson = None
    out_network_fp_geojson = None
    min_speed = None
    max_speed = None
    indicator_groups = None

    def generate_agent_segment_ids(self, ff_start_pts, ff_end_pts):
        # Load nearest with segments network
        nearest = NearestSegmentIds(self.network_fp_shp)
        print(f'Loaded {self.name} segments ({len(nearest.segments_pts)})')

        # Filter start points based on max_speed attribute
        sim_start_pts = ff_start_pts[ff_start_pts['max_speed'].between(self.min_speed, self.max_speed)]
        # Copy start data
        sim_start_pts = sim_start_pts.reset_index().rename({'index': 'datetime'}, axis=1).set_index('device_id')
        start_end_seg_ids = pd.DataFrame(index=sim_start_pts.index)
        start_end_seg_ids['start_datetime'] = sim_start_pts['datetime']
        start_end_seg_ids['start_latitude'] = sim_start_pts['LATITUDE']
        start_end_seg_ids['start_longitude'] = sim_start_pts['LONGITUDE']
        # Find start nearest segment ID
        nearest_start_pts = nearest.find_nearest_segments(sim_start_pts)
        print(f'Found {self.name} nearest START points ({len(nearest_start_pts)})')
        start_end_seg_ids['start_ID_unique'] = nearest_start_pts

        # Filter end points based on max_speed attribute
        sim_end_pts = ff_end_pts[ff_end_pts['max_speed'].between(self.min_speed, self.max_speed)]
        # Copy end data
        sim_end_pts = sim_end_pts.reset_index().rename({'index': 'datetime'}, axis=1).set_index('device_id')
        start_end_seg_ids['end_datetime'] = sim_end_pts['datetime']
        start_end_seg_ids['end_latitude'] = sim_end_pts['LATITUDE']
        start_end_seg_ids['end_longitude'] = sim_end_pts['LONGITUDE']
        # Find end nearest segment ID
        nearest_end_pts = nearest.find_nearest_segments(sim_end_pts)
        print(f'Found {self.name} nearest END points ({len(nearest_end_pts)})')
        start_end_seg_ids['end_ID_unique'] = nearest_end_pts

        # Save it to csv
        start_end_seg_ids.to_csv(self.agents_seg_ids_fp_csv)

        return start_end_seg_ids

    def run_agent_paths(self):
        print(f'### Start {self.name} ###')

        # Load city graph
        graph = CityGraph(
            graph=load_graph(self.network_fp_shp),
            indicator_groups=self.indicator_groups
        )

        # Load agent start points and compute their paths
        paths = create_agent_paths(graph, self.agents_seg_ids_fp_csv)
        # Update the graph with the count path property
        graph.count_paths(paths)

        save_agent_paths(paths, self.agent_paths_fp_geojson)

        graph.save_geojson(self.out_network_fp_geojson)
