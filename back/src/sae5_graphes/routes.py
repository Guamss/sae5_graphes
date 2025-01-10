from pydantic import Field
from flask_cors import CORS

from flask import Flask, request, jsonify
from pydantic import BaseModel
from spectree import SpecTree, Response
from sae5_graphes import models
from exceptions import *

app = Flask(__name__)
CORS(app)
api = SpecTree('flask')

# La grille de base est 20x20
grille = models.Grille(5, 5)


class GridSize(BaseModel):
    height: int = Field(20, title="Hauteur de la grille", description="Hauteur de la grille entre 2 et 1000")
    width: int = Field(20, title="Largeur de la grille", description="Largeur de la grille entre 2 et 1000")


class GridWeights(BaseModel):
    grid: list[list[int]] = Field([[1, 3, 5], [3, 1, 5]], title="Tableau 2D de la grille",
                                  description="Liste des poids de la grille")


# ---- Actions sur la grille ---- #
@app.route('/grid/dimensions', methods=['GET'])
@api.validate(tags=["Grille"])
def get_grid_dimensions():
    """
    Obtenir la grille entière sous de dimensions Hauteur-Largeur.
    """
    try:
        response = {
            "height": grille.height,
            "width": grille.width
        }
        if response:
            return jsonify(response), 200
        else:
            return jsonify({"error": "Les dimensions de la grille n'ont pas pu être déterminés"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/grid/dimensions', methods=['PUT'])
@api.validate(tags=["Grille"], json=GridSize)
def edit_grid(json: GridSize):
    """
    Modifie la grille avec les dimensions Hauteur-Largeur.
    """
    try:
        # Gestion taille trop grande/petite
        if json.height > 1000 or json.width > 1000:
            return jsonify({"error": "La grille a une taille trop grande"}), 400
        if json.height < 2 or json.width < 2:
            return jsonify({"error": "La grille a une taille trop petite"}), 400

        # [Requête back-end] - MAJ de la grille
        global grille
        grille = models.Grille(json.height, json.width)
        return jsonify({"height": grille.height, "width": grille.width}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/grid/weights', methods=['GET'])
@api.validate(tags=["Grille"])
def get_grid_weights():
    """
    Obtenir la grille des poids sous forme de tableau 2D.
    """
    try:
        grid_repr = [[sommet.weight for sommet in row] for row in grille.tab]
        if grid_repr:
            return jsonify(grid_repr), 200
        else:
            return jsonify({"error": "Le poids de la grille n'ont pas pu être déterminés"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/grid/weights', methods=['PUT'])
@api.validate(tags=["Grille"], json=GridWeights)
def update_grid_weights(json: GridWeights):
    """
    Mise à jour des poids de plusieurs sommets spécifiques de la grille.
    """
    try:
        columns = len(json.grid)
        rows = len(json.grid[0])

        if columns != grille.height or rows != grille.width:
            return jsonify({"error": "La grille a une taille different de la requête"}), 400

        for col in range(columns):
            for row in range(rows):
                grille.tab[col][row].set_weight(json.grid[col][row])

        return jsonify({"message": "Tous les poids de la grille ont été mis à jour avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


class StartEndPoints(BaseModel):
    start_x: int = Field(19, title="X du sommet de départ")
    start_y: int = Field(0, title="Y du sommet de départ")
    end_x: int = Field(0, title="X du sommet de fin")
    end_y: int = Field(19, title="Y du sommet de fin")


def execute_algorithm_common(start, end, algorithm_func):
    try:
        result = algorithm_func(start, end)
        return jsonify({
            "visited": {str(k): [str(v) for v in vs] for k, vs in result[0].items()},
            "solution": {str(k): str(v) for k, v in result[1].items()}
        }), 200
    except NotConnectedGraphException as e:
        return jsonify({"error": "Le graphe n'est pas connexe", "details": str(e)}), 400
    except IndexError as e:
        return jsonify({"error": "Coordonnées hors de la grille", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Une erreur est survenue", "details": str(e)}), 500


from functools import wraps

# Fonction générique pour gérer les routes d'algorithmes
def algorithm_route(algorithm_func):
    @wraps(algorithm_func)
    @api.validate(tags=["Algorithmes"], json=StartEndPoints)
    def wrapper():
        data = request.get_json()
        json = StartEndPoints(**data)
        try:
            start = grille.tab[json.start_x][json.start_y]
            end = grille.tab[json.end_x][json.end_y]
        except IndexError:
            return jsonify({"error": "Coordonnées hors de la grille"}), 400
        return execute_algorithm_common(start, end, algorithm_func)
    return wrapper

# Routes spécifiques pour chaque algorithme
@app.route('/algorithm/dfs', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def dfs():
    return algorithm_route(grille.parcours_profondeur)()

@app.route('/algorithm/bfs', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def bfs():
    return algorithm_route(grille.parcours_largeur)()

@app.route('/algorithm/dijkstra', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def dijkstra():
    return algorithm_route(grille.parcours_dijkstra)()

@app.route('/algorithm/bellman_ford', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def bellman_ford():
    return algorithm_route(grille.bellman_ford)()

@app.route('/algorithm/a_star', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def a_star():
    return algorithm_route(grille.a_star)()

@app.route('/algorithm/random_walk', methods=['POST'])
@api.validate(tags=["Algorithmes"], json=StartEndPoints)
def random_walk():
    return algorithm_route(grille.allerAToire)()


if __name__ == "__main__":
    api.register(app)
    app.run(debug=True)
