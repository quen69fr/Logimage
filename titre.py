# coding: utf-8

from affichage import *
import os


class Titre:
    def __init__(self, titre: str = None, titre_sauvegarde: str = None):
        self.texte = DEFAULT_TITRE if titre is None else titre
        self.ecran = None
        self.x = 0
        self.y = 0
        self.largeur = 0
        self.hauteur = 0

        self.titre_sauvegarde = titre_sauvegarde
        if self.titre_sauvegarde is None:
            self.update_titre_sauvegarde()

        self.selectinne = False
        self.update_ecran()

    def update_titre_sauvegarde(self):
        titre_sauvegarde = self.texte
        for lettres_sepeciale, lettre in [("§!@#$%^&*()[]{};:,./<>\?|²¨`'°~-=_+" + '"', ""), ("ç", "c"), ("ñ", "n"),
                                          ("àâä", "a"), ("éêèë", "e"),  ("îï", "i"), ("ôö", "o"), ("ùûü", "u")]:
            for lettre_speciale in lettres_sepeciale:
                titre_sauvegarde = titre_sauvegarde.replace(lettre_speciale, lettre)
        for i, lette in enumerate(titre_sauvegarde):
            if lette == ' ':
                if i + 1 < len(titre_sauvegarde):
                    titre_sauvegarde = titre_sauvegarde[:i + 1] + \
                                       titre_sauvegarde[i + 1].upper() + \
                                       titre_sauvegarde[i + 2:]
        titre_sauvegarde = titre_sauvegarde.replace(' ', '')
        titre_sauvegarde2 = titre_sauvegarde + '.json'
        n = 0
        while titre_sauvegarde2 in os.listdir(NOM_DOSSIER_SAUVEGARDE):
            n += 1
            titre_sauvegarde2 = titre_sauvegarde + str(n) + '.json'
        self.titre_sauvegarde = titre_sauvegarde2

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
            if self.selectinne:
                if len(self.texte) == 0:
                    self.new_texte(DEFAULT_TITRE)
                self.selectinne = False
                self.update_titre_sauvegarde()

    def gere_clavier(self, event):
        if self.selectinne:
            if event.key == pygame.K_RETURN or event.key == 271:
                if len(self.texte) == 0:
                    self.new_texte(DEFAULT_TITRE)
                self.selectinne = False
                self.update_titre_sauvegarde()
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
