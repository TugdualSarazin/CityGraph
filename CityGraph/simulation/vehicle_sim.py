from CityGraph.indicator.indicator10 import Indicator10
from CityGraph.indicator.indicator_group import IndicatorGroup
from CityGraph.simulation.simulation import Simulation


class VehicleSim(Simulation):
    # max_speed : [28,8 km/h, 144 km/h]
    min_speed = 8.
    max_speed = 40.

    # Output indicator
    out_indicator = Indicator10(key='VEQI', factor=0., name='VEQI')

    # Input indicators
    in_indicators = []
