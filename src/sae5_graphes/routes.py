from pydantic import Field

from flask import Flask, request, jsonify
from pydantic import BaseModel
from spectree import SpecTree, Response
from sae5_graphes import models

app = Flask(__name__)
api = SpecTree('flask')

# La grille de base est 20x20
grille = models.Grille(20, 20)


class GrilleDimensions(BaseModel):
    height: int = Field(20, title="Hauteur de la grille", description="Hauteur de la grille entre 2 et 1000")
    width: int = Field(20, title="Largeur de la grille", description="Largeur de la grille entre 2 et 1000")


@app.route('/getGridDimensions', methods=['GET'])
@api.validate(tags=["Grid"])
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
            return jsonify({"error": "Les dimensions de la grille n'ont pas pu être déterminés"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/editGrid', methods=['PUT'])
@api.validate(tags=["Grid"], json=GrilleDimensions)
def edit_grid(json: GrilleDimensions):
    """
    Modifie la grille entière sous forme de tableau 2D
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

@app.route('/getGridWeights', methods=['GET'])
@api.validate(tags=["Grid"])
def get_grid_weights():
    """
    Obtenir la grille entière sous forme de tableau 2D.
    """
    try:
        grid_repr = [[sommet.weight for sommet in row] for row in grille.tab]
        if grid_repr:
            return jsonify(grid_repr), 200
        else:
            return jsonify({"error": "Le poids de la grille n'ont pas pu être déterminés"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    api.register(app)
    app.run(debug=True)
