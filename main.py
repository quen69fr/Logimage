# coding: utf-8

from fenetre import *


if __name__ == "__main__":
    pygame.init()
    fenetre = Fenetre()

    while fenetre.running:
        fenetre.update()
        fenetre.affiche()

    pygame.quit()
