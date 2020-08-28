# coding: utf-8

from titre import *
from fonctions_correction_logimage import *
import json
from threading import Thread

PARAM_LOGIMAGE_NOM = "0"
PARAM_LOGIMAGE_DIMENTIONS = "1"
PARAM_LOGIMAGE_SEQUENCES_LIGNES = "2"
PARAM_LOGIMAGE_SEQUENCES_COLONNES = "3"
PARAM_LOGIMAGE_POSSIBLE = "4"
PARAM_LOGIMAGE_FAISABLE = "5"
PARAM_LOGIMAGE_CORRIGE = "6"
PARAM_LOGIMAGE_NB_ETAPES_ODRI = "7"
PARAM_LOGIMAGE_MODE = "8"

PARAM_LOGIMAGE_NOM_SAUVEGARDE = "-1"
PARAM_LOGIMAGE_CASES = "-2"


def create_logimage_sauvegarde(titre_sauvegarde_logimage: str, mode_logimage):
    with open(NOM_DOSSIER_SAUVEGARDE + titre_sauvegarde_logimage, "r") as sauvegarde_logimage:
        dict_logimage = json.load(sauvegarde_logimage)
        dernier_cases_sans_erreurs = None
        if mode_logimage == MODE_LOGIMAGE_CREER:
            cases = dict_logimage[PARAM_LOGIMAGE_CORRIGE]
            correction = None
        elif mode_logimage == MODE_LOGIMAGE_FAIT and dict_logimage[PARAM_LOGIMAGE_MODE] == MODE_LOGIMAGE_FAIT:
            cases = dict_logimage[PARAM_LOGIMAGE_CORRIGE][0]
            correction = dict_logimage[PARAM_LOGIMAGE_CORRIGE][1]
            if len(dict_logimage[PARAM_LOGIMAGE_CORRIGE]) == 3:
                dernier_cases_sans_erreurs = dict_logimage[PARAM_LOGIMAGE_CORRIGE][2]
        else:
            cases = [[CASE_INCONNUE for _ in range(dict_logimage[PARAM_LOGIMAGE_DIMENTIONS][0])]
                     for _ in range(dict_logimage[PARAM_LOGIMAGE_DIMENTIONS][1])]
            correction = dict_logimage[PARAM_LOGIMAGE_CORRIGE]

        return Logimage(cases, dict_logimage[PARAM_LOGIMAGE_SEQUENCES_LIGNES],
                        dict_logimage[PARAM_LOGIMAGE_SEQUENCES_COLONNES],
                        mode_logimage, None, dict_logimage[PARAM_LOGIMAGE_NOM], titre_sauvegarde_logimage, correction,
                        dict_logimage[PARAM_LOGIMAGE_NB_ETAPES_ODRI], dernier_cases_sans_erreurs)


def impr_logimage_sauvegarde(titre_sauvegarde_logimage: str):
    with open(NOM_DOSSIER_SAUVEGARDE + titre_sauvegarde_logimage, "r") as sauvegarde_logimage:
        dict_logimage = json.load(sauvegarde_logimage)
        cases_correction = dict_logimage[PARAM_LOGIMAGE_CORRIGE]
        cases_vierge = [[False for _ in range(dict_logimage[PARAM_LOGIMAGE_DIMENTIONS][0])]
                        for _ in range(dict_logimage[PARAM_LOGIMAGE_DIMENTIONS][1])]
        for cases, suplement_nom, nb_etapes in [(cases_vierge, SUPLEMENT_NOM_FICHIER_VIERGE, None),
                                                (cases_correction, SUPLEMENT_NOM_FICHIER_CORRECTION,
                                                 dict_logimage[PARAM_LOGIMAGE_NB_ETAPES_ODRI])]:
            logimage = Logimage(cases, dict_logimage[PARAM_LOGIMAGE_SEQUENCES_LIGNES],
                                dict_logimage[PARAM_LOGIMAGE_SEQUENCES_COLONNES],
                                MODE_LOGIMAGE_IMPR, COTE_CASE_IMPR, dict_logimage[PARAM_LOGIMAGE_NOM],
                                titre_sauvegarde_logimage, nb_etapes_ordinateur=nb_etapes)
            logimage.imprime_png(suplement_nom)


def create_logimage_nouveau(mode_logimage, dimentions=DEFAULT_TAILLE_GRILLE, titre=None):
    nb_colonnes, nb_lignes = dimentions
    if mode_logimage == MODE_LOGIMAGE_CREER or mode_logimage == MODE_LOGIMAGE_IMPR:
        return Logimage([[False for _ in range(nb_colonnes)] for _ in range(nb_lignes)],
                        [[] for _ in range(nb_lignes)], [[] for _ in range(nb_colonnes)], MODE_LOGIMAGE_CREER, None,
                        titre)
    else:
        return Logimage([[CASE_INCONNUE for _ in range(nb_colonnes)] for _ in range(nb_lignes)],
                        [[] for _ in range(nb_lignes)], [[] for _ in range(nb_colonnes)], MODE_LOGIMAGE_RENTRE, None,
                        titre)


def create_logimage_creer_png(chemin_image: str):
    image = pygame.image.load(f'{NOM_DOSSIER_ENTREES_PNG}{chemin_image}')
    largeur, hauteur = image.get_size()
    # logimage = create_logimage_nouveau(MODE_LOGIMAGE_CREER, (largeur, hauteur), chemin_image[:-4])

    cases = [[False for _ in range(largeur)] for _ in range(hauteur)]

    for ligne in range(hauteur):
        for colonne in range(largeur):
            if image.get_at((colonne, ligne)) == NOIR:
                cases[ligne][colonne] = True

    return Logimage(cases, [[] for _ in range(hauteur)], [[] for _ in range(largeur)], MODE_LOGIMAGE_CREER, None,
                    chemin_image[:-4])


