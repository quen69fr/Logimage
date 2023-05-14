# coding: utf-8

from fenetre import *


# TODO : - Seuils max proportionnels à la difficulté...
#        - Se poser la question : qu'est ce que cette case peut être plutôt que comment je
#          peux arranger la séquence... => Essayer de remplir les petites successions de cases
#          inconnues
#        - Essayer de fabriquer des contres-exemples quand la recherche prend du temps...
#        - Deep learning (neural network) : Pour savoir quelle ligne il faut tester quand
#                                           les tests commencent à être long... (et peut-
#                                           être même quelle méthode utiliser)


if __name__ == "__main__":
    pygame.init()
    fenetre = Fenetre()

    while fenetre.running:
        fenetre.update()
        fenetre.affiche()

    pygame.quit()
