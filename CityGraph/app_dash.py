import dash
import dash_cytoscape as cyto
import dash_html_components as html
from CityGraph.Optimizer import Optimizer, Agent
from CityGraph.agent_path import AgentPath
from CityGraph.city_graph import CityGraph, Indicator10
from CityGraph.edge_type_minimal import EdgeType
from CityGraph.graph_drawer import Drawer
from CityGraph.graph_tool import find_edge_by_attr, load_graph, print_edges, find_node_by_edge_type

import seaborn as sns

pal = sns.color_palette("vlag")
pal_hls = sns.hls_palette(12, l=.3, s=.8).as_hex()
print(pal_hls)
exit()

app = dash.Dash(__name__)

pedestrian_network = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\01_Working Folder\\03_QGIS\\01_Layers\\04_Agent_Networks\\Pedestrian_Network\\Pedestrian_Network.shp'
car_network = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\01_Working Folder\\03_QGIS\\01_Layers\\04_Agent_Networks\\Car_Network\\Car_Network.shp'
bike_network = 'G:\\.shortcut-targets-by-id\\1PdvfhIn79l59AQIgWd15x0QJYSTWki1L\\01. Studio_ Internet Of Buildings\\01_Working Folder\\03_QGIS\\01_Layers\\04_Agent_Networks\\Bike_Network\\Bike_Network.shp'
G = load_graph(car_network)
EdgeType.set_agent_type_weights(G)
city_graph = CityGraph(G, geo_graph=True, indicator_groups=[Indicator10('maxspeed')])

elements = []


def to_id(node):
    return str(node[0]) + ',' + str(node[1])


for n, d in G.nodes(data=True):
    elements.append(
        {'data': {'id': to_id(n)}, 'position': {'x': n[0], 'y': n[1]}}
    )

for u, v, d in G.edges(data=True):
    maxspeed = d['maxspeed']
    elements.append(
        {'data': {'source': to_id(u), 'target': to_id(v), 'maxspeed': maxspeed, 'color': pal(maxspeed)}}
    )
print(elements)

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=elements,
        stylesheet=[
            # Group selectors
            {
                'selector': 'node',
                'style': {
                    'width': 4,
                    'height': 4,
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'line-color': 'data(color)',
                }
            }
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
