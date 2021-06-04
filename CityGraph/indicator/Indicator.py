class Indicator:
    key = None
    norm_key = None
    name = None

    def __init__(self, key, name):
        self.key = key
        self.norm_key = 'norm_' + key

        if name:
            self.name = name
        else:
            self.name = key
