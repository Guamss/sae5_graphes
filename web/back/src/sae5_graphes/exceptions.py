class BadWeightException(Exception):
    def __init__(self):
        super().__init__("Poids invalide")


class NotConnectedGraphException(Exception):
    def __init__(self):
        self.message = "Le Graphe est non connnexe"
        super().__init__(self.message)
