# coding: utf-8

from outils import *
import pygame


def affiche_surface(surface: pygame.Surface, x: int, y: int, screen: pygame.Surface,
                    x_0gauche_1centre_2droite=0, y_0haut_1centre_2bas=0, largeur: int = None, hauteur: int = None):
    if x_0gauche_1centre_2droite == 0 and y_0haut_1centre_2bas == 0:
        screen.blit(surface, (x, y))
    else:
        if largeur is None and hauteur is None:
            largeur, hauteur = surface.get_size()
        screen.blit(surface, (int(x - largeur * x_0gauche_1centre_2droite / 2),
                              int(y - hauteur * y_0haut_1centre_2bas / 2)))


def affiche_texte(texte: str, x: int, y: int, screen: pygame.Surface or None, police=DEFAULT_POLICE[0],
                  taille: int = DEFAULT_POLICE[1], couleur=NOIR, x_0gauche_1centre_2droite=0, y_0haut_1centre_2bas=0):
    font = pygame.font.Font(police, taille)
    surface = font.render(texte, True, couleur)
    if screen is None:
        return surface
    affiche_surface(surface, x, y, screen, x_0gauche_1centre_2droite, y_0haut_1centre_2bas)


def affiche_rect_transparent(rect, screen, couleur, alpha):
    rectangle = pygame.Surface((rect[2], rect[3]))
    rectangle.fill(couleur)
    rectangle.set_alpha(alpha)
    screen.blit(rectangle, (rect[0], rect[1]))


class Bouton:
    def __init__(self, x: int, y: int, largeur: int, hauteur: int, type_bouton: str, x_0gauche_1centre_2droite=0,
                 y_0haut_1centre_2bas=0, police: tuple = DEFAULT_POLICE):
        couleur_contours, couleur_fond, largeur_contours, couleur_texte = DIC_STYLES_BOUTONS[type_bouton]
        self.type = type_bouton
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.x_0gauche_1centre_2droite = x_0gauche_1centre_2droite
        self.y_0haut_1centre_2bas = y_0haut_1centre_2bas

        self.ecran = pygame.Surface((self.largeur, self.hauteur))
        self.ecran.fill(couleur_contours)
        pygame.draw.rect(self.ecran, couleur_fond, (largeur_contours, largeur_contours,
                                                    self.largeur - 2 * largeur_contours,
                                                    self.hauteur - 2 * largeur_contours))
        texte = DIC_TEXTES_BOUTONS[self.type]
        affiche_texte(texte, int(self.largeur / 2), int(self.hauteur / 2), self.ecran, police[0], police[1],
                      couleur_texte, 1, 1)

    def clic(self, x_souris: int, y_souris: int):
        if self.x < x_souris < self.x + self.largeur and self.y < y_souris < self.y + self.hauteur:
            return True
        return False

    def affiche(self, screen: pygame.Surface):
        affiche_surface(self.ecran, self.x, self.y, screen, self.x_0gauche_1centre_2droite, self.y_0haut_1centre_2bas,
                        self.largeur, self.hauteur)
