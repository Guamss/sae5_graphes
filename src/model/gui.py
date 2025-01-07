from tkinter import *
from math import cos, sin, sqrt, radians
import random


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

        # Création des 6 côtés de l'hexagone
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
    def __init__(self):
        Tk.__init__(self)
        self.title("Hexagones")
        self.geometry("800x600")

        # Définir la taille initiale de la grille
        self.hex_size = 20
        self.num_cols = 20
        self.num_rows = 12

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

        self.selected_color = "black"  # Couleur sélectionnée par défaut (noir)

        # Liaisons des événements
        self.canvas.bind("<Button-1>", self.click)  # Clic simple
        self.canvas.bind("<B1-Motion>", self.drag)  # Dragging avec le clic gauche


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
        Button(self, text="Dijkstra").grid(row=0, column=6, padx=5, pady=5, sticky=W)
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
                id = f"{c + 1}-{r + 1}"
                h = ColorHexagon(self.canvas,
                                 c * self.hex_width + self.hex_width / 2,
                                 r * self.hex_height + self.hex_height / 4 + offset,
                                 size,
                                 "white",
                                 id)
                self.hexagons[id] = h

            # TODO : peindre le Départ et la fin
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

    def paint_hexagon(self, x, y):
        """
        Colorie un hexagone en fonction des coordonnées (x, y)
        """
        closest = self.canvas.find_closest(x, y)
        if closest:
            tags = self.canvas.gettags(closest[0])
            if tags:
                hex_id = tags[0]  # Le premier tag correspond à l'ID
                hexagon = self.hexagons.get(hex_id)  # Accès direct au dictionnaire
                if hexagon:
                    hexagon.color = self.selected_color
                    self.canvas.itemconfigure(closest[0], fill=self.selected_color)


    def unique_color_check(self, color):
        pass

    def clear_all(self):
        """
        Réinitialise tous les hexagones à blanc
        """
        for hexagon in self.hexagons.values():
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
            self.canvas.itemconfigure(hexagon.id, fill=random_color)

    def a_star(self):
        """
        Fonction de démonstration pour l'algorithme A*
        """
        pass


if __name__ == '__main__':
    app = App()
    app.mainloop()


