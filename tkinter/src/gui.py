from tkinter import messagebox, Canvas, Tk, IntVar, Menu, Frame, Scale, HORIZONTAL, Label, Button, LAST
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
        self.color = color
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
        """
        Initialise l'application avec une grille d'hexagones.

        Args:
            num_cols (int): Le nombre de colonnes d'hexagones.
            num_rows (int): Le nombre de lignes d'hexagones.
            window_height (int): Hauteur de la fenêtre.
            window_width (int): Largeur de la fenêtre.
        """
        super().__init__()
        self.scale_widget = None
        self.title("Hexagones")
        self.geometry(f"{window_height}x{window_width}")

        # Définir la taille initiale de la grille
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.hex_size = min((window_width * 0.6 / ((self.num_cols+1) * 1.5)),
                            (window_height * 0.9 / ((self.num_rows+1) * sqrt(3))))

        self.hex_width = self.hex_size * 1.5  # Largeur d'un hexagone
        self.hex_height = self.hex_size * sqrt(3)  # Hauteur d'un hexagone

        self.canvas = Canvas(self,
                             width=self.hex_width * self.num_cols + self.hex_width / 2,
                             height=self.hex_height * self.num_rows + self.hex_height,
                             bg=BLACK)
        self.canvas.grid(row=1, column=1, columnspan=8, rowspan=7)

        self.selected_color = BLACK

        self.bind("<Configure>", self.on_resize)
        self.resize_id = None
        self.canvas.bind("<Button-1>", self.click)  # Clic simple
        self.canvas.bind("<B1-Motion>", self.drag)  # Drag

        self.is_stopped_button_pressed = False
        self.sum_weight = 0

        self.grille = Grille(num_cols, num_rows)
        self.start = self.grille.tab[0][self.num_cols - 1]
        self.end = self.grille.tab[self.num_rows - 1][0]

        self.speed = IntVar()
        self.old_speed = None

        self.paths = []
        self.chemins = None

        self.create_elements()

        self.hexagons = {}
        self.init_grid(self.num_cols, self.num_rows, self.hex_size)

        self.fen_size: tuple = (window_height, window_width)

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

        self.scale_widget = Scale(frame_config_algo_exec, variable=self.speed, from_=1, to=1000, orient=HORIZONTAL)
        self.scale_widget.pack(side="top", pady=5)
        Label(frame_config_algo_exec, text="Vitesse d'exécution (en ms)").pack(side="top", pady=5)

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
        Initialise une grille 2D d'hexagones, un départ et un objectif.

        Args:
            cols (int): Le nombre de colonnes d'hexagones.
            rows (int): Le nombre de lignes d'hexagones.
            size (float): La taille des hexagones.
        """
        old_selected = self.selected_color
        self.selected_color = None
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
                if self.start == self.grille.tab[r][c]:
                    self.paint_hexagon(c, r, PURPLE)
                elif self.end == self.grille.tab[r][c]:
                    self.paint_hexagon(c, r, RED)
                else:
                    colors = {
                        1: WHITE,
                        3: BLUE,
                        5: GREEN,
                        10: YELLOW,
                        self.grille.WALL: BLACK
                    }
                    self.paint_hexagon(c, r, colors[self.grille.tab[r][c].weight])

        self.init_hexagones()
        self.selected_color = old_selected

    def set_color(self, color):
        """
        Définit la couleur sélectionnée pour colorier un hexagone.

        Args:
            color (str): La couleur à appliquer.
        """
        self.selected_color = color

    def stop_algo_exec(self):
        """
        Arrête l'exécution de l'algorithme en cours.
        """
        self.is_stopped_button_pressed = True

    def click(self, evt):
        """
        Gère le clic simple pour colorier les hexagones.

        Args:
            evt (Event): L'événement de clic.
        """
        self.paint_hexagon_on_click(evt.x, evt.y)

    def drag(self, evt):
        """
        Gère le drag pour colorier plusieurs hexagones.

        Args:
            evt (Event): L'événement de drag.
        """
        self.paint_hexagon_on_click(evt.x, evt.y)

    def get_hexagon_center(self, x, y):
        """
        Calcule le centre d'un hexagone en fonction de ses coordonnées (colonne, ligne).

        Args:
            x (int): La colonne de l'hexagone.
            y (int): La ligne de l'hexagone.

        Returns:
            tuple: Un tuple (x, y) représentant le centre de l'hexagone.
        """
        offset = self.hex_size * sqrt(3) / 2 if y % 2 else 0
        center_x = y * self.hex_width + self.hex_width + self.hex_height / 3
        center_y = (x * self.hex_height + self.hex_height / 2 + offset) + self.hex_height / 2
        return center_x, center_y

    def paint_path(self, start, end, color):
        """
        Dessine une flèche entre deux hexagones, avec une tendance visuelle en fonction de la disposition hexagonale.

        Args:
            start (Sommet): Le sommet de départ.
            end (Sommet): Le sommet de fin.
            color (str): La couleur de la flèche.
        """
        start_x, start_y = self.get_hexagon_center(start.x, start.y)
        end_x, end_y = self.get_hexagon_center(end.x, end.y)

        self.paths.append(self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=self.hex_size//5, arrow=LAST
        ))

    def paint_hexagon(self, col: int, row: int, color: str):
        """
        Colorie un hexagone avec la couleur spécifiée.

        Args:
            col (int): La colonne de l'hexagone.
            row (int): La ligne de l'hexagone.
            color (str): La couleur à appliquer.
        """
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
        """
        Gère le redimensionnement de la fenêtre.

        Args:
            event (Event): L'événement de redimensionnement.
        """
        if self.resize_id is not None:
            self.after_cancel(self.resize_id)

        self.resize_id = self.after(300, self.on_resize_released)

    def on_resize_released(self):
        """
        Recalcule les dimensions de la grille après un redimensionnement de la fenêtre.
        """
        height = self.winfo_height()

        width = self.winfo_width()

        if self.fen_size != (height, width):
            self.fen_size = (height, width)

            self.hex_size = min((width * 0.6 / ((self.num_cols+1) * 1.5)),
                                (height * 0.9 / ((self.num_rows+1) * sqrt(3))))
            self.hex_width = self.hex_size * 1.5
            self.hex_height = self.hex_size * sqrt(3)
            self.canvas.config(width=(self.num_cols+2)*self.hex_width, height=(self.num_rows+2)*self.hex_height)

            self.canvas.delete("all")

            self.init_grid(self.num_cols, self.num_rows, self.hex_size)
            if self.chemins:
                self.old_speed = self.speed.get()
                self.scale_widget.config(state='disabled', from_=0)
                self.speed.set(0)
                for arrow in self.paths:
                    self.canvas.delete(arrow)
                self.paths = []
                self._display_results(self.chemins[:], self.start)

    def paint_hexagon_on_click(self, x, y):
        """
        Colorie un hexagone en fonction des coordonnées (x, y) après un clic.

        Args:
            x (int): La position X du clic.
            y (int): La position Y du clic.
        """
        closest = self.canvas.find_closest(x, y)
        if closest:
            tags = self.canvas.gettags(closest[0])
            if tags:
                hex_id = tags[0]
                hexagon = self.hexagons.get(hex_id)
                if hexagon:

                    col, row = map(int, hex_id.split("-"))

                    if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                        color = self.selected_color
                        self.paint_hexagon(col, row, color)

    def unique_color_replace(self):
        """
        Remplace la couleur sélectionnée par défaut (blanc) dans toute la grille.
        """
        for hexagon in self.hexagons.values():
            if hexagon.color == self.selected_color:
                hexagon.color = WHITE
                self.canvas.itemconfigure(hexagon.id, fill=WHITE)

    def clear_arrows(self):
        """
        Efface toutes les flèches (chemins) affichées sur le canevas.
        """
        self.sum_weight = 0
        for arrow in self.paths:
            self.canvas.delete(arrow)
        self.paths = []
        self.chemins = None

    def clear_all(self):
        """
        Réinitialise tous les hexagones à blanc.
        """
        for hexagon in self.hexagons.values():
            y, x = map(int, hexagon.id.split("-"))
            if not self.is_sommet_start_or_end(self.grille.tab[x][y]):
                self.grille.tab[x][y].weight = 1
                hexagon.color = WHITE
                self.canvas.itemconfigure(hexagon.id, fill=WHITE)
        self.clear_arrows()
        self.chemins = None

    def is_sommet_start_or_end(self, sommet: Sommet):
        """
        Vérifie si un sommet est le point de départ ou d'arrivée.

        Args:
            sommet (Sommet): Le sommet à vérifier.

        Returns:
            bool: Retourne True si c'est le sommet de départ ou d'arrivée, sinon False.
        """
        return (self.start.x == sommet.x and self.start.y == sommet.y) or (
                self.end.x == sommet.x and self.end.y == sommet.y)

    def weight_popup(self):
        """
        Affiche une fenêtre popup avec la distance parcourue par le chemin rouge.
        """
        if self.sum_weight > 0:
            messagebox.showinfo("Distance parourue", f"La distance parcourue par le chemin rouge : {self.sum_weight}")
        else:
            messagebox.showwarning("Aucun parcours detecté", "Il faut exécuter un algorithme afin d'avoir une distance")

    def random_colors(self):
        """
        Applique des couleurs aléatoires aux hexagones de la grille.
        """
        colors = [BLACK, WHITE, BLUE, GREEN, YELLOW]
        for hex_id, hexagon in self.hexagons.items():
            random_color = random.choice(colors)
            col, row = map(int, hex_id.split("-"))

            if not self.is_sommet_start_or_end(self.grille.tab[row][col]):
                self.paint_hexagon(col, row, random_color)
                if row == 0:
                    self.update()

    def init_hexagones(self):
        """
        Initialise le départ en bas à gauche et l'objectif en haut à droite.
        """
        startHexagon = self.hexagons.get(f"{self.num_cols - 1}-{0}")
        startHexagon.color = PURPLE
        self.canvas.itemconfigure(startHexagon.id, fill=PURPLE)

        endHexagon = self.hexagons.get(f"{0}-{self.num_rows - 1}")
        endHexagon.color = RED
        self.canvas.itemconfigure(endHexagon.id, fill=RED)

    def a_star(self):
        """
        Lance l'algorithme A* pour trouver le chemin optimal entre le départ et l'objectif.
        """
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.a_star(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_parcours_en_largeur(self):
        """
        Lance l'algorithme de parcours en largeur.
        """
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_largeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_parcours_en_profondeur(self):
        """
        Lance l'algorithme de parcours en profondeur.
        """
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_profondeur(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_allerAToire(self):
        """
        Lance l'algorithme AllerÀToire.
        """
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.allerAToire(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_dijkstra(self):
        """
        Lance l'algorithme de Dijkstra pour trouver le chemin optimal entre le départ et l'objectif.
        """
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.parcours_dijkstra(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def launch_bellman_ford(self):
        """
        Lance l'algorithme de Bellman-Ford pour trouver le chemin optimal entre le départ et l'objectif.
        """
        self.is_stopped_button_pressed = False
        self.clear_arrows()
        self.grille.init_grid()
        try:
            chemins = self.grille.bellman_ford(self.start, self.end)
            self._display_results(chemins, self.start)
        except NotConnectedGraphException as e:
            self.alert_popup(e.message)

    def alert_popup(self, text):
        """
        Affiche une popup d'erreur avec le message spécifié.

        Args:
            text (str): Le message d'erreur à afficher.
        """
        messagebox.showerror("Erreur d'exécution", text)

    def _display_results(self, chemins, start):
        """
        Affiche les résultats d'un algorithme sous forme de flèches.

        Args:
            chemins (list): La liste des chemins calculés par l'algorithme.
            start (Sommet): Le sommet de départ.
        """
        self.chemins = chemins[:]
        disp_queue = []
        for sommet in chemins[0].keys():
            for voisin in chemins[0][sommet]:
                disp_queue.append((sommet, voisin))
        self._progressive_display_all(disp_queue, chemins, start)

    def _progressive_display_all(self, chemin: list[tuple], chemins, start):
        """
        Affiche progressivement les chemins entre les sommets.

        Args:
            chemin (list[tuple]): La liste des arêtes à afficher.
            chemins (dict): Dictionnaire des chemins.
            start (Sommet): Le sommet de départ.
        """
        if len(chemin) > 0 and not self.is_stopped_button_pressed:
            sommet, suivant = chemin.pop(0)
            self.paint_path(sommet, suivant, "#757575")
            self.after(int(self.speed.get()), self._progressive_display_all, chemin, chemins, start)
        else:
            self._progressive_display_best(chemins[1], start)

    def _progressive_display_best(self, chemin, sommet):
        """
        Affiche progressivement le meilleur chemin.

        Args:
            chemin (dict): Le dictionnaire représentant le chemin optimal.
            sommet (Sommet): Le sommet actuel.
        """
        if sommet in chemin.keys() and not self.is_stopped_button_pressed:
            self.sum_weight += sommet.weight
            suivant = chemin[sommet]
            self.paint_path(sommet, suivant, RED)
            self.after(int(self.speed.get()), self._progressive_display_best, chemin, suivant)
            if self.old_speed:
                self.speed.set(self.old_speed)
                self.scale_widget.config(state='normal', from_=1)
                self.old_speed = None
