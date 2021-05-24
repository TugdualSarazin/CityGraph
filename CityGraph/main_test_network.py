import networkx as nx

from CityGraph.Optimizer import Optimizer, Agent
from CityGraph.agent_path import AgentPath
from CityGraph.city_graph import CityGraph
from CityGraph.edge_type_opti import EdgeType
from CityGraph.graph_drawer import Drawer
from CityGraph.graph_tool import find_edge_by_attr, load_graph, print_edges, find_node_by_edge_type


def main():
    G = load_graph('../data/Network/22@_Road_network_4326.shp')
    EdgeType.set_weight(G)
    city_graph = CityGraph(G, geo_graph=True)

    # graph_drawer = GraphDrawer(G, dpi=300, node_size=1, edge_size=2)
    graph_drawer = Drawer(city_graph, dpi=200, node_size=0, edge_size=2)
    #graph_drawer.draw_weights()
    # print_edges(G)

    _, source_pedestrian = find_edge_by_attr(G, 'osm_id', '648433598')
    #_, source_car = find_edge_by_attr(G, 'OBJECTID', 243)
    #_, target = find_edge_by_attr(G, 'OBJECTID', 217)


    ped = Agent(agent_type='Pedestrian', src_node=source_pedestrian, dest_type='connector')

    ped.best_paths(G)
    exit()

    #print('Path: ', source_pedestrian, ' -> ', target)
    Optimizer(city_graph, source_pedestrian, source_car, target).optimize(20)

    #graph_drawer.draw_static([AgentPath('Pedestrian', G, source, target)])
    #graph_drawer.draw_static([AgentPath('Car driver', G, source, target)])

    target_residence = next(iter(find_node_by_edge_type(G, 'residence')), target)
    target_office = next(iter(find_node_by_edge_type(G, 'office')), target)

    pedestrian_path = AgentPath('Pedestrian', G, source_pedestrian, target_residence, 'red')
    car_driver_path = AgentPath('Car driver', G, source_car, target_office, 'blue')

    graph_drawer.static_agents_paths([pedestrian_path, car_driver_path], '../out/san_juan_multi_paths_car.png')

    #nx.write_shp(G, '../data/Network_test/generated')


if __name__ == "__main__":
    main()
