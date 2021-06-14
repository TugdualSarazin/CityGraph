from CityGraph.simulation.all_simulations import PedestrianCurrentScenarioSim, BikeCurrentScenarioSim, ALL_SIMULATIONS


def main():
    # TODO
    # Apply Scenario rules
    # Include health -> Diana
    # Create JSON of the webapp
    # Process final score

    #BikeCurrentScenarioSim().run_agent_paths()
    #PedestrianCurrentScenarioSim().run_agent_paths()
    # Run all simulations
    [sim.run_agent_paths() for sim in ALL_SIMULATIONS]

    # graph_drawer = Drawer(car_graph, dpi=200, node_size=0, edge_size=2)
    # graph_drawer.static_agents_paths(car_paths)
    # graph_drawer.draw_weights()


if __name__ == "__main__":
    main()
