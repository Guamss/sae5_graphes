from models import Grille

grille = Grille(1000, 100)
print(grille)

start = grille.tab[2][2]
end = grille.tab[99][90]

result = grille.parcours_dijkstra(start, end)
print(result)
