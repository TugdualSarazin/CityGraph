class Indicator10:
    key = None
    norm_key = None
    name = None
    factor = 0.
    bigger_is_better = True

    def __init__(self, key, factor, bigger_is_better=True, name=None):
        self.key = key
        self.norm_key = 'norm_' + key
        self.factor = factor
        self.bigger_is_better = bigger_is_better
        if name:
            self.name = name
        else:
            self.name = key

    def normalize(self, val):
        return (10. - val) / 10.

    def compute_indicator_edge(self, data_edge):
        val = data_edge.get(self.key)
        # If the value exists
        if val is not None:
            # Normalize indicator and save
            norm_val = self.normalize(val)
            data_edge[self.norm_key] = norm_val
            return norm_val
        else:
            data_edge[self.norm_key] = None
            return None

    def __str__(self):
        return f'Indic10(key={self.key}, factor={self.factor}, bigger_is_better={self.bigger_is_better})'

    def __repr__(self):
        return self.__str__()


