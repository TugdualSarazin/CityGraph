from CityGraph.intervention.intervention import Intervention, EffectFix
from CityGraph.simulation.bike_sim import BikeSim


class InterventionA(Intervention):
    effects = [EffectFix(BikeSim.B2_8trees, 7.27)]