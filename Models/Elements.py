class Elements:
    def __init__(self, element, estimate, fit = False, iterlist = False):
        self.element = element
        self.estimate = estimate
        self.fit = fit
        self.iterlist = iterlist

    def get(self):
        return {
            "element": self.element,
            "estimate": self.estimate,
            "fit": self.fit,
            "iterlist": self.iterlist,
        }