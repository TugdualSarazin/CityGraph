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
    in_indicators = [
        IndicatorGroup(
            key='intersection_safety',
            grp_factor=0.42,
            indicators=[
                Indicator10(key='B1.2dashed', factor=3., name='Dashed intersection bicycle lane'),
            ]),
        IndicatorGroup(
            key='street_design',
            grp_factor=2.05,
            indicators=[
                Indicator10(key='B2.2width', factor=4., name='Bike Width of Bike Lane'),
                Indicator10(key='B2.3mark', factor=4., name='Bicycle Lane Markings'),
                Indicator10(key='B2.6slope', factor=4., name='Street Slope'),
                Indicator10(key='B2.7drivew', factor=4., name='Driveway Cuts'),
                Indicator10(key='B2.8trees', factor=4., name='Presence of Trees'),
            ]),
        IndicatorGroup(
            key='vehicle_traffic',
            grp_factor=1.39,
            indicators=[
                Indicator10(key='B3.1speed', factor=3., name='Posted Speed Limit'),
                Indicator10(key='B3.3heav', factor=3., name='Percentage of Heavy Vehicle'),
                Indicator10(key='B3.6num_la', factor=3., name='Number of Lanes'),
            ]),
        IndicatorGroup(
            key='safety',
            grp_factor=0.42,
            indicators=[
                Indicator10(key='B4.1lane_s', factor=4., name='Presence of Bicycle Lane Signs'),
                Indicator10(key='B4.2noctur', factor=4., name='Bicycle/Pedestrian Scale Lighting'),
            ]),
        IndicatorGroup(
            key='land_use',
            grp_factor=0.66,
            indicators=[
                Indicator10(key='B5.1bparki', factor=4., name='Bicycle Parking'),
                Indicator10(key='B5.2retail', factor=4., name='Retail Use'),
            ])
    ]

    # Indicators
