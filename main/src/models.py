import sys
from typing import Union
from exceptions import *
import random

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
    """

    def __init__(self, height: int, width: int) -> None:
        self.height: int = height
        self.width: int = width
        self.WALL: int = sys.maxsize # on prend un entier très grand pour définir ce qu'est un mur
        self.tab: list[list[Sommet]] = \
            [[Sommet(1, x, y) for y in range(width)] for x in range(height)]

    def __str__(self) -> str:
        out: str = ""
        for ligne in self.tab:
            out += (" ".join(str(sommet.weight) for sommet in ligne)) + "\n"
        return out

    def init_grid(self):
        for i in range(len(self.tab)):
            for j in range(len(self.tab[i])):
                self.tab[i][j].visited = False

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
                        if s.y % 2:  # Colone
                            if i == s.x + 1:
                                neighbors.add(self.tab[i][j])
                        else:  # Colone paire
                            if i == s.x - 1:
                                neighbors.add(self.tab[i][j])
                    else:  # Une case coté direct
                        neighbors.add(self.tab[i][j])

        return neighbors

    def is_connexe(self):
        start = self.tab[0][0]

    def parcours_profondeur(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Le parcours en profondeur va parcourir le graphe jusqu'à trouver une impasse (sommet sans voisin) et ensuite
        revenir en arrière afin de retrouver un voisin non visité. Cette application est faites récursivement

        :param start: sommet de départ
        :param end: sommet d'arrivée
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
            if not neighbor.visited and neighbor.weight != self.WALL:
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

    def parcours_dijkstra(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []

        while len(queue) > 0:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            visited.append(current)
            current[0].visited = True
            for neighbor in self.get_neighbors(current[0]):

                # --- Zone parallèlisable (on verra si c'est nécessaire)

                if not neighbor.visited and neighbor.weight != self.WALL:
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

        dico_all_result = self.get_all_result_dict(visited)

        back: list[tuple[Sommet, int, Sommet]] = []
        found_end = False
        for t in visited:
            if t[0].x == end.x and t[0].y == end.y:
                back.append(t)
                visited.remove(t)
                found_end = True

        if not found_end:
            raise NotConnectedGraphException()

        while back[-1][0].x != start.x or back[-1][0].y != start.y:
            for t in visited:
                if t[0].x == back[-1][2].x and t[0].y == back[-1][2].y:
                    back.append(t)
                    visited.remove(t)

        result: list[Sommet] = []
        for i in range(len(back) - 1, -1, -1):
            result.append(back[i][0])

        dico_result: dict[Sommet, Sommet] = dict()
        for i in range(len(result)-1):
            dico_result[result[i]] = result[i+1]

        return dico_all_result, dico_result

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

    def parcours_largeur(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
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
                    if not neighbor.visited and neighbor.weight != self.WALL:
                        is_in_queue = False
                        for t in queue:
                            if t[0] == neighbor:
                                is_in_queue = True
                                if current[1] + neighbor.weight < t[1]:
                                    queue.insert(queue.index(t), (neighbor, current[1] + neighbor.weight, current[0]))
                                    queue.remove(t)
                        if not is_in_queue:
                            queue.append((neighbor, current[1] + neighbor.weight, current[0]))

        result: list[Sommet] = []
        for i in range(len(visited) - 1, -1, -1):
            result.append(visited[i][0])

        dico_result: dict[Sommet, Sommet] = dict()
        for i in range(len(result)-1):
            dico_result[result[i]] = result[i+1]

        dico_all_result = self.get_all_result_dict(visited)

        return dico_all_result, dico_result # ca pue du cul

    import random

    import random

    def allerAToire(self, start: Sommet, end: Sommet) -> tuple[
        dict[Sommet, set[Sommet]], dict[tuple[int, int], tuple[int, int]]]:
        """
        Parcourt la grille de manière aléatoire de start à end.

        Args:
            start (Sommet): le sommet de départ
            end (Sommet): le sommet de fin

        Returns:
            tuple[dict[Sommet, set[Sommet]], dict[tuple[int, int], tuple[int, int]]]:
            - Le premier dictionnaire contient les sommets et leurs voisins atteignables sous forme d'ensemble.
            - Le deuxième dictionnaire contient les coordonnées du chemin parcouru.
        """
        queue: list[Sommet] = [start]
        reachable: dict[Sommet, set[Sommet]] = {start: set()}
        path: dict[tuple[int, int], tuple[int, int]] = {}
        end_reached: bool = False  # Drapeau pour indiquer si la fin est atteinte

        while queue and not end_reached:
            current = queue.pop(0)

            neighbors = self.get_neighbors(current)
            reachable[current] = neighbors

            if neighbors:
                not_walls = [neighbor for neighbor in neighbors if neighbor.weight != self.WALL]
                reachable[current] = set(not_walls)
                if not_walls:
                    neighbor = random.choice(not_walls)
                    queue.append(neighbor)
                    path[(current.x, current.y)] = (neighbor.x, neighbor.y)

                    if neighbor == end:
                        end_reached = True
                else:
                    # Si tous les voisins sont des murs, afficher un message
                    raise NotConnectedGraphException()

        # Vérifier si le sommet de fin n'est jamais atteint
        if not end_reached:
            raise NotConnectedGraphException()

        return reachable, path


    def bron_kerbosch(self) -> list[set[Sommet]]:
        """
        Implémente l'algorithme de Bron-Kerbosch pour trouver les ensembles stables maximaux
        sur un graphe représenté par une grille.

        Args:
            graph (Grille): La grille représentant le graphe.

        Returns:
            list[set[Sommet]]: Liste des ensembles stables maximaux.
        """
        r = set()  # Ensemble courant
        p = {sommet for ligne in self.tab for sommet in ligne}  # Sommets à explorer
        x = set()  # Sommets exclus
        cliques = []  # Résultat des cliques maximales

        stack = [(r, p, x)]  # Pile pour simuler la récursivité
        while stack:
            r, p, x = stack.pop()

            if not p and not x:  # Condition de clique maximale
                cliques.append(r)
            else:
                for sommet in list(p):
                    neighbors = self.get_neighbors(sommet)
                    stack.append((
                        r.union({sommet}),
                        p.intersection(neighbors),
                        x.intersection(neighbors)
                    ))
                    p.remove(sommet)
                    x.add(sommet)

        return cliques

    def bellman_ford(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        # Initialisation des distances avec l'infini (sys.maxsize)
        distances = {sommet: sys.maxsize for ligne in self.tab for sommet in ligne}
        predecessors: dict[Sommet, Union[Sommet, None]] = {sommet: None for ligne in self.tab for sommet in ligne}  # Dictionnaire des prédécesseurs
        next_nodes = {}  # Dictionnaire des voisins sélectionnés, construit dynamiquement dans l'ordre des visites

        distances[start] = 0
        visited_order = []  # Liste pour suivre l'ordre des visites des sommets

        # Pour chaque sommet, on met à jour les distances en fonction des voisins
        for _ in range(len(self.tab) * len(self.tab[0]) - 1):  # Pas besoin de vérifier après len(grille) - 1 itérations
            for ligne in self.tab:
                for sommet in ligne:
                    for voisin in self.get_neighbors(sommet):
                        # Mise à jour des distances si un chemin plus court est trouvé
                        if distances[voisin] > distances[sommet] + voisin.weight:
                            distances[voisin] = distances[sommet] + voisin.weight
                            predecessors[voisin] = sommet

                            # Ajout au dictionnaire dans l'ordre de traitement
                            if sommet not in next_nodes:
                                next_nodes[sommet] = set()
                                visited_order.append(sommet)  # Ajouter le sommet à la liste d'ordre
                            next_nodes[sommet].add(voisin)

        # Vérification des cycles négatifs (optionnel selon le contexte)
        for ligne in self.tab:
            for sommet in ligne:
                for voisin in self.get_neighbors(sommet):
                    if distances[voisin] > distances[sommet] + voisin.weight:
                        raise ValueError("Le graphe contient un cycle négatif")

        # Construction du dictionnaire des chemins optimaux (chemin le plus rapide)
        shortest_path_dict = {}
        current = end
        while current is not None and predecessors[current] is not None:
            shortest_path_dict[current] = predecessors[current]
            current = predecessors[current]

        shortest_path_dict = {v: k for k, v in reversed(list(shortest_path_dict.items()))}

        # Si le sommet 'end' est encore inatteignable, lever une exception
        if distances[end] == sys.maxsize:
            raise NotConnectedGraphException()

        # Réorganisation finale de `next_nodes` selon l'ordre de visite
        ordered_next_nodes = {sommet: next_nodes[sommet] for sommet in visited_order}

        # Retourner les deux dictionnaires dans un tuple
        return ordered_next_nodes, shortest_path_dict

    def a_star(self, start: Sommet, end: Sommet):
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
