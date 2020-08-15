# coding: utf-8

from outils import *
import time

plus_lent_moins_de_memoire = True
possibilitees_pour_x_sur_n = {}

LISTE_TRUE = [True]
LISTE_FALSE = [False]


def set_plus_lent_moins_de_memoire(value):
    global plus_lent_moins_de_memoire
    plus_lent_moins_de_memoire = value


def clear_possibilitees_pour_x_sur_n():
    global possibilitees_pour_x_sur_n
    possibilitees_pour_x_sur_n.clear()


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


# def find_tous_les_cas_de_figure_d_une_sequense(nb_cases: int, sequence: list):
#     t1 = time.time()
#     liste_possibilitees_simplifiees = find_toutes_possibilitees_pour_x_sur_n(len(sequence),
#                                                                              nb_cases - sum(sequence) + 1)
#     t2 = time.time()
#     liste_possibilitees = []
#     print_correction(f'Etape 2 : {len(liste_possibilitees_simplifiees)} possibilités')
#     for possibilitee_simplifiee in liste_possibilitees_simplifiees:
#         possibilitee = []
#         i = 0
#         for case in possibilitee_simplifiee:
#             if case:
#                 if i > 0:
#                     possibilitee += [False]
#                 possibilitee += [True] * sequence[i]
#                 i += 1
#             else:
#                 possibilitee += [False]
#         liste_possibilitees.append(possibilitee)
#     t3 = time.time()
#     return liste_possibilitees
#
#
# def find_toutes_les_possibilitees_d_une_sequense(cases: list, sequence: list):
#     t0 = time.time()
#     liste_index_True = []
#     liste_index_False = []
#     for i, case in enumerate(cases):
#         if not case == CASE_INCONNUE:
#             if case:
#                 liste_index_True.append(i)
#             else:
#                 liste_index_False.append(i)
#
#     liste_possibilitees = []
#      tous_les_cas_de_figure_d_une_sequense, t1, t2, t3 = \
#          find_tous_les_cas_de_figure_d_une_sequense(len(cases), sequence)
#     for possibilitees in tous_les_cas_de_figure_d_une_sequense:
#         possible = True
#         for i in liste_index_True:
#             if not possibilitees[i]:
#                 possible = False
#                 break
#         if possible:
#             for i in liste_index_False:
#                 if possibilitees[i]:
#                     possible = False
#                     break
#             if possible:
#                 liste_possibilitees.append(possibilitees)
#
#     t4 = time.time()
#
#     dtT = round(t4 - t0, 2)
#     dt1 = round(t2 - t1, 2)
#     dt2 = round(t3 - t2, 2)
#     dt3 = round(t4 - t0 - t3 + t1, 2)
#
#     print_correction(f'{dtT}s  --> 1: {dt1}s  +  2: {dt2}s  +  3: {dt3}s')
#
#     return liste_possibilitees


def find_toutes_les_possibilitees_d_une_sequense(cases: list, sequence: list):
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


def test_reste_cases_inconnues(cases):
    for ligne in cases:
        if CASE_INCONNUE in ligne:
            return True
    return False


def trouve_cases_communes_rapide_memoire(ligne, sequence):
    try:
        liste_possibilitees = find_toutes_les_possibilitees_d_une_sequense(ligne, sequence)
    except MemoryError:
        return RETURN_ERREUR_MEMOIRE
    else:
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
