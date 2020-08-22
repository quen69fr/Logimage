# coding: utf-8

from outils import *
from variables_globales import *
import pygame
import math


def affiche_surface(surface: pygame.Surface, x: int, y: int, screen: pygame.Surface,
                    x_0gauche_1centre_2droite=0, y_0haut_1centre_2bas=0, largeur: int = None, hauteur: int = None):
    if x_0gauche_1centre_2droite == 0 and y_0haut_1centre_2bas == 0:
        screen.blit(surface, (x, y))
    else:
        if largeur is None and hauteur is None:
            largeur, hauteur = surface.get_size()
        screen.blit(surface, (int(x - largeur * x_0gauche_1centre_2droite / 2),
                              int(y - hauteur * y_0haut_1centre_2bas / 2)))


dict_fonts = {}


def affiche_texte(texte: str, x: int, y: int, screen: pygame.Surface or None, police=DEFAULT_POLICE[0],
                  taille: int = DEFAULT_POLICE[1], couleur=NOIR, x_0gauche_1centre_2droite=0, y_0haut_1centre_2bas=0):
    if police not in dict_fonts:
        dict_fonts[police] = {}
    if taille not in dict_fonts[police]:
        dict_fonts[police][taille] = pygame.font.Font(police, int(taille))
    font = dict_fonts[police][taille]
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
                 y_0haut_1centre_2bas=0):
        couleur_contours_texte, couleur_fond, largeur_contours, police = DIC_BOUTONS[PARAM_BOUTON_STYLE][type_bouton]
        self.type = type_bouton
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.x_0gauche_1centre_2droite = x_0gauche_1centre_2droite
        self.y_0haut_1centre_2bas = y_0haut_1centre_2bas

        self.type_action = DIC_BOUTONS[PARAM_BOUTON_TYPE_ACTION][type_bouton]
        self.valeur = DIC_BOUTONS[PARAM_BOUTON_VALEUR][type_bouton]
        self.raccourci = DIC_BOUTONS[PARAM_BOUTON_RACCOURCI][type_bouton]

        self.ecran = pygame.Surface((self.largeur, self.hauteur))
        self.ecran_selectionne = pygame.Surface((self.largeur, self.hauteur))
        self.ecran.fill(couleur_contours_texte)
        self.ecran_selectionne.fill(couleur_fond)
        pygame.draw.rect(self.ecran, couleur_fond, (largeur_contours, largeur_contours,
                                                    self.largeur - 2 * largeur_contours,
                                                    self.hauteur - 2 * largeur_contours))
        pygame.draw.rect(self.ecran_selectionne, couleur_contours_texte, (largeur_contours, largeur_contours,
                                                                          self.largeur - 2 * largeur_contours,
                                                                          self.hauteur - 2 * largeur_contours))
        texte = DIC_BOUTONS[PARAM_BOUTON_TEXTE][self.type]
        if self.raccourci is not None:
            texte = f'{texte} ({self.raccourci})'
        affiche_texte(texte, int(self.largeur / 2), int(self.hauteur / 2), self.ecran, police[0], police[1],
                      couleur_contours_texte, 1, 1)
        affiche_texte(texte, int(self.largeur / 2), int(self.hauteur / 2), self.ecran_selectionne, police[0], police[1],
                      couleur_fond, 1, 1)

    def fait_action(self):
        if self.type_action == TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE:
            if get_action_logimage_ligne_possible() == self.valeur:
                set_action_logimage_ligne_possible(None)
            else:
                set_action_logimage_ligne_possible(self.valeur)
        elif self.type_action == TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE:
            if get_action_logimage_colonne_possible() == self.valeur:
                set_action_logimage_colonne_possible(None)
            else:
                set_action_logimage_colonne_possible(self.valeur)
        elif self.type_action == TYPE_ACTION_COLORIER_CASE:
            set_action_colorier_case(not get_action_colorier_case())
        elif self.type_action == TYPE_ACTION_CRAYON:
            set_action_logimage_mode_crayon(not get_action_logimage_mode_crayon())
        elif self.type_action == TYPE_ACTION_CORRIGER_LOGIMAGE:
            set_action_corriger_logimage(not get_action_corriger_logimage())
        elif self.type_action == TYPE_ACTION_POINTEUR:
            set_action_pointeur(not get_action_pointeur())

    def clic(self, x_souris: int, y_souris: int):
        if self.x < x_souris < self.x + self.largeur and self.y < y_souris < self.y + self.hauteur:
            self.fait_action()
            return True
        return False

    def gere_clavier(self, event):
        if self.raccourci is not None and event.unicode.upper() == self.raccourci:
            self.fait_action()
            return True
        return False

    def affiche(self, screen: pygame.Surface):
        ecran = self.ecran
        if (self.type_action == TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE and
            get_action_logimage_ligne_possible() == self.valeur) or \
                (self.type_action == TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE and
                 get_action_logimage_colonne_possible() == self.valeur) or \
                (self.type_action == TYPE_ACTION_TESTER_LOGIMAGE and get_action_test_creation()) or \
                (self.type_action == TYPE_ACTION_COLORIER_CASE and get_action_colorier_case()) or \
                (self.type_action == TYPE_ACTION_CRAYON and get_action_logimage_mode_crayon()) or \
                (self.type_action == TYPE_ACTION_POINTEUR and get_action_pointeur()) or \
                (self.type_action == TYPE_ACTION_CORRIGER_LOGIMAGE and get_action_corriger_logimage()):
            ecran = self.ecran_selectionne

        affiche_surface(ecran, self.x, self.y, screen, self.x_0gauche_1centre_2droite, self.y_0haut_1centre_2bas,
                        self.largeur, self.hauteur)


