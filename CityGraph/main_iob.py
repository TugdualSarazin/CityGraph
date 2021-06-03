from CityGraph.simulation.all_simulations import PedestrianCurrentScenarioSim, BikeCurrentScenarioSim, ALL_SIMULATIONS


def main():
    # TODO
    # Split trajectories with stops
    # Include health -> Diana
    # Include VEQI
    # transform final metrics into 0-10

    BikeCurrentScenarioSim().run_agent_paths()
    PedestrianCurrentScenarioSim().run_agent_paths()
    # Run all simulations
    #[sim.run_agent_paths() for sim in ALL_SIMULATIONS]

    # graph_drawer = Drawer(car_graph, dpi=200, node_size=0, edge_size=2)
    # graph_drawer.static_agents_paths(car_paths)
    # graph_drawer.draw_weights()


if __name__ == "__main__":
    main()
