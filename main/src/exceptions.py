class BadWeightException(Exception):
    def __init__(self):
        super().__init__("Poids invalide")


class NotConnectedGraphException(Exception):
    def __init__(self):
        super().__init__("Le Graphe est non connnexe")
