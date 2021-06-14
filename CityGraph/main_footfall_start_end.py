import os

import geopandas as gpd

from CityGraph.simulation.all_simulations import ALL_SIMULATIONS


# Loaded trajectories (8473)
# ==== Gen pedestrian start end ID_unique ====
# Loaded pedestrian segments (17069)
# Filtered pedestrian trajectories (4287)
# Found pedestrian nearest START points (4287)
# Found pedestrian nearest END points (4287)
#
# ==== Gen bike start end ID_unique ====
# Loaded bike segments (36622)
# Filtered bike trajectories (2407)
# Found bike nearest START points (2407)
# Found bike nearest END points (2407)
#
# ==== Gen vehicle start end ID_unique ====
# Loaded vehicle segments (6406)
# Filtered vehicle trajectories (1455)
# Found vehicle nearest START points (1455)
# Found vehicle nearest END points (1455)

def main():
    nrows = None
    # nrows = 10
    data_folder = os.getcwd() + '/../data/'

    # Load footfall trajectories
    traj_gdf = (
        gpd.read_file(data_folder + '/Footfall_Trajectories/Footfall_Trajectories.gpkg', rows=nrows)
            .rename({'id': 'device_id'}, axis=1)
            .set_index('device_id')
    )
    print(f'Loaded trajectories ({(len(traj_gdf))})')

    # Find nearest segment ids for all simulations
    [sim.generate_agent_segment_ids(traj_gdf) for sim in ALL_SIMULATIONS]


if __name__ == "__main__":
    main()
