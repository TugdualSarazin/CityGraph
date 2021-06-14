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
    in_indicators = [
        IndicatorGroup(
            key='car_lane_design',
            grp_factor=1.4,
            indicators=[
                Indicator10(key='V1.1type', factor=2.1, name='Type of road'),
                Indicator10(key='V2.1lane', factor=3.4, name='Lanes'),
                Indicator10(key='V3.1twoway', factor=2.4, name='Two way traffic'),
            ]),
        IndicatorGroup(
            key='vehicle_traffic',
            grp_factor=3.4,
            indicators=[
                Indicator10(key='V4.1speed', factor=4.3, name='Speed'),
                Indicator10(key='V5.1volume', factor=2.2, name='Traffic volume'),
            ]),
        IndicatorGroup(
            key='calming_design',
            grp_factor=0.3,
            indicators=[
                Indicator10(key='V6.1calm', factor=0.4, name='TCFS (street traffic calming geatures) '),
            ]),
    ]
