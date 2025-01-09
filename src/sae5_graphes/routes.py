from pydantic import Field

from flask import Flask, request, jsonify
from pydantic import BaseModel
from spectree import SpecTree, Response
from sae5_graphes import models

app = Flask(__name__)
api = SpecTree('flask')

# La grille de base est 20x20
grille = models.Grille(20, 20)


class GridSize(BaseModel):
    height: int = Field(20, title="Hauteur de la grille", description="Hauteur de la grille entre 2 et 1000")
    width: int = Field(20, title="Largeur de la grille", description="Largeur de la grille entre 2 et 1000")


class GridWeights(BaseModel):
    grid: list[list[int]] = Field([[1, 3, 5], [3, 1, 5]], title="Tableau 2D de la grille", description="Liste des poids de la grille")

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

if __name__ == "__main__":
    api.register(app)
    app.run(debug=True)
