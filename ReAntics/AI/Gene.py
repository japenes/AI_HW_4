class Gene:
    attributes = []
    fitnessScore = 0
    def __init__(self, array):
        self.attributes = array
        fitnessScore = 0

    def setFitness(self, score):
        fitnessScore = score
