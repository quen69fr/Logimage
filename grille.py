# coding: utf-8

from affichage import *


class Grille:
    def __init__(self, largeur: int = DEFAULT_TAILLE_GRILLE[0], hauteur: int = DEFAULT_TAILLE_GRILLE[1],
                 logimage_cote_case=False, cases: list = None,
                 quadrillage_principal_x=True, quadrillage_principal_y=True):
        self.largeur = largeur
        self.hauteur = hauteur
        if cases is None:
            self.cases = [[False for _ in range(self.largeur)] for _ in range(self.hauteur)]
        else:
            self.cases = cases

        self.mode_suppression_ligne = False
        self.mode_suppression_colonne = False
        self.mode_suppression_groupe_lignes = False
        self.mode_suppression_groupe_colonnes = False
        self.mode_ajout_ligne = False
        self.mode_ajout_colonne = False
        self.mode_ajout_groupe_lignes = False
        self.mode_ajout_groupe_colonnes = False

        self.cote_case = 0
        self.taille_quadrillage = 0
        self.ecart_quadrillage_principal = 0
        self.largeur_pixel = 0
        self.hauteur_pixel = 0
        self.x = 0
        self.y = 0
        self.ecran = None

        if logimage_cote_case:
            self.cote_case = COTE_CASE_LOGIMAGE
            self.init_grille(quadrillage_principal_x, quadrillage_principal_y)
        else:
            self.init_grille_et_ajuste_cote_case()

    def init_grille_et_ajuste_cote_case(self):
        self.cote_case = min((HAUTEUR - MARGE_GRILLE_BORD_HAUT - MARGE_GRILLE_BORD_BAS) // self.hauteur,
                             (LARGEUR - MARGE_GRILLE_BORD_DROITE - MARGE_GRILLE_BORD_GAUCHE) // self.largeur)
        self.init_grille()

    def init_grille(self, quadrillage_principal_x=True, quadrillage_principal_y=True):
        self.taille_quadrillage = max(1, int(COEF_TAILLE_QUADRILLAGE * self.cote_case))
        self.ecart_quadrillage_principal = max(1, int(COEF_TAILLE_QUADRILLAGE_PRINCIPALE_ECART * self.cote_case))
        self.largeur_pixel = self.cote_case * self.largeur
        self.hauteur_pixel = self.cote_case * self.hauteur
        self.x = MARGE_GRILLE_BORD_DROITE + (LARGEUR - MARGE_GRILLE_BORD_DROITE - MARGE_GRILLE_BORD_GAUCHE
                                             - self.largeur_pixel) // 2
        self.y = MARGE_GRILLE_BORD_HAUT + (HAUTEUR - MARGE_GRILLE_BORD_HAUT - MARGE_GRILLE_BORD_BAS
                                           - self.hauteur_pixel) // 2
        decalage = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
        self.ecran = pygame.Surface((self.largeur_pixel + decalage, self.hauteur_pixel + decalage))
        self.ecran.fill(COULEUR_QUADRILLAGE)
        for ligne in range(self.hauteur):
            for colonne in range(self.largeur):
                self.dessine_case(ligne, colonne, quadrillage_principal_x, quadrillage_principal_y)

    def get_valeur_case(self, ligne, colonne):
        return self.cases[ligne][colonne]

    def set_valeur_case(self, ligne, colonne, valeur):
        self.cases[ligne][colonne] = valeur
        self.dessine_case(ligne, colonne)

    def change_case(self, ligne, colonne):
        valeur = not self.get_valeur_case(ligne, colonne)
        self.set_valeur_case(ligne, colonne, valeur)

    def get_case_clic(self, x_souris, y_souris):
        colonne = (x_souris - self.x) // self.cote_case
        ligne = (y_souris - self.y) // self.cote_case
        if 0 <= colonne < self.largeur and 0 <= ligne < self.hauteur:
            return ligne, colonne
        return None

    def get_intersection_clic(self, x_souris, y_souris):
        decalage = int(self.cote_case / 2)
        colonne = (x_souris - self.x + decalage) // self.cote_case
        ligne = (y_souris - self.y + decalage) // self.cote_case
        if 0 <= colonne <= self.largeur and 0 <= ligne <= self.hauteur:
            return ligne, colonne
        return None

    def ajoute_ligne(self, position, nb=1):
        for _ in range(nb):
            self.cases.insert(position, [False for _ in range(self.largeur)])
        self.hauteur += nb
        self.init_grille_et_ajuste_cote_case()

    def ajoute_colonne(self, position, nb=1):
        for ligne in self.cases:
            for _ in range(nb):
                ligne.insert(position, False)
        self.largeur += nb
        self.init_grille_et_ajuste_cote_case()

    def supprime_ligne(self, position, nb=1):
        n = 0
        for pos in range(min(position + nb - int(nb / 2) - 1, len(self.cases) - 1),
                         max(-1, position - int(nb / 2) - 1), -1):
            if len(self.cases) > 1:
                del self.cases[pos]
                n += 1
        self.hauteur -= n
        self.init_grille_et_ajuste_cote_case()

    def supprime_colonne(self, position, nb=1):
        n = 0
        for pos in range(min(position + nb - int(nb / 2) - 1, len(self.cases[0]) - 1),
                         max(-1, position - int(nb / 2) - 1), -1):
            if len(self.cases[0]) > 1:
                for ligne in self.cases:
                    del ligne[pos]
                n += 1
        self.largeur -= n
        self.init_grille_et_ajuste_cote_case()

    def gere_clic(self, x_souris, y_souris):
        if self.mode_ajout_ligne or self.mode_ajout_colonne or \
                self.mode_ajout_groupe_lignes or self.mode_ajout_groupe_colonnes:
            intersection = self.get_intersection_clic(x_souris, y_souris)
            if intersection is not None:
                ligne, colonne = intersection
                if self.mode_ajout_ligne:
                    self.ajoute_ligne(ligne)
                    self.mode_ajout_ligne = False
                if self.mode_ajout_colonne:
                    self.ajoute_colonne(colonne)
                    self.mode_ajout_colonne = False
                if self.mode_ajout_groupe_lignes:
                    self.ajoute_ligne(ligne, QUADRILLAGE_PRINCIPALE)
                    self.mode_ajout_groupe_lignes = False
                if self.mode_ajout_groupe_colonnes:
                    self.ajoute_colonne(colonne, QUADRILLAGE_PRINCIPALE)
                    self.mode_ajout_groupe_colonnes = False
        else:
            case = self.get_case_clic(x_souris, y_souris)
            if case is not None:
                ligne, colonne = case
                if self.mode_suppression_ligne or self.mode_suppression_colonne or \
                        self.mode_suppression_groupe_lignes or self.mode_suppression_groupe_colonnes:
                    if self.mode_suppression_ligne:
                        self.supprime_ligne(ligne)
                        self.mode_suppression_ligne = False
                    if self.mode_suppression_colonne:
                        self.supprime_colonne(colonne)
                        self.mode_suppression_colonne = False
                    if self.mode_suppression_groupe_lignes:
                        self.supprime_ligne(ligne, QUADRILLAGE_PRINCIPALE)
                        self.mode_suppression_groupe_lignes = False
                    if self.mode_suppression_groupe_colonnes:
                        self.supprime_colonne(colonne, QUADRILLAGE_PRINCIPALE)
                        self.mode_suppression_groupe_colonnes = False
                else:
                    self.change_case(ligne, colonne)

    def reste_cases_inconnues(self):
        for ligne in self.cases:
            if CASE_INCONNUE in ligne:
                return True
        return False

    def dessine_case(self, ligne, colonne, quadrillage_principal_x=True, quadrillage_principal_y=True):
        case = self.get_valeur_case(ligne, colonne)
        couleur = COULEUR_CASE_VIDE
        nb = None
        if case == CASE_INCONNUE:
            couleur = COULEUR_CASE_INCONNUE
        elif type(case) == int:
            nb = case
        elif case:
            couleur = COULEUR_CASE_PLEINE
        decalage = self.taille_quadrillage + self.ecart_quadrillage_principal
        x = self.cote_case * colonne + decalage
        y = self.cote_case * ligne + decalage
        cote_x = cote_y = self.cote_case - self.taille_quadrillage
        if quadrillage_principal_x:
            reste_x = colonne % QUADRILLAGE_PRINCIPALE
        else:
            reste_x = -1
        if reste_x == 0 or colonne == 0:
            x += self.ecart_quadrillage_principal
            cote_x -= self.ecart_quadrillage_principal
        elif reste_x == QUADRILLAGE_PRINCIPALE - 1 or colonne == self.largeur - 1:
            cote_x -= self.ecart_quadrillage_principal

        if quadrillage_principal_y:
            reste_y = ligne % QUADRILLAGE_PRINCIPALE
        else:
            reste_y = -1
        if reste_y == 0 or ligne == 0:
            y += self.ecart_quadrillage_principal
            cote_y -= self.ecart_quadrillage_principal
        elif reste_y == QUADRILLAGE_PRINCIPALE - 1 or ligne == self.hauteur - 1:
            cote_y -= self.ecart_quadrillage_principal

        pygame.draw.rect(self.ecran, couleur, (x, y, cote_x, cote_y))
        if nb is not None:
            decalage += self.cote_case // 2
            x = self.cote_case * colonne + decalage
            y = self.cote_case * ligne + decalage
            affiche_texte(str(nb), x, y, self.ecran, taille=int(COEF_TAILLE_POLICE * self.cote_case),
                          couleur=COULEUR_NB, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)

    def affiche_select(self, screen: pygame.Surface, x_souris, y_souris):
        if self.mode_suppression_ligne or self.mode_suppression_colonne:
            case = self.get_case_clic(x_souris, y_souris)
            if case is not None:
                ligne, colonne = case
                if self.mode_suppression_ligne:
                    affiche_rect_transparent((self.x,
                                              self.y + self.cote_case * ligne + self.ecart_quadrillage_principal,
                                              self.largeur_pixel, self.cote_case), screen, COULEUR_SUPPRESSION[0],
                                             COULEUR_SUPPRESSION[1])
                if self.mode_suppression_colonne:
                    affiche_rect_transparent((self.x + self.cote_case * colonne + self.ecart_quadrillage_principal,
                                              self.y, self.cote_case, self.hauteur_pixel), screen,
                                             COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])
        if self.mode_ajout_ligne or self.mode_ajout_colonne or \
                self.mode_ajout_groupe_lignes or self.mode_ajout_groupe_colonnes:
            intersection = self.get_intersection_clic(x_souris, y_souris)
            if intersection is not None:
                ligne, colonne = intersection
                trai = int(COEF_TAILLE_AJOUT * self.cote_case)
                trai_sur_2 = int(COEF_TAILLE_AJOUT * self.cote_case / 2)
                if self.mode_ajout_ligne or self.mode_ajout_groupe_lignes:
                    affiche_rect_transparent((self.x, (self.y + self.cote_case * ligne - trai_sur_2 +
                                                       self.ecart_quadrillage_principal), self.largeur_pixel, trai),
                                             screen, COULEUR_AJOUT[0], COULEUR_AJOUT[1])
                if self.mode_ajout_colonne or self.mode_ajout_groupe_colonnes:
                    affiche_rect_transparent(((self.x + self.cote_case * colonne - trai_sur_2 +
                                               self.ecart_quadrillage_principal), self.y, trai, self.hauteur_pixel),
                                             screen, COULEUR_AJOUT[0], COULEUR_AJOUT[1])
        if self.mode_suppression_groupe_lignes or self.mode_suppression_groupe_colonnes:
            case = self.get_case_clic(x_souris, y_souris)
            if case is not None:
                ligne, colonne = case
                if self.mode_suppression_groupe_lignes:
                    for pos in range(min(ligne + QUADRILLAGE_PRINCIPALE - int(QUADRILLAGE_PRINCIPALE / 2) - 1,
                                         len(self.cases) - 1),
                                     max(-1, ligne - int(QUADRILLAGE_PRINCIPALE / 2) - 1), -1):
                        affiche_rect_transparent((self.x,
                                                  self.y + self.cote_case * pos + self.ecart_quadrillage_principal,
                                                  self.largeur_pixel, self.cote_case), screen, COULEUR_SUPPRESSION[0],
                                                 COULEUR_SUPPRESSION[1])
                if self.mode_suppression_groupe_colonnes:
                    for pos in range(min(colonne + QUADRILLAGE_PRINCIPALE - int(QUADRILLAGE_PRINCIPALE / 2) - 1,
                                         len(self.cases[0]) - 1),
                                     max(-1, colonne - int(QUADRILLAGE_PRINCIPALE / 2) - 1), -1):
                        affiche_rect_transparent((self.x + self.cote_case * pos + self.ecart_quadrillage_principal,
                                                  self.y, self.cote_case, self.hauteur_pixel), screen,
                                                 COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])

    def affiche(self, screen: pygame.Surface):
        screen.blit(self.ecran, (self.x, self.y))
