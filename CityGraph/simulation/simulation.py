import os

from shapely.geometry import Point

from CityGraph.agent_path import create_agent_paths, save_agent_paths
from CityGraph.city_graph import CityGraph
from CityGraph.graph_tool import load_graph
from CityGraph.indicator.indicator10 import Indicator10
from CityGraph.indicator.indicator_group import IndicatorGroup
from CityGraph.trajectory.nearest_semgent_ids import NearestSegmentIds


class Simulation:
    root_path = os.getcwd() + '/../'
    name = None
    network_fp_shp = None
    agents_seg_ids_fp_csv = None
    agent_paths_fp_geojson = None
    out_network_fp_geojson = None
    out_network_min_fp_geojson = None
    min_speed = None
    max_speed = None
    out_indicator = None
    in_indicators = None
    health_indicators = [
        IndicatorGroup(
            key='physical_health',
            grp_factor=1.,
            indicators=[
                Indicator10(key='H1.1NO2', factor=1., name='Physical health- NO2'),
                Indicator10(key='H1.2PM10', factor=1., name='Physical health- PM10'),
                Indicator10(key='H1.3PM2.5', factor=1., name='Physical health- PM2.5'),
                Indicator10(key='H1.4hie', factor=1., name='Physical health- Heat Island effect'),
                Indicator10(key='H1.5accide', factor=1., name='Physical health- Accidents '),
            ]),
        IndicatorGroup(
            key='mental_health',
            grp_factor=1.,
            indicators=[
                Indicator10(key='H2.1noise', factor=1., name='Mental Health - Noise'),
                Indicator10(key='H2.2visibi', factor=1., name='Mental Health - Visibility'),
                Indicator10(key='H2.3ndvi', factor=1., name='Mental health- NDVI'),
                Indicator10(key='H2.4insec', factor=1., name='Mental health- Insecurity'),
            ]),
        IndicatorGroup(
            key='social_health',
            grp_factor=1.,
            indicators=[
                Indicator10(key='H3.1acc_pub', factor=1., name='Social Health- accessibility to public transport'),
                Indicator10(key='H3.2acc_gen', factor=1., name='Social Health- general accessibility'),
                Indicator10(key='H3.3poi_ped', factor=1.,
                            name='Social Health - proximity of poi ( recreation, retail, restaurant for ped)'),
                Indicator10(key='H3.3poi_bike', factor=1.,
                            name='Social Health - proximity of poi (school, work, recreation for bike)'),
            ])
    ]

    def generate_agent_segment_ids(self, traj_gdf):
        print(f"\n==== Gen {self.name} start end ID_unique ====")

        # Load nearest with segments network
        nearest = NearestSegmentIds(self.network_fp_shp)
        print(f'Loaded {self.name} segments ({len(nearest.segments_pts)})')

        # Filter trajectories with max_speed attribute
        traj_sim = traj_gdf[traj_gdf['max_speed'].between(self.min_speed, self.max_speed)].copy()
        print(f'Filtered {self.name} trajectories ({len(traj_sim)})')

        # Extract start points
        start_pts = traj_gdf.geometry.apply(lambda geo: Point(geo.coords[0]))
        traj_sim['start_latitude'] = start_pts.y
        traj_sim['start_longitude'] = start_pts.x
        # Find start nearest segment ID
        traj_sim['start_ID_unique'] = nearest.find_nearest_segments(start_pts)
        print(f"Found {self.name} nearest START points ({len(traj_sim['start_ID_unique'].notnull())})")

        # Extract end points
        end_pts = traj_gdf.geometry.apply(lambda geo: Point(geo.coords[-1]))
        traj_sim['end_latitude'] = end_pts.y
        traj_sim['end_longitude'] = end_pts.x
        # Find end nearest segment ID
        traj_sim['end_ID_unique'] = nearest.find_nearest_segments(end_pts)
        print(f"Found {self.name} nearest END points ({len(traj_sim['end_ID_unique'].notnull())})")

        # Save it to csv
        traj_sim.drop('geometry', axis=1).to_csv(self.agents_seg_ids_fp_csv)

        return traj_sim

    def run_agent_paths(self):
        print(f'### Start {self.name} ###')

        # Load city graph
        graph = CityGraph(
            graph=load_graph(self.network_fp_shp),
            in_indicators=self.in_indicators,
            out_indicator=self.out_indicator,
            health_indicators=self.health_indicators
        )
        print(f"Loaded {self.name} network ({len(graph.graph.edges)} edges)")

        # Load agent start points and compute their paths
        paths = create_agent_paths(graph, self.agents_seg_ids_fp_csv)
        # Update the graph with the count path property
        graph.count_paths(paths)

        # Save the agent path to geojson
        save_agent_paths(paths, self.agent_paths_fp_geojson)

        # print(d)

        # Save the output network to geojson 4326 with all data
        gdf = graph.save_geojson(filepath=self.out_network_fp_geojson,
                                 save_out_indic=True,
                                 save_npaths=True,
                                 save_grp_indic=True,
                                 save_leaf_indic=True,
                                 save_health_grp_indic=False,
                                 save_health_leaf_indic=False,
                                 with_normalize=False,
                                 add_attributes=['fclass', 'name', 'ID_unique'])

        # Save the output network to geojson 4326 with minimal data
        gdf = graph.save_geojson(filepath=self.out_network_min_fp_geojson,
                                 save_out_indic=True,
                                 save_npaths=True,
                                 save_grp_indic=False,
                                 save_leaf_indic=False,
                                 save_health_grp_indic=False,
                                 save_health_leaf_indic=False,
                                 with_normalize=False,
                                 add_attributes=[])

        print(f"Saved output network ({len(gdf)} lines) to {self.out_network_fp_geojson}")
