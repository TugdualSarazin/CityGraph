from CityGraph.indicator.indicator10 import Indicator10


class IndicatorGroup:
    key = None
    norm_key = None
    name = None
    grp_factor = 0.
    indicators = []

    def __init__(self, key, grp_factor, indicators: [Indicator10], name=None):
        self.key = key
        self.norm_key = 'grp_norm_' + key

        self.grp_factor = grp_factor
        self.indicators = indicators
        if name:
            self.name = name
        else:
            self.name = key

    def compute_group_edge(self, data_edge):
        grp_sum_val = 0
        grp_sum_factors = 0
        # Compute indicators of a group
        for indic in self.indicators:
            norm_val = indic.compute_indicator_edge(data_edge)
            # If the indicator found a value add to the group sum and sum factors
            if norm_val is not None:
                grp_sum_val += norm_val * indic.factor
                grp_sum_factors += indic.factor

        # Keys found for this group
        if grp_sum_factors > 0:
            # Normalize group indicator and save
            norm_grp = grp_sum_val / grp_sum_factors
            data_edge[self.norm_key] = norm_grp
            return norm_grp

        # No key found for this groupd
        else:
            data_edge[self.norm_key] = None
            return None

    def __str__(self):
        return f'{self.key}(grp_factor={self.grp_factor}, indicatos:{self.indicators})'

    def __repr__(self):
        return self.__str__()

