from pydantic import Field

from flask import Flask, request, jsonify
from pydantic import BaseModel
from spectree import SpecTree, Response
from models import Grille, Sommet
from sae5_graphes import models

app = Flask(__name__)
api = SpecTree('flask')

# La grille de base est 20x20
grille = models.Grille(20, 20)


class GrilleDimensions(BaseModel):
    height: int = Field(20, title="Hauteur de la grille", description="Hauteur de la grille entre 2 et 1000")
    width: int = Field(20, title="Largeur de la grille", description="Largeur de la grille entre 2 et 1000")


@app.route('/getGrid', methods=['GET'])
@api.validate(tags=["Grid"])
def get_grid():
    """
    Obtenir la grille entière sous forme de tableau 2D.
    """
    response = {
        "width": grille.width,
        "height": grille.height
    }
    return jsonify(response), 200


if __name__ == "__main__":
    api.register(app)
    app.run(debug=True)
