from CityGraph.simulation.bike_sim import BikeSim
from CityGraph.simulation.pedestrian_sim import PedestrianSim
from CityGraph.simulation.simulation import Simulation
from CityGraph.simulation.vehicle_sim import VehicleSim


class PedestrianCurrentScenarioSim(PedestrianSim):
    name = 'pedestrian_current_scenario'
    sim_folder = Simulation.root_path + '/data/01_PEQI_Pedestrian Network/'
    network_fp_shp = sim_folder + '/Pedestrian_peqi_fin.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/agent_seg_ids-{name}.csv'
    agent_paths_fp_geojson = sim_folder + f'/agent_paths-{name}.geojson'
    out_network_fp_geojson = sim_folder + f'/final-{name}.geojson'


class BikeCurrentScenarioSim(BikeSim):
    name = 'bike_current_scenario'
    sim_folder = Simulation.root_path + '/data/02_BEQI_Bike_Network/'
    network_fp_shp = sim_folder + 'Dongxuan_BEQI.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/agent_seg_ids-{name}.csv'
    agent_paths_fp_geojson = sim_folder + f'/agent_paths-{name}.geojson'
    out_network_fp_geojson = sim_folder + f'/final-{name}.geojson'


class VehicleCurrentScenarioSim(VehicleSim):
    name = 'vehicle_current_scenario'
    sim_folder = Simulation.root_path + '/data/03_VEQI_Vehicle_Network/'
    network_fp_shp = sim_folder + 'XXXX_VEQI.shp'
    agents_seg_ids_fp_csv = sim_folder + f'/agent_seg_ids-{name}.csv'
    agent_paths_fp_geojson = sim_folder + f'/agent_paths-{name}.geojson'
    out_network_fp_geojson = sim_folder + f'/final-{name}.geojson'


ALL_SIMULATIONS = [PedestrianCurrentScenarioSim(), BikeCurrentScenarioSim()]