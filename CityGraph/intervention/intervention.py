


class InterventionEffect:
    def __init__(self, indicator):
        self.indicator = indicator


class EffectFix(InterventionEffect):
    def __init__(self, indicator, update_val):
        super().__init__(indicator)
        self.update_val = update_val


class EffectPercent(InterventionEffect):
    def __init__(self, indicator, update_percent):
        super().__init__(indicator)
        self.update_percent = update_percent

class Intervention:
    effects = []

    def condition(self, edge_data):
        pass