class Vignette:
    def __init__(self, rect, ecran):
        self.x, self.y, self.largeur, self.hauteur = rect
        self.ecran = ecran

    def clic(self, x_souris: int, y_souris: int):
        if self.x < x_souris < self.x + self.largeur and self.y < y_souris < self.y + self.hauteur:
            return True
        return False

    def affiche(self, screen: pygame.Surface):
        affiche_surface(self.ecran, self.x, self.y, screen, largeur=self.largeur, hauteur=self.hauteur)


class VignetteCategorie(Vignette):
    def __init__(self, categorie, rect, nb_logimages):
        self.categorie = categorie
        x, y, largeur, hauteur = rect
        ecran = pygame.Surface((largeur, hauteur))
        couleur1, couleur2, marge, texte = STYLE_VIGNETTE_LOGIMAGE
        marge = max(1, int(largeur * marge))
        police, taille = texte
        taille *= largeur
        centre_x = largeur // 2

        ecran.fill(couleur1)
        pygame.draw.rect(ecran, couleur2, (marge, marge, largeur - 2 * marge, hauteur - 2 * marge))

        if self.categorie == CATEGORIE_IMPOSSIBLE:
            couleur1 = COULEUR_ECHEC
            texte = TEXTE_CATEGORIE_IMPOSSIBLE
        elif self.categorie == CATEGORIE_INFAISABLE:
            couleur1 = COULEUR_ECHEC
            texte = TEXTE_CATEGORIE_INFAISABLE
        elif self.categorie == CATEGORIE_PNG:
            texte = TEXTE_CATEGORIE_PNG
        elif self.categorie[1] == math.inf:
            texte = f'+ de {self.categorie[0]}'
        elif self.categorie[0] == 0:
            texte = f'- de {self.categorie[1]}'
        else:
            texte = f'{self.categorie[0]}-{self.categorie[1]}'

        affiche_texte(texte, centre_x, marge * 4, ecran, police,
                      int(taille * 1.1), couleur1, x_0gauche_1centre_2droite=1)
        affiche_texte(f'{nb_logimages} logimages', centre_x, hauteur - marge * 3, ecran, police,
                      int(taille * 0.9), COULEUR_SECONDAIRE_VIGNETTE, x_0gauche_1centre_2droite=1,
                      y_0haut_1centre_2bas=2)

        Vignette.__init__(self, rect, ecran)


