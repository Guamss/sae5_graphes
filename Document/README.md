<h1 style="text-align:center;">Chiffredeux</h1>

Chiffredeux est une application permettant de visualiser des parcours de graphes et de comprendre le fonctionnement des 
algorithmes de recherche de chemins. Développée avec Python pour l'application de bureau, ainsi qu'Angular pour 
l'application web, l'application offre une vue interactive des parcours sur une grille hexagonale, où chaque hexagone 
possède un poids influençant le coût du chemin.

Les utilisateurs peuvent choisir entre parmi plusieurs algorithmes de parcours, et l'application affichera visuellement 
le chemin parcouru et mettra en évidence le chemin d'un point A à un point B avec un tracé en rouge, selon l'algorithme de parcours 
sélectionné. Chiffredeux permet ainsi de mieux comprendre et de visualiser les principes des algorithmes de graphes de manière 
interactive et intuitive.

> ### Table des matières :

> #### Aspect technique
* Installation et configuration
* Langages et outils utilisés
* Architecture du logiciel

> #### Aspect fonctionnel
* Présentation de l'interface du logiciel (tkinter)
  - Fonctionnalités principales 
  - Gestion des erreurs et messages

* Présentation de l'interface web (angular)
  - Fonctionnalités principales 
  - Gestion des erreurs et messages

> #### Aspect théorique 
* Présentation des algorithmes (screen un exemple pour chaque parcours) (mettre des liens)
  - Parcours en profondeur 
  - Parcours en largeur
  - Parcours Bellman-ford
  - Dijkstra
  - A*
  - AllerÀToire

> ##### Installation et configuration
Python, nodejs, docker
librairie utilisé : tkinter, random, math

> ##### Langages et outils utilisés
* **Python :**
Le cœur de notre projet repose sur le langage Python, que nous avons utilisé pour implémenter l’ensemble des algorithmes 
de parcours ainsi que pour la gestion et le traitement des hexagones, qui sont au cœur de notre application. Python s’est 
imposé comme un choix stratégique grâce à sa simplicité et ses très bonne bibliothèques. Cela nous ont permis de développer 
des solutions performantes, tout en assurant une grande fiabilité.<br>

* **Tkinter :**
Pour l’interface graphique de l’application bureau, nous avons utilisé Tkinter, une bibliothèque native de Python. 
Tkinter nous a permis de créer une interface légère et intuitive avec des éléments interactifs tels que des boutons,
des champs de saisie ou encore la grille d'héxagone.<br>

* **Angular pour l'interface web :**
Pour répondre au besoin d’une interface web, nous avons opté pour Angular, un framework front-end basé sur TypeScript. 
Angular a été utilisé pour développer une interface utilisateur interactive et dynamique, capable de gérer efficacement 
les données en temps réel. <br>

* **API Flask :**
Pour connecter nos algorithmes Python avec l’interface web développée en Angular, nous avons utilisé une API construite 
avec le framework Flask. Flask s’est avéré être un choix idéal car nous avions déjà eu l’opportunité de l’utiliser en 
cours, ce qui nous a permis de tirer parti de notre expérience avec ce framework léger. <br>


> ##### Architecture du logiciel
L’architecture logicielle de notre application repose sur une organisation modulaire qui garantit une séparation claire 
des responsabilités entre les différents composants de l'application. Le composant Modèle est représenté par le fichier 
**models.py**, qui regroupe l’ensemble des données et de la logique métier, notamment les algorithmes de parcours et la gestion 
des hexagones. Ce module constitue le cœur fonctionnel de l’application, conçu pour être indépendant de toute interface 
utilisateur.

Pour l’interface utilisateur, deux approches distinctes ont été adoptée :
- **Dans la version avec l'exécutable**, nous avons utilisé un fichier **gui.py** utilisant principalement du Tkinter pour 
concevoir une interface graphique interactive, permettant une utilisation directe des fonctionnalités de l'application.
- **Dans la version web**, une interface dynamique a été développée en Angular, rendant l’application accessible depuis un navigateur.
La connexion entre les algorithmes Python et l’interface web Angular est assurée par une API Flask utilisé comme un intermédiaire 
de communication entre les composants, facilitant les échanges de données et permettant l’intégration fluide des deux environnements.

> ##### Présentation de l'interface du logiciel
...
> ##### Présentation de l'interface web
...

> ### Aspect théorique : 
À présent, nous allons présenter de manière théorique les différents parcours de graphe que nous avons implémentés dans 
le cadre de ce projet. Ces parcours incluent le parcours en profondeur, le parcours en largeur, l’algorithme de Bellman-Ford, 
l’algorithme de Dijkstra, l’algorithme A*, ainsi qu’un parcours spécifique que nous avons nommé AllerÀToire. Chacun de ces 
algorithmes offre une approche unique pour explorer ou trouver des chemins dans un graphe, avec des caractéristiques et 
des applications distinctes.

```
⚠️ Si le sommet de destination n'est pas atteignable car le sommet de départ et d'arrivé ne sont pas dans le même 
graphe, une exception est levée. Mais si le graphe n'est pas connexe et que le sommet de départ et d'arrivé sont dans le 
même graphe, le parcours se réalise en prenant en compte uniquement le graphe où se trouve le sommet de départ et d'arrivé.
```

> ##### #### Parcours en profondeur
###### Explication :
Le parcours en profondeur est une méthode classique utilisée pour explorer un graphe. 
Elle fonctionne en partant d’un sommet de départ et en explorant autant que possible chaque chemin avant de revenir en 
arrière lorsque l'on atteint une impasse (sommet avec que des voisins visités ou un mur). Une fois une impasse atteinte, 
il revient en arrière pour explorer d'autres voisins non visités du sommet précédent et cela se fait récursivement dans notre cas.
Les sommets visités sont enregistrés dans un dictionnaire de set pour éviter les doublons et retracer le chemin menant au sommet d'arrivé.

Le parcours en profondeur ne garantit pas le chemin le plus court dans un graphe et il peut explorer inutilement de 
nombreuses branches d’un graphe avant de trouver la solution.


###### Exemple :

> ##### #### Parcours en largeur
###### Explication :
###### Exemple :

> ##### #### Parcours avec l’algorithme de Bellman-Ford
###### Explication :
###### Exemple :

> ##### #### Parcours avec l’algorithme de Dijkstra
###### Explication :
###### Exemple :

> ##### #### Parcours avec A*
###### Explication :
###### Exemple :

> ##### #### Parcours AllerÀToire
###### Explication :
###### Exemple :

