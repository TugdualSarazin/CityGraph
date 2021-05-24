import geojson
import pandas as pd
from geojson import FeatureCollection

from CityGraph.agent_path import AgentPath
from CityGraph.city_graph import CityGraph
from CityGraph.graph_tool import load_graph
from CityGraph.indicator import IndicatorGroup, Indicator10


def create_agent_paths(graph, filepath):
    df_agents = pd.read_csv(filepath,
                            header=0,
                            names=['agent_id', 'seg_id_start', 'seg_id_stop'],
                            usecols=['agent_id', 'seg_id_start', 'seg_id_stop'],
                            skip_blank_lines=True)
    f = lambda row: AgentPath(graph, row.agent_id, int(row.seg_id_start), int(row.seg_id_stop))
    return df_agents.apply(f, axis=1).to_list()


def save_agent_paths(agent_paths: [AgentPath], filepath):
    line_agent_paths = [apath.geojson_line() for apath in agent_paths]
    with open(filepath, 'w') as geojson_file:
        geojson.dump(obj=FeatureCollection(line_agent_paths), fp=geojson_file)


def process_pedestrian():
    grp_intersection_safety = IndicatorGroup(
        key='intersection_safety',
        grp_factor=1.05,
        indicators=[
            Indicator10(key='1.1', factor=2.1, name='Cross walks'),
            Indicator10(key='1.2', factor=2.4, name='Ladder Crosswalks'),
            Indicator10(key='1.3', factor=2.4, name='Countdown in signal'),
            Indicator10(key='1.5', factor=2.4, name='Crosswalk scramble'),
            Indicator10(key='1.6', factor=2.4, name='No Turn on Red'),
            Indicator10(key='1.7', factor=2.4, name='Intersection traffic calming features'),
            Indicator10(key='1.8', factor=2.4, name='Additional Signs for pedestrians')
        ])

    grp_traffic = IndicatorGroup(
        key='traffic',
        grp_factor=0.76,
        indicators=[
            Indicator10(key='2.1num_lan', factor=2.4, name='Number of lanes'),
            Indicator10(key='2.2twoway', factor=1.8, name='Two way traffic'),
            Indicator10(key='2.3speed', factor=2.7, name='Vehicle speed')
        ])

    grp_street_design = IndicatorGroup(
        key='street_design',
        grp_factor=1.1,
        indicators=[
            Indicator10(key='3.1Width', factor=2.4, name='Width of Sidewalk'),
            Indicator10(key='3.3Obstacl', factor=2.1, name='Large SW Obstructions'),
            Indicator10(key='3.5Cuts', factor=1.8, name='Driveway Cuts'),
            Indicator10(key='3.6Trees', factor=1.8, name='Trees'),
            Indicator10(key='3.8Sitting', factor=1.8, name='Public Sitting'),
            Indicator10(key='3.7Buffer', factor=2.1, name='Presence of a Buffer'),
        ])

    grp_land_use = IndicatorGroup(
        key='land_use',
        grp_factor=0.18,
        indicators=[
            Indicator10(key='4.1artsite', factor=1.8, name='Public Art/ Historic Sites'),
            Indicator10(key='4.2restaur', factor=2.1, name='Restaurant and Retail Use'),
        ])

    grp_perceived_safety = IndicatorGroup(
        key='perceived_safety',
        grp_factor=0.43,
        indicators=[
            Indicator10(key='5.2litter', factor=1.8, name='Litter'),
            Indicator10(key='5.3nocturn', factor=2.4, name='Lighting (now only nocturnal economic activities)'),
            Indicator10(key='5.4constru', factor=1.8, name='Construction sites'),
            Indicator10(key='5.5ruins', factor=1.8, name='Abandoned buildings'),
        ])

    folder = '../data/01_PEQI_Pedestrian Network/'

    graph = CityGraph(
        graph=load_graph(folder + 'Pedestrian_peqi_fin.shp'),
        indicator_groups=[grp_intersection_safety, grp_traffic, grp_street_design, grp_land_use, grp_perceived_safety]
    )

    paths = create_agent_paths(graph, folder + 'footfall_pedestrian.csv')
    graph.count_paths(paths)

    save_agent_paths(paths, folder + '/pedestrian_agent_paths.geojson')

    graph.save_geojson(folder + '/pedestrian.geojson')


def main():
    process_pedestrian()

    # pedestrian_paths = create_agent_paths(pedestrian_graph, '../data/01_PEQI_Pedestrian Network/agent_pedestrian_start_stop.csv')

    # graph_drawer = Drawer(car_graph, dpi=200, node_size=0, edge_size=2)
    # graph_drawer.static_agents_paths(car_paths)
    # graph_drawer.draw_weights()


if __name__ == "__main__":
    main()
