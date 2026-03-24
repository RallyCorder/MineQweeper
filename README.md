# MineQweeper
Minesweeper in Qt Pyside, that's about it.

Copied from answer to how this'll be made:
1. matrix python
2. position x,y en liste, int
3. perlin noise / autre noise generator, où la valeur la plus haute est une bombe et les graduations sont les environs, avec des modulations aux modèles pour plus ou moins de pics
4. ^
5. crée un matrix intiale et une de jeu, utilisé la première comme référence et comparé avec la deuxième pour voir les différences du user input
6.
    - Game Over
    - Révéler certaines cases alentours
    - soit n'existe pas, ou peut être usé pour les flags
7.
    - Constructeur UI
    - Constructeur Jeu
    - [Tercière pour les interactions du joueur, peut-être inclus dans les deux précédentes]
8. Le joueur révèle des cases masquées, si c'est une bombe, il perd: si c'en ai pas une, il révèle du terrain. Il peut placer des drapeux sur les endroits il croit se trouve une bombe, si il trouve toute les bombes, il gagne.
9. ^

# Prolongements
Si on a le temps et le courage

- Avoir la possibilité à la fin d’une partie de rejouer une autre partie.
- Permettre de changer la taille de la grille
- Pouvoir choisir entre plusieurs niveaux de difficultés avec plus ou moins de
bombes en fonction de la taille de la grille de jeu.
- Mettre un timer pour mettre une limite de temps ou un chrono pour noter le
temps de résolution.
- Faire une interface graphique avec l’outil de votre choix. Vous pouvez utiliser les
bibliothèques pygame ou tkinter.
- Gérer les joueurs dans une base de données (comme vu en TP) et pouvoir noter les
temps et tenir à jour un tableau de joueurs ayant les meilleurs temps au jeu.
- Avoir la possibilité de mettre des drapeaux comme dans le jeu originel.
- Faire en sorte que la première case jouée ne peut pas être une bombe.
