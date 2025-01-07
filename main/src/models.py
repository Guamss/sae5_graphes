from typing import Union
from sys import maxsize
from queue import Queue
import random

from exceptions import NotConnectedGraphException

WALL: int = maxsize  # on prend un entier très grand pour définir ce qu'est un mur


class Sommet:
    def __init__(self, weight: int, x: int, y: int) -> None:
        """
        Le sommet d'un graphe

        Args:
            weight (int): le poids du sommet dans le graphe
            x (int): les coordonnées du sommet en abscisse
            y (int): les coordonnées du sommet en ordonnée

        Fields:
            weight (int): le poids du sommet dans le graphe
            x (int): les coordonnées du sommet en abscisse
            y (int): les coordonnées du sommet en ordonnée
            visited (bool): si le sommet a déjà été visité
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

        Fields:
            height (int): hauteur de la grille
            width (int): largeur de la grille
            tab (list[list[Sommet]]): tableau 2D des sommets potentiel du graphe
            paths (dict): liste des chemins trouvés par un algorithme
    """

    def __init__(self, height: int, width: int) -> None:
        self.height: int = height
        self.width: int = width
        self.tab: list[list[Sommet]] = \
            [[Sommet(random.randint(1, 10), x, y) for y in range(width)] for x in range(height)]
        self.paths: dict = {}

    def __str__(self) -> str:
        out: str = ""
        for ligne in self.tab:
            out += (" ".join(str(sommet.weight) for sommet in ligne)) + "\n"
        return out

    def get_neighbors(self, s: Sommet) -> set[Sommet]:
        """
        Renvoie les voisins du sommet s

        Args :
            s (Sommet) : le sommet concerné

        Returns :
            list[Sommet] : les voisins du sommet s
        """
        neighbors: set[Sommet] = set()
        for i in range(s.x - 1, s.x + 2):
            for j in range(s.y - 1, s.y + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i != s.x or j != s.y):  # in Grille && !current
                    if i != s.x and j != s.y:  # Une case angle
                        if s.y % 2:  # Colone impaire
                            if i == s.x + 1:
                                neighbors.add(self.tab[i][j])
                        else:  # Colone paire
                            if i == s.x - 1:
                                neighbors.add(self.tab[i][j])
                    else:  # Une case coté direct
                        neighbors.add(self.tab[i][j])

        return neighbors

    def parcours_profondeur(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Le parcours en profondeur va parcourir le graphe jusqu'à trouver une impasse (sommet sans voisin) et ensuite
        revenir en arrière afin de retrouver un voisin non visité. Cette application est faites récursivement

        :param start: sommet de départ
        :return: liste des chemins possible
        """
        # Parcours en profondeur
        visited = {}
        solution: dict[Sommet, Sommet] = {}
        self.parcours_profondeur_recursive(start, visited,solution,end)
        return visited, solution

    def parcours_profondeur_recursive(self, s: Sommet, visited: dict[Sommet, set[Sommet]],
                                      solution: dict[Sommet, Sommet], end: Sommet):
        s.visited = True
        visited[s] = self.get_neighbors(s)
        if s == end:
            return True

        for neighbor in self.get_neighbors(s):
            if not neighbor.visited:
                solution[s] = neighbor
                if self.parcours_profondeur_recursive(neighbor, visited, solution, end):
                    return True
        return False

    def parcours_naif(self, start: Sommet, end: Sommet) -> dict[Sommet, list[Sommet]]:
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
            visited.visited = True
            visited.append(actual_sommet)
            if actual_sommet == end:
                end_reached = True

            actual_sommet_neighbors = self.get_neighbors(actual_sommet)
            min_weight_neighbor: Sommet = Sommet(9999, 0, 0)  # un sommet quelconque
            for neighbor in actual_sommet_neighbors:
                if neighbor.weight < min_weight_neighbor.weight and not neighbor.visited:
                    min_weight_neighbor = neighbor
            actual_sommet = min_weight_neighbor

        return {start: visited}

    def run_parcours_dijkstra(self, start: Sommet, end: Sommet) -> dict[Sommet, set[Sommet]]:
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []

        while len(queue) > 0:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            visited.append(current)
            current[0].visited = True
            for neighbor in self.get_neighbors(current[0]):

                # --- Zone parallèlisable

                if not neighbor.visited:
                    is_in_queue = False
                    for t in queue:
                        if t[0] == neighbor:
                            is_in_queue = True
                            if current[1] + neighbor.weight < t[1]:
                                queue.remove(t)
                                queue.append((neighbor, current[1] + neighbor.weight, current[0]))
                    if not is_in_queue:
                        queue.append((neighbor, current[1] + neighbor.weight, current[0]))

                # --- Fin de zone

            queue.sort(key=lambda t: t[1])

        # --- Zone calcul du meilleur parcours / TODO : à renvoyer en tuple pour la meilleur possibilité
        #
        # back: list[tuple[Sommet, int, Union[Sommet, None]]] = []
        # for t in visited:
        #     if t[0].x == end.x and t[0].y == end.y:
        #         back.append(t)
        #         visited.remove(t)
        #
        # while back[-1][0].x != start.x or back[-1][0].y != start.y:
        #     for t in visited:
        #         if t[0].x == back[-1][2].x and t[0].y == back[-1][2].y:
        #             back.append(t)
        #             visited.remove(t)
        #
        # result: list[Sommet] = []
        # for i in range(len(back) - 1, -1, -1):
        #     result.append(back[i][0])
        #
        # --- Fin de zone

        dico_all_result = self.get_all_result_dict(visited)

        return dico_all_result

    @staticmethod
    def get_all_result_dict(visited: list[tuple[Sommet, int, Union[Sommet, None]]]) -> dict[Sommet, set[Sommet]]:
        result: dict[Sommet, set[Sommet]] = {}
        for t in visited:
            if t[0] != t[2]:

                if t[2] in result.keys():
                    result[t[2]].add(t[0])
                else:
                    result[t[2]] = {t[0]}
        return result

    def parcours_en_largeur(self, start: Sommet, end: Sommet) -> dict[Sommet, set[Sommet]]:
        """
        Vérifie si la grille est connexe jusqu'à l'arrivée. Si c'est le cas prend le chemin le plus court, sinon
        relève une NotConnectedGraphException.

        Args:
            start (Sommet): le sommet de départ
            end (Sommet): le sommet de fin

        Returns:
            dict[Sommet, set[Sommet]]: jsp
        """
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []
        is_end_reached = False
        while len(queue) > 0 and not is_end_reached:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            if current[0].x == end.x and current[0].y == end.y:
                is_end_reached = True
            else:
                visited.append(current)
                current[0].visited = True
                for neighbor in self.get_neighbors(current[0]):
                    if not neighbor.visited:
                        is_in_queue = False
                        for t in queue:
                            if t[0] == neighbor:
                                is_in_queue = True
                                if current[1] + neighbor.weight < t[1]:
                                    queue.insert(queue.index(t), (neighbor, current[1] + neighbor.weight, current[0]))
                                    queue.remove(t)
                        if not is_in_queue:
                            queue.append((neighbor, current[1] + neighbor.weight, current[0]))

        return self.get_all_result_dict(visited)

    def bellman_ford(self, start: Sommet, end: Sommet):
        """
        Implémentation de l'algorithme de Bellman-Ford pour trouver le plus court chemin entre deux sommets.
        """
        # 1. Initialisation des distances et des prédécesseurs
        distances = {sommet: float('inf') for ligne in self.tab for sommet in ligne}
        predecessors = {sommet: None for ligne in self.tab for sommet in ligne}
        distances[start] = 0

        # 2. Relaxation des arêtes sur |V|-1 itérations
        for _ in range(len(distances) - 1):
            for sommet in distances:
                for voisin, poids in sommet.voisins:
                    # Calcul de la nouvelle distance
                    nouvelle_distance = distances[sommet] + poids
                    if nouvelle_distance < distances[voisin]:
                        distances[voisin] = nouvelle_distance
                        predecessors[voisin] = sommet

        # 3. Vérification des chemins manquants (ce qui est déjà fait dans les passes précédentes)

        # 4. Récupérer le plus court chemin
        if distances[end] == float('inf'):
            return None, None  # Aucun chemin trouvé

        # Construction du plus court chemin sous forme de liste
        chemin = []
        current = end
        while current is not None:
            chemin.append(current)
            current = predecessors[current]
        chemin.reverse()  # Le chemin doit être dans l'ordre du départ à l'arrivée

        return distances, chemin  # Renvoie les distances et le chemin