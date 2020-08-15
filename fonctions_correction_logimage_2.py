# coding: utf-8

from outils import *
import time
import random


def trouve_degres_et_x(sequences, nb_cases):
    return len(sequences) + 1, nb_cases - sum(sequences) - len(sequences) + 1


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


def trouve_nb_possiblilitees(degres, x):
    return grille_degres[degres][x]


def trouve_valeur_reste(degres, x, num):
    nb_1 = 0
    for i, nb_2 in enumerate(grille_degres[degres]):
        if nb_2 >= num:
            return x - i, num - nb_1
        nb_1 = nb_2


def trouve_possibilite_simplifiee(degres, x, num):
    liste_cases_vides = []
    for deg in range(degres, 0, -1):
        valeur, num = trouve_valeur_reste(deg, x, num)
        x -= valeur
        liste_cases_vides.append(valeur)
    return liste_cases_vides


LISTE_TRUE = [True]
LISTE_FALSE = [False]


def trouve_possibilite(sequences, degres, x, num):
    possibilite_simplifiee = trouve_possibilite_simplifiee(degres, x, num)
    possibilite = LISTE_FALSE * possibilite_simplifiee[0]
    for i, nb_cases_coloriees in enumerate(sequences):
        if i > 0:
            possibilite += LISTE_FALSE
        possibilite += LISTE_TRUE * nb_cases_coloriees + LISTE_FALSE * possibilite_simplifiee[i + 1]
    return possibilite


def trouve_cases_communes_peu_memoire(ligne, sequence, degres=None, x=None, nb_possibilitees_max=None):
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
    liste_cases_communes = []
    premiere_possibilite = True
    try:
        if nb_possibilitees_max < 5:
            liste = list(range(1, nb_possibilitees_max + 1))
        else:
            liste = list(range(2, nb_possibilitees_max))
            liste.remove(nb_possibilitees_max // 2)
            random.shuffle(liste)
            liste = [1, nb_possibilitees_max, nb_possibilitees_max // 2] + liste
    except MemoryError:
        print_correction(f'-> Erreur : trop de possibilités à explorer')
        return RETURN_ERREUR_MEMOIRE
    else:
        num = 1
        for num in liste:
            possibilite = trouve_possibilite(sequence, degres, x, num)
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
        print_correction(f'-> {round(time.time() - t0, 2)} sec ({liste.index(num) + 1} possibilitées explorées)')
        return liste_cases_communes
