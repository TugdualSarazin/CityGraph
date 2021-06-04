from CityGraph.indicator.indicator10 import Indicator10
from CityGraph.indicator.indicator_group import IndicatorGroup
from CityGraph.simulation.simulation import Simulation


class PedestrianSim(Simulation):
    # pedestrian = max_speed : [0 km/h, 5.04 km/h]
    min_speed = 0
    max_speed = 1.4

    # Output indicator
    out_indicator = Indicator10(key='PEQI', factor=0., name='PEQI')

    # Input indicators
    in_indicators = [
        IndicatorGroup(
            key='intersection_safety',
            grp_factor=1.05,
            indicators=[
                Indicator10(key='1.1', factor=2.1, name='Cross walks'),
                Indicator10(key='1.2', factor=2.4, name='Ladder Crosswalks'),
                Indicator10(key='1.3', factor=2.4, name='Countdown in signal'),
                Indicator10(key='1.5', factor=2.4, name='Crosswalk scramble'),
                Indicator10(key='1.6', factor=2.4, name='No Turn on Red'),
                Indicator10(key='1.7', factor=2.4, name='Intersection traffic calming features'),
                Indicator10(key='1.8', factor=2.4, name='Additional Signs for pedestrians')
            ]),

        IndicatorGroup(
            key='traffic',
            grp_factor=0.76,
            indicators=[
                Indicator10(key='2.1num_lan', factor=2.4, name='Number of lanes'),
                Indicator10(key='2.2twoway', factor=1.8, name='Two way traffic'),
                Indicator10(key='2.3speed', factor=2.7, name='Vehicle speed')
            ]),

        IndicatorGroup(
            key='street_design',
            grp_factor=1.1,
            indicators=[
                Indicator10(key='3.1Width', factor=2.4, name='Width of Sidewalk'),
                Indicator10(key='3.3Obstacl', factor=2.1, name='Large SW Obstructions'),
                Indicator10(key='3.5Cuts', factor=1.8, name='Driveway Cuts'),
                Indicator10(key='3.6Trees', factor=1.8, name='Trees'),
                Indicator10(key='3.8Sitting', factor=1.8, name='Public Sitting'),
                Indicator10(key='3.7Buffer', factor=2.1, name='Presence of a Buffer'),
            ]),

        IndicatorGroup(
            key='land_use',
            grp_factor=0.18,
            indicators=[
                Indicator10(key='4.1artsite', factor=1.8, name='Public Art/ Historic Sites'),
                Indicator10(key='4.2restaur', factor=2.1, name='Restaurant and Retail Use'),
            ]),
        IndicatorGroup(
            key='perceived_safety',
            grp_factor=0.43,
            indicators=[
                Indicator10(key='5.2litter', factor=1.8, name='Litter'),
                Indicator10(key='5.3nocturn', factor=2.4, name='Lighting (now only nocturnal economic activities)'),
                Indicator10(key='5.4constru', factor=1.8, name='Construction sites'),
                Indicator10(key='5.5ruins', factor=1.8, name='Abandoned buildings'),
            ])
    ]
