# coding: utf-8

from affichage import *


class Titre:
    def __init__(self):
        self.texte = DEFAULT_TITRE
        self.ecran = None
        self.x = 0
        self.y = 0
        self.largeur = 0
        self.hauteur = 0

        self.selectinne = False
        self.update_ecran()

    def update_ecran(self):
        surface = affiche_texte(self.texte, 0, 0, None, taille=TAILLE_TITRE, couleur=COULEUR_TITRE)
        largeur, hauteur = surface.get_size()
        self.largeur = largeur + 2 * MARGE_TITRE
        self.hauteur = hauteur + 2 * MARGE_TITRE
        self.x = MARGE_GRILLE_BORD_DROITE + (LARGEUR - MARGE_GRILLE_BORD_DROITE - MARGE_GRILLE_BORD_GAUCHE
                                             - self.largeur) // 2
        self.y = (MARGE_GRILLE_BORD_HAUT - self.hauteur) // 2

        self.ecran = pygame.Surface((self.largeur, self.hauteur))
        self.ecran.fill(COULEUR_FOND)
        affiche_surface(surface, MARGE_TITRE, MARGE_TITRE, self.ecran)

    def new_texte(self, new_texte: str):
        self.texte = new_texte
        self.update_ecran()

    def gere_clic(self, x_souris: int, y_souris: int):
        if self.x < x_souris < self.x + self.largeur and self.y < y_souris < self.y + self.hauteur:
            self.selectinne = True
            self.new_texte('')
        else:
            if len(self.texte) == 0:
                self.new_texte(DEFAULT_TITRE)
            self.selectinne = False

    def gere_clavier(self, event):
        if self.selectinne:
            if event.key == pygame.K_RETURN or event.key == 271:
                if len(self.texte) == 0:
                    self.new_texte(DEFAULT_TITRE)
                self.selectinne = False
            elif event.key == pygame.K_BACKSPACE:
                self.new_texte(self.texte[:-1])
            else:
                if len(self.texte) < LONGEUR_TITRE_MAX:
                    self.new_texte(self.texte + event.unicode)

    def affiche(self, screen: pygame.Surface):
        affiche_surface(self.ecran, self.x, self.y, screen)
        if self.selectinne:
            pygame.draw.rect(screen, CONTOURS_TITRE_SELECTIONNE[0], (self.x, self.y, self.largeur, self.hauteur),
                             CONTOURS_TITRE_SELECTIONNE[1])
