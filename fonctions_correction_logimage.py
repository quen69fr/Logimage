# coding: utf-8

from outils import *
import time
import random
import copy


def trouve_sequence_ligne(ligne):
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

    return sequence_ligne


plus_lent_moins_de_memoire = True
possibilitees_pour_x_sur_n = {}


def set_plus_lent_moins_de_memoire(value):
    global plus_lent_moins_de_memoire
    plus_lent_moins_de_memoire = value


def clear_possibilitees_pour_x_sur_n():
    global possibilitees_pour_x_sur_n
    possibilitees_pour_x_sur_n.clear()


LISTE_TRUE = [True]
LISTE_FALSE = [False]

grille_degres = []


def init_grille_derges(derges_max=DEGRES_X_MAX_METHODE_2_CORRECTION_LOGIMAGE[0],
                       x_max=DEGRES_X_MAX_METHODE_2_CORRECTION_LOGIMAGE[1]):
    global grille_degres
    grille_degres = [[1] + [0 for _ in range(x_max - 1)]]
    for dergres in range(1, derges_max + 1):
        liste_degres = []
        valeur = 0
        for sup in grille_degres[dergres - 1]:
            valeur += sup
            liste_degres.append(valeur)
        grille_degres.append(liste_degres)


def test_reste_cases_inconnues(cases):
    for ligne in cases:
        if CASE_INCONNUE in ligne:
            return True
    return False


def trouve_degres_et_x(sequence, nb_cases):
    return len(sequence) + 1, nb_cases - sum(sequence) - len(sequence) + 1


def trouve_valeur_reste(degres, x, num):
    nb_1 = 0
    for i, nb_2 in enumerate(grille_degres[degres]):
        if nb_2 >= num:
            return x - i, num - nb_1
        nb_1 = nb_2


def trouve_nb_possiblilitees(degres, x):
    if degres < len(grille_degres) and x < len(grille_degres[degres]):
        return grille_degres[degres][x]
    return SEUIL_MAX_CORRECTION + 1


def trouve_nb_possiblilitees_pour_x_sur_n(x, n):
    return trouve_nb_possiblilitees(x + 1, n - x)


def find_toutes_possibilitees_pour_x_sur_n(x, n):
    global possibilitees_pour_x_sur_n
    global plus_lent_moins_de_memoire
    if not (x, n) in possibilitees_pour_x_sur_n:
        listes_possiblilitees = []
        if x == 0:
            listes_possiblilitees.append(LISTE_FALSE * n)
        else:
            d = n - x
            if d == 0:
                listes_possiblilitees.append(LISTE_TRUE * x)
            elif x == 1:
                for i in range(d + 1):
                    listes_possiblilitees.append(LISTE_FALSE * (d - i) + LISTE_TRUE + LISTE_FALSE * i)
            else:
                for i in range(d + 1):
                    for possiblitees in find_toutes_possibilitees_pour_x_sur_n(x - 1, x + i - 1):
                        listes_possiblilitees.append((d - i) * LISTE_FALSE + LISTE_TRUE + possiblitees)

        if plus_lent_moins_de_memoire:
            return listes_possiblilitees
        possibilitees_pour_x_sur_n[(x, n)] = listes_possiblilitees

    return possibilitees_pour_x_sur_n[(x, n)]


def find_toutes_les_possibilitees_d_une_sequense_m1(cases: list, sequence: list):
    t0 = time.time()
    liste_index_True = []
    liste_index_False = []
    for i, case in enumerate(cases):
        if not case == CASE_INCONNUE:
            if case:
                liste_index_True.append(i)
            else:
                liste_index_False.append(i)

    t1 = time.time()
    liste_possibilitees_simplifiees = find_toutes_possibilitees_pour_x_sur_n(len(sequence),
                                                                             len(cases) - sum(sequence) + 1)
    t2 = time.time()
    liste_possibilitees = []
    for possibilitee_simplifiee in liste_possibilitees_simplifiees:
        possibilitee = []
        i = 0
        for case in possibilitee_simplifiee:
            if case:
                if i > 0:
                    possibilitee += LISTE_FALSE
                possibilitee += LISTE_TRUE * sequence[i]
                i += 1
            else:
                possibilitee += LISTE_FALSE

        possible = True
        for i in liste_index_True:
            if not possibilitee[i]:
                possible = False
                break
        if possible:
            for i in liste_index_False:
                if possibilitee[i]:
                    possible = False
                    break
            if possible:
                liste_possibilitees.append(possibilitee)

    t3 = time.time()

    dtT = round(t3 - t0, 2)
    dt1 = round(t2 - t1, 2)
    dt2 = round(t3 - t2, 2)

    print_correction(f'-> {dtT} sec  =  {dt1}s  +  {dt2}s  ({len(liste_possibilitees)} possibilitées retenues)')

    return liste_possibilitees


