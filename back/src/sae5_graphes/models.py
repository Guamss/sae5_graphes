import sys
from typing import Union
from exceptions import *
import random


class Sommet:
    """
    Représente un sommet dans un graphe, avec un poids et des coordonnées dans un espace 2D.

    Attributes:
        weight (int): Le poids du sommet dans le graphe.
        x (int): La coordonnée en abscisse (ligne).
        y (int): La coordonnée en ordonnée (colonne).
        visited (bool): Indicateur si le sommet a été visité lors d'une recherche.

    Args:
        weight (int): Le poids du sommet.
        x (int): Coordonnée x (ligne).
        y (int): Coordonnée y (colonne).
    """

    def __init__(self, weight: int, x: int, y: int) -> None:
        self.weight: int = weight
        self.x: int = x  # La ligne
        self.y: int = y  # La colonne
        self.visited = False

    def __eq__(self, other: object) -> bool:
        """
        Compare deux sommets pour savoir s'ils ont les mêmes coordonnées.

        Args:
            other (object): L'autre objet à comparer.

        Returns:
            bool: True si les coordonnées (x, y) sont identiques, sinon False.
        """
        if not isinstance(other, Sommet):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """
        Retourne un hash basé sur les coordonnées du sommet.

        Returns:
            int: Le hash du sommet.
        """
        return hash((self.x, self.y))

    def __str__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères du sommet.

        Returns:
            str: Représentation du sommet.
        """
        return f"{self.weight} | [{self.x}, {self.y}]"

    def __repr__(self) -> str:
        """
        Retourne une représentation officielle du sommet.

        Returns:
            str: Représentation officielle du sommet.
        """
        return f"({self.x}, {self.y})"


class Grille:
    """
    Représente une grille de sommets organisés dans un tableau 2D, utilisée pour effectuer des algorithmes de recherche de chemin.

    Attributes:
        height (int): La hauteur de la grille (nombre de lignes).
        width (int): La largeur de la grille (nombre de colonnes).
        tab (list[list[Sommet]]): Un tableau 2D contenant les sommets de la grille.
        WALL (int): Valeur représentant un mur dans la grille.

    Args:
        height (int): Hauteur de la grille.
        width (int): Largeur de la grille.
    """

    def __init__(self, height: int, width: int) -> None:
        self.height: int = height
        self.width: int = width
        self.WALL: int = 10000  # Un très grand nombre représentant un mur.
        self.tab: list[list[Sommet]] = \
            [[Sommet(1, x, y) for y in range(height)] for x in range(width)]

    def __str__(self) -> str:
        out: str = ""
        for ligne in self.tab:
            out += (" ".join(str(sommet.weight) for sommet in ligne)) + "\n"
        return out

    def init_grid(self):
        """
        Réinitialise la grille en marquant tous les sommets comme non visités.
        Cette méthode permet de préparer la grille pour une nouvelle exécution d'algorithmes de recherche.
        """
        for i in range(len(self.tab)):
            for j in range(len(self.tab[i])):
                self.tab[i][j].visited = False

    def get_neighbors(self, s: Sommet) -> set[Sommet]:
        """
        Retourne les voisins d'un sommet donné.

        Args:
            s (Sommet): Le sommet pour lequel obtenir les voisins.

        Returns:
            set[Sommet]: Un ensemble de voisins du sommet s.
        """
        neighbors: set[Sommet] = set()
        for i in range(s.x - 1, s.x + 2):
            for j in range(s.y - 1, s.y + 2):
                if 0 <= i < self.width and 0 <= j < self.height and (i != s.x or j != s.y):  # in Grille && !current
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

    def get_nbr_wall(self) -> int:
        """
        Calcule et retourne le nombre total de murs dans la grille.

        Returns:
            int: Le nombre total de murs.
        """
        nbr_wall: int = 0
        for ligne in self.tab:  # Parcourt chaque ligne (liste de sommets)
            for sommet in ligne:  # Parcourt chaque sommet de la ligne
                if sommet.weight == self.WALL:
                    nbr_wall += 1
        return nbr_wall
    def parcours_profondeur(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Effectue un parcours en profondeur du graphe pour trouver un chemin entre le sommet de départ et d'arrivée.
        Cette méthode parcourt récursivement le graphe et backtrack lorsqu'elle atteint une impasse.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant deux dictionnaires :
                - Le premier dictionnaire contient les sommets visités et leurs voisins.
                - Le second dictionnaire contient les prédécesseurs pour chaque sommet sur le chemin.
        """
        visited = {}
        self.parcours_profondeur_recursive(start, end, visited)

        if len(visited) != (self.height * self.width) - self.get_nbr_wall() and end not in visited:
            raise NotConnectedGraphException()

        solution: dict[Sommet, Sommet] = {}
        courant = end
        antecedent = None

        while courant != start:
            for sommet in visited:
                if courant in visited[sommet]:
                    antecedent = courant
                    courant = sommet
            solution[courant] = antecedent
        return visited, solution

    def parcours_profondeur_recursive(self, s: Sommet, end: Sommet, visited: dict[Sommet, set[Sommet]], ):
        """
        Méthode récursive pour le parcours en profondeur.

        Args:
            s (Sommet): Le sommet actuellement exploré.
            end (Sommet): Le sommet de fin.
            visited (dict): Dictionnaire des sommets visités et leurs voisins.

        Returns:
            bool: Retourne True si un chemin vers le sommet d'arrivée a été trouvé, sinon False.
        """
        s.visited = True
        if s not in visited:
            visited[s] = set()

        for neighbor in self.get_neighbors(s):
            if not neighbor.visited and neighbor.weight != self.WALL:
                visited[s].add(neighbor)
                if self.parcours_profondeur_recursive(neighbor, end, visited):
                    return True
        return False

    def parcours_dijkstra(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Implémente l'algorithme de Dijkstra pour trouver le chemin le plus court entre deux sommets.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant deux dictionnaires :
                - Le premier dictionnaire contient tous les résultats intermédiaires des sommets visités.
                - Le second dictionnaire contient le chemin le plus court du sommet de départ au sommet d'arrivée.
        """
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []

        while len(queue) > 0:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            visited.append(current)
            current[0].visited = True
            for neighbor in self.get_neighbors(current[0]):
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
        """
        Génère un dictionnaire des résultats de tous les sommets visités, associant chaque sommet à ses voisins.

        Args:
            visited (list): Liste des tuples contenant le sommet, la distance et son prédécesseur.

        Returns:
            dict: Un dictionnaire où chaque clé est un sommet et chaque valeur est un ensemble de ses voisins.
        """
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
        Implémente l'algorithme de parcours en largeur pour trouver le chemin le plus court entre deux sommets.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant deux dictionnaires :
                - Le premier dictionnaire contient les sommets visités et leurs voisins atteignables.
                - Le second dictionnaire contient les prédécesseurs pour chaque sommet sur le chemin.
        """
        queue: list[tuple[Sommet, int, Union[Sommet, None]]] = [(start, 0, start)]
        visited: list[tuple[Sommet, int, Union[Sommet, None]]] = []
        is_end_reached = False
        while len(queue) > 0 and not is_end_reached:
            current: tuple[Sommet, int, Sommet] = queue.pop(0)
            if current[0].x == end.x and current[0].y == end.y:
                is_end_reached = True
                visited.append(current)
                current[0].visited = True
            else:
                visited.append(current)
                current[0].visited = True
                for neighbor in self.get_neighbors(current[0]):
                    if not neighbor.visited and neighbor.weight != self.WALL:
                        is_in_queue = False
                        for t in queue:
                            if t[0] == neighbor:
                                is_in_queue = True
                        if not is_in_queue:
                            queue.append((neighbor, current[1] + neighbor.weight, current[0]))

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
        for i in range(len(result) - 1):
            dico_result[result[i]] = result[i + 1]

        return dico_all_result, dico_result

    def allerAToire(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Effectue un parcours aléatoire de la grille de start à end, en choisissant des voisins au hasard.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant :
                - Le premier dictionnaire contient les sommets et leurs voisins atteignables.
                - Le second dictionnaire contient les prédécesseurs pour reconstruire le chemin parcouru.
        """
        queue: list[Sommet] = [start]
        reachable: dict[Sommet, set[Sommet]] = {start: set()}
        path: dict[Sommet, Sommet] = dict()
        visited: set[Sommet] = set()
        known: set[Sommet] = set()
        end_reached: bool = False

        while queue and not end_reached:
            current = queue.pop()
            visited.add(current)
            known = known.union(set(self.get_neighbors(current)))

            neighbors = self.get_neighbors(current)

            all_walls: bool = True
            for s in known-visited:
                if s.weight != self.WALL:
                    all_walls = False
            if all_walls:
                raise NotConnectedGraphException()

            if neighbors:
                not_walls = [neighbor for neighbor in neighbors if neighbor.weight != self.WALL]
                if not_walls:
                    neighbor = random.choice(not_walls)
                    queue.append(neighbor)
                    if current in reachable.keys():
                        reachable[current].add(neighbor)
                    else:
                        reachable[current] = {neighbor}
                    path[current] = neighbor

                    if neighbor.x == end.x and neighbor.y == end.y:
                        end_reached = True

        return reachable, path

    def bellman_ford(self, start: Sommet, end: Sommet) -> tuple[
        dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Implémente l'algorithme de Bellman-Ford pour déterminer les chemins les plus courts à partir d'un sommet source.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant deux dictionnaires :
                - Le premier dictionnaire contient les sommets et leurs voisins atteignables.
                - Le second dictionnaire contient les prédécesseurs pour reconstruire le chemin le plus court.
        """
        distances = {sommet: float('inf') for ligne in self.tab for sommet in ligne}
        distances[start] = 0
        predecessors = {sommet: None for ligne in self.tab for sommet in ligne}

        visited_order = []

        for _ in range(self.width * self.height - 1):
            for ligne in self.tab:
                for sommet in ligne:
                    for neighbor in self.get_neighbors(sommet):
                        if sommet.weight != self.WALL and neighbor.weight != self.WALL:
                            new_distance = distances[sommet] + neighbor.weight
                            if new_distance < distances[neighbor]:
                                distances[neighbor] = new_distance
                                predecessors[neighbor] = sommet
                                if neighbor not in visited_order:
                                    visited_order.append(neighbor)

        reachable = {}
        for sommet in visited_order:
            pred = predecessors[sommet]
            if pred:
                if pred in reachable:
                    reachable[pred].add(sommet)
                else:
                    reachable[pred] = {sommet}

        shortest_path = {}
        current = end
        while current != start and predecessors[current] is not None:
            shortest_path[predecessors[current]] = current
            current = predecessors[current]

        if current != start:
            raise NotConnectedGraphException()

        return reachable, shortest_path

    def heuristique_manhattan(self, end: Sommet) -> dict[Sommet:int]:
        """
        Calcule la distance heuristique de Manhattan entre chaque sommet de la grille et le sommet d'arrivée.

        Args:
            end (Sommet): Le sommet d'arrivée.

        Returns:
            dict: Un dictionnaire où chaque clé est un sommet et la valeur est sa distance heuristique vers l'arrivée.
        """
        distance_heuristique = {}
        for ligne in self.tab:
            for sommet in ligne:
                if sommet.weight != self.WALL:
                    distance = abs(end.x - sommet.x) + abs(end.y - sommet.y)
                    distance_heuristique[sommet] = distance
        return distance_heuristique

    def a_star(self, start: Sommet, end: Sommet) -> tuple[dict[Sommet, set[Sommet]], dict[Sommet, Sommet]]:
        """
        Implémente l'algorithme A* pour trouver le chemin le plus court entre deux sommets, en utilisant une heuristique de Manhattan.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet d'arrivée.

        Returns:
            tuple: Un tuple contenant deux dictionnaires :
                - Le premier dictionnaire contient les sommets visités et leurs voisins atteignables.
                - Le second dictionnaire contient les prédécesseurs pour reconstruire le chemin le plus court.
        """
        heuristique_manhattan = self.heuristique_manhattan(end)  # Valeur heuriqtique de chaque sommet
        cout_deplacement: dict[Sommet: int] = {start: 0}
        cout_acces_total: dict[Sommet: int] = {
            start: heuristique_manhattan[start]}  # heuristique manhattan + déplacement

        queue: list[tuple[Sommet: int]] = [(start, cout_acces_total[start])]
        predecesseur: dict[Sommet: Sommet] = {start: None}
        chemin_parcouru: dict[Sommet, set[Sommet]] = {}

        courant = queue.pop(0)[0]
        courant.visited = True
        while courant != end:
            courant_voisin = self.get_neighbors(courant)
            if courant not in chemin_parcouru:
                chemin_parcouru[courant] = set()
            for voisin in courant_voisin:
                if voisin.weight == self.WALL or voisin.visited:
                    continue
                chemin_parcouru[courant].add(voisin)
                voisin.visited = True
                predecesseur[voisin] = courant
                cout_deplacement[voisin] = cout_deplacement[courant] + voisin.weight
                cout_acces_total[voisin] = heuristique_manhattan[voisin] + cout_deplacement[voisin]
                queue.append((voisin, cout_acces_total[voisin]))
                queue.sort(key=lambda x: x[1])
            if len(queue) == 0:
                raise NotConnectedGraphException()
            courant = queue.pop(0)[0]
        # Solution
        solution: dict[Sommet, Sommet] = {}
        courant = end

        while courant != start:
            courant_predecesseur = predecesseur[courant]
            solution[courant_predecesseur] = courant
            courant = predecesseur[courant]
        return chemin_parcouru, solution
