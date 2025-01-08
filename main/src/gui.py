from tkinter import *
from math import cos, sin, sqrt, radians
import random

from exceptions import NotConnectedGraphException
from models import Grille, Sommet


# TODO faire des constantes pour les couleurs (code rgb)

class ColorHexagon:
    def __init__(self, parent, x, y, length, color, id):
        self.parent = parent  # Grille d'hexagones
        self.x = x  # Longueur x
        self.y = y  # Largeur y
        self.length = length  # Taille
        self.color = color  # Type la case (black,white...)
        self.id = id  # Format Colonne - Ligne
        self.selected = False

        self.draw()

    def draw(self):
        start_x = self.x
        start_y = self.y
        angle = 60  # Angle de l'hexagone en degrés

        # création des 6 côtés de l'hexagone
        coords = []
        for i in range(6):
            end_x = start_x + self.length * cos(radians(angle * i))
            end_y = start_y + self.length * sin(radians(angle * i))
            coords.append([start_x, start_y])
            start_x = end_x
            start_y = end_y
        self.parent.create_polygon(
            *[coord for point in coords for coord in point],
            fill=self.color,
            outline="gray",
            tags=self.id
        )


class App(Tk):
    def __init__(self, num_cols, num_rows, window_width, window_height):
        super().__init__()
        self.title("Hexagones")
        self.geometry(f"{window_width}x{window_height}")

        # Définir la taille initiale de la grille
        self.hex_size = 20
        self.num_cols = num_cols
        self.num_rows = num_rows

        self.hex_width = self.hex_size * 1.5  # Largeur d'un hexagone
        self.hex_height = self.hex_size * sqrt(3)  # Hauteur d'un hexagone

        # Crée un canevas pour afficher les hexagones
        self.canvas = Canvas(self,
                             width=self.hex_width * self.num_cols + self.hex_width / 2,
                             height=self.hex_height * self.num_rows + self.hex_height,
                             bg="black")
        self.canvas.grid(row=1, column=1, columnspan=8, rowspan=7)

        # Création de la grille d'hexagones
        self.hexagons = {}
        self.init_grid(self.num_cols, self.num_rows, self.hex_size)

        self.selected_color = "black"  # Couleur sélectionnée par défaut pour dessiner

        # Liaisons des événements
        self.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.click)  # Clic simple
        self.canvas.bind("<B1-Motion>", self.drag)  # Dragging avec le clic gauche

        self.grille = Grille(num_cols, num_rows)
        self.start = self.grille.tab[0][self.num_rows - 1]
        self.end = self.grille.tab[self.num_cols - 1][0]

        self.speed = DoubleVar()

        self.paths = []

        self.create_elements()

    def create_elements(self):
        """
        Crée les elements et les boutons et les place en haut de la fenêtre. TODO docstring a refaire
        """
        # Boutons d'en haut, Algo etc
        Button(self, text="Effacer Tout", command=self.clear_all).grid(row=0, column=0, padx=5, pady=5, sticky="news")
        Button(self, text="Effacer Résultats", command=self.clear_arrows).grid(row=0, column=1, padx=5, pady=5,
                                                                               sticky="news")
        Button(self, text="Répartir les poids aléatoirement", command=self.random_colors).grid(row=0, column=2, padx=5,
                                                                                               pady=5, sticky="news")
        Button(self, text="Parcours en profondeur", command=self.launch_parcours_en_profondeur).grid(row=0, column=3,
                                                                                                     padx=5, pady=5,
                                                                                                     sticky="news")
        Button(self, text="Parcours en largeur", command=self.launch_parcours_en_largeur).grid(row=0, column=4, padx=5,
                                                                                               pady=5, sticky="news")
        Button(self, text="Bellman-Ford", command=self.launch_bellman_ford).grid(row=0, column=5, padx=5, pady=5,
                                                                                 sticky="news")
        Button(self, text="Dijkstra", command=self.launch_dijkstra).grid(row=0, column=6, padx=5, pady=5, sticky="news")
        Button(self, text="A*", command=self.a_star).grid(row=0, column=7, padx=5, pady=5, sticky="news")
        Button(self, text="AllerÀToire", command=self.launch_allerAToire).grid(row=0, column=8, padx=5, pady=5,
                                                                               sticky="news")
        (Scale(self, variable=self.speed, from_=1, to=1000, orient=HORIZONTAL)
         .grid(row=3, column=8, padx=5, pady=5, sticky="news"))

        # Boutons couleurs
        (Button(self, text="Noir", bg="black", fg="white", command=lambda: self.set_color("black"))
         .grid(row=1, column=0, padx=5, pady=5, sticky="ew"))
        (Button(self, text="Blanc", bg="white", fg="black", command=lambda: self.set_color("white"))
         .grid(row=2, column=0, padx=5, pady=5, sticky="news"))
        (Button(self, text="Bleu", bg="blue", fg="white", command=lambda: self.set_color("blue"))
         .grid(row=3, column=0, padx=5, pady=5, sticky="ew"))
        (Button(self, text="Vert", bg="green", fg="white", command=lambda: self.set_color("green"))
         .grid(row=4, column=0, padx=5, pady=5, sticky="ew"))
        (Button(self, text="Jaune", bg="yellow", fg="black", command=lambda: self.set_color("yellow"))
         .grid(row=5, column=0, padx=5, pady=5, sticky="ew"))
        (Button(self, text="Depart", bg="magenta", fg="white", command=lambda: self.set_color("magenta"))
         .grid(row=6, column=0, padx=5, pady=5, sticky="ew"))
        (Button(self, text="Objectif", bg="red", fg="white", command=lambda: self.set_color("red"))
         .grid(row=7, column=0, padx=5, pady=5, sticky="ew"))

    def init_grid(self, cols, rows, size):
        """
        Initialise une grille 2D d'hexagones, un départ et un objectif
        """
        for c in range(cols):
            offset = size * sqrt(3) / 2 if c % 2 else 0
            for r in range(rows):
                id = f"{c}-{r}"
                h = ColorHexagon(self.canvas,
                                 c * self.hex_width + self.hex_width / 2,
                                 r * self.hex_height + self.hex_height / 4 + offset,
                                 size,
                                 "white",
                                 id)
                self.hexagons[id] = h
        self.init_hexagones()

    def set_color(self, color):
        self.selected_color = color

    def click(self, evt):
        """
        Gère le clic simple pour colorier les hexagones
        """
        self.paint_hexagon_on_click(evt.x, evt.y)

    def drag(self, evt):
        """
        Gère le drag pour colorier plusieurs hexagones
        """
        self.paint_hexagon_on_click(evt.x, evt.y)

    def get_hexagon_center(self, x, y):
        """
        Calcule le centre d'un hexagone en fonction de ses coordonnées (colonne, ligne).
        """
        offset = self.hex_size * sqrt(3) / 2 if y % 2 else 0
        center_x = y * self.hex_width + self.hex_width * 0.8
        center_y = (x * self.hex_height + self.hex_height / 4 + offset) + self.hex_height / 2
        return center_x, center_y

    def paint_path(self, start, end, color):
        """
        Dessine une flèche entre deux hexagones, avec une tendance visuelle en fonction de la disposition hexagonale.
        """
        start_x, start_y = self.get_hexagon_center(start.x, start.y)
        end_x, end_y = self.get_hexagon_center(end.x, end.y)

        self.paths.append(self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=2, arrow=LAST
        ))

    def paint_hexagon(self, x: int, y: int, color: str):
        hexagon = self.hexagons.get(f"{x}-{y}")

        if color in ["magenta", "red"]:  # Départ ou arrivée
            self.unique_color_replace()
            self.grille.tab[x][y].weight = 1

        if hexagon:
            hexagon.color = color
            if color == "black":
                self.grille.tab[y][x].weight = self.grille.WALL
            elif color == "white":
                self.grille.tab[y][x].weight = 1
            elif color == "red":
                self.end = self.grille.tab[y][x]
            elif color == "magenta":
                self.start = self.grille.tab[y][x]
            elif color == "blue":
                self.grille.tab[y][x].weight = 3
            elif color == "green":
                self.grille.tab[y][x].weight = 5
            else:
                self.grille.tab[y][x].weight = 10

        self.canvas.itemconfigure(hexagon.id, fill=color)
        # self.canvas.itemconfigure(closest[0], fill=color)

    def on_resize(self, event):
        height = self.winfo_height()
        width = self.winfo_width()

        self.hex_size = (height*0.6) / self.num_cols / sqrt(3)  # TODO : trouver relation de hex_size
        self.hex_width = width * 0.6 / self.num_cols
        self.hex_height = height * 0.6 / self.num_rows
        self.canvas.config(width=width * 0.6, height=height * 0.6)

        self.canvas.delete("all")

        self.init_grid(self.num_cols, self.num_rows, self.hex_width)

    def paint_hexagon_on_click(self, x, y):
        """
        Colorie un hexagone en fonction des coordonnées (x, y)
        """
        closest = self.canvas.find_closest(x, y)
        if closest:
            tags = self.canvas.gettags(closest[0])
            if tags:
                hex_id = tags[0]  # Le premier tag correspond à l'ID de l'hexagone
                hexagon = self.hexagons.get(hex_id)  # Récupère l'hexagone correspondant
                if hexagon:

                    row, col = map(int, hex_id.split("-"))

                    if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                        color = self.selected_color
                        self.paint_hexagon(row, col, color)

    def unique_color_replace(self):
        for hexagon in self.hexagons.values():
            if hexagon.color == self.selected_color:
                hexagon.color = "white"
                self.canvas.itemconfigure(hexagon.id, fill="white")

    def clear_arrows(self):
        for arrow in self.paths:
            self.canvas.delete(arrow)
        self.paths = []

    def clear_all(self):
        """
        Réinitialise tous les hexagones à blanc
        """
        for hexagon in self.hexagons.values():
            y, x = map(int, hexagon.id.split("-"))
            if hexagon.color != 'magenta' and hexagon.color != 'red':
                self.grille.tab[x][y].weight = 1
                hexagon.color = "white"
                self.canvas.itemconfigure(hexagon.id, fill="white")
        self.clear_arrows()

    def clear_results(self):
        """
        Efface les résultats spécifiques (si nécessaire)
        """
        pass

    def is_sommet_start_or_end(self, sommet: Sommet):
        return (self.start.x == sommet.x and self.start.y == sommet.y) or (
                self.end.x == sommet.x and self.end.y == sommet.y)

    def random_colors(self):
        """
        Applique des couleurs aléatoires aux hexagones
        """
        colors = ["black", "white", "blue", "green", "yellow"]
        for hex_id, hexagon in self.hexagons.items():
            random_color = random.choice(colors)
            col, row = map(int, hex_id.split("-"))

            if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                self.paint_hexagon(col, row, random_color)

    def init_hexagones(self):
        # Initialisation du départ en bas à gauche
        startHexagon = self.hexagons.get(f"{self.num_cols - 1}-{0}")
        startHexagon.color = "magenta"
        self.canvas.itemconfigure(startHexagon.id, fill="magenta")

        # Initialisation de l'objectif en haut à droite
        endHexagon = self.hexagons.get(f"{0}-{self.num_rows - 1}")
        endHexagon.color = "red"
        self.canvas.itemconfigure(endHexagon.id, fill="red")

    def a_star(self):
        """
        Fonction de démonstration pour l'algorithme A*
        """
        pass

    def launch_parcours_en_largeur(self):
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_largeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def launch_parcours_en_profondeur(self):
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_profondeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def launch_allerAToire(self):
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.allerAToire(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def launch_dijkstra(self):
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_dijkstra(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def launch_bellman_ford(self):
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.bellman_ford(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def _display_results(self, chemins, start):
        disp_queue = []
        for sommet in chemins[0].keys():
            for voisin in chemins[0][sommet]:
                disp_queue.append((sommet, voisin))
        self._progressive_display_all(disp_queue, chemins, start)

    def _progressive_display_all(self, chemin: list[tuple], chemins, start):
        if len(chemin) > 0:
            sommet, suivant = chemin.pop(0)
            self.paint_path(sommet, suivant, "grey")
            self.after(int(self.speed.get()), self._progressive_display_all, chemin, chemins, start)
        else:
            self._progressive_display_best(chemins[1], start)

    def _progressive_display_best(self, chemin, sommet):
        if sommet in chemin.keys():
            suivant = chemin[sommet]
            self.paint_path(sommet, suivant, "red")
            self.after(int(self.speed.get()), self._progressive_display_best, chemin, suivant)