def trouve_possibilite_simplifiee_m2(degres, x, num):
    liste_cases_vides = []
    for deg in range(degres, 0, -1):
        valeur, num = trouve_valeur_reste(deg, x, num)
        x -= valeur
        liste_cases_vides.append(valeur)
    return liste_cases_vides


def trouve_possibilite_m2(sequences, degres, x, num):
    possibilite_simplifiee = trouve_possibilite_simplifiee_m2(degres, x, num)
    possibilite = LISTE_FALSE * possibilite_simplifiee[0]
    for i, nb_cases_coloriees in enumerate(sequences):
        if i > 0:
            possibilite += LISTE_FALSE
        possibilite += LISTE_TRUE * nb_cases_coloriees + LISTE_FALSE * possibilite_simplifiee[i + 1]
    return possibilite


def test_ligne_possible_sequence_m3(ligne, sequence):
    sequence_ligne = []
    n = 0
    for case in ligne:
        if case:
            n += 1
        else:
            if n > 0:
                if not sequence[len(sequence_ligne)] == n:
                    return False
                sequence_ligne.append(n)
                n = 0
    if n > 0:
        if not sequence[len(sequence_ligne)] == n:
            return False
        sequence_ligne.append(n)

    return True


def find_toutes_les_possibilitees_d_une_ligne_m3(cases: list, sequence: list):
    t0 = time.time()
    pos_cases_inconnues = []
    nb_cases_pleines = 0
    cases_copy_avec_cases_vide = copy.deepcopy(cases)
    for i, case in enumerate(cases):
        if case == CASE_INCONNUE:
            pos_cases_inconnues.append(i)
            cases_copy_avec_cases_vide[i] = False
        elif case:
            nb_cases_pleines += 1

    t1 = time.time()
    liste_possibilitees_simplifiees = find_toutes_possibilitees_pour_x_sur_n(sum(sequence) - nb_cases_pleines,
                                                                             len(pos_cases_inconnues))
    t2 = time.time()
    liste_possibilitees = []
    for possibilitee_simplifiee in liste_possibilitees_simplifiees:
        possibilitee = copy.deepcopy(cases_copy_avec_cases_vide)
        for i, case in enumerate(possibilitee_simplifiee):
            if case:
                possibilitee[pos_cases_inconnues[i]] = True

        if test_ligne_possible_sequence_m3(possibilitee, sequence):
            liste_possibilitees.append(possibilitee)

    t3 = time.time()

    dtT = round(t3 - t0, 2)
    dt1 = round(t2 - t1, 2)
    dt2 = round(t3 - t2, 2)

    print_correction(f'-> {dtT} sec  =  {dt1}s  +  {dt2}s  ({len(liste_possibilitees)} possibilitées retenues)')

    return liste_possibilitees


def trouve_cases_communes_liste_possibilites(ligne, liste_possibilitees: list):
    if len(liste_possibilitees) == 0:
        return None
    liste_cases_communes = []
    for j, case in enumerate(ligne):
        if case == CASE_INCONNUE:
            valeur_case = liste_possibilitees[0][j]
            for possibilitee in liste_possibilitees:
                if not possibilitee[j] == valeur_case:
                    valeur_case = None
                    break
            if valeur_case is not None:
                liste_cases_communes.append((j, valeur_case))
    return liste_cases_communes


def calcul_score_ligne(cases, sequence):
    nb_cases = len(cases)
    degres, x = trouve_degres_et_x(sequence, nb_cases)
    methode_1_ou_2 = trouve_nb_possiblilitees(degres, x)
    methode_3 = trouve_nb_possiblilitees_pour_x_sur_n(sum(sequence) - cases.count(True), cases.count(CASE_INCONNUE))
    if not methode_3 > SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE and \
            (methode_3 < methode_1_ou_2 * COEF_RENTABILITE_METHODE_1 or
             (methode_1_ou_2 > SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE and methode_3 < methode_1_ou_2)):
        return methode_3, False
    return methode_1_ou_2, True