class VignetteLogimage(Vignette):
    def __init__(self, nom, rect: tuple, titre: str, dimention: tuple, possible: bool, faisable: bool,
                 sauvegarde: bool):
        self.nom = nom
        x, y, largeur, hauteur = rect
        ecran = pygame.Surface((largeur, hauteur))
        couleur1, couleur2, marge, texte = STYLE_VIGNETTE_LOGIMAGE
        marge = max(1, int(largeur * marge))
        police, taille = texte
        taille *= largeur
        centre_x = largeur // 2
        texte = None
        couleur_texte = None
        decalage_y = 0
        if dimention is None and possible is None and faisable is None:
            taille *= 1.3
            marge *= 2
        else:
            decalage_y = marge
            if possible:
                if faisable:
                    texte = TEXTE_FAISABLE
                    couleur_texte = COULEUR_SUCCES
                else:
                    texte = TEXTE_INFAISABLE
                    couleur_texte = COULEUR_ECHEC
            else:
                texte = TEXTE_IMPOSSIBLE
                couleur_texte = COULEUR_ECHEC
        if sauvegarde:
            marge *= 2
            texte = TEXTE_SAUVEGARDE
            couleur_texte = COULEUR_SUCCES

        ecran.fill(couleur1)
        pygame.draw.rect(ecran, couleur2, (marge, marge, largeur - 2 * marge, hauteur - 2 * marge))
        if sauvegarde:
            marge /= 2
        if len(titre) >= 12:
            coef_titre = (10 / len(titre)) ** 0.8
        else:
            coef_titre = 1
        affiche_texte(titre, centre_x, hauteur // 2 - decalage_y, ecran, police,
                      int(taille * 1.2 * coef_titre), couleur1, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
        if texte is not None:
            affiche_texte(texte, centre_x, marge * 2, ecran, police, int(taille * 0.6), couleur_texte,
                          x_0gauche_1centre_2droite=1)
        if dimention is not None:
            affiche_texte(f'{dimention[0]}x{dimention[1]}', centre_x, hauteur - marge, ecran, police,
                          int(taille * 0.9), COULEUR_SECONDAIRE_VIGNETTE, x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=2)

        Vignette.__init__(self, rect, ecran)


class VignettePng(Vignette):
    def __init__(self, rect: tuple, titre: str, dimention: tuple):
        self.nom = titre
        x, y, largeur, hauteur = rect
        ecran = pygame.Surface((largeur, hauteur))
        couleur1, couleur2, marge, texte = STYLE_VIGNETTE_LOGIMAGE
        marge = max(1, int(largeur * marge))
        police, taille = texte
        taille *= largeur
        centre_x = largeur // 2
        decalage_y = 0

        ecran.fill(couleur1)
        pygame.draw.rect(ecran, couleur2, (marge, marge, largeur - 2 * marge, hauteur - 2 * marge))

        if len(titre) >= 11:
            coef_titre = (9 / len(titre)) ** 0.8
        else:
            coef_titre = 1
        affiche_texte(titre, centre_x, hauteur // 2 - decalage_y, ecran, police,
                      int(taille * 1.2 * coef_titre), couleur1, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
        affiche_texte(TEXTE_CATEGORIE_PNG, centre_x, marge * 2, ecran, police, int(taille * 0.6), COULEUR_SUCCES,
                      x_0gauche_1centre_2droite=1)
        affiche_texte(f'{dimention[0]}x{dimention[1]}', centre_x, hauteur - marge, ecran, police,
                      int(taille * 0.9), COULEUR_SECONDAIRE_VIGNETTE, x_0gauche_1centre_2droite=1,
                      y_0haut_1centre_2bas=2)

        Vignette.__init__(self, rect, ecran)
