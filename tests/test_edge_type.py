import networkx as nx

from CityGraph.edge_type import EdgeType


# TODO: check for every type_factors and every agent_type

def test_set_edge_type_weights():
    # Init graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5])
    # Nature path 1 -> 2 -> 4
    G.add_edge(1, 2, type='sidewalk', length=1)
    G.add_edge(2, 4, type='sidewalk', length=2)
    # Time path 1 -> 3 -> 4
    G.add_edge(1, 3, type='crossing', length=3)
    G.add_edge(3, 4, type='crossing', length=4)

    EdgeType.set_edge_type_weights(G)
    # Sidewalk 1-2
    assert G[1][2]['walk'] == 1 * 4
    assert G[1][2]['bike'] == 1 * 5
    # Sidewalk 2-4
    assert G[2][4]['walk'] == 2 * 4
    assert G[2][4]['bike'] == 2 * 5
    # Crossing 1-3
    assert G[1][3]['walk'] == 3 * 2
    assert G[1][3]['bike'] == 3 * 3
    # Crossing 3-4
    assert G[3][4]['walk'] == 4 * 2
    assert G[3][4]['bike'] == 4 * 3


def test_set_agent_type_weights():
    # Init graph
    G = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4, 5])
    # Nature path 1 -> 2 -> 4
    G.add_edge(1, 2, walk=10, bike=100, nature=1000)
    EdgeType.set_agent_type_weights(G)
    assert G[1][2]['Pedestrian'] == 2 * 10 + 0 * 100 + 1 * 1000
    assert G[1][2]['biker'] == 0 * 10 + 2 * 100 + 1 * 1000