def gere_case_trouve_possibilite_plus_a_gauche_possible(ligne: list, sequence_inverse: list, ligne_construction: list,
                                                        num_bloc: int, i_min: int = None, i_max: int = None,
                                                        i_suivant: int = None, test_noir_devant=False):
    if i_min is None:
        i_min = ligne_construction.index(num_bloc)
    if i_max is None:
        i_max = i_min + sequence_inverse[num_bloc] - 1
    if i_suivant is None:
        if num_bloc > 0:
            i_suivant = ligne_construction.index(num_bloc - 1)
        else:
            i_suivant = len(ligne) + 1

    if i_suivant == i_max + 1:
        if num_bloc > 0:
            i_suivant_max = i_suivant + sequence_inverse[num_bloc - 1]
            ligne_construction[i_suivant] = -1
            ligne_construction[i_suivant_max] = num_bloc - 1
            if gere_case_trouve_possibilite_plus_a_gauche_possible(ligne, sequence_inverse, ligne_construction,
                                                                   num_bloc - 1, i_suivant + 1, i_suivant_max):
                test_noir_devant = True
                i_suivant = ligne_construction.index(num_bloc - 1)
            else:
                return False
        else:
            return False
    if test_noir_devant:
        for i in range(i_suivant - 2, i_min, -1):
            case = ligne[i]
            if ligne_construction[i] == -1 and not case == CASE_INCONNUE and case:
                i_min_2 = i - sequence_inverse[num_bloc] + 1
                for i_ in range(i_min, i_max + 1):
                    ligne_construction[i_] = -1
                for i_ in range(i_min_2, i + 1):
                    ligne_construction[i_] = num_bloc
                return gere_case_trouve_possibilite_plus_a_gauche_possible(ligne, sequence_inverse, ligne_construction,
                                                                           num_bloc, i_min_2, i, i_suivant)

    decale_bloc = False
    for i in range(i_min, i_max + 1):
        if not ligne[i]:
            decale_bloc = True

    for i in [i_min - 1, i_max + 1]:
        if 0 <= i < len(ligne):
            case = ligne[i]
            if not case == CASE_INCONNUE and case:
                decale_bloc = True

    if decale_bloc:
        if i_max + 1 == len(ligne):
            return False
        ligne_construction[i_min] = -1
        ligne_construction[i_max + 1] = num_bloc
        return gere_case_trouve_possibilite_plus_a_gauche_possible(ligne, sequence_inverse, ligne_construction,
                                                                   num_bloc, i_min + 1, i_max + 1, i_suivant)
    return True


def trouve_possibilite_plus_a_gauche_possible(ligne: list, sequence: list, a_droite: bool):
    ligne = ligne[:]
    sequence = sequence[:]
    if a_droite:
        sequence.reverse()
        ligne.reverse()
    ligne_construction = [-1 for _ in range(len(ligne))]
    i = 0
    num_bloc = len(sequence) - 1
    for bloc in sequence:
        for _ in range(bloc):
            ligne_construction[i] = num_bloc
            i += 1
        i += 1
        num_bloc -= 1

    sequence.reverse()
    for num_bloc in range(len(sequence)):
        if not gere_case_trouve_possibilite_plus_a_gauche_possible(ligne, sequence, ligne_construction, num_bloc,
                                                                   test_noir_devant=True):
            return None

    if a_droite:
        ligne_construction.reverse()
    num_vide = -1
    vide_moins_1 = False
    for i, case in enumerate(ligne_construction):
        if case == -1:
            ligne_construction[i] = num_vide
            vide_moins_1 = False
        else:
            if not vide_moins_1:
                num_vide -= 1
                vide_moins_1 = True
            if a_droite:
                ligne_construction[i] = len(sequence) - 1 - ligne_construction[i]

    return ligne_construction


# Trouve cases communes (différentes méthodes) :
def trouve_cases_communes_methode_1(ligne, sequence):
    # Trouve toutes les possibilitées pour une séquence, ne retient que les lignes compatibles avec la ligne en cours,
    # retourne les cases communes entre toutes ces lignes possibles.
    try:
        liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense_m1(ligne, sequence)
    except MemoryError:
        return RETURN_ERREUR_MEMOIRE
    else:
        return trouve_cases_communes_liste_possibilites(ligne, liste_possibilitees)


