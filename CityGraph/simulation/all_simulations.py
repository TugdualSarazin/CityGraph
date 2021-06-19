from CityGraph.simulation.bike_sim import BikeSim
from CityGraph.simulation.pedestrian_sim import PedestrianSim
from CityGraph.simulation.simulation import Simulation
from CityGraph.simulation.vehicle_sim import VehicleSim


class PedestrianCurrentScenarioSim(PedestrianSim):
    name = 'pedestrian'
    sim_folder = Simulation.root_path + '/data/01_PEQI_Pedestrian Network/'
    network_fp_shp = sim_folder + '/Pedestrian_peqi_fin.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/{name}-agent_seg_ids.csv'
    agent_paths_fp_geojson = sim_folder + f'/{name}-agent_paths.geojson'
    out_network_fp_geojson = sim_folder + f'/mobility_{name}-all.geojson'
    out_network_min_fp_geojson = sim_folder + f'/mobility_{name}-min.geojson'


class BikeCurrentScenarioSim(BikeSim):
    name = 'bike'
    sim_folder = Simulation.root_path + '/data/02_BEQI_Bike_Network/'
    network_fp_shp = sim_folder + 'Dongxuan_BEQI.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/{name}-agent_seg_ids.csv'
    agent_paths_fp_geojson = sim_folder + f'/{name}-agent_paths.geojson'
    out_network_fp_geojson = sim_folder + f'/mobility_{name}-all.geojson'
    out_network_min_fp_geojson = sim_folder + f'/mobility_{name}-min.geojson'


class VehicleCurrentScenarioSim(VehicleSim):
    name = 'vehicle'
    sim_folder = Simulation.root_path + '/data/03_VEQI_Vehicle_Network/'
    network_fp_shp = sim_folder + 'VEQI_with_V6.1.shp'
    #network_fp_shp = sim_folder + 'veqi_health final.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/{name}-agent_seg_ids.csv'
    agent_paths_fp_geojson = sim_folder + f'/{name}-agent_paths.geojson'
    out_network_fp_geojson = sim_folder + f'/mobility_{name}-all.geojson'
    out_network_min_fp_geojson = sim_folder + f'/mobility_{name}-min.geojson'


ALL_SIMULATIONS = [PedestrianCurrentScenarioSim(), BikeCurrentScenarioSim(), VehicleCurrentScenarioSim()]
#ALL_SIMULATIONS = [VehicleCurrentScenarioSim()]
