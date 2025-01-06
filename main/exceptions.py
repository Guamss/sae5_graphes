# modèle d'exception pour des exceptions à venir
class BadWeightException(Exception):
    def __init__(self):
        super().__init__("Poids invalide")
