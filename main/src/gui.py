from tkinter import messagebox, Canvas, Tk, DoubleVar, Menu, Frame, Scale, HORIZONTAL, Label, Button, LAST
from math import cos, sin, sqrt, radians
import random

from exceptions import NotConnectedGraphException
from models import Grille, Sommet

BLACK = "black"
WHITE = "#E0E0E0"
BLUE = "#00BCD4"
GREEN = "#9CCC65"
YELLOW = "#FBC02D"
PURPLE = "#BA68C8"
RED = "#D50000"

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
    def __init__(self, num_cols, num_rows, window_height, window_width):
        super().__init__()
        self.title("Hexagones")
        self.geometry(f"{window_height}x{window_width}")

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
                             bg=BLACK)
        self.canvas.grid(row=1, column=1, columnspan=8, rowspan=7)

        # Création de la grille d'hexagones
        self.hexagons = {}
        self.init_grid(self.num_cols, self.num_rows, self.hex_size)

        self.selected_color = BLACK  # Couleur sélectionnée par défaut pour dessiner

        # Liaisons des événements
        self.bind("<Configure>", self.on_resize)
        self.resize_id = None
        self.canvas.bind("<Button-1>", self.click)  # Clic simple
        self.canvas.bind("<B1-Motion>", self.drag)  # Dragging avec le clic gauche

        self.is_stopped_button_pressed = False
        self.sum_weight = 0

        self.grille = Grille(num_cols, num_rows)
        self.start = self.grille.tab[0][self.num_cols - 1]
        self.end = self.grille.tab[self.num_rows - 1][0]

        self.speed = DoubleVar()

        self.paths = []

        self.create_elements()

    def create_elements(self):
        """
        Crée les éléments et les boutons et les place en haut de la fenêtre.
        """

        menu_bar = Menu(self)

        algo_menu = Menu(menu_bar, tearoff=0)
        algo_menu.add_command(label="Parcours en profondeur", command=self.launch_parcours_en_profondeur)
        algo_menu.add_command(label="Parcours en largeur", command=self.launch_parcours_en_largeur)
        algo_menu.add_command(label="Bellman-Ford", command=self.launch_bellman_ford)
        algo_menu.add_command(label="Dijkstra", command=self.launch_dijkstra)
        algo_menu.add_command(label="A*", command=self.a_star)
        algo_menu.add_command(label="AllerÀToire", command=self.launch_allerAToire)
        menu_bar.add_cascade(label="Algorithmes", menu=algo_menu)

        clear_menu = Menu(menu_bar, tearoff=0)
        clear_menu.add_command(label="Effacer Tout", command=self.clear_all)
        clear_menu.add_command(label="Effacer Résultats", command=self.clear_arrows)
        menu_bar.add_cascade(label="Effacer", menu=clear_menu)

        menu_bar.add_command(label="Répartir les poids aléatoirement", command=self.random_colors)
        menu_bar.add_command(label="Afficher la distance parcourue", command=self.weight_popup)

        self.config(menu=menu_bar)

        frame_config_algo_exec = Frame(self)
        frame_config_algo_exec.grid(row=0, column=10, rowspan=5, padx=20, pady=10,
                                  sticky="ne")

        Button(frame_config_algo_exec, text="Stopper l'exécution", command=self.stop_algo_exec).pack(side="bottom", padx=5, pady=5)

        Scale(frame_config_algo_exec, variable=self.speed, from_=1, to=1000, orient=HORIZONTAL).pack(side="top", pady=5)
        Label(frame_config_algo_exec, text="Vitesse d'exécution (en ms)").pack(side="top", pady=5)

        # Boutons couleurs
        Button(self, text="Mur", bg=BLACK, fg=WHITE, command=lambda: self.set_color(BLACK)).grid(row=1, column=0,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="news")
        Button(self, text="Blanc (poids = 1)", bg=WHITE, fg=BLACK, command=lambda: self.set_color(WHITE)).grid(row=2,
                                                                                                               column=0,
                                                                                                               padx=5,
                                                                                                               pady=5,
                                                                                                               sticky="news")
        Button(self, text="Bleu (poids = 3)", bg=BLUE, fg=BLACK, command=lambda: self.set_color(BLUE)).grid(row=3,
                                                                                                            column=0,
                                                                                                            padx=5,
                                                                                                            pady=5,
                                                                                                            sticky="news")
        Button(self, text="Vert (poids = 5)", bg=GREEN, fg=BLACK, command=lambda: self.set_color(GREEN)).grid(row=4,
                                                                                                              column=0,
                                                                                                              padx=5,
                                                                                                              pady=5,
                                                                                                              sticky="news")
        Button(self, text="Jaune (poids = 10)", bg=YELLOW, fg=BLACK, command=lambda: self.set_color(YELLOW)).grid(row=5,
                                                                                                                  column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5,
                                                                                                                  sticky="news")
        Button(self, text="Départ", bg=PURPLE, fg=BLACK, command=lambda: self.set_color(PURPLE)).grid(row=6, column=0,
                                                                                                      padx=5, pady=5,
                                                                                                      sticky="news")
        Button(self, text="Objectif", bg=RED, fg=BLACK, command=lambda: self.set_color(RED)).grid(row=7, column=0,
                                                                                                  padx=5, pady=5,
                                                                                                  sticky="news")

    def init_grid(self, cols, rows, size):
        """
        Initialise une grille 2D d'hexagones, un départ et un objectif
        """
        for c in range(cols):
            offset = size * sqrt(3) / 2 if c % 2 else 0
            for r in range(rows):
                id = f"{c}-{r}"
                h = ColorHexagon(self.canvas,
                                 c * self.hex_width + self.hex_width,
                                 r * self.hex_height + self.hex_height / 2 + offset,
                                 size,
                                 WHITE,
                                 id)
                self.hexagons[id] = h
        self.init_hexagones()

    def set_color(self, color):
        self.selected_color = color

    def stop_algo_exec(self):
        self.is_stopped_button_pressed = True

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
        center_x = y * self.hex_width + self.hex_width + self.hex_height / 3
        center_y = (x * self.hex_height + self.hex_height / 2 + offset) + self.hex_height / 2
        return center_x, center_y

    def paint_path(self, start, end, color):
        """
        Dessine une flèche entre deux hexagones, avec une tendance visuelle en fonction de la disposition hexagonale.
        """
        start_x, start_y = self.get_hexagon_center(start.x, start.y)
        end_x, end_y = self.get_hexagon_center(end.x, end.y)

        self.paths.append(self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=self.hex_size//4, arrow=LAST
        ))

    def paint_hexagon(self, col: int, row: int, color: str):
        hexagon = self.hexagons.get(f"{col}-{row}")

        if color in [PURPLE, RED]:  # Départ ou arrivée
            self.unique_color_replace()
            self.grille.tab[row][col].weight = 1

        if hexagon:
            hexagon.color = color
            if color == BLACK:
                self.grille.tab[row][col].weight = self.grille.WALL
            elif color == WHITE:
                self.grille.tab[row][col].weight = 1
            elif color == RED:
                self.end = self.grille.tab[row][col]
            elif color == PURPLE:
                self.start = self.grille.tab[row][col]
            elif color == BLUE:
                self.grille.tab[row][col].weight = 3
            elif color == GREEN:
                self.grille.tab[row][col].weight = 5
            else:
                self.grille.tab[row][col].weight = 10

        self.canvas.itemconfigure(hexagon.id, fill=color)

    def on_resize(self, event):
        if self.resize_id is not None:
            self.after_cancel(self.resize_id)

        self.resize_id = self.after(100, self.on_resize_released)

    def on_resize_released(self):
        height = self.winfo_height()
        width = self.winfo_width()

        self.hex_size = min((width * 0.6 / ((self.num_cols+1) * 1.5)),
                            (height * 0.95 / ((self.num_rows+1) * sqrt(3))))
        self.hex_width = self.hex_size * 1.5
        self.hex_height = self.hex_size * sqrt(3)
        self.canvas.config(width=(self.num_cols+2)*self.hex_width, height=(self.num_rows+2)*self.hex_height)

        self.canvas.delete("all")

        self.init_grid(self.num_cols, self.num_rows, self.hex_size)

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

                    col, row = map(int, hex_id.split("-"))

                    if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                        color = self.selected_color
                        self.paint_hexagon(col, row, color)

    def unique_color_replace(self):
        for hexagon in self.hexagons.values():
            if hexagon.color == self.selected_color:
                hexagon.color = WHITE
                self.canvas.itemconfigure(hexagon.id, fill=WHITE)

    def clear_arrows(self):
        self.sum_weight = 0
        for arrow in self.paths:
            self.canvas.delete(arrow)
        self.paths = []

    def clear_all(self):
        """
        Réinitialise tous les hexagones à blanc
        """
        for hexagon in self.hexagons.values():
            y, x = map(int, hexagon.id.split("-"))
            if not self.is_sommet_start_or_end(self.grille.tab[x][y]):
                self.grille.tab[x][y].weight = 1
                hexagon.color = WHITE
                self.canvas.itemconfigure(hexagon.id, fill=WHITE)
        self.clear_arrows()

    def clear_results(self):
        """
        Efface les résultats spécifiques (si nécessaire)
        """
        pass

    def is_sommet_start_or_end(self, sommet: Sommet):
        return (self.start.x == sommet.x and self.start.y == sommet.y) or (
                self.end.x == sommet.x and self.end.y == sommet.y)

    def weight_popup(self):
        if self.sum_weight > 0:
            messagebox.showinfo("Distance parourue", f"La distance parcourue par le chemin rouge : {self.sum_weight}")
        else:
            messagebox.showwarning("Aucun parcours detecté", "Il faut exécuter un algorithme afin d'avoir une distance")

    def random_colors(self):
        """
        Applique des couleurs aléatoires aux hexagones
        """
        colors = [BLACK, WHITE, BLUE, GREEN, YELLOW]
        for hex_id, hexagon in self.hexagons.items():
            random_color = random.choice(colors)
            col, row = map(int, hex_id.split("-"))

            if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                self.paint_hexagon(col, row, random_color)

    def init_hexagones(self):
        # Initialisation du départ en bas à gauche
        startHexagon = self.hexagons.get(f"{self.num_cols - 1}-{0}")
        startHexagon.color = PURPLE
        self.canvas.itemconfigure(startHexagon.id, fill=PURPLE)

        # Initialisation de l'objectif en haut à droite
        endHexagon = self.hexagons.get(f"{0}-{self.num_rows - 1}")
        endHexagon.color = RED
        self.canvas.itemconfigure(endHexagon.id, fill=RED)

    def a_star(self):
        """
        Fonction de démonstration pour l'algorithme A*
        """
        pass

    def launch_parcours_en_largeur(self):
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_largeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_parcours_en_profondeur(self):
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_profondeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_allerAToire(self):
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.allerAToire(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_dijkstra(self):
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_dijkstra(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_bellman_ford(self):
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.bellman_ford(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def alert_popup(self, text):
        messagebox.showerror("Erreur d'exécution", text)

    def _display_results(self, chemins, start):
        disp_queue = []
        for sommet in chemins[0].keys():
            for voisin in chemins[0][sommet]:
                disp_queue.append((sommet, voisin))
        self._progressive_display_all(disp_queue, chemins, start)

    def _progressive_display_all(self, chemin: list[tuple], chemins, start):
        if len(chemin) > 0 and not self.is_stopped_button_pressed:
            sommet, suivant = chemin.pop(0)
            self.paint_path(sommet, suivant, "#757575")
            self.after(int(self.speed.get()), self._progressive_display_all, chemin, chemins, start)
        else:
            self._progressive_display_best(chemins[1], start)

    def _progressive_display_best(self, chemin, sommet):
        if sommet in chemin.keys() and not self.is_stopped_button_pressed:
            self.sum_weight += sommet.weight
            suivant = chemin[sommet]
            self.paint_path(sommet, suivant, RED)
            self.after(int(self.speed.get()), self._progressive_display_best, chemin, suivant)