class Logimage:
    def __init__(self, cases: list, sequences_lignes: list, sequences_colonnes: list, mode_logimage,
                 cote_case: int or None, titre: str or None, titre_sauvegarde: str = None, corrige: list = None,
                 nb_etapes_ordinateur: int = None, dernier_cases_sans_erreurs: list = None):
        self.mode_logimage = mode_logimage

        self.cases = cases
        self.corrige = corrige
        self.possible = None
        self.faisable = None
        self.nb_etapes_ordinateur = nb_etapes_ordinateur
        self.sequences_lignes = sequences_lignes
        self.sequences_colonnes = sequences_colonnes
        self.titre = Titre(titre, titre_sauvegarde)

        self.nb_lignes = len(self.cases)
        self.nb_colonnes = len(self.cases[0])
        self.nb_colonnes_sequences_ligne = max([len(sequence) for sequence in self.sequences_lignes])
        self.nb_lignes_sequences_colonne = max([len(sequence) for sequence in self.sequences_colonnes])
        if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
            self.sequences_corrigees = None
            self.nb_colonnes_sequences_ligne += 1
            self.nb_lignes_sequences_colonne += 1
        elif self.mode_logimage == MODE_LOGIMAGE_CORRECTION:
            self.ligne_ou_colonne_en_cours = None
            self.cases_ordonnees_colonnes = []
            self.update_cases_ordonnees_colonnes()
        if self.mode_logimage == MODE_LOGIMAGE_FAIT:
            self.dic_points_crayon = {}
            self.liste_cases_rayees = []
            self.taille_point_crayon = 0
            self.aide = None
            self.stop_tread_aide = True
        else:
            self.logimage_correction_progressive = None

        self.update_sequences_auto = self.mode_logimage == MODE_LOGIMAGE_CREER

        self.cote_case_fixe = cote_case is not None

        self.cote_case = cote_case if self.cote_case_fixe else 0
        self.ecran = None
        self.x_ecran = 0
        self.y_ecran = 0
        self.largeur_ecran = 0
        self.hauteur_ecran = 0
        self.x_origine_sur_ecran = 0
        self.y_origine_sur_ecran = 0
        self.taille_quadrillage = 0
        self.ecart_quadrillage_principal = 0
        self.taille_texte = 0

        self.derniere_case_modifiee = None
        self.recadre = True
        self.cases_affiche_en_attente = {}

        self.trouve_erreurs = self.mode_logimage == MODE_LOGIMAGE_FAIT
        if self.trouve_erreurs:
            self.dernier_cases_sans_erreurs = dernier_cases_sans_erreurs
            self.liste_erreurs = []
            self.update_liste_erreur()

        if self.update_sequences_auto:
            self.update_all_sequences_lignes()
            self.update_all_sequences_colonnes()

        if self.mode_logimage == MODE_LOGIMAGE_IMPR:
            self.update_affichage()
        else:
            self.updating_thread = False
            self.update_affichage_thread()

    # -----------------------------------------------------------------

    def teste_coherence_sequences(self):
        for ligne in self.sequences_lignes:
            if len(ligne) == 0:
                return False
        for colonne in self.sequences_colonnes:
            if len(colonne) == 0:
                return False
        if self.update_sequences_auto:
            return True
        somme_lignes_totale = 0
        for ligne in self.sequences_lignes:
            somme_ligne = sum(ligne)
            if somme_ligne + len(ligne) - 1 > self.nb_colonnes:
                return False
            somme_lignes_totale += somme_ligne
        somme_colonnes_totale = 0
        for colonne in self.sequences_colonnes:
            somme_colonne = sum(colonne)
            if somme_colonne + len(colonne) - 1 > self.nb_lignes:
                return False
            somme_colonnes_totale += somme_colonne
        if not somme_lignes_totale == somme_colonnes_totale:
            return False
        return True

    def corrige_logimage_old_1(self):
        print_correction(f'Correction de {self.titre.texte} :')
        t0 = time.time()
        potentiellement_impossible = not self.update_sequences_auto
        lignes_erreur_memoire = []
        colonnes_erreur_memoire = []
        clear_possibilitees_pour_x_sur_n()
        set_plus_lent_moins_de_memoire(False)
        plus_lent_et_moins_de_memoire = False
        cases = [[CASE_INCONNUE for _ in range(self.nb_colonnes)] for _ in range(self.nb_lignes)]
        cases_ordonnees_colonnes = []
        for j in range(len(cases[0])):
            colonne = []
            for ligne in cases:
                colonne.append(ligne[j])
            cases_ordonnees_colonnes.append(colonne)

        self.possible = self.teste_coherence_sequences()

        nb_etapes = 0
        if self.possible:
            self.faisable = False

            stop = False
            lignes_a_tester = [i for i in range(self.nb_lignes)]
            colonnes_a_tester = [j for j in range(self.nb_colonnes)]
            while not stop:
                for i in lignes_a_tester:
                    if stop:
                        break
                    ligne = cases[i]
                    liste_nbs = self.sequences_lignes[i]
                    if CASE_INCONNUE not in ligne:
                        if potentiellement_impossible:
                            sequence_ligne = []
                            n = 0
                            for case in ligne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_ligne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_ligne.append(n)
                            if not sequence_ligne == liste_nbs:
                                print_correction('----- IMPOSSIBLE -----')
                                self.possible = False
                                stop = True
                                break
                        continue
                    print_correction(f'ligne {i}:')
                    etape = False
                    try:
                        liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense_m1(ligne, liste_nbs)
                    except MemoryError:
                        print_correction('Erreur : trop de possibilités')
                        if i not in lignes_erreur_memoire:
                            lignes_erreur_memoire.append(i)
                    else:
                        if i in lignes_erreur_memoire:
                            lignes_erreur_memoire.remove(i)
                        if potentiellement_impossible:
                            if len(liste_possibilitees) == 0:
                                print_correction('----- IMPOSSIBLE -----')
                                self.possible = False
                                stop = True
                                break
                        for j, case in enumerate(ligne):
                            if case == CASE_INCONNUE:
                                valeur_case = liste_possibilitees[0][j]
                                for possibilitee in liste_possibilitees:
                                    if not possibilitee[j] == valeur_case:
                                        valeur_case = None
                                        break
                                if valeur_case is not None:
                                    print_correction(f'-------- case {i}, {j}')
                                    cases[i][j] = valeur_case
                                    cases_ordonnees_colonnes[j][i] = valeur_case
                                    if j not in colonnes_a_tester:
                                        colonnes_a_tester.append(j)
                                    etape = True
                                    if not test_reste_cases_inconnues(cases):
                                        print_correction('-------- FIN --------')
                                        self.faisable = True
                                        nb_etapes += 1
                                        stop = True
                                        break
                    if etape:
                        nb_etapes += 1
                if stop:
                    break
                lignes_a_tester = []
                if len(colonnes_a_tester) == 0:
                    if not plus_lent_et_moins_de_memoire and (len(lignes_erreur_memoire) > 0 or
                                                              len(colonnes_erreur_memoire) > 0):
                        clear_possibilitees_pour_x_sur_n()
                        lignes_a_tester = lignes_erreur_memoire[:]
                        colonnes_a_tester = colonnes_erreur_memoire[:]
                        plus_lent_et_moins_de_memoire = True
                        set_plus_lent_moins_de_memoire(True)
                        print_correction('==> Mode plus long moins de mémoire')
                    else:
                        print_correction('----- INFAISABLE -----')
                        break

                for j in colonnes_a_tester:
                    if stop:
                        break
                    colonne = cases_ordonnees_colonnes[j]
                    liste_nbs = self.sequences_colonnes[j]
                    if CASE_INCONNUE not in colonne:
                        if potentiellement_impossible:
                            sequence_colonne = []
                            n = 0
                            for case in colonne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_colonne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_colonne.append(n)
                            if not sequence_colonne == liste_nbs:
                                print_correction('----- IMPOSSIBLE -----')
                                self.possible = False
                                stop = True
                                break
                        continue
                    print_correction(f'colonne {j}:')
                    etape = False
                    try:
                        liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense_m1(colonne, liste_nbs)
                    except MemoryError:
                        print_correction('Erreur : trop de possibilités')
                        if j not in colonnes_erreur_memoire:
                            colonnes_erreur_memoire.append(j)
                    else:
                        if j in colonnes_erreur_memoire:
                            colonnes_erreur_memoire.remove(j)
                        if potentiellement_impossible:
                            if len(liste_possibilitees) == 0:
                                print_correction('----- IMPOSSIBLE -----')
                                self.possible = False
                                stop = True
                                break
                        for i, case in enumerate(colonne):
                            if case == CASE_INCONNUE:
                                valeur_case = liste_possibilitees[0][i]
                                for possibilitee in liste_possibilitees:
                                    if not possibilitee[i] == valeur_case:
                                        valeur_case = None
                                        break
                                if valeur_case is not None:
                                    print_correction(f'-------- case {i}, {j}')
                                    cases[i][j] = valeur_case
                                    cases_ordonnees_colonnes[j][i] = valeur_case
                                    if i not in lignes_a_tester:
                                        lignes_a_tester.append(i)
                                    etape = True
                                    if not test_reste_cases_inconnues(cases):
                                        print_correction('-------- FIN --------')
                                        self.faisable = True
                                        nb_etapes += 1
                                        stop = True
                                        break
                    if etape:
                        nb_etapes += 1
                if stop:
                    break
                colonnes_a_tester = []
                if len(lignes_a_tester) == 0:
                    if not plus_lent_et_moins_de_memoire and (len(lignes_erreur_memoire) > 0 or
                                                              len(colonnes_erreur_memoire) > 0):
                        clear_possibilitees_pour_x_sur_n()
                        lignes_a_tester = lignes_erreur_memoire[:]
                        colonnes_a_tester = colonnes_erreur_memoire[:]
                        plus_lent_et_moins_de_memoire = True
                        set_plus_lent_moins_de_memoire(True)
                        print_correction('==> Mode plus long moins de mémoire')
                    else:
                        print_correction('----- INFAISABLE -----')
                        break

        print_correction(f'Durée totale : {int((time.time() - t0) // 60)} min {round((time.time() - t0) % 60, 2)} sec')

        if self.possible:
            self.nb_etapes_ordinateur = nb_etapes
            self.corrige = cases
            if not self.faisable and (len(lignes_erreur_memoire) > 0 or len(colonnes_erreur_memoire) > 0):
                return False
        else:
            self.faisable = None
            self.nb_etapes_ordinateur = None
            self.corrige = None
        return True

    def corrige_logimage_old_2(self):
        print_correction(f'Correction de {self.titre.texte} :')
        t0 = time.time()
        potentiellement_impossible = not self.update_sequences_auto

        cases = [[CASE_INCONNUE for _ in range(self.nb_colonnes)] for _ in range(self.nb_lignes)]

        cases_ordonnees_colonnes = [[CASE_INCONNUE for _ in range(self.nb_lignes)] for _ in range(self.nb_colonnes)]
        erreur_memoire = False

        nb_cases_fixees = 0
        nb_cases_a_fixees = self.nb_lignes * self.nb_colonnes

        self.possible = self.teste_coherence_sequences()

        self.nb_etapes_ordinateur = 0
        if self.possible:
            self.faisable = False
            stop = False
            lignes_a_tester = [i for i in range(self.nb_lignes)]
            colonnes_a_tester = [j for j in range(self.nb_colonnes)]
            while not stop:
                # Les lignes :
                for i in lignes_a_tester:
                    if stop:
                        break
                    ligne = cases[i]
                    liste_nbs = self.sequences_lignes[i]
                    if CASE_INCONNUE not in ligne:
                        if potentiellement_impossible:
                            sequence_ligne = []
                            n = 0
                            for case in ligne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_ligne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_ligne.append(n)
                            if not sequence_ligne == liste_nbs:
                                self.possible = False
                                stop = True
                                break
                        continue

                    print_correction(f'___ LIGNE {i} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent_old(ligne, liste_nbs)

                    if liste_cases_communes is None:
                        self.possible = False
                        stop = True
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for j, valeur in liste_cases_communes:
                                print_correction(f'-------> case {i}, {j}')
                                cases[i][j] = valeur
                                cases_ordonnees_colonnes[j][i] = valeur
                                if j not in colonnes_a_tester:
                                    colonnes_a_tester.append(j)
                            nb_cases_fixees += len(liste_cases_communes)
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                stop = True
                                break
                if stop:
                    break
                lignes_a_tester = []
                if len(colonnes_a_tester) == 0:
                    break

                # Les colonnes :
                for j in colonnes_a_tester:
                    if stop:
                        break
                    colonne = cases_ordonnees_colonnes[j]
                    liste_nbs = self.sequences_colonnes[j]
                    if CASE_INCONNUE not in colonne:
                        if potentiellement_impossible:
                            sequence_colonne = []
                            n = 0
                            for case in colonne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_colonne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_colonne.append(n)
                            if not sequence_colonne == liste_nbs:
                                self.possible = False
                                stop = True
                                break
                        continue

                    print_correction(f'___ COLONNE {j} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent_old(colonne, liste_nbs)

                    if liste_cases_communes is None:
                        self.possible = False
                        stop = True
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for i, valeur in liste_cases_communes:
                                print_correction(f'-------> case {i}, {j}')
                                cases[i][j] = valeur
                                cases_ordonnees_colonnes[j][i] = valeur
                                if i not in lignes_a_tester:
                                    lignes_a_tester.append(i)
                            nb_cases_fixees += len(liste_cases_communes)
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                stop = True
                                break

                if stop:
                    break
                colonnes_a_tester = []
                if len(lignes_a_tester) == 0:
                    break

        if self.possible:
            self.corrige = cases
            if self.faisable:
                print_correction('-------- FIN --------')
            else:
                if erreur_memoire:
                    print_correction('-------- ERREUR --------')
                    self.nb_etapes_ordinateur *= -1
                else:
                    print_correction('----- INFAISABLE -----')

        else:
            self.faisable = None
            self.nb_etapes_ordinateur = None
            self.corrige = None
            print_correction('----- IMPOSSIBLE -----')

        print_correction('')
        print_correction(f'Durée totale : {int((time.time() - t0) // 60)} min {round((time.time() - t0) % 60, 2)} sec')

    def corrige_logimage_old_3(self):
        print_correction(f'Correction de {self.titre.texte} :')
        t0 = time.time()
        potentiellement_impossible = not self.update_sequences_auto

        clear_possibilitees_pour_x_sur_n()

        cases = [[CASE_INCONNUE for _ in range(self.nb_colonnes)] for _ in range(self.nb_lignes)]
        cases_ordonnees_colonnes = [[CASE_INCONNUE for _ in range(self.nb_lignes)] for _ in range(self.nb_colonnes)]
        erreur_memoire = False

        nb_cases_fixees = 0
        nb_cases_a_fixees = self.nb_lignes * self.nb_colonnes

        self.possible = self.teste_coherence_sequences()

        self.nb_etapes_ordinateur = 0
        if self.possible:
            self.faisable = False

            lignes_colonnes_a_tester = {}
            for i in range(self.nb_lignes):
                sequence = self.sequences_lignes[i]
                if self.nb_colonnes - sum(sequence) - len(sequence) + 1 < max(sequence):
                    lignes_colonnes_a_tester[(True, i)] = calcul_score_ligne(cases[i], sequence)
            for j in range(self.nb_colonnes):
                sequence = self.sequences_colonnes[j]
                if self.nb_lignes - sum(sequence) - len(sequence) + 1 < max(sequence):
                    lignes_colonnes_a_tester[(False, j)] = calcul_score_ligne(cases_ordonnees_colonnes[j], sequence)
            while len(lignes_colonnes_a_tester) > 0:
                ligne_colonne_min = min(lignes_colonnes_a_tester,
                                        key=lambda key: lignes_colonnes_a_tester[key][0] * COEF_RENTABILITE_METHODE_1
                                        if (lignes_colonnes_a_tester[key][1] and
                                            lignes_colonnes_a_tester[key][0] < SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE)
                                        else lignes_colonnes_a_tester[key][0])
                ligne_ou_pas, n = ligne_colonne_min
                nb_possibilites, methode_1_ou_2 = lignes_colonnes_a_tester[ligne_colonne_min]
                del lignes_colonnes_a_tester[ligne_colonne_min]

                if ligne_ou_pas:
                    ligne = cases[n]
                    liste_nbs = self.sequences_lignes[n]
                    if CASE_INCONNUE not in ligne:
                        if potentiellement_impossible:
                            sequence_ligne = []
                            n = 0
                            for case in ligne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_ligne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_ligne.append(n)
                            if not sequence_ligne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ LIGNE {n} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent(ligne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for j, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {n}, {j}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                cases[n][j] = valeur
                                cases_ordonnees_colonnes[j][n] = valeur
                                lignes_colonnes_a_tester[(False, j)] = \
                                    calcul_score_ligne(cases_ordonnees_colonnes[j], self.sequences_colonnes[j])
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

                else:
                    colonne = cases_ordonnees_colonnes[n]
                    liste_nbs = self.sequences_colonnes[n]
                    if CASE_INCONNUE not in colonne:
                        if potentiellement_impossible:
                            sequence_colonne = []
                            n = 0
                            for case in colonne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_colonne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_colonne.append(n)
                            if not sequence_colonne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ COLONNE {n} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent(colonne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for i, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {i}, {n}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                cases[i][n] = valeur
                                cases_ordonnees_colonnes[n][i] = valeur
                                lignes_colonnes_a_tester[(True, i)] = \
                                    calcul_score_ligne(cases[i], self.sequences_lignes[i])
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

        if self.possible:
            self.corrige = cases
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                self.sequences_corrigees = [copy.deepcopy(self.sequences_lignes),
                                            copy.deepcopy(self.sequences_colonnes)]
            if self.faisable:
                print_correction('-------- FIN --------')
            else:
                if erreur_memoire:
                    print_correction('-------- ERREUR --------')
                    self.nb_etapes_ordinateur *= -1
                else:
                    print_correction('----- INFAISABLE -----')

        else:
            self.faisable = None
            self.nb_etapes_ordinateur = None
            self.corrige = None
            print_correction('----- IMPOSSIBLE -----')

        print_correction('')
        print_correction(f'Durée totale : {int((time.time() - t0) // 60)} min {round((time.time() - t0) % 60, 2)} sec')

    def corrige_logimage_affichage_old_4(self):
        print_correction(f'Correction de {self.titre.texte} :')
        t0 = time.time()
        potentiellement_impossible = not self.update_sequences_auto

        clear_possibilitees_pour_x_sur_n()

        self.logimage_correction_progressive = Logimage([[CASE_INCONNUE for _ in range(self.nb_colonnes)]
                                                         for _ in range(self.nb_lignes)], self.sequences_lignes,
                                                        self.sequences_colonnes, MODE_LOGIMAGE_CORRECTION, None,
                                                        f'CORRECTION : {self.titre.texte}', 'Inutile')
        cases = self.logimage_correction_progressive.cases
        cases_ordonnees_colonnes = self.logimage_correction_progressive.cases_ordonnees_colonnes

        erreur_memoire = False
        nb_cases_fixees = 0
        nb_cases_a_fixees = self.nb_lignes * self.nb_colonnes

        self.possible = self.teste_coherence_sequences()

        self.nb_etapes_ordinateur = 0
        if self.possible:
            self.faisable = False

            lignes_colonnes_a_tester = {}
            for i in range(self.nb_lignes):
                lignes_colonnes_a_tester[(True, i)] = calcul_score_ligne(cases[i], self.sequences_lignes[i])
            for j in range(self.nb_colonnes):
                lignes_colonnes_a_tester[(False, j)] = calcul_score_ligne(cases_ordonnees_colonnes[j],
                                                                          self.sequences_colonnes[j])
            while len(lignes_colonnes_a_tester) > 0:
                self.logimage_correction_progressive.ligne_ou_colonne_en_cours = \
                    min(lignes_colonnes_a_tester,
                        key=lambda key: lignes_colonnes_a_tester[key][0] * COEF_RENTABILITE_METHODE_1
                        if (lignes_colonnes_a_tester[key][1] and
                            lignes_colonnes_a_tester[key][0] < SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE)
                        else lignes_colonnes_a_tester[key][0])
                ligne_ou_pas, n = self.logimage_correction_progressive.ligne_ou_colonne_en_cours
                nb_possibilites, methode_1_ou_2 = \
                    lignes_colonnes_a_tester[self.logimage_correction_progressive.ligne_ou_colonne_en_cours]
                del lignes_colonnes_a_tester[self.logimage_correction_progressive.ligne_ou_colonne_en_cours]

                if ligne_ou_pas:
                    ligne = cases[n]
                    liste_nbs = self.sequences_lignes[n]
                    if CASE_INCONNUE not in ligne:
                        if potentiellement_impossible:
                            sequence_ligne = []
                            n = 0
                            for case in ligne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_ligne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_ligne.append(n)
                            if not sequence_ligne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ LIGNE {n} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent(ligne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for j, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {n}, {j}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                self.logimage_correction_progressive.set_case_grille(n, j, valeur)
                                lignes_colonnes_a_tester[(False, j)] = \
                                    calcul_score_ligne(cases_ordonnees_colonnes[j], self.sequences_colonnes[j])
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

                else:
                    colonne = cases_ordonnees_colonnes[n]
                    liste_nbs = self.sequences_colonnes[n]
                    if CASE_INCONNUE not in colonne:
                        if potentiellement_impossible:
                            sequence_colonne = []
                            n = 0
                            for case in colonne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_colonne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_colonne.append(n)
                            if not sequence_colonne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ COLONNE {n} ___')
                    liste_cases_communes = trouve_cases_communes_intelligent(colonne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for i, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {i}, {n}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                self.logimage_correction_progressive.set_case_grille(i, n, valeur)
                                lignes_colonnes_a_tester[(True, i)] = \
                                    calcul_score_ligne(cases[i], self.sequences_lignes[i])
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

        dossier_sauvegarde = None
        if self.possible:
            self.corrige = cases
            if self.faisable:
                print_correction('-------- FIN --------')
            else:
                if erreur_memoire:
                    print_correction('-------- ERREUR --------')
                    self.nb_etapes_ordinateur *= -1
                    dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_INF_ERREURS
                else:
                    print_correction('----- INFAISABLE -----')
                    dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_INFAISABLES

        else:
            self.faisable = None
            self.nb_etapes_ordinateur = None
            self.corrige = None
            print_correction('----- IMPOSSIBLE -----')
            dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_IMPOSSIBLES

        print_correction('')
        print_correction(f'Durée totale : {int((time.time() - t0) // 60)} min {round((time.time() - t0) % 60, 2)} sec')
        self.logimage_correction_progressive.ligne_ou_colonne_en_cours = None
        self.logimage_correction_progressive = None
        if dossier_sauvegarde is not None:
            logimage_impr = Logimage(self.corrige, self.sequences_lignes, self.sequences_colonnes, MODE_LOGIMAGE_IMPR,
                                     COTE_CASE_IMPR, self.titre.texte, self.titre.titre_sauvegarde,
                                     nb_etapes_ordinateur=self.nb_etapes_ordinateur)
            logimage_impr.imprime_png('', f'{dossier_sauvegarde}{self.titre.titre_sauvegarde[:-5]}.png')

    def corrige_logimage_affichage(self):
        print_correction(f'Correction de {self.titre.texte} :')
        t0 = time.time()
        potentiellement_impossible = not self.update_sequences_auto

        clear_possibilitees_pour_x_sur_n()

        self.logimage_correction_progressive = Logimage([[CASE_INCONNUE for _ in range(self.nb_colonnes)]
                                                         for _ in range(self.nb_lignes)], self.sequences_lignes,
                                                        self.sequences_colonnes, MODE_LOGIMAGE_CORRECTION, None,
                                                        f'CORRECTION : {self.titre.texte}', 'Inutile')
        cases = self.logimage_correction_progressive.cases
        cases_ordonnees_colonnes = self.logimage_correction_progressive.cases_ordonnees_colonnes

        erreur_memoire = False
        nb_cases_fixees = 0
        nb_cases_a_fixees = self.nb_lignes * self.nb_colonnes

        self.possible = self.teste_coherence_sequences()

        self.nb_etapes_ordinateur = 0
        if self.possible:
            self.faisable = False

            lignes_colonnes_a_tester = {}
            liste_lignes_colonnes_a_tester_grossierement = []
            for i in range(self.nb_lignes):
                lignes_colonnes_a_tester[(True, i)] = calcul_score_ligne(cases[i], self.sequences_lignes[i])
                liste_lignes_colonnes_a_tester_grossierement.append((True, i))
            for j in range(self.nb_colonnes):
                lignes_colonnes_a_tester[(False, j)] = calcul_score_ligne(cases_ordonnees_colonnes[j],
                                                                          self.sequences_colonnes[j])
                liste_lignes_colonnes_a_tester_grossierement.append((False, j))

            while len(lignes_colonnes_a_tester) > 0:
                ligne_ou_pas, n = min(lignes_colonnes_a_tester,
                                      key=lambda key: lignes_colonnes_a_tester[key][0] * COEF_RENTABILITE_METHODE_1
                                      if (lignes_colonnes_a_tester[key][1] and
                                          lignes_colonnes_a_tester[key][0] < SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE)
                                      else lignes_colonnes_a_tester[key][0])
                nb_possibilites, methode_1_ou_2 = lignes_colonnes_a_tester[(ligne_ou_pas, n)]
                if nb_possibilites < SEUIL_RENTABILITE_METHODE_GROSSIERE or \
                        len(liste_lignes_colonnes_a_tester_grossierement) == 0:
                    del lignes_colonnes_a_tester[(ligne_ou_pas, n)]
                    if (ligne_ou_pas, n) in liste_lignes_colonnes_a_tester_grossierement:
                        liste_lignes_colonnes_a_tester_grossierement.remove((ligne_ou_pas, n))
                    methode_grossiere = False
                else:
                    ligne_ou_pas, n = liste_lignes_colonnes_a_tester_grossierement[0]
                    del liste_lignes_colonnes_a_tester_grossierement[0]
                    methode_grossiere = True
                self.logimage_correction_progressive.ligne_ou_colonne_en_cours = ligne_ou_pas, n

                if ligne_ou_pas:
                    ligne = cases[n]
                    liste_nbs = self.sequences_lignes[n]
                    if CASE_INCONNUE not in ligne:
                        if potentiellement_impossible:
                            sequence_ligne = []
                            n = 0
                            for case in ligne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_ligne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_ligne.append(n)
                            if not sequence_ligne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ LIGNE {n} ___')
                    if methode_grossiere:
                        liste_cases_communes = trouve_cases_communes_grossierement(ligne, liste_nbs)
                    else:
                        liste_cases_communes = trouve_cases_communes_intelligent(ligne, liste_nbs,
                                                                                 methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        if not methode_grossiere:
                            erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for j, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {n}, {j}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                self.logimage_correction_progressive.set_case_grille(n, j, valeur)
                                lignes_colonnes_a_tester[(False, j)] = \
                                    calcul_score_ligne(cases_ordonnees_colonnes[j], self.sequences_colonnes[j])
                                if (False, j) not in liste_lignes_colonnes_a_tester_grossierement:
                                    liste_lignes_colonnes_a_tester_grossierement.append([False, j])
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

                else:
                    colonne = cases_ordonnees_colonnes[n]
                    liste_nbs = self.sequences_colonnes[n]
                    if CASE_INCONNUE not in colonne:
                        if potentiellement_impossible:
                            sequence_colonne = []
                            n = 0
                            for case in colonne:
                                if case:
                                    n += 1
                                else:
                                    if n > 0:
                                        sequence_colonne.append(n)
                                        n = 0
                            if n > 0:
                                sequence_colonne.append(n)
                            if not sequence_colonne == liste_nbs:
                                self.possible = False
                                break
                        continue

                    print_correction(f'___ COLONNE {n} ___')
                    if methode_grossiere:
                        liste_cases_communes = trouve_cases_communes_grossierement(colonne, liste_nbs)
                    else:
                        liste_cases_communes = trouve_cases_communes_intelligent(colonne, liste_nbs,
                                                                                 methode_1_ou_2, nb_possibilites)

                    if liste_cases_communes is None:
                        self.possible = False
                        break
                    elif liste_cases_communes == RETURN_ERREUR_MEMOIRE:
                        if not methode_grossiere:
                            erreur_memoire = True
                    else:
                        if len(liste_cases_communes) > 0:
                            self.nb_etapes_ordinateur += 1
                            for i, valeur in liste_cases_communes:
                                nb_cases_fixees += 1
                                print_correction(f'-------> case {i}, {n}   ({nb_cases_fixees}/{nb_cases_a_fixees})')
                                self.logimage_correction_progressive.set_case_grille(i, n, valeur)
                                lignes_colonnes_a_tester[(True, i)] = \
                                    calcul_score_ligne(cases[i], self.sequences_lignes[i])
                                if (True, i) not in liste_lignes_colonnes_a_tester_grossierement:
                                    liste_lignes_colonnes_a_tester_grossierement.append((True, i))
                            if nb_cases_fixees >= nb_cases_a_fixees:
                                self.faisable = True
                                break

        dossier_sauvegarde = None
        if self.possible:
            self.corrige = cases
            if self.faisable:
                print_correction('-------- FIN --------')
            else:
                if erreur_memoire:
                    print_correction('-------- ERREUR --------')
                    self.nb_etapes_ordinateur *= -1
                    dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_INF_ERREURS
                else:
                    print_correction('----- INFAISABLE -----')
                    dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_INFAISABLES

        else:
            self.faisable = None
            self.nb_etapes_ordinateur = None
            self.corrige = None
            print_correction('----- IMPOSSIBLE -----')
            dossier_sauvegarde = NOM_DOSSIER_SAUVEGARDE_IMAGES_IMPOSSIBLES

        print_correction('')
        print_correction(f'Durée totale : {int((time.time() - t0) // 60)} min {round((time.time() - t0) % 60, 2)} sec')
        self.logimage_correction_progressive.ligne_ou_colonne_en_cours = None
        self.logimage_correction_progressive = None
        if dossier_sauvegarde is not None:
            logimage_impr = Logimage(cases, self.sequences_lignes, self.sequences_colonnes, MODE_LOGIMAGE_IMPR,
                                     COTE_CASE_IMPR, self.titre.texte, self.titre.titre_sauvegarde,
                                     nb_etapes_ordinateur=self.nb_etapes_ordinateur)
            logimage_impr.imprime_png('', dossier_sauvegarde)

    def trouve_ligne_colonne_aide(self):
        lignes_colonnes_a_tester = [(True, n) for n in range(self.nb_lignes)] + \
                                   [(False, n) for n in range(self.nb_colonnes)]
        random.shuffle(lignes_colonnes_a_tester)
        for ligne_ou_pas, n in lignes_colonnes_a_tester:
            if self.stop_tread_aide:
                return False
            if ligne_ou_pas:
                ligne = self.cases[n]
                if CASE_INCONNUE not in ligne:
                    continue
                liste_nbs = self.sequences_lignes[n]
            else:
                ligne = [ligne[n] for ligne in self.cases]
                if CASE_INCONNUE not in ligne:
                    continue
                liste_nbs = self.sequences_colonnes[n]
            if len(trouve_cases_communes_grossierement(ligne, liste_nbs)) > 0:
                self.aide = (ligne_ou_pas, n)
                return True

        # for n, ligne in enumerate(self.cases):
        #     if self.stop_tread_aide:
        #         return False
        #     liste_nbs = self.sequences_lignes[n]
        #     if len(trouve_cases_communes_grossierement(ligne, liste_nbs)) > 0:
        #         self.aide = (True, n)
        #         return True
        #
        # for n in range(self.nb_colonnes):
        #     if self.stop_tread_aide:
        #         return False
        #     colonne = [ligne[n] for ligne in self.cases]
        #     liste_nbs = self.sequences_colonnes[n]
        #     if len(trouve_cases_communes_grossierement(colonne, liste_nbs)) > 0:
        #         self.aide = (False, n)
        #         return True

        cases_ordonnees_colonnes = [[ligne[j] for ligne in self.cases] for j in range(self.nb_colonnes)]
        lignes_colonnes_a_tester = {}
        for i in range(self.nb_lignes):
            if CASE_INCONNUE in self.cases[i]:
                lignes_colonnes_a_tester[(True, i)] = calcul_score_ligne(self.cases[i], self.sequences_lignes[i])
        for j in range(self.nb_colonnes):
            if CASE_INCONNUE in cases_ordonnees_colonnes[j]:
                lignes_colonnes_a_tester[(False, j)] = calcul_score_ligne(cases_ordonnees_colonnes[j],
                                                                          self.sequences_colonnes[j])

        while len(lignes_colonnes_a_tester) > 0:
            if self.stop_tread_aide:
                return False
            ligne_ou_pas, n = min(lignes_colonnes_a_tester,
                                  key=lambda key: lignes_colonnes_a_tester[key][0] * COEF_RENTABILITE_METHODE_1
                                  if (lignes_colonnes_a_tester[key][1] and
                                      lignes_colonnes_a_tester[key][0] < SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE)
                                  else lignes_colonnes_a_tester[key][0])
            nb_possibilites, methode_1_ou_2 = lignes_colonnes_a_tester[(ligne_ou_pas, n)]
            del lignes_colonnes_a_tester[(ligne_ou_pas, n)]
            if ligne_ou_pas:
                ligne = self.cases[n]
                liste_nbs = self.sequences_lignes[n]
                if len(trouve_cases_communes_intelligent(ligne, liste_nbs, methode_1_ou_2, nb_possibilites)) > 0:
                    self.aide = (True, n)
                    return True

            else:
                colonne = cases_ordonnees_colonnes[n]
                liste_nbs = self.sequences_colonnes[n]
                if len(trouve_cases_communes_intelligent(colonne, liste_nbs,  methode_1_ou_2, nb_possibilites)) > 0:
                    self.aide = (False, n)
                    return True
        return False

    def stop_aide(self):
        self.stop_tread_aide = True
        set_action_aide(False)

    def gere_aide(self):
        if len(self.liste_erreurs) > 0:
            self.aide = False
        elif not test_reste_cases_inconnues(self.cases):
            self.stop_aide()
        else:
            self.aide = None
            self.stop_tread_aide = False
            thread_aide = Thread(target=self.trouve_ligne_colonne_aide)
            thread_aide.start()

    def return_dict_logimage(self):
        if self.mode_logimage == MODE_LOGIMAGE_CREER:
            corrige = self.cases
        elif self.mode_logimage == MODE_LOGIMAGE_FAIT and self.trouve_erreurs:
            if len(self.liste_erreurs) == 0:
                corrige = [self.cases, self.corrige]
            else:
                corrige = [self.cases, self.corrige, self.dernier_cases_sans_erreurs]
        else:
            corrige = self.corrige
        return {
            PARAM_LOGIMAGE_NOM: self.titre.texte,
            PARAM_LOGIMAGE_DIMENTIONS: (self.nb_colonnes, self.nb_lignes),
            PARAM_LOGIMAGE_SEQUENCES_LIGNES: self.sequences_lignes,
            PARAM_LOGIMAGE_SEQUENCES_COLONNES: self.sequences_colonnes,
            PARAM_LOGIMAGE_POSSIBLE: self.possible,
            PARAM_LOGIMAGE_FAISABLE: self.faisable,
            PARAM_LOGIMAGE_CORRIGE: corrige,
            PARAM_LOGIMAGE_NB_ETAPES_ODRI: self.nb_etapes_ordinateur,
            PARAM_LOGIMAGE_MODE: self.mode_logimage
        }

    def sauvegarde_logimage(self, dossier_sauvegarde=NOM_DOSSIER_SAUVEGARDE):
        titre = NOM_FICHIER_SAUVEGARDE if self.mode_logimage == MODE_LOGIMAGE_FAIT else self.titre.titre_sauvegarde
        with open(dossier_sauvegarde + titre, 'w') as sauvegarde_logimage:
            json.dump(self.return_dict_logimage(), sauvegarde_logimage)
        return True

    def imprime_png(self, suplement_nom: str, dossier=NOM_DOSSIER_IMPR):
        largeur = self.largeur_ecran + MARGE_COTE_IMPR * 2
        hauteur = self.hauteur_ecran + MARGE_COTE_IMPR * 2 + HAUTEUR_BANDEAU_TITRE_IMPR
        ecran_total = pygame.Surface((largeur, hauteur))
        ecran_total.fill(BLANC)
        self.x_ecran = MARGE_COTE_IMPR
        self.y_ecran = MARGE_COTE_IMPR + HAUTEUR_BANDEAU_TITRE_IMPR
        self.affiche(ecran_total)
        affiche_texte(self.titre.texte, int(largeur / 2), int(HAUTEUR_BANDEAU_TITRE_IMPR / 2) + MARGE_COTE_IMPR,
                      ecran_total, taille=TAILLE_TEXTE_TITRE_IMPR, couleur=COULEUR_TITRE,
                      x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
        if self.nb_etapes_ordinateur is not None:
            affiche_texte(TEXTE_NB_ETAPES_IMPR + str(self.nb_etapes_ordinateur), largeur - 1 - MARGE_COTE_IMPR,
                          MARGE_COTE_IMPR, ecran_total, x_0gauche_1centre_2droite=2)
        pygame.image.save(ecran_total,
                          f'{dossier}{self.titre.titre_sauvegarde[:-5]}{suplement_nom}{FORMAT_FICHIER_IMPR}')

    # -----------------------------------------------------------------

    def update_cases_ordonnees_colonnes(self):
        self.cases_ordonnees_colonnes = [[ligne[j] for ligne in self.cases] for j in range(self.nb_colonnes)]

    def update_all_sequences_lignes(self):
        for ligne in range(self.nb_lignes):
            self.update_1_sequence_ligne(ligne)

    def update_all_sequences_colonnes(self):
        for colonne in range(self.nb_colonnes):
            self.update_1_sequence_colonne(colonne)

    def update_1_sequence_ligne(self, ligne):
        if 0 <= ligne < self.nb_lignes:
            sequence_ligne = trouve_sequence_ligne(self.cases[ligne])
            if sequence_ligne == self.sequences_lignes:
                return False
            if len(self.sequences_lignes[ligne]) == len(sequence_ligne):
                self.sequences_lignes[ligne] = sequence_ligne
            else:
                self.sequences_lignes[ligne] = sequence_ligne
                nb_colonnes_sequences_ligne = max([len(sequence) for sequence in self.sequences_lignes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_colonnes_sequences_ligne += 1
                if not nb_colonnes_sequences_ligne == self.nb_colonnes_sequences_ligne:
                    self.nb_colonnes_sequences_ligne = nb_colonnes_sequences_ligne
                    self.recadre = True
            self.pre_affiche_1_sequense_ligne(ligne)
            return True
        return False

    def update_1_sequence_colonne(self, colonne):
        if 0 <= colonne < self.nb_colonnes:
            sequence_colonne = trouve_sequence_ligne([ligne[colonne] for ligne in self.cases])
            if sequence_colonne == self.sequences_colonnes:
                return False
            if len(self.sequences_colonnes[colonne]) == len(sequence_colonne):
                self.sequences_colonnes[colonne] = sequence_colonne
            else:
                self.sequences_colonnes[colonne] = sequence_colonne
                nb_lignes_sequences_colonne = max([len(sequence) for sequence in self.sequences_colonnes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_lignes_sequences_colonne += 1
                if not nb_lignes_sequences_colonne == self.nb_lignes_sequences_colonne:
                    self.nb_lignes_sequences_colonne = nb_lignes_sequences_colonne
                    self.recadre = True
            self.pre_affiche_1_sequense_colonne(colonne)
            return True
        return False

    def add_ligne(self, pos, valeur_case, nb):
        if 0 <= pos <= self.nb_lignes:
            for _ in range(nb):
                self.cases.insert(pos, [valeur_case for _ in range(self.nb_colonnes)])
                self.sequences_lignes.insert(pos, [])
                if self.update_sequences_auto:
                    self.update_1_sequence_ligne(pos)
            self.nb_lignes += nb
            if self.update_sequences_auto:
                self.update_all_sequences_colonnes()
            self.recadre = True
            return True
        return False

    def add_colonne(self, pos, valeur_case, nb):
        if 0 <= pos <= self.nb_colonnes:
            for _ in range(nb):
                for ligne in self.cases:
                    ligne.insert(pos, valeur_case)
                self.sequences_colonnes.insert(pos, [])
                if self.update_sequences_auto:
                    self.update_1_sequence_colonne(pos)
            self.nb_colonnes += nb
            if self.update_sequences_auto:
                self.update_all_sequences_colonnes()
            self.recadre = True
            return True
        return False

    def remove_ligne(self, pos, nb):
        n = 0
        pos_min = pos - nb // 2
        pos_max = pos_min + nb - 1
        for pos in range(pos_max, pos_min - 1, -1):
            if 0 <= pos < self.nb_lignes and self.nb_lignes - n > 1:
                del self.cases[pos]
                self.remove_sequence_ligne(pos)
                n += 1
        if n > 0:
            self.nb_lignes -= n
            if self.update_sequences_auto:
                self.update_all_sequences_colonnes()
            self.recadre = True
            return True
        return False

    def remove_colonne(self, pos, nb):
        n = 0
        pos_min = pos - nb // 2
        pos_max = pos_min + nb - 1
        for pos in range(pos_max, pos_min - 1, -1):
            if 0 <= pos < self.nb_colonnes and self.nb_colonnes - n > 1:
                for ligne in self.cases:
                    del ligne[pos]
                self.remove_sequence_colonne(pos)
                n += 1
        if n > 0:
            self.nb_colonnes -= n
            if self.update_sequences_auto:
                self.update_all_sequences_lignes()
            self.recadre = True
            return True
        return False

    def get_case_grille(self, ligne, colonne):
        if 0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes:
            return self.cases[ligne][colonne]
        return None

    def get_case_sequence_ligne(self, ligne, num):
        if 0 <= ligne < self.nb_lignes and 0 <= num < len(self.sequences_lignes[ligne]):
            return self.sequences_lignes[ligne][num]
        return None

    def get_case_sequence_colonne(self, colonne, num):
        if 0 <= colonne < self.nb_colonnes and 0 <= num < len(self.sequences_colonnes[colonne]):
            return self.sequences_colonnes[colonne][num]
        return None

    def set_case_grille_sans_update_erreurs(self, ligne, colonne, valeur):
        old_value = self.get_case_grille(ligne, colonne)
        if not (old_value is None or old_value == valeur):
            self.cases[ligne][colonne] = valeur
            if self.mode_logimage == MODE_LOGIMAGE_CORRECTION:
                self.cases_ordonnees_colonnes[colonne][ligne] = valeur
            if self.update_sequences_auto:
                self.update_1_sequence_ligne(ligne)
                self.update_1_sequence_colonne(colonne)
            self.pre_affiche_1_case_grille(ligne, colonne)
            # if self.mode_logimage == MODE_LOGIMAGE_FAIT:
            #     if (ligne, colonne) in self.dic_points_crayon:
            #         del self.dic_points_crayon[(ligne, colonne)]
            return True
        return False

    def set_case_grille(self, ligne, colonne, valeur):
        if self.set_case_grille_sans_update_erreurs(ligne, colonne, valeur):
            if self.trouve_erreurs:
                self.update_liste_erreur(ligne, colonne)
            return True
        return False

    def set_case_sequence_ligne(self, ligne, num, valeur):
        old_value = self.get_case_sequence_ligne(ligne, num)
        if not (old_value is None or old_value == valeur):
            self.sequences_lignes[ligne][num] = valeur
            self.pre_affiche_1_case_sequense_ligne(ligne, num)
            return True
        return False

    def set_case_sequence_colonne(self, colonne, num, valeur):
        old_value = self.get_case_sequence_colonne(colonne, num)
        if not (old_value is None or old_value == valeur):
            self.sequences_colonnes[colonne][num] = valeur
            self.pre_affiche_1_case_sequense_colonne(colonne, num)
            return True
        return False

    def add_case_sequence_ligne(self, ligne, valeur):
        if 0 <= ligne < self.nb_lignes:
            self.sequences_lignes[ligne].insert(0, valeur)
            max_ligne = len(self.sequences_lignes[ligne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_ligne += 1
            if max_ligne > self.nb_colonnes_sequences_ligne:
                self.nb_colonnes_sequences_ligne = max_ligne
                self.recadre = True
            self.pre_affiche_1_sequense_ligne(ligne)
            return True
        return False

    def add_case_sequence_colonne(self, colonne, valeur):
        if 0 <= colonne < self.nb_colonnes:
            self.sequences_colonnes[colonne].insert(0, valeur)
            max_colonne = len(self.sequences_colonnes[colonne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_colonne += 1
            if max_colonne > self.nb_lignes_sequences_colonne:
                self.nb_lignes_sequences_colonne = max_colonne
                self.recadre = True
            self.pre_affiche_1_sequense_colonne(colonne)
            return True
        return False

    def remove_sequence_ligne(self, ligne):
        if 0 <= ligne < self.nb_lignes:
            max_ligne = len(self.sequences_lignes[ligne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_ligne += 1
            del self.sequences_lignes[ligne]
            if max_ligne == self.nb_colonnes_sequences_ligne:
                nb_colonnes_sequences_ligne = max([len(sequence) for sequence in self.sequences_lignes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_colonnes_sequences_ligne += 1
                if not nb_colonnes_sequences_ligne == self.nb_colonnes_sequences_ligne:
                    self.nb_colonnes_sequences_ligne = nb_colonnes_sequences_ligne
                    self.recadre = True
            return True
        return False

    def remove_sequence_colonne(self, colonne):
        if 0 <= colonne < self.nb_colonnes:
            max_colonne = len(self.sequences_colonnes[colonne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_colonne += 1
            del self.sequences_colonnes[colonne]
            if max_colonne == self.nb_lignes_sequences_colonne:
                nb_lignes_sequences_colonne = max([len(sequence) for sequence in self.sequences_colonnes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_lignes_sequences_colonne += 1
                if not nb_lignes_sequences_colonne == self.nb_lignes_sequences_colonne:
                    self.nb_lignes_sequences_colonne = nb_lignes_sequences_colonne
                    self.recadre = True
            return True
        return False

    def remove_case_sequence_ligne(self, ligne, num):
        if 0 <= ligne < self.nb_lignes and 0 <= num < len(self.sequences_lignes[ligne]):
            max_ligne = len(self.sequences_lignes[ligne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_ligne += 1
            del self.sequences_lignes[ligne][num]
            if max_ligne == self.nb_colonnes_sequences_ligne:
                nb_colonnes_sequences_ligne = max([len(sequence) for sequence in self.sequences_lignes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_colonnes_sequences_ligne += 1
                if not nb_colonnes_sequences_ligne == self.nb_colonnes_sequences_ligne:
                    self.nb_colonnes_sequences_ligne = nb_colonnes_sequences_ligne
                    self.recadre = True
            self.pre_affiche_1_sequense_ligne(ligne)
            return True
        return False

    def remove_case_sequence_colonne(self, colonne, num):
        if 0 <= colonne < self.nb_colonnes and 0 <= num < len(self.sequences_colonnes[colonne]):
            max_colonne = len(self.sequences_colonnes[colonne])
            if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                max_colonne += 1
            del self.sequences_colonnes[colonne][num]
            if max_colonne == self.nb_lignes_sequences_colonne:
                nb_lignes_sequences_colonne = max([len(sequence) for sequence in self.sequences_colonnes])
                if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    nb_lignes_sequences_colonne += 1
                if not nb_lignes_sequences_colonne == self.nb_lignes_sequences_colonne:
                    self.nb_lignes_sequences_colonne = nb_lignes_sequences_colonne
                    self.recadre = True
            self.pre_affiche_1_sequense_colonne(colonne)
            return True
        return False

    def remet_liste_erreur_a_zero(self):
        self.liste_erreurs = []
        self.dernier_cases_sans_erreurs = copy.deepcopy(self.cases)

    def mettre_toutes_cases_valeur(self, valeur):
        for ligne in range(self.nb_lignes):
            for colonne in range(self.nb_colonnes):
                self.set_case_grille_sans_update_erreurs(ligne, colonne, valeur)
        if valeur == CASE_INCONNUE:
            self.remet_liste_erreur_a_zero()
        else:
            self.update_liste_erreur()

    def reprendre_dernier_cases_sans_erreurs(self):
        if self.trouve_erreurs:
            for i, ligne in enumerate(self.dernier_cases_sans_erreurs):
                for j, case in enumerate(ligne):
                    self.set_case_grille_sans_update_erreurs(i, j, case)
        self.liste_erreurs = []

    def update_liste_erreur(self, ligne=None, colonne=None):
        if self.trouve_erreurs:
            if ligne is None or colonne is None:
                self.liste_erreurs = []
                for i, ligne in enumerate(self.corrige):
                    for j, case in enumerate(ligne):
                        case_reele = self.get_case_grille(i, j)
                        if not case_reele == CASE_INCONNUE and not case == case_reele:
                            self.liste_erreurs.append((i, j))
            else:
                case = self.get_case_grille(ligne, colonne)
                if not (case == CASE_INCONNUE or case == self.corrige[ligne][colonne]):
                    if not (ligne, colonne) in self.liste_erreurs:
                        self.liste_erreurs.append((ligne, colonne))
                else:
                    if (ligne, colonne) in self.liste_erreurs:
                        self.liste_erreurs.remove((ligne, colonne))
            if len(self.liste_erreurs) == 0:
                self.dernier_cases_sans_erreurs = copy.deepcopy(self.cases)

    def corrige_erreurs(self):
        if self.trouve_erreurs:
            for ligne, colonne in self.liste_erreurs[:]:
                self.set_case_grille_sans_update_erreurs(ligne, colonne, self.corrige[ligne][colonne])
        self.remet_liste_erreur_a_zero()

    def enleve_erreurs(self):
        if self.trouve_erreurs:
            liste_erreurs = self.liste_erreurs[:]
            for ligne, colonne in liste_erreurs:
                self.set_case_grille_sans_update_erreurs(ligne, colonne, CASE_INCONNUE)
        self.remet_liste_erreur_a_zero()

    def tout_corriger(self):
        for i, ligne in enumerate(self.corrige):
            for j, case in enumerate(ligne):
                self.set_case_grille_sans_update_erreurs(i, j, case)
        self.remet_liste_erreur_a_zero()
        self.liste_erreurs = []
        self.dernier_cases_sans_erreurs = copy.deepcopy(self.cases)

    def efface_tout_crayon(self):
        if self.mode_logimage == MODE_LOGIMAGE_FAIT:
            self.dic_points_crayon = {}

    def efface_cases_rayees(self):
        self.liste_cases_rayees = []

    # -----------------------------------------------------------------

    def recadre_ecran(self):
        nb_lignes_total = self.nb_lignes + self.nb_lignes_sequences_colonne
        nb_colonnes_total = self.nb_colonnes + self.nb_colonnes_sequences_ligne
        cote_case = self.cote_case
        if not self.cote_case_fixe:
            cote_case = min((HAUTEUR - MARGE_GRILLE_BORD_HAUT - MARGE_GRILLE_BORD_BAS) // nb_lignes_total,
                            (LARGEUR - MARGE_GRILLE_BORD_DROITE - MARGE_GRILLE_BORD_GAUCHE) // nb_colonnes_total)

        self.cote_case = cote_case
        self.taille_quadrillage = max(1, int(COEF_TAILLE_QUADRILLAGE * self.cote_case))
        self.ecart_quadrillage_principal = max(1, int(COEF_TAILLE_QUADRILLAGE_PRINCIPALE_ECART * self.cote_case))
        self.taille_texte = int(COEF_TAILLE_POLICE * self.cote_case)

        if self.mode_logimage == MODE_LOGIMAGE_FAIT:
            self.taille_point_crayon = max(1, int(COEF_TAILLE_POINTS_CRAYON * self.cote_case))

        decalage = self.taille_quadrillage + self.ecart_quadrillage_principal
        decalage1 = decalage + self.taille_quadrillage // 2
        decalage2 = decalage + self.ecart_quadrillage_principal

        self.x_origine_sur_ecran = self.cote_case * self.nb_colonnes_sequences_ligne + decalage1
        self.y_origine_sur_ecran = self.cote_case * self.nb_lignes_sequences_colonne + decalage1

        self.largeur_ecran = self.cote_case * nb_colonnes_total + decalage2
        self.hauteur_ecran = self.cote_case * nb_lignes_total + decalage2
        self.x_ecran = MARGE_GRILLE_BORD_DROITE + (LARGEUR - MARGE_GRILLE_BORD_DROITE - MARGE_GRILLE_BORD_GAUCHE
                                                   - self.largeur_ecran) // 2
        self.y_ecran = MARGE_GRILLE_BORD_HAUT + (HAUTEUR - MARGE_GRILLE_BORD_HAUT - MARGE_GRILLE_BORD_BAS
                                                 - self.hauteur_ecran) // 2
        self.ecran = pygame.Surface((self.largeur_ecran, self.hauteur_ecran))

        if self.nb_lignes_sequences_colonne > 0 and self.nb_colonnes_sequences_ligne > 0:
            pygame.draw.rect(self.ecran, BLANC, (0, 0, self.cote_case * self.nb_colonnes_sequences_ligne,
                                                 self.cote_case * self.nb_lignes_sequences_colonne))

    def test_souris_sur_ecran(self, x_souris, y_souris):
        if self.x_ecran <= x_souris <= self.x_ecran + self.largeur_ecran and \
                self.y_ecran <= y_souris <= self.y_ecran + self.hauteur_ecran:
            return True
        return False

    def get_ligne_colonne_souris(self, x_souris, y_souris):
        return (y_souris - self.y_ecran - self.y_origine_sur_ecran) // self.cote_case, \
               (x_souris - self.x_ecran - self.x_origine_sur_ecran) // self.cote_case

    def get_ligne_colonne_intersection_souris(self, x_souris, y_souris):
        return (y_souris - self.y_ecran - self.y_origine_sur_ecran + self.cote_case // 2) // self.cote_case, \
               (x_souris - self.x_ecran - self.x_origine_sur_ecran + self.cote_case // 2) // self.cote_case

    def gere_clic_up(self, x_souris, y_souris, sens=1):
        self.derniere_case_modifiee = None
        action_logimage_ligne_possible_ = get_action_logimage_ligne_possible()
        action_logimage_colonne_possible_ = get_action_logimage_colonne_possible()

        if action_logimage_ligne_possible_ is not None or action_logimage_colonne_possible_ is not None or \
                get_action_colorier_case():
            if sens == -1:
                set_action_logimage_ligne_possible(None)
                set_action_logimage_colonne_possible(None)
                set_action_colorier_case(False)
            else:
                if self.x_ecran <= x_souris <= self.x_ecran + self.largeur_ecran and \
                        self.y_ecran <= y_souris <= self.y_ecran + self.hauteur_ecran:
                    i, j = self.get_ligne_colonne_souris(x_souris, y_souris)
                    if 0 <= i < self.nb_lignes and 0 <= j < self.nb_colonnes:
                        self.gere_clic_up_grille(i, j, sens)

                if action_logimage_ligne_possible_ is not None or action_logimage_colonne_possible_ is not None:
                    i, j = self.get_ligne_colonne_intersection_souris(x_souris, y_souris)
                    if 0 <= i <= self.nb_lignes and 0 <= j <= self.nb_colonnes:
                        self.gere_clic_up_intersection(i, j)

    def gere_clic_down(self, x_souris, y_souris, sens=1):
        action_logimage_ligne_possible_ = get_action_logimage_ligne_possible()
        action_logimage_colonne_possible_ = get_action_logimage_colonne_possible()

        if action_logimage_ligne_possible_ is None and action_logimage_colonne_possible_ is None and \
                not get_action_colorier_case():
            if self.test_souris_sur_ecran(x_souris, y_souris):
                i, j = self.get_ligne_colonne_souris(x_souris, y_souris)
                if not (i, j) == self.derniere_case_modifiee:
                    if get_action_aide() and (not type(self.aide) == tuple or not (self.aide == (True, i) or
                                                                                   self.aide == (False, j))):
                        self.stop_aide()
                    self.derniere_case_modifiee = (i, j)
                    if 0 <= i < self.nb_lignes and 0 <= j < self.nb_colonnes:
                        self.gere_clic_down_grille(i, j, sens)
                    else:
                        self.gere_clic_down_hors_grille(i, j, sens)

    def gere_clic_up_grille(self, ligne, colonne, sens):
        action_logimage_ligne_possible_ = get_action_logimage_ligne_possible()
        action_logimage_colonne_possible_ = get_action_logimage_colonne_possible()
        action_colorier_case_ = get_action_colorier_case()

        if action_logimage_ligne_possible_ is None and action_logimage_colonne_possible_ is None:
            if self.mode_logimage == MODE_LOGIMAGE_CREER:
                self.set_case_grille(ligne, colonne, not self.get_case_grille(ligne, colonne))
            elif self.mode_logimage == MODE_LOGIMAGE_FAIT:
                if action_colorier_case_:
                    self.set_case_grille(ligne, colonne, self.corrige[ligne][colonne])
                    set_action_colorier_case(False)
                else:
                    index = LISTE_ORDRE_VALEUR_CASE_CLIC.index(self.get_case_grille(ligne, colonne)) - 1
                    if sens == 1:
                        index -= len(LISTE_ORDRE_VALEUR_CASE_CLIC) - 2
                    self.set_case_grille(ligne, colonne, LISTE_ORDRE_VALEUR_CASE_CLIC[index])

        if action_colorier_case_ and 0 <= ligne <= self.nb_lignes and 0 <= colonne <= self.nb_colonnes:
            self.set_case_grille(ligne, colonne, self.corrige[ligne][colonne])
            set_action_colorier_case(False)

        if action_logimage_ligne_possible_ is not None and 0 <= ligne <= self.nb_lignes:
            if action_logimage_ligne_possible_ == ACTION_SUPR_1:
                if self.remove_ligne(ligne, 1):
                    set_action_logimage_ligne_possible(None)
            elif action_logimage_ligne_possible_ == ACTION_SUPR_GROUPE:
                if self.remove_ligne(ligne, 5):
                    set_action_logimage_ligne_possible(None)

        if action_logimage_colonne_possible_ is not None and 0 <= colonne <= self.nb_colonnes:
            if action_logimage_colonne_possible_ == ACTION_SUPR_1:
                if self.remove_colonne(colonne, 1):
                    set_action_logimage_colonne_possible(None)
            elif action_logimage_colonne_possible_ == ACTION_SUPR_GROUPE:
                if self.remove_colonne(colonne, 5):
                    set_action_logimage_colonne_possible(None)

    def gere_clic_down_grille(self, ligne, colonne, sens):
        if self.mode_logimage == MODE_LOGIMAGE_CREER:
            self.set_case_grille(ligne, colonne, not self.get_case_grille(ligne, colonne))
        elif self.mode_logimage == MODE_LOGIMAGE_FAIT:
            if get_action_logimage_mode_crayon():
                # if self.get_case_grille(ligne, colonne) == CASE_INCONNUE:
                if (ligne, colonne) in self.dic_points_crayon:
                    if sens == 1:
                        if self.dic_points_crayon[(ligne, colonne)] == 1:
                            self.dic_points_crayon[(ligne, colonne)] = 2
                        else:
                            del self.dic_points_crayon[(ligne, colonne)]
                    else:
                        del self.dic_points_crayon[(ligne, colonne)]
                else:
                    if sens == 1:
                        self.dic_points_crayon[(ligne, colonne)] = 1
            else:
                index = LISTE_ORDRE_VALEUR_CASE_CLIC.index(self.get_case_grille(ligne, colonne)) - 1
                if sens == 1:
                    index -= len(LISTE_ORDRE_VALEUR_CASE_CLIC) - 2
                self.set_case_grille(ligne, colonne, LISTE_ORDRE_VALEUR_CASE_CLIC[index])

    def gere_clic_down_hors_grille(self, i, j, sens):
        if self.mode_logimage == MODE_LOGIMAGE_RENTRE:
            if self.nb_lignes > i >= 0 > j >= - self.nb_colonnes_sequences_ligne:
                num = j + len(self.sequences_lignes[i])
                self.gere_clic_down_sequences_lignes_mode_rentre(i, num, sens)
            elif self.nb_colonnes > j >= 0 > i >= - self.nb_lignes_sequences_colonne:
                num = i + len(self.sequences_colonnes[j])
                self.gere_clic_down_sequences_colonnes_mode_rentre(j, num, sens)

        if self.mode_logimage == MODE_LOGIMAGE_FAIT:
            if self.nb_lignes > i >= 0 > j >= - len(self.sequences_lignes[i]) or \
                    self.nb_colonnes > j >= 0 > i >= - len(self.sequences_colonnes[j]):
                if (i, j) in self.liste_cases_rayees:
                    self.liste_cases_rayees.remove((i, j))
                else:
                    self.liste_cases_rayees.append((i, j))

    def gere_clic_down_sequences_lignes_mode_rentre(self, ligne, num, sens):
        if sens == 1:
            if num >= 0:
                self.set_case_sequence_ligne(ligne, num, self.get_case_sequence_ligne(ligne, num) + 1)
            else:
                self.add_case_sequence_ligne(ligne, 1)
        else:
            if num >= 0:
                case = self.get_case_sequence_ligne(ligne, num)
                if case > 1:
                    self.set_case_sequence_ligne(ligne, num, case - 1)
                else:
                    self.remove_case_sequence_ligne(ligne, num)

    def gere_clic_down_sequences_colonnes_mode_rentre(self, colonne, num, sens):
        if sens == 1:
            if num >= 0:
                self.set_case_sequence_colonne(colonne, num, self.get_case_sequence_colonne(colonne, num) + 1)
            else:
                self.add_case_sequence_colonne(colonne, 1)
        else:
            if num >= 0:
                case = self.get_case_sequence_colonne(colonne, num)
                if case > 1:
                    self.set_case_sequence_colonne(colonne, num, case - 1)
                else:
                    self.remove_case_sequence_colonne(colonne, num)

    def gere_clic_up_intersection(self, ligne, colonne):
        action_logimage_ligne_possible_ = get_action_logimage_ligne_possible()
        action_logimage_colonne_possible_ = get_action_logimage_colonne_possible()

        if action_logimage_ligne_possible_ is not None and 0 <= ligne <= self.nb_lignes:
            if action_logimage_ligne_possible_ == ACTION_ADD_1:
                valeur = False if self.mode_logimage == MODE_LOGIMAGE_CREER else CASE_INCONNUE
                if self.add_ligne(ligne, valeur, 1):
                    set_action_logimage_ligne_possible(None)
            elif action_logimage_ligne_possible_ == ACTION_ADD_GROUPE:
                valeur = False if self.mode_logimage == MODE_LOGIMAGE_CREER else CASE_INCONNUE
                if self.add_ligne(ligne, valeur, 5):
                    set_action_logimage_ligne_possible(None)

        if action_logimage_colonne_possible_ is not None and 0 <= colonne <= self.nb_colonnes:
            if action_logimage_colonne_possible_ == ACTION_ADD_1:
                valeur = False if self.mode_logimage == MODE_LOGIMAGE_CREER else CASE_INCONNUE
                if self.add_colonne(colonne, valeur, 1):
                    set_action_logimage_colonne_possible(None)
            elif action_logimage_colonne_possible_ == ACTION_ADD_GROUPE:
                valeur = False if self.mode_logimage == MODE_LOGIMAGE_CREER else CASE_INCONNUE
                if self.add_colonne(colonne, valeur, 5):
                    set_action_logimage_colonne_possible(None)

    # -----------------------------------------------------------------

    def pre_affiche_tout(self):
        for ligne in range(self.nb_lignes):
            self.pre_affiche_1_sequense_ligne(ligne)
            for colonne in range(self.nb_colonnes):
                self.pre_affiche_1_case_grille(ligne, colonne)
                if ligne == 0:
                    self.pre_affiche_1_sequense_colonne(colonne)

    def pre_affiche_1_sequense_ligne(self, ligne):
        for num in range(self.nb_colonnes_sequences_ligne):
            self.pre_affiche_1_case_sequense_ligne(ligne, num)

    def pre_affiche_1_sequense_colonne(self, colonne):
        for num in range(self.nb_lignes_sequences_colonne):
            self.pre_affiche_1_case_sequense_colonne(colonne, num)

    def pre_affiche_1_case_sequense_ligne(self, ligne, num):
        j = num - len(self.sequences_lignes[ligne])
        if j >= 0:
            j -= self.nb_colonnes_sequences_ligne
        self.pre_affiche_1_case(ligne, j, COULEUR_CASE_VIDE, self.get_case_sequence_ligne(ligne, num))

    def pre_affiche_1_case_sequense_colonne(self, colonne, num):
        i = num - len(self.sequences_colonnes[colonne])
        if i >= 0:
            i -= self.nb_lignes_sequences_colonne
        self.pre_affiche_1_case(i, colonne, COULEUR_CASE_VIDE, self.get_case_sequence_colonne(colonne, num))

    def pre_affiche_1_case_grille(self, ligne, colonne):
        case = self.get_case_grille(ligne, colonne)
        if case is not None:
            couleur = COULEUR_CASE_VIDE
            if case == CASE_INCONNUE:
                if not self.mode_logimage == MODE_LOGIMAGE_RENTRE:
                    if self.mode_logimage == MODE_LOGIMAGE_IMPR or self.mode_logimage == MODE_LOGIMAGE_CORRECTION:
                        couleur = COULEUR_CASE_INCONNUE_ROUGE
                    else:
                        couleur = COULEUR_CASE_INCONNUE_BLEU
            elif case:
                couleur = COULEUR_CASE_PLEINE
            self.pre_affiche_1_case(ligne, colonne, couleur)

    def pre_affiche_1_case(self, i: int, j: int, couleur: tuple, nb: int = None):
        texte = None if nb is None else str(nb)
        self.cases_affiche_en_attente[(i, j)] = couleur, texte

    def get_pos_case(self, i: int, j: int):
        return j * self.cote_case + self.x_origine_sur_ecran - self.taille_quadrillage // 2, \
               i * self.cote_case + self.y_origine_sur_ecran - self.taille_quadrillage // 2

    def affiche_case(self, i: int, j: int, couleur: tuple, texte, ecran: pygame.Surface = None):
        if ecran is None:
            ecran = self.ecran
        x, y = self.get_pos_case(i, j)
        largeur = self.cote_case - self.taille_quadrillage
        hauteur = self.cote_case - self.taille_quadrillage

        if i == 0 or i == - self.nb_lignes_sequences_colonne or (i > 0 and i % QUADRILLAGE_PRINCIPALE == 0):
            y += self.ecart_quadrillage_principal
            hauteur -= self.ecart_quadrillage_principal
        if i == -1 or i == self.nb_lignes - 1 or \
                (i > 0 and i % QUADRILLAGE_PRINCIPALE == QUADRILLAGE_PRINCIPALE - 1):
            hauteur -= self.ecart_quadrillage_principal

        if j == 0 or j == - self.nb_colonnes_sequences_ligne or (j > 0 and j % QUADRILLAGE_PRINCIPALE == 0):
            x += self.ecart_quadrillage_principal
            largeur -= self.ecart_quadrillage_principal
        if j == -1 or j == self.nb_colonnes - 1 or \
                (j > 0 and j % QUADRILLAGE_PRINCIPALE == QUADRILLAGE_PRINCIPALE - 1):
            largeur -= self.ecart_quadrillage_principal

        pygame.draw.rect(ecran, couleur, (x, y, largeur, hauteur))
        if texte is not None:
            affiche_texte(texte, x + largeur // 2, y + hauteur // 2 + 1, ecran, taille=self.taille_texte,
                          couleur=COULEUR_NB, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)

    def update_affichage_recadre_si_necessaire(self):
        if self.recadre:
            self.cases_affiche_en_attente = {}
            self.recadre_ecran()
            self.pre_affiche_tout()
            self.recadre = False

    def update_affichage_thread(self):
        self.update_affichage_recadre_si_necessaire()
        if not self.updating_thread and len(self.cases_affiche_en_attente) > 0:
            thread_affichage = Thread(target=self.update_affichage)
            self.updating_thread = True
            thread_affichage.start()

    def update_affichage(self):
        self.update_affichage_recadre_si_necessaire()
        while len(self.cases_affiche_en_attente) > 0:
            (i, j), (couleur, texte) = self.cases_affiche_en_attente.popitem()
            self.affiche_case(i, j, couleur, texte)
        self.updating_thread = False

    def affiche_ligne_colonne_actions(self, screen: pygame.Surface, ligne_ou_pas, n):
        x, y = self.get_pos_case(n, n)
        d = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
        cote = self.cote_case - self.taille_quadrillage
        if ligne_ou_pas:
            affiche_rect_transparent((self.x_ecran + d, self.y_ecran + y, self.largeur_ecran - 2 * d, cote),
                                     screen, COULEUR_POINTEUR[0], COULEUR_POINTEUR[1])
        else:
            affiche_rect_transparent((self.x_ecran + x, self.y_ecran + d, cote, self.hauteur_ecran - 2 * d),
                                     screen, COULEUR_POINTEUR[0], COULEUR_POINTEUR[1])

    def affiche_actions(self, screen: pygame.Surface, x_souirs: int, y_souris: int):
        if self.mode_logimage == MODE_LOGIMAGE_CORRECTION:
            if self.ligne_ou_colonne_en_cours is not None:
                ligne_ou_pas, n = self.ligne_ou_colonne_en_cours
                self.affiche_ligne_colonne_actions(screen, ligne_ou_pas, n)
        else:
            action_logimage_ligne_possible_ = get_action_logimage_ligne_possible()
            action_logimage_colonne_possible_ = get_action_logimage_colonne_possible()
            action_test_creation_ = get_action_test_creation()
            action_colorier_case_ = get_action_colorier_case()
            action_corriger_logimage_ = get_action_corriger_logimage()
            action_pointeur_ = get_action_pointeur()
            action_aide_ = get_action_aide()

            if action_logimage_ligne_possible_ is not None:
                if action_logimage_ligne_possible_ == ACTION_ADD_1 or \
                        action_logimage_ligne_possible_ == ACTION_ADD_GROUPE:
                    ligne_inter, colonne_inter = self.get_ligne_colonne_intersection_souris(x_souirs, y_souris)
                    if 0 <= ligne_inter <= self.nb_lignes and 0 <= colonne_inter <= self.nb_colonnes:
                        ecart_y = int(COEF_ECART_TAILLE_TRAI_AJOUT * self.cote_case)
                        x, y = self.get_pos_case(ligne_inter, 0)
                        dx = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                        affiche_rect_transparent((self.x_ecran + dx, self.y_ecran + y - ecart_y,
                                                  self.largeur_ecran - 2 * dx, ecart_y * 2),
                                                 screen, COULEUR_AJOUT[0], COULEUR_AJOUT[1])
                else:
                    ligne, colonne = self.get_ligne_colonne_souris(x_souirs, y_souris)
                    if 0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes:
                        if action_logimage_ligne_possible_ == ACTION_SUPR_1:
                            x, y = self.get_pos_case(ligne, 0)
                            dx = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                            affiche_rect_transparent((self.x_ecran + dx, self.y_ecran + y, self.largeur_ecran - 2 * dx,
                                                      self.cote_case - self.taille_quadrillage),
                                                     screen, COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])
                        else:
                            x, y_min = self.get_pos_case(max(ligne - QUADRILLAGE_PRINCIPALE // 2, 0), 0)
                            x, y_max = \
                                self.get_pos_case(min(ligne - QUADRILLAGE_PRINCIPALE // 2 + QUADRILLAGE_PRINCIPALE,
                                                      self.nb_lignes), 0)
                            dx = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                            affiche_rect_transparent((self.x_ecran + dx, self.y_ecran + y_min,
                                                      self.largeur_ecran - 2 * dx,
                                                      y_max - y_min - self.taille_quadrillage),
                                                     screen, COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])

            if action_logimage_colonne_possible_ is not None:
                if action_logimage_colonne_possible_ == ACTION_ADD_1 or \
                        action_logimage_colonne_possible_ == ACTION_ADD_GROUPE:
                    ligne_inter, colonne_inter = self.get_ligne_colonne_intersection_souris(x_souirs, y_souris)
                    if 0 <= ligne_inter <= self.nb_lignes and 0 <= colonne_inter <= self.nb_colonnes:
                        ecart_x = int(COEF_ECART_TAILLE_TRAI_AJOUT * self.cote_case)
                        x, y = self.get_pos_case(0, colonne_inter)
                        dy = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                        affiche_rect_transparent((self.x_ecran + x - ecart_x, self.y_ecran + dy, ecart_x * 2,
                                                  self.hauteur_ecran - 2 * dy),
                                                 screen, COULEUR_AJOUT[0], COULEUR_AJOUT[1])
                else:
                    ligne, colonne = self.get_ligne_colonne_souris(x_souirs, y_souris)
                    if 0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes:
                        if action_logimage_colonne_possible_ == ACTION_SUPR_1:
                            x, y = self.get_pos_case(0, colonne)
                            dy = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                            affiche_rect_transparent((self.x_ecran + x, self.y_ecran + dy,
                                                      self.cote_case - self.taille_quadrillage,
                                                      self.hauteur_ecran - 2 * dy),
                                                     screen, COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])
                        else:
                            x_min, y = self.get_pos_case(0, max(colonne - QUADRILLAGE_PRINCIPALE // 2, 0))
                            x_max, y = self.get_pos_case(0, min(colonne - QUADRILLAGE_PRINCIPALE // 2 +
                                                                QUADRILLAGE_PRINCIPALE, self.nb_colonnes))
                            dy = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                            affiche_rect_transparent((self.x_ecran + x_min, self.y_ecran + dy,
                                                      x_max - x_min - self.taille_quadrillage,
                                                      self.hauteur_ecran - 2 * dy),
                                                     screen, COULEUR_SUPPRESSION[0], COULEUR_SUPPRESSION[1])

            if action_test_creation_:
                if self.possible:
                    if self.faisable:
                        affiche_texte(TEXTE_FAISABLE, self.x_ecran + self.largeur_ecran // 2,
                                      self.y_ecran + self.hauteur_ecran // 2, screen,
                                      taille=TAILLE_POLICE_GROSSE_CENTREE, couleur=COULEUR_SUCCES,
                                      x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                    else:
                        if self.mode_logimage == MODE_LOGIMAGE_CREER:
                            for i, ligne in enumerate(self.corrige):
                                for j, case in enumerate(ligne):
                                    if case == CASE_INCONNUE:
                                        x, y = self.get_pos_case(i, j)
                                        cote_case = self.cote_case - self.taille_quadrillage
                                        affiche_rect_transparent((self.x_ecran + x, self.y_ecran + y, cote_case,
                                                                  cote_case), screen, COULEUR_CASES_ERREUR[0],
                                                                 COULEUR_CASES_ERREUR[1])
                        else:
                            affiche_texte(TEXTE_INFAISABLE, self.x_ecran + self.largeur_ecran // 2,
                                          self.y_ecran + self.hauteur_ecran // 2, screen,
                                          taille=TAILLE_POLICE_GROSSE_CENTREE,
                                          couleur=COULEUR_SUCCES, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                else:
                    affiche_texte(TEXTE_IMPOSSIBLE, self.x_ecran + self.largeur_ecran // 2,
                                  self.y_ecran + self.hauteur_ecran // 2, screen, taille=TAILLE_POLICE_GROSSE_CENTREE,
                                  couleur=COULEUR_ECHEC, x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)

            if action_colorier_case_:
                ligne, colonne = self.get_ligne_colonne_souris(x_souirs, y_souris)
                if 0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes:
                    x, y = self.get_pos_case(ligne, colonne)
                    affiche_rect_transparent((self.x_ecran + x, self.y_ecran + y,
                                              self.cote_case - self.taille_quadrillage,
                                              self.cote_case - self.taille_quadrillage),
                                             screen, COULEUR_AJOUT[0], COULEUR_AJOUT[1])

            if action_corriger_logimage_:
                for i, j in self.liste_erreurs:
                    x, y = self.get_pos_case(i, j)
                    cote_case = self.cote_case - self.taille_quadrillage
                    affiche_rect_transparent((self.x_ecran + x, self.y_ecran + y, cote_case, cote_case), screen,
                                             COULEUR_CASES_ERREUR[0], COULEUR_CASES_ERREUR[1])
                if len(self.liste_erreurs) == 0 and not test_reste_cases_inconnues(self.cases):
                    affiche_texte(TEXTE_BRAVO, self.x_ecran + self.largeur_ecran // 2 + self.x_origine_sur_ecran // 2,
                                  self.y_ecran + self.hauteur_ecran // 2 + self.y_origine_sur_ecran // 2, screen,
                                  taille=TAILLE_TEXTE_ACTION_CENTRE, couleur=COULEUR_SUCCES,
                                  x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)

            if self.mode_logimage == MODE_LOGIMAGE_FAIT:
                for pos, nb in self.dic_points_crayon.items():
                    x, y = self.get_pos_case(pos[0], pos[1])
                    demi_cote_case = (self.cote_case - self.taille_quadrillage) // 2
                    case = self.get_case_grille(pos[0], pos[1])
                    if case == CASE_INCONNUE:
                        couleur_points_crayon = COULEUR_POINTS_CRAYON_CASE_INCONNUE
                    elif case:
                        couleur_points_crayon = COULEUR_POINTS_CRAYON_CASE_PLEINE
                    else:
                        couleur_points_crayon = COULEUR_POINTS_CRAYON_CASE_VIDE
                    if nb == 1:
                        pygame.draw.circle(screen, couleur_points_crayon, (self.x_ecran + x + demi_cote_case,
                                                                           self.y_ecran + y + demi_cote_case),
                                           self.taille_point_crayon)
                    else:
                        decalage = int(self.cote_case * 0.15)
                        for i in [-1, 1]:
                            pygame.draw.circle(screen, couleur_points_crayon,
                                               (self.x_ecran + x + demi_cote_case + i * decalage,
                                                self.y_ecran + y + demi_cote_case),
                                               self.taille_point_crayon)

                for i, j in self.liste_cases_rayees:
                    x, y = self.get_pos_case(i, j)
                    affiche_rect_transparent((self.x_ecran + x, self.y_ecran + y,
                                              self.cote_case - self.taille_quadrillage,
                                              self.cote_case - self.taille_quadrillage),
                                             screen, NOIR, 150)

            if action_pointeur_:
                if self.test_souris_sur_ecran(x_souirs, y_souris):
                    ligne, colonne = self.get_ligne_colonne_souris(x_souirs, y_souris)
                    if ligne >= 0 or colonne >= 0:
                        x, y = self.get_pos_case(ligne, colonne)
                        d = self.taille_quadrillage + self.ecart_quadrillage_principal * 2
                        cote = self.cote_case - self.taille_quadrillage
                        if 0 <= ligne < self.nb_lignes:
                            affiche_rect_transparent((self.x_ecran + d, self.y_ecran + y, self.largeur_ecran - 2 * d,
                                                      cote), screen, COULEUR_POINTEUR[0], COULEUR_POINTEUR[1])
                        if 0 <= colonne < self.nb_colonnes:
                            affiche_rect_transparent((self.x_ecran + x, self.y_ecran + d, cote,
                                                      self.hauteur_ecran - 2 * d), screen, COULEUR_POINTEUR[0],
                                                     COULEUR_POINTEUR[1])

            if action_aide_:
                if self.aide is None:
                    affiche_texte(TEXTE_PATIENTER_AIDE,
                                  self.x_ecran + self.largeur_ecran // 2 + self.x_origine_sur_ecran // 2,
                                  self.y_ecran + self.hauteur_ecran // 2 + self.y_origine_sur_ecran // 2, screen,
                                  taille=int(TAILLE_TEXTE_ACTION_CENTRE * 0.9), couleur=COULEUR_SUCCES,
                                  x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)
                elif type(self.aide) == tuple:
                    ligne_ou_pas, n = self.aide
                    self.affiche_ligne_colonne_actions(screen, ligne_ou_pas, n)
                else:
                    affiche_texte(TEXTE_VOIR_ERREUR_AIDE,
                                  self.x_ecran + self.largeur_ecran // 2 + self.x_origine_sur_ecran // 2,
                                  self.y_ecran + self.hauteur_ecran // 2 + self.y_origine_sur_ecran // 2, screen,
                                  taille=int(TAILLE_TEXTE_ACTION_CENTRE * 0.9), couleur=COULEUR_ECHEC,
                                  x_0gauche_1centre_2droite=1, y_0haut_1centre_2bas=1)

    def affiche(self, screen: pygame.Surface):
        self.update_affichage_thread()
        screen.blit(self.ecran, (self.x_ecran, self.y_ecran))
