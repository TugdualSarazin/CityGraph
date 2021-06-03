import geojson
import pandas as pd
from geojson import FeatureCollection

from CityGraph.agent_path import AgentPath


def create_agent_paths(city_graph, filepath):
    # Load start and end points
    df_agents = pd.read_csv(filepath, usecols=['device_id', 'start_ID_unique', 'end_ID_unique'])
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