from itertools import product
from typing import Union
import random

class Sommet:
    def __init__(self, weight: int, x: int, y: int) -> None:
        """
        Le sommet d'un graphe

        Args:
            weight (int): le poids du sommet dans le graphe
            x (int): les coordonnées du sommet en abscisse
            y (int): les coordonnées du sommet en ordonnée
        """
        self.weight: int = weight
        self.x: int = x  # La ligne
        self.y: int = y  # La colonne
        self.visited = False

    # self.is_start = False
    # self.is_end = False

    def set_weight(self, weight: int):
        self.weight: int = weight
        return self

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Sommet):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))  # Utilise les coordonnées pour générer un hash unique

    def __str__(self) -> str:
        return f"{self.weight} | [{self.x}, {self.y}]"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


class Grille:
    """
        Une grille de sommets

        Args:
            height (int): hauteur de la grille
            width (int): largeur de la grille
            tab (list[list[Sommet]]): tableau 2D des sommets potentiel du graphe
            paths (dict): liste des chemins trouvés par un algorithme
    """

    def __init__(self, height: int, width: int) -> None:
        self.height: int = height
        self.width: int = width
        self.tab: list[list[Sommet]] = [[Sommet(random.randint(1, 10), x, y) for y in range(width)] for x in range(height)]
        self.paths: dict = {}

    def __str__(self) -> str:
        out: str = ""
        for ligne in self.tab:
            out += (" ".join(str(sommet.weight) for sommet in ligne))+"\n"
        return out

    def get_neighbors(self, s: Sommet) -> list[Sommet]:
        """
        Renvoie les voisins du sommet s

        Args :
            s (Sommet) : le sommet concerné

        Returns :
            list[Sommet] : les voisins du sommet s
        """
        neighbors: list[Sommet] = []
        for i in range(s.x - 1, s.x + 2):
            for j in range(s.y - 1, s.y + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i != s.x or j != s.y):  # Bien dans la grille et n'est pas la case elle-même
                    if i != s.x and j != s.y:  # Une case angle
                        if s.y % 2:  # Colone impaire
                            if i == s.x + 1:
                                neighbors.append(self.tab[i][j])
                        else:  # Colone paire
                            if i == s.x - 1:
                                neighbors.append(self.tab[i][j])
                    else:  # Une case coté direct
                        neighbors.append(self.tab[i][j])

        return neighbors

    def parcours_profondeur(self, start: Sommet, end: Sommet, visited=None) -> dict[Sommet, list[Sommet]]:
        """
        Le parcours en profondeur va parcourir le graphe jusqu'à trouver une impasse (sommet sans voisin) et ensuite
        revenir en arrière afin de retrouver un voisin non visité. Cette application est récursive et retourne l'ensemble
        des chemins possible à partir du sommet "start"

        :param start: sommet de départ
        :param end: sommet d'arrivée
        :param visited: liste des sommets visités
        :return: liste des chemins possible
        """
        if visited is None:
            visited = {}
        if start in visited:
            return visited

        visited[start] = self.get_neighbors(start)

        for neighbor in self.get_neighbors(start):
            if neighbor not in visited:
                self.parcours_profondeur(neighbor, visited)
        return visited


    def parcours_naif(self, start:Sommet, end: Sommet) -> dict[Sommet, list[Sommet]]:
        """
        Le parcours naif va se contenter de parcourir la grille en prenant ses voisins avec le poid le moins lourd

        Args:
            start (Sommet): le sommet de départ
            end: (Sommet): le sommet de fin
        """
        # TODO : a faire en recurcif pour remonter quand ça tourne en rond
        visited = []
        end_reached = False
        actual_sommet = start
        while not end_reached:
            visited.append(actual_sommet)
            if actual_sommet == end:
                end_reached = True

            actual_sommet_neighbors = self.get_neighbors(actual_sommet)
            min_weight_neighbor: Sommet = Sommet(9999, 0, 0) # un sommet quelconque
            for neighbor in actual_sommet_neighbors:
                if neighbor.weight < min_weight_neighbor.weight and neighbor not in visited:
                    min_weight_neighbor = neighbor
            actual_sommet = min_weight_neighbor

        return {start: visited}




    def parcours_dijkstra(self, start: Sommet, end: Sommet) -> dict[Sommet, list[Sommet]]:
        # TODO : Thomas  -  En cours, non fonctionnel  -
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []

        while len(queue) > 0:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            visited.append(current)
            current[0].visited = True
            for neighbor in self.get_neighbors(current[0]):

                if not neighbor.visited:
                    is_in_queue = False
                    for t in queue:
                        if t[0] == neighbor:
                            is_in_queue = True
                            if current[1] + neighbor.weight < t[1]:
                                queue.append((neighbor, current[1] + neighbor.weight, current[0]))
                    if not is_in_queue:
                        queue.append((neighbor, current[1] + neighbor.weight, current[0]))

            queue.sort(key=lambda t: t[1])

        back: list[tuple[Sommet, int, Union[Sommet, None]]] = []
        for t in visited:
            if t[0].x == end.x and t[0].y == end.y:
                back.append(t)
                visited.remove(t)

        while back[-1][0].x != start.x or back[-1][0].y != start.y:
            for t in visited:
                if t[0].x == back[-1][2].x and t[0].y == back[-1][2].y:
                    back.append(t)
                    visited.remove(t)

        result: list[Sommet] = []
        for i in range(len(back)-1, -1, -1):
            result.append(back[i][0])

        return result
