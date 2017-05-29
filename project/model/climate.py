
class ClimateModel(object):

    def __init__(self, *args, **kwargs):
        self.prec = []
        self.temp = []

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
