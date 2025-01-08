from tkinter import *
from math import cos, sin, sqrt, radians
import random

from exceptions import NotConnectedGraphException
from models import Grille


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
    def __init__(self, num_cols, num_rows):
        Tk.__init__(self)
        self.title("Hexagones")
        self.geometry("800x600")

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

        # Création des boutons (au-dessus de la grille)
        self.create_buttons()

        # Création de la grille d'hexagones
        self.hexagons = {}
        self.init_grid(self.num_cols, self.num_rows, self.hex_size)

        self.selected_color = "black"  # Couleur sélectionnée par défaut pour dessiner

        # Liaisons des événements
        self.canvas.bind("<Button-1>", self.click)  # Clic simple
        self.canvas.bind("<B1-Motion>", self.drag)  # Dragging avec le clic gauche

        self.grille = Grille(num_cols, num_rows)
        self.start = self.grille.tab[0][self.num_rows - 1]
        self.end = self.grille.tab[self.num_cols - 1][0]

    def create_buttons(self):
        """
        Crée les boutons et les place en haut de la fenêtre.
        """
        # Boutons d'en haut, Algo etc
        Button(self, text="Effacer Tout", command=self.clear_all).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        Button(self, text="Effacer Résultats", command=self.clear_results).grid(row=0, column=1, padx=5, pady=5,
                                                                                sticky=W)
        Button(self, text="Aléatoire", command=self.random_colors).grid(row=0, column=2, padx=5, pady=5, sticky=W)
        Button(self, text="Parcours en profondeur").grid(row=0, column=3, padx=5, pady=5, sticky=W)
        Button(self, text="Parcours en largeur").grid(row=0, column=4, padx=5, pady=5, sticky=W)
        Button(self, text="Bellman-Ford").grid(row=0, column=5, padx=5, pady=5, sticky=W)
        Button(self, text="Dijkstra", command=self.launch_dijkstra).grid(row=0, column=6, padx=5, pady=5, sticky=W)
        Button(self, text="A*", command=self.a_star).grid(row=0, column=7, padx=5, pady=5, sticky=W)

        # Boutons couleurs
        (Button(self, text="Noir", bg="black", fg="white", command=lambda: self.set_color("black"))
         .grid(row=1, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Blanc", bg="white", fg="black", command=lambda: self.set_color("white"))
         .grid(row=2, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Bleu", bg="blue", fg="white", command=lambda: self.set_color("blue"))
         .grid(row=3, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Vert", bg="green", fg="white", command=lambda: self.set_color("green"))
         .grid(row=4, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Jaune", bg="yellow", fg="black", command=lambda: self.set_color("yellow"))
         .grid(row=5, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Depart", bg="magenta", fg="white", command=lambda: self.set_color("magenta"))
         .grid(row=6, column=0, padx=5, pady=5, sticky=W))
        (Button(self, text="Objectif", bg="red", fg="white", command=lambda: self.set_color("red"))
         .grid(row=7, column=0, padx=5, pady=5, sticky=W))

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
        self.paint_hexagon(evt.x, evt.y)

    def drag(self, evt):
        """
        Gère le drag pour colorier plusieurs hexagones
        """
        self.paint_hexagon(evt.x, evt.y)

    def get_hexagon_center(self, x, y):
        """
        Calcule le centre d'un hexagone en fonction de ses coordonnées (colonne, ligne).
        """
        offset = self.hex_size * sqrt(3) / 2 if x % 2 else 0
        center_x = x * self.hex_width + self.hex_width / 2
        center_y = y * self.hex_height + self.hex_height / 4 + offset
        return center_x, center_y

    def paint_path(self, start, end):
        """
        Dessine une flèche entre deux hexagones, avec une tendance visuelle en fonction de la disposition hexagonale.
        """
        start_x, start_y = self.get_hexagon_center(start.x, start.y)
        end_x, end_y = self.get_hexagon_center(end.x, end.y)

        # Ajustements pour une tendance visuelle
        if start.x < end.x:  # Mouvement vers la droite
            if start.y % 2 == 0:
                # Si la colonne de départ est pair, la flèche monte légèrement
                start_y -= self.hex_size / 3
                end_y += self.hex_size / 3
            else:
                # Si la colonne de départ est impair, la flèche descend légèrement
                start_y += self.hex_size / 3
                end_y -= self.hex_size / 3
        elif start.x > end.x:  # Mouvement vers la gauche
            if start.y % 2 == 0:
                start_y += self.hex_size / 3
                end_y -= self.hex_size / 3
            else:
                start_y -= self.hex_size / 3
                end_y += self.hex_size / 3

        # Dessiner la flèche
        self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill="black", width=2, arrow=LAST
        )

    def paint_hexagon(self, x, y):
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
                    y, x = hex_id.split("-")
                    x = int(x)
                    y = int(y)
                    # S'il s'agit d'un Départ/Objectif, on remplace le précédent
                    if self.selected_color in ["magenta", "red"]:
                        self.unique_color_replace()
                        self.grille.tab[x][y].weight = 1

                    # On colorie l'hexagone sélectionné
                    hexagon.color = self.selected_color
                    if self.selected_color == "black":
                        self.grille.tab[x][y].weight = self.grille.WALL
                    elif self.selected_color == "white":
                        self.grille.tab[x][y].weight = 1
                    elif self.selected_color == "red":
                        self.end = self.grille.tab[x][y]
                    elif self.selected_color == "magenta":
                        self.start = self.grille.tab[x][y]
                    elif self.selected_color == "blue":
                        self.grille.tab[x][y].weight = 3
                    elif self.selected_color == "green":
                        self.grille.tab[x][y].weight = 5
                    else:
                        self.grille.tab[x][y].weight = 10

                    self.canvas.itemconfigure(closest[0], fill=self.selected_color)
                    # print(f"Hexagone {hex_id} colorié en {self.selected_color}")

    def unique_color_replace(self):
        for hexagon in self.hexagons.values():
            if hexagon.color == self.selected_color:
                hexagon.color = "white"
                self.canvas.itemconfigure(hexagon.id, fill="white")

    def clear_all(self):
        """
        Réinitialise tous les hexagones à blanc
        """
        for hexagon in self.hexagons.values():
            y, x = hexagon.id.split("-")
            x = int(x)
            y = int(y)
            if hexagon.color != 'magenta' and hexagon.color != 'red':
                self.grille.tab[x][y].weight = 1
                hexagon.color = "white"
                self.canvas.itemconfigure(hexagon.id, fill="white")

    def clear_results(self):
        """
        Efface les résultats spécifiques (si nécessaire)
        """
        pass

    def random_colors(self):
        """
        Applique des couleurs aléatoires aux hexagones
        """
        colors = ["black", "white", "blue", "green", "yellow"]
        for hexagon in self.hexagons.values():
            random_color = random.choice(colors)
            hexagon.color = random_color
            self.paint_hexagon()
            self.canvas.itemconfigure(hexagon.id, fill=random_color)

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

    def launch_dijkstra(self):
        self.grille.init_grid()
        try :
            chemins = self.grille.parcours_dijkstra(self.start, self.end)
            self._progressive_display(chemins[1], self.start)
        except NotConnectedGraphException as e:
            print(e.message)

    def _progressive_display(self, chemin, sommet):
        if sommet in chemin.keys():
            suivant = chemin[sommet]
            self.paint_path(sommet, suivant)
            self.after(500, self._progressive_display, chemin, suivant)

