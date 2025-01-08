from gui import App
from models import Grille, Sommet

WIDTH = 20
HEIGHT = 20

if __name__ == "__main__":
    app = App(HEIGHT, WIDTH, 1000, 800)
    app.mainloop()
    # Initialisez votre grille et vos sommets
    ma_grille = Grille(10, 10)  # Exemple avec une grille de 10x10
    start = ma_grille.tab[2][2]  # Exemple de sommet de départ en (0,0)
    end = ma_grille.tab[5][5]    # Exemple de sommet de fin en (9,9)

    # Appelez la méthode AllerAToire
    reachable, path = ma_grille.allerAToire(start, end)

    # Affichez les résultats
    print("Sommets atteignables :", reachable)
    print("Chemin parcouru :", path)
