# coding: utf-8

from outils import *
import time
import copy


PRINT_CORRECTION = False
PLUS_LENT_MOINS_DE_MEMOIRE = False


def print_correction(string: str):
    if PRINT_CORRECTION:
        print(string)


def get_permutations(counts, length):
    if len(counts) == 0:
        row = []
        for x in range(length):
            row.append(False)
        return [row]

    permutations = []

    for start in range(length - counts[0] + 1):
        permutation = []
        for x in range(start):
            permutation.append(False)
        for x in range(start, start + counts[0]):
            permutation.append(True)
        x = start + counts[0]
        if x < length:
            permutation.append(False)
            x += 1
        if x == length and len(counts) == 0:
            permutations.append(permutation)
            break
        sub_start = x
        sub_rows = get_permutations(counts[1:len(counts)], length - sub_start)
        for sub_row in sub_rows:
            sub_permutation = copy.deepcopy(permutation)
            for x in range(sub_start, length):
                sub_permutation.append(sub_row[x - sub_start])
            permutations.append(sub_permutation)
    return permutations


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

        if PLUS_LENT_MOINS_DE_MEMOIRE:
            return listes_possiblilitees
        possibilitees_pour_x_sur_n[(x, n)] = listes_possiblilitees

    return possibilitees_pour_x_sur_n[(x, n)]


def find_tous_les_cas_de_figure_d_une_sequense(nb_cases: int, sequence: list):
    t1 = time.time()
    liste_possibilitees_simplifiees = find_toutes_possibilitees_pour_x_sur_n(len(sequence),
                                                                             nb_cases - sum(sequence) + 1)
    t2 = time.time()
    liste_possibilitees = []
    print_correction(f'Etape 2 : {len(liste_possibilitees_simplifiees)} possibilités')
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
    t3 = time.time()
    return liste_possibilitees, t1, t2, t3


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

    liste_possibilitees = []
    tous_les_cas_de_figure_d_une_sequense, t1, t2, t3 = find_tous_les_cas_de_figure_d_une_sequense(len(cases), sequence)
    for possibilitees in tous_les_cas_de_figure_d_une_sequense:
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

    t4 = time.time()

    dtT = round(t4 - t0, 2)
    dt1 = round(t2 - t1, 2)
    dt2 = round(t3 - t2, 2)
    dt3 = round(t4 - t0 - t3 + t1, 2)

    print_correction(f'{dtT}s  --> 1: {dt1}s  +  2: {dt2}s  +  3: {dt3}s')

    return liste_possibilitees


def test_reste_cases_inconnues(cases):
    for ligne in cases:
        if CASE_INCONNUE in ligne:
            return True
    return False
