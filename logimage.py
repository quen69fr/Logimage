# coding: utf-8

from grille import *
import copy


possibilitees_pour_x_sur_n = {}


def find_toutes_possibilitees_pour_x_sur_n(x, n):
    if not (x, n) in possibilitees_pour_x_sur_n:
        listes_possiblilitees = []
        if x == 0:
            listes_possiblilitees.append([False] * n)
        else:
            d = n - x
            if d == 0:
                listes_possiblilitees.append([True] * x)
            elif x == 1:
                for i in range(d + 1):
                    listes_possiblilitees.append([False] * (d - i) + [True] + [False] * i)
            else:
                for i in range(d + 1):
                    for possiblitees in find_toutes_possibilitees_pour_x_sur_n(x - 1, x + i - 1):
                        listes_possiblilitees.append((d - i) * [False] + [True] + possiblitees)

        possibilitees_pour_x_sur_n[(x, n)] = listes_possiblilitees

    return possibilitees_pour_x_sur_n[(x, n)]


def find_tous_les_cas_de_figure_d_une_sequense(nb_cases: int, sequence: list):
    liste_possibilitees_simplifiees = find_toutes_possibilitees_pour_x_sur_n(len(sequence),
                                                                             nb_cases - sum(sequence) + 1)
    liste_possibilitees = []
    for possibilitee_simplifiee in liste_possibilitees_simplifiees:
        possibilitee = []
        i = 0
        for case in possibilitee_simplifiee:
            if case:
                if i > 0:
                    possibilitee += [False]
                possibilitee += [True] * sequence[i]
                i += 1
            else:
                possibilitee += [False]
        liste_possibilitees.append(possibilitee)
    return liste_possibilitees


def find_toutes_les_possibilitees_d_une_sequense(cases: list, sequence: list):
    liste_index_True = []
    liste_index_False = []
    for i, case in enumerate(cases):
        if not case == CASE_INCONNUE:
            if case:
                liste_index_True.append(i)
            else:
                liste_index_False.append(i)

    liste_possibilitees = []
    for possibilitees in find_tous_les_cas_de_figure_d_une_sequense(len(cases), sequence):
        possible = True
        for i in liste_index_True:
            if not possibilitees[i]:
                possible = False
                break
        if possible:
            for i in liste_index_False:
                if possibilitees[i]:
                    possible = False
                    break
            if possible:
                liste_possibilitees.append(possibilitees)

    return liste_possibilitees