def trouve_cases_communes_methode_2(ligne, sequence, degres=None, x=None, nb_possibilitees_max=None):
    # Même principe que la méthode 1 sauf que les possibilité sont trouvés au fur et à mesure (la technique pour les
    # rechercher est un peu différente). Cette technique est donc plus lente mais elle utilise très peu de mémoire,
    # elle permet ainsi de gérer des cas où le nombre de possibilités est très élevé.
    t0 = time.time()
    if degres or x is None:
        degres, x = trouve_degres_et_x(sequence, len(ligne))
    if nb_possibilitees_max is None:
        nb_possibilitees_max = trouve_nb_possiblilitees(degres, x)
    if nb_possibilitees_max > SEUIL_MAX_CORRECTION:
        print_correction(f'-> Erreur : trop de possibilités à explorer')
        return RETURN_ERREUR_MEMOIRE
    liste_cases_True = []
    liste_cases_False = []
    liste_cases_vides = []
    for n, case in enumerate(ligne):
        if case == CASE_INCONNUE:
            liste_cases_vides.append(n)
        elif case:
            liste_cases_True.append(n)
        else:
            liste_cases_False.append(n)
    case_centre = (nb_possibilitees_max + 1) // 2
    liste_cases_communes = []
    premiere_possibilite = True
    i = 0
    while i < nb_possibilitees_max:
        i += 1
        if i == 1:
            num = 1
        elif i == 2:
            num = nb_possibilitees_max
        elif i == 3:
            num = case_centre
        else:
            quotient = i // 4
            reste = i % 4
            if reste == 0:
                num = nb_possibilitees_max - quotient
            elif reste == 1:
                num = 1 + quotient
            elif reste == 2:
                num = case_centre + quotient
            else:
                num = case_centre - quotient
        possibilite = trouve_possibilite_m2(sequence, degres, x, num)
        possible = True
        for case_True in liste_cases_True:
            if not possibilite[case_True]:
                possible = False
                break
        if not possible:
            continue
        for case_False in liste_cases_False:
            if possibilite[case_False]:
                possible = False
                break
        if not possible:
            continue
        if premiere_possibilite:
            for case_vide in liste_cases_vides:
                liste_cases_communes.append((case_vide, possibilite[case_vide]))
            premiere_possibilite = False
        else:
            for n_case in range(len(liste_cases_communes) - 1, -1, -1):
                case, valeur = liste_cases_communes[n_case]
                if not valeur == possibilite[case]:
                    del liste_cases_communes[n_case]
        if not premiere_possibilite and len(liste_cases_communes) == 0:
            break
    if premiere_possibilite:
        return None
    print_correction(f'-> {round(time.time() - t0, 2)} sec ({i} possibilitées explorées)')
    return liste_cases_communes


def trouve_cases_communes_methode_3(ligne, sequence):
    # Trouve toutes les possibilitées pour une séquence, ne retient que les lignes compatibles avec la ligne en cours,
    # retourne les cases communes entre toutes ces lignes possibles.
    try:
        liste_possibilitees = find_toutes_les_possibilitees_d_une_ligne_m3(ligne, sequence)
    except MemoryError:
        return RETURN_ERREUR_MEMOIRE
    else:
        return trouve_cases_communes_liste_possibilites(ligne, liste_possibilitees)


def trouve_cases_communes_intelligent_old(ligne, sequence, degres=None, x=None, nb_possibilitees_max=None):
    if degres or x is None:
        degres, x = trouve_degres_et_x(sequence, len(ligne))
    if nb_possibilitees_max is None:
        nb_possibilitees_max = trouve_nb_possiblilitees(degres, x)
    # if MODE_LOGIMAGE_PEU_DE_MEMOIRE_MAIS_PLUS_LENT:  # Ne sert plus ...
    if x == -1:
        print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
        return trouve_cases_communes_methode_2(ligne, sequence, degres, x, nb_possibilitees_max)
    else:
        if nb_possibilitees_max > SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE:
            print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
            return trouve_cases_communes_methode_2(ligne, sequence, degres, x, nb_possibilitees_max)
        else:
            if nb_possibilitees_max > SEUIL_MAX_METODE_RECURSIVE_AVEC_MEMOIRE:
                set_plus_lent_moins_de_memoire(True)
            else:
                set_plus_lent_moins_de_memoire(False)
            print_correction(f'Méthode 1:         ({nb_possibilitees_max} possibilitées)')
            possibilites = trouve_cases_communes_methode_1(ligne, sequence)
            if possibilites == RETURN_ERREUR_MEMOIRE:
                print_correction('Echec méthode 1 !')
                print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
                return trouve_cases_communes_methode_2(ligne, sequence, degres, x, nb_possibilitees_max)
            else:
                return possibilites


