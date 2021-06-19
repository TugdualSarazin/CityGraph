class Indicator:

    def __init__(self, key, name):
        self.key = key
        self.norm_key = 'norm_' + key

        if name:
            self.name = name
        else:
            self.name = key

    def get(self, edge_data):
        return edge_data.get(self.key)