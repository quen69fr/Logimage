# coding: utf-8

from fenetre import *


if __name__ == "__main__":
    fenetre = Fenetre()

    while fenetre.running:
        fenetre.update()
        fenetre.affiche()

