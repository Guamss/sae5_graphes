import unittest
import requests

class TestAPI(unittest.TestCase):
    # URL de base de ton API
    BASE_URL = "http://127.0.0.1:5000/"  # Change ceci selon l'adresse de ton API

    def test_get_grid_dimensions(self):
        """
        Teste l'endpoint /grid/dimensions pour récupérer les dimensions de la grille.
        """
        # URL complète de l'endpoint
        url = f"{self.BASE_URL}/grid/dimensions"

        # Effectuer une requête GET
        response = requests.get(url)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 200, "Le statut HTTP doit être 200.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIn("height", data, "La clé 'height' doit être présente dans la réponse.")
        self.assertIn("width", data, "La clé 'width' doit être présente dans la réponse.")
        self.assertEqual(data["height"], 20, "La hauteur de la grille doit être 20 par défaut.")
        self.assertEqual(data["width"], 20, "La largeur de la grille doit être 20 par défaut.")

    def test_put_edit_grid_valid(self):
        """
        Teste la modification des dimensions de la grille avec des valeurs valides.
        """
        url = f"{self.BASE_URL}/grid/dimensions"
        payload = {"height": 50, "width": 50}
        response = requests.put(url, json=payload)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 200, "Le statut HTTP doit être 200.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIn("height", data, "La clé 'height' doit être présente dans la réponse.")
        self.assertIn("width", data, "La clé 'width' doit être présente dans la réponse.")
        self.assertEqual(data["height"], 50, "La hauteur de la grille doit être mise à jour à 50.")
        self.assertEqual(data["width"], 50, "La largeur de la grille doit être mise à jour à 50.")

    def test_put_edit_grid_too_large(self):
        """
        Teste la modification des dimensions de la grille avec des valeurs trop grandes.
        """
        url = f"{self.BASE_URL}/grid/dimensions"
        payload = {"height": 1500, "width": 50}
        response = requests.put(url, json=payload)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 400, "Le statut HTTP doit être 400 pour une taille trop grande.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIn("error", data, "La réponse doit contenir une clé 'error'.")
        self.assertEqual(data["error"], "La grille a une taille trop grande",
                         "Le message d'erreur doit indiquer une taille trop grande.")

    def test_put_edit_grid_too_small(self):
        """
        Teste la modification des dimensions de la grille avec des valeurs trop petites.
        """
        url = f"{self.BASE_URL}/grid/dimensions"
        payload = {"height": 1, "width": 50}
        response = requests.put(url, json=payload)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 400, "Le statut HTTP doit être 400 pour une taille trop petite.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIn("error", data, "La réponse doit contenir une clé 'error'.")
        self.assertEqual(data["error"], "La grille a une taille trop petite",
                         "Le message d'erreur doit indiquer une taille trop petite.")

    def test_get_grid_weights(self):
        """
        Teste l'endpoint /grid/weights pour récupérer les poids de la grille sous forme de tableau 2D.
        """
        url = f"{self.BASE_URL}/grid/weights"
        response = requests.get(url)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 200, "Le statut HTTP doit être 200.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIsInstance(data, list, "La réponse doit être une liste.")
        self.assertTrue(all(isinstance(row, list) for row in data), "Chaque élément de la réponse doit être une liste.")
        self.assertTrue(all(isinstance(weight, int) for row in data for weight in row), "Chaque élément de la grille doit être un entier.")

    def test_get_grid_weights_empty(self):
        """
        Teste le cas où la grille serait vide (théorique).
        """
        url = f"{self.BASE_URL}/grid/weights"
        # Simulez un cas où `grille.tab` serait vide
        response = requests.get(url)

        # Vérifier le code de statut (si vide, 404 attendu)
        if response.status_code == 404:
            data = response.json()
            self.assertIn("error", data, "La réponse doit contenir une clé 'error' si la grille est vide.")
            self.assertEqual(data["error"], "Le poids de la grille n'ont pas pu être déterminés", "Le message d'erreur doit indiquer une grille vide.")
        else:
            self.assertEqual(response.status_code, 200, "Le statut HTTP doit être 200 si la grille n'est pas vide.")

    def test_get_grid_weights_error_handling(self):
        """
        Teste la gestion des erreurs pour l'endpoint /grid/weights.
        """
        url = f"{self.BASE_URL}/grid/weights"

        # Simuler une exception dans le serveur
        # Vous pouvez ajuster `grille.tab` ou introduire une erreur dans le serveur Flask pour déclencher une exception
        response = requests.get(url)

        # Vérifiez que le serveur gère correctement les exceptions
        if response.status_code == 500:
            data = response.json()
            self.assertIn("error", data, "La réponse doit contenir une clé 'error' en cas d'erreur serveur.")
        else:
            self.assertEqual(response.status_code, 200, "Le statut HTTP doit être 200 si aucune erreur serveur n'est présente.")

    def test_put_update_grid_weights_size_mismatch(self):
        """
        Teste la mise à jour des poids de la grille avec une taille incompatible.
        """
        url = f"{self.BASE_URL}/grid/weights"
        payload = {
            "grid": [
                [1, 2],
                [3, 4]
            ]  # Taille incompatible avec la grille actuelle
        }

        response = requests.put(url, json=payload)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 400, "Le statut HTTP doit être 400 pour une taille incompatible.")

        # Vérifier le contenu de la réponse
        data = response.json()
        self.assertIn("error", data, "La réponse doit contenir une clé 'error'.")
        self.assertEqual(
            data["error"],
            "La grille a une taille different de la requête",
            "Le message d'erreur doit indiquer une taille incompatible.",
        )

    def test_put_update_grid_weights_invalid_data(self):
        """
        Teste la mise à jour des poids avec des données non valides.
        """
        url = f"{self.BASE_URL}/grid/weights"
        payload = {
            "grid": [
                [1, "invalid", 3],  # Valeur non valide
                [4, 5, 6],
                [7, 8, 9]
            ]
        }

        response = requests.put(url, json=payload)

        # Vérifier le code de statut
        self.assertEqual(response.status_code, 422, "Le statut HTTP doit être 422 pour des données invalides.")


if __name__ == '__main__':
    unittest.main()