def trouve_cases_communes_intelligent(ligne, sequence, meilleur_methode_1_ou_2: bool, nb_possibilitees_max: int):
    if nb_possibilitees_max > SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE:
        methode = 2
    else:
        if meilleur_methode_1_ou_2:
            methode = 1
        else:
            methode = 3
        if nb_possibilitees_max > SEUIL_MAX_METODE_RECURSIVE_AVEC_MEMOIRE:
            set_plus_lent_moins_de_memoire(True)
        else:
            set_plus_lent_moins_de_memoire(False)
    if methode == 1:
        print_correction(f'Méthode 1:         ({nb_possibilitees_max} possibilitées)')
        possibilites = trouve_cases_communes_methode_1(ligne, sequence)
        if possibilites == RETURN_ERREUR_MEMOIRE:
            print_correction('Echec méthode 1 !')
            print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
            degres, x = trouve_degres_et_x(sequence, len(ligne))
            return trouve_cases_communes_methode_2(ligne, sequence, degres, x, nb_possibilitees_max)
        else:
            return possibilites
    elif methode == 2:
        print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
        degres, x = trouve_degres_et_x(sequence, len(ligne))
        return trouve_cases_communes_methode_2(ligne, sequence, degres, x, nb_possibilitees_max)
    elif methode == 3:
        print_correction(f'Méthode 3:         ({nb_possibilitees_max} possibilitées)')
        possibilites = trouve_cases_communes_methode_3(ligne, sequence)
        if possibilites == RETURN_ERREUR_MEMOIRE:
            print_correction('Echec méthode 1 !')
            degres, x = trouve_degres_et_x(sequence, len(ligne))
            return trouve_cases_communes_intelligent(ligne, sequence, True, trouve_nb_possiblilitees(degres, x))
        else:
            return possibilites


def trouve_cases_communes_grossierement(ligne, sequence):
    print_correction(f'Méthode grossière:')
    t0 = time.time()
    ligne_a_gauche = trouve_possibilite_plus_a_gauche_possible(ligne, sequence, False)
    if ligne_a_gauche is None:
        return None
    ligne_a_droite = trouve_possibilite_plus_a_gauche_possible(ligne, sequence, True)
    if ligne_a_droite is None:
        return None

    if AFFICHE_DETAILS_METHODE_GROSSIERE:
        texte = 'Ligne :  '
        for case in ligne:
            if case == CASE_INCONNUE:
                texte += ' '
            elif case:
                texte += 'X'
            else:
                texte += '.'
        print_correction(sequence)
        print_correction(texte)
        texte = 'Gauche : '
        for case in ligne_a_gauche:
            if case >= 0:
                texte += 'X'
            else:
                texte += '.'
        print_correction(texte)
        texte = 'Droite : '
        for case in ligne_a_droite:
            if case >= 0:
                texte += 'X'
            else:
                texte += '.'
        print_correction(texte)

    liste_cases_communes = []
    for i, case in enumerate(ligne_a_droite):
        if ligne[i] == CASE_INCONNUE and case == ligne_a_gauche[i]:
            liste_cases_communes.append((i, case >= 0))
    print_correction(f'-> {round(time.time() - t0, 2)} sec')
    return liste_cases_communes


# Tests :
def test_et_compare_fonctions_correction_logimage(nb_essais=100):
    init_grille_derges()
    for i in range(nb_essais):
        nb_cases = random.randint(15, 50)
        nb_True = random.randint(1, nb_cases - 1)
        ligne = [True for _ in range(nb_True)] + [False for _ in range(nb_cases - nb_True)]
        random.shuffle(ligne)
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
        nb_cases_inconnues = random.randint(0, nb_cases)
        for j in range(nb_cases_inconnues):
            num = random.randint(0, nb_cases - 1 - j)
            while not ligne[num] == CASE_INCONNUE:
                ligne[num] = CASE_INCONNUE
                num = random.randint(0, nb_cases - 1 - j)
        degres, x = trouve_degres_et_x(sequence_ligne, len(ligne))
        nb_po = trouve_nb_possiblilitees(degres, x)
        print()
        print(f'{nb_po} possibilités : {nb_cases} cases dont {nb_True} pleines' +
              f' et {nb_cases_inconnues} effacées, {len(sequence_ligne)} nbs dans la sequences')
        liste1 = trouve_cases_communes_methode_1(ligne, sequence_ligne)
        liste2 = trouve_cases_communes_methode_2(ligne, sequence_ligne, degres, x, nb_po)
        liste3 = trouve_cases_communes_methode_3(ligne, sequence_ligne)

        if not (liste1.sort() == liste2.sort()) or not (liste2.sort() == liste3.sort()):
            print("ERREUR : Les 3 fonctions n'ont pas trouvées le même résultat !")
