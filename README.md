# tron

Le but est de construire un jeu de type TRON avec scrolling différentiel.

Ce jeu est inspriré du [jeu Tron 2 sur HP48](https://www.hpcalc.org/details/6997).

## pré-requis

- Python 3.8.2
- pygame 2.6.1 (SDL 2.28.4)

## règle du jeu 

Le jeu Tron est basé sur le concept du film "Tron", où chaque joueur pilote une moto futuriste laissant derrière elle une traînée solide.

Le but est de faire en sorte que l'adversaire s'écrase contre un mur ou une traînée, tout en évitant de s'y heurter soi-même. 

Chaque moto dispose de deux options spéciales :
- TURBO : Augmente la vitesse de la moto.
- INVISIBILITY : Rend la moto invisible (et invincible ?) pendant un court instant.

Le premier joueur à atteindre un score prédéfini remporte la partie.