class Logimage:
    def __init__(self, grille: Grille, titre):
        self.cases = grille.cases
        self.largeur = grille.largeur
        self.hauteur = grille.hauteur
        self.titre = titre
        for i, lette in enumerate(titre):
            if lette == ' ':
                if i + 1 < len(titre):
                    titre = titre[:i + 1] + titre[i + 1].upper() + titre[i + 2:]
        self.titre_sauvegarde = titre.replace(' ', '')

        self.liste_nbs_colonnes = []
        self.liste_nbs_lignes = []
        self.ecran_nbs_colonnes = None
        self.ecran_nbs_lignes = None
        self.size_ecrans_nbs = 0, 0
        self.ecran_vierge = None
        self.ecran_correction = None
        self.ecran_ordinateur = None
        self.nb_etapes_ordinateur = None
        self.ecran_size = 0, 0
        self.ecran_vierge_final = None
        self.ecran_correction_final = None
        self.ecran_ordinateur_final = None

        self.make_listes_nbs_colonnes_lignes()
        self.make_ecrans_nbs_colonnes_lignes()
        self.make_ecrans_vierge_correction()
        self.make_ecran_ordinateur()
        self.make_ecrans_vierge_correction_ordinateur_finaux()
        self.save_ecrans_vierge_correction_ordinateur_finaux()

    def make_listes_nbs_colonnes_lignes(self):
        for ligne in self.cases:
            liste_nbs = []
            n = 0
            for case in ligne:
                if case:
                    n += 1
                else:
                    if n > 0:
                        liste_nbs.append(n)
                        n = 0
            if n > 0:
                liste_nbs.append(n)
            self.liste_nbs_lignes.append(liste_nbs)

        for n_colonne in range(self.largeur):
            liste_nbs = []
            n = 0
            for ligne in self.cases:
                case = ligne[n_colonne]
                if case:
                    n += 1
                else:
                    if n > 0:
                        liste_nbs.append(n)
                        n = 0
            if n > 0:
                liste_nbs.append(n)
            self.liste_nbs_colonnes.append(liste_nbs)

    def make_ecrans_nbs_colonnes_lignes(self):
        max_nbs_lignes = max([len(ligne) for ligne in self.liste_nbs_lignes])
        liste_nbs_lignes = copy.deepcopy(self.liste_nbs_lignes)
        for ligne in liste_nbs_lignes:
            while len(ligne) < max_nbs_lignes:
                ligne.insert(0, False)
        grille_nbs_lignes = Grille(max_nbs_lignes, self.hauteur, True, liste_nbs_lignes,
                                   quadrillage_principal_x=False)

        max_nbs_colonnes = max([len(colonne) for colonne in self.liste_nbs_colonnes])
        liste_nbs_colonnes = copy.deepcopy(self.liste_nbs_colonnes)
        for colonne in liste_nbs_colonnes:
            while len(colonne) < max_nbs_colonnes:
                colonne.insert(0, False)
        liste_nbs_colonnes_retourner = []
        for j in range(max_nbs_colonnes):
            ligne = []
            for colonne in liste_nbs_colonnes:
                ligne.append(colonne[j])
            liste_nbs_colonnes_retourner.append(ligne)
        grille_nbs_colonnes = Grille(self.largeur, max_nbs_colonnes, True, liste_nbs_colonnes_retourner,
                                     quadrillage_principal_y=False)

        self.ecran_nbs_lignes = grille_nbs_lignes.ecran
        self.ecran_nbs_colonnes = grille_nbs_colonnes.ecran
        self.size_ecrans_nbs = self.ecran_nbs_lignes.get_width(), self.ecran_nbs_colonnes.get_height()

    def make_ecrans_vierge_correction(self):
        grille_vierge = Grille(self.largeur, self.hauteur, True)
        grille_correction = Grille(self.largeur, self.hauteur, True, self.cases)
        self.ecran_vierge = grille_vierge.ecran
        self.ecran_correction = grille_correction.ecran
        self.ecran_size = self.ecran_correction.get_size()

    def make_ecran_ordinateur(self):
        grille_ordi = Grille(self.largeur, self.hauteur, True, [[CASE_INCONNUE for _ in range(self.largeur)]
                                                                for _ in range(self.hauteur)])
        cases_ordonnees_colonnes = []
        for j in range(len(grille_ordi.cases[0])):
            colonne = []
            for ligne in grille_ordi.cases:
                colonne.append(ligne[j])
            cases_ordonnees_colonnes.append(colonne)

        self.nb_etapes_ordinateur = None

        nb_etapes = 0
        derniere_etape = None
        stop = False
        while not stop:
            for i, ligne in enumerate(grille_ordi.cases):
                if stop:
                    break
                liste_nbs = self.liste_nbs_lignes[i]
                liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense(ligne, liste_nbs)
                etape = False
                for j, case in enumerate(ligne):
                    if case == CASE_INCONNUE:
                        valeur_case = liste_possibilitees[0][j]
                        for possibilitee in liste_possibilitees:
                            if not possibilitee[j] == valeur_case:
                                valeur_case = None
                                break
                        if valeur_case is not None:
                            grille_ordi.set_valeur_case(i, j, valeur_case)
                            cases_ordonnees_colonnes[j][i] = valeur_case
                            etape = True
                            if not grille_ordi.reste_cases_inconnues():
                                self.nb_etapes_ordinateur = self.largeur * self.hauteur, nb_etapes
                                stop = True
                                break
                if etape:
                    nb_etapes += 1
                    derniere_etape = (0, i)
                else:
                    if derniere_etape == (0, i):
                        stop = True
                        break

            for j, colonne in enumerate(cases_ordonnees_colonnes):
                if stop:
                    break
                liste_nbs = self.liste_nbs_colonnes[j]
                liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense(colonne, liste_nbs)
                etape = False
                for i, case in enumerate(colonne):
                    if case == CASE_INCONNUE:
                        valeur_case = liste_possibilitees[0][i]
                        for possibilitee in liste_possibilitees:
                            if not possibilitee[i] == valeur_case:
                                valeur_case = None
                                break
                        if valeur_case is not None:
                            grille_ordi.set_valeur_case(i, j, valeur_case)
                            cases_ordonnees_colonnes[j][i] = valeur_case
                            etape = True
                            if not grille_ordi.reste_cases_inconnues():
                                self.nb_etapes_ordinateur = self.largeur * self.hauteur, nb_etapes
                                stop = True
                                break
                if etape:
                    nb_etapes += 1
                    derniere_etape = (1, j)
                else:
                    if derniere_etape == (1, j):
                        stop = True
                        break

            if derniere_etape is None:
                stop = True

        if self.nb_etapes_ordinateur is None:
            self.nb_etapes_ordinateur = None, nb_etapes

        self.ecran_ordinateur = grille_ordi.ecran

    def make_ecrans_vierge_correction_ordinateur_finaux(self):
        decalage = int(COTE_CASE_LOGIMAGE * (COEF_TAILLE_QUADRILLAGE_PRINCIPALE_ECART * 2 + COEF_TAILLE_QUADRILLAGE))
        largeur = self.size_ecrans_nbs[0] + self.ecran_size[0] - decalage + 2
        hauteur = self.size_ecrans_nbs[1] + self.ecran_size[1] - decalage + HAUTEUR_BANDEAU_TITRE_LOGIMAGE + 1

        self.ecran_vierge_final = pygame.Surface((largeur, hauteur))
        self.ecran_correction_final = pygame.Surface((largeur, hauteur))
        self.ecran_ordinateur_final = pygame.Surface((largeur, hauteur))

        for ecran in [self.ecran_vierge_final, self.ecran_correction_final, self.ecran_ordinateur_final]:
            ecran.fill(BLANC)
            affiche_texte(self.titre, int(largeur / 2), int(HAUTEUR_BANDEAU_TITRE_LOGIMAGE / 2), ecran,
                          taille=TAILLE_TEXTE_TITRE_LOGIMAGE, couleur=COULEUR_TITRE, x_0gauche_1centre_2droite=1,
                          y_0haut_1centre_2bas=1)
            affiche_surface(self.ecran_nbs_colonnes, largeur - 1, HAUTEUR_BANDEAU_TITRE_LOGIMAGE, ecran,
                            x_0gauche_1centre_2droite=2)
            affiche_surface(self.ecran_nbs_lignes, 1, hauteur - 1, ecran, y_0haut_1centre_2bas=2)

        affiche_surface(self.ecran_vierge, largeur - 1, hauteur - 1, self.ecran_vierge_final,
                        x_0gauche_1centre_2droite=2, y_0haut_1centre_2bas=2,
                        largeur=self.ecran_size[0], hauteur=self.ecran_size[1])
        affiche_surface(self.ecran_correction, largeur - 1, hauteur - 1, self.ecran_correction_final,
                        x_0gauche_1centre_2droite=2, y_0haut_1centre_2bas=2,
                        largeur=self.ecran_size[0], hauteur=self.ecran_size[1])
        affiche_surface(self.ecran_ordinateur, largeur - 1, hauteur - 1, self.ecran_ordinateur_final,
                        x_0gauche_1centre_2droite=2, y_0haut_1centre_2bas=2,
                        largeur=self.ecran_size[0], hauteur=self.ecran_size[1])

        affiche_texte(TEXTE_NB_ETAPES(self.nb_etapes_ordinateur), largeur - 1, 4, self.ecran_ordinateur_final,
                      x_0gauche_1centre_2droite=2)

    def save_ecrans_vierge_correction_ordinateur_finaux(self):
        pygame.image.save(self.ecran_vierge_final, f'ImagesSortie/{self.titre_sauvegarde}-Vierge.png')
        pygame.image.save(self.ecran_correction_final, f'ImagesSortie/{self.titre_sauvegarde}-Correction.png')
        pygame.image.save(self.ecran_ordinateur_final, f'ImagesSortie/{self.titre_sauvegarde}-Ordinateur.png')
