from CityGraph.indicator.Indicator import Indicator


def normalize10(val):
    return (10. - val) / 10.


def denormalize10(norm_val):
    return 10 - (10. * norm_val)


class Indicator10(Indicator):
    key = None
    norm_key = None
    name = None
    factor = 0.
    bigger_is_better = True

    def __init__(self, key, factor, name=None):
        super().__init__(key, name)
        self.factor = factor

    def compute_indicator_edge(self, data_edge):
        val = data_edge.get(self.key)
        # If the value exists
        if val is not None:
            # Normalize indicator and save
            norm_val = normalize10(val)
            data_edge[self.norm_key] = norm_val
            return norm_val
        else:
            data_edge[self.norm_key] = None
            return None

    def __str__(self):
        return f'Indic10(key={self.key}, factor={self.factor})'

    def __repr__(self):
        return self.__str__()
