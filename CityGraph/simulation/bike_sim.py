from CityGraph.indicator.indicator10 import Indicator10
from CityGraph.indicator.indicator_group import IndicatorGroup
from CityGraph.simulation.simulation import Simulation



class BikeSim(Simulation):
    # bike = max_speed : [5.04 km/h, 28.8 km/h]
    min_speed = 1.4
    max_speed = 8.

    # Output indicator
    out_indicator = Indicator10(key='BEQI', factor=0., name='BEQI')

    # Input indicators
    B1_2dashed = Indicator10(key='B1.2dashed', factor=3., name='Dashed intersection bicycle lane')

    B2_2width = Indicator10(key='B2.2width', factor=4., name='Bike Width of Bike Lane')
    B2_3mark = Indicator10(key='B2.3mark', factor=4., name='Bicycle Lane Markings')
    B2_6slope = Indicator10(key='B2.6slope', factor=4., name='Street Slope')
    B2_7drivew = Indicator10(key='B2.7drivew', factor=4., name='Driveway Cuts')
    B2_8trees = Indicator10(key='B2.8trees', factor=4., name='Presence of Trees')

    B3_1speed = Indicator10(key='B3.1speed', factor=3., name='Posted Speed Limit')
    B3_3heav = Indicator10(key='B3.3heav', factor=3., name='Percentage of Heavy Vehicle')
    B3_6num_la = Indicator10(key='B3.6num_la', factor=3., name='Number of Lanes')

    B4_1lane_s = Indicator10(key='B4.1lane_s', factor=4., name='Presence of Bicycle Lane Signs')
    B4_2noctur = Indicator10(key='B4.2noctur', factor=4., name='Bicycle/Pedestrian Scale Lighting')

    B5_1bparki = Indicator10(key='B5.1bparki', factor=4., name='Bicycle Parking')
    B5_2retail = Indicator10(key='B5.2retail', factor=4., name='Retail Use')

    in_indicators = [
        IndicatorGroup(key='intersection_safety', grp_factor=0.42, indicators=[B1_2dashed]),
        IndicatorGroup(key='street_design', grp_factor=2.05,
                       indicators=[B2_2width, B2_3mark, B2_6slope, B2_7drivew, B2_8trees]),
        IndicatorGroup(key='vehicle_traffic', grp_factor=1.39, indicators=[B3_1speed, B3_3heav, B3_6num_la]),
        IndicatorGroup(key='safety', grp_factor=0.42, indicators=[B4_1lane_s, B4_2noctur]),
        IndicatorGroup(key='land_use', grp_factor=0.66, indicators=[B5_1bparki, B5_2retail])
    ]
