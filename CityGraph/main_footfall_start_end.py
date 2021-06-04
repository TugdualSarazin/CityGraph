import os
from datetime import datetime, timedelta

import geopandas as gpd
import movingpandas as mpd

from CityGraph.simulation.all_simulations import ALL_SIMULATIONS


def filter_geo_district(gdf, filter_shp_fp):
    # Load filter
    district_filter = gpd.read_file(filter_shp_fp).loc[0, 'geometry']
    # Filter the geo dataframe with the district shape
    filtered_gdf = gdf[gdf.within(district_filter)]
    print(f"Filter input len: {len(gdf)} -> output len {len(filtered_gdf)}")
    return filtered_gdf


def load_footfall(footfall_fp, nrows=None):
    ff = gpd.read_file(footfall_fp, rows=nrows)

    ff['geometry'] = ff['geometry'].apply(lambda geo: geo.simplify(1))
    ff['dt'] = ff['TIMESTAMP'].apply(lambda ts: datetime.fromtimestamp(ts))
    ff['device_id'] = ff.apply(lambda r: r['DEVICE_AID'] + r['dt'].strftime('_%Y-%m-%d'), axis=1)
    ff.set_index('dt', inplace=True)
    ff.drop(['TIMESTAMP', 'DEVICE_AID'], axis=1, inplace=True)

    # ff = ff.to_crs("EPSG:4326")

    print(f'Loaded footfall points ({len(ff)})')
    return ff


def gen_traj_min_length(gdf, traj_min_length, stop_max_diameter, stop_min_duration):
    tc = mpd.TrajectoryCollection(gdf, 'device_id', min_length=traj_min_length)
    print(f'Transformed footfall to trajectories of min_length={traj_min_length}m ({len(tc)})')

    split_tc = mpd.StopSplitter(tc).split(max_diameter=stop_max_diameter, min_duration=stop_min_duration)
    print(f'Split trajectories with max_diameter={stop_max_diameter}m and min_duration={stop_min_duration} ({len(split_tc)})')
    return split_tc


def start_end_pts_max_speed(ff_tc):
    # Add speed to each part of the trajectory
    ff_tc.add_speed()


    # Compute the maximum speed
    max_speed = [traj.df.speed.max() for traj in ff_tc.trajectories]

    # TODO: generalize speed based on time (Diego video 17:48)

    # Start points with max_speed
    start_pts = ff_tc.get_start_locations()
    start_pts['max_speed'] = max_speed

    # End points with max_speed
    end_pts = ff_tc.get_end_locations()
    end_pts['max_speed'] = max_speed

    return start_pts, end_pts


def main():
    data_folder_path = os.getcwd()+'/../data/'

    # Load points
    #ff_points = load_footfall(data_folder_path+'/Footfall_District/Footfall_District.shp')
    ff_points = load_footfall(data_folder_path+'/Footfall_District/Footfall_District.shp', nrows=1000)

    # Filter with district area
    # ff_points = filter_geo_district(ff_points, data_folder_path+'/district_filter_area/district_filter_area.shp')

    # Gen trajectory from footfall points and filter trajectory by length > 50m
    ff_tc = gen_traj_min_length(ff_points,
                                traj_min_length=50,
                                stop_max_diameter=10,
                                stop_min_duration=timedelta(seconds=120))

    ff_tc.to_trajectories.to_file(data_folder_path+'/Footfall_Trajectories/Footfall_Trajectories.shp')
    # [print(traj, "\n--------------") for traj in ff_tc]

    # Loaded footfall points (367808)
    # Transformed footfall to trajectories of min_length=50m (3307)
    # Split trajectories with max_diameter=10m and min_duration=0:02:00 (5387)

    exit()

    # Extract start and end points of footfall trajectories and compute max_speed for each
    ff_start_pts, ff_end_pts = start_end_pts_max_speed(ff_tc)

    # Generate start and stop segment ids for each simulation
    [sim.generate_agent_segment_ids(ff_start_pts, ff_end_pts) for sim in ALL_SIMULATIONS]

if __name__ == "__main__":
    main()
