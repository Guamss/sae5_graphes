import unittest

from web.back.src.sae5_graphes.models import Grille


class TestGrille(unittest.TestCase):
    def setUp(self):
        # Créer une grille 5x5
        self.grille = Grille(5, 5)

    def test_get_neighbors(self):
        """
        Test des voisins pour différents sommets dans la grille.
        """
        test_cases = [
            {
                "name": "center",
                "sommet": self.grille.tab[2][2],
                "expected": {
                    self.grille.tab[1][1], self.grille.tab[1][2], self.grille.tab[1][3],
                    self.grille.tab[2][1], self.grille.tab[3][2], self.grille.tab[2][3]
                }
            },
            {
                "name": "corner",
                "sommet": self.grille.tab[0][0],
                "expected": {
                    self.grille.tab[0][1], self.grille.tab[1][0]
                }
            },
            {
                "name": "edge",
                "sommet": self.grille.tab[0][2],
                "expected": {
                    self.grille.tab[0][1],
                    self.grille.tab[1][2], self.grille.tab[0][3]
                }
            }
        ]

        for case in test_cases:
            with self.subTest(case=case["name"]):
                voisins = self.grille.get_neighbors(case["sommet"])
                self.assertEqual(voisins, case["expected"])


    def test_parcour_profondeur(self):
        pass

    def test_parcours_naif(self):
        pass

    def test_parcours_dijkstra(self):
        pass
