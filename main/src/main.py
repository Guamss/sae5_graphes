from models import Grille

grille = Grille(10, 10)
print(grille)

start = grille.tab[0][0]
end = grille.tab[0][2]

#result = grille.run_parcours_dijkstra(start, end)
#print("--- dijkstra ---", result)

result = grille.parcours_profondeur(start,end)
#print("--- profondeur ---", result)
#result = grille.parcours_en_largeur(start, end)
print(result)


#distances, chemin = grille.bellman_ford(start, end)

# Affichage des résultats
#if distances and chemin:
#    print("Distances :", distances)
#    print("Le plus court chemin :", [f"({sommet.x}, {sommet.y})" for sommet in chemin])
#else:
#    print("Aucun chemin trouvé.")