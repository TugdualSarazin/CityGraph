import os
from datetime import datetime, timedelta

import geopandas as gpd
import movingpandas as mpd


def load_footfall_pts(footfall_fp, nrows=None):
    ff = gpd.read_file(footfall_fp, rows=nrows)

    ff['geometry'] = ff['geometry'].apply(lambda geo: geo.simplify(1))
    ff['dt'] = ff['TIMESTAMP'].apply(lambda ts: datetime.fromtimestamp(ts))
    ff.rename({'DEVICE_AID': 'device_id'}, axis=1, inplace=True)
    ff.set_index('dt', inplace=True)
    ff.drop(['TIMESTAMP'], axis=1, inplace=True)

    print(f'Loaded footfall points ({len(ff)})')
    return ff


def gen_traj_min_length(gdf, traj_min_length, stop_max_diameter, stop_min_duration):
    tc = mpd.TrajectoryCollection(gdf, 'device_id', min_length=traj_min_length)
    print(f'Transformed footfall to trajectories of min_length={traj_min_length}m ({len(tc)})')

    split_tc = mpd.StopSplitter(tc).split(max_diameter=stop_max_diameter, min_duration=stop_min_duration)
    print(f'Split trajectories with max_diameter={stop_max_diameter}m,' \
          + f' min_duration={stop_min_duration}, min_length={traj_min_length}m ({len(split_tc)})')
    return split_tc


def to_gdf_max_speed(ff_tc):
    # Process speed
    ff_tc.add_speed()

    traj_gdf = ff_tc.to_traj_gdf()
    traj_gdf['max_speed'] = [traj.df.speed.max() for traj in ff_tc.trajectories]

    print(f'Processed max_speed of trajectories ({len(traj_gdf)})')

    return traj_gdf

# Loaded footfall points (540615)
# Transformed footfall to trajectories of min_length=100m (4651)
# Split trajectories with max_diameter=20m, min_duration=0:02:00, min_length=100m (8439)
# Processed max_speed of trajectories (8439)

def main():
    nrows = None
    #nrows = 1000

    data_folder = os.getcwd() + '/../data/'

    # Load points
    ff_points = load_footfall_pts(data_folder + '/raw_footfall/ff-all-district_25831', nrows=nrows)

    # Gen trajectory from footfall points
    # Filter trajectory by length > 50m
    # Split it by stops
    ff_tc = gen_traj_min_length(ff_points,
                                traj_min_length=100,
                                stop_max_diameter=20,
                                stop_min_duration=timedelta(seconds=120))

    # Process max_speed of trajectories
    traj_gdf = to_gdf_max_speed(ff_tc)

    # Save footfall trajectories file
    traj_gdf.to_file(data_folder + '/Footfall_Trajectories/Footfall_Trajectories.gpkg', driver="GPKG")


if __name__ == "__main__":
    main()
