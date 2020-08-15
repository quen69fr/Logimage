# coding: utf-8

from fonctions_correction_logimage_1 import *
from fonctions_correction_logimage_2 import *


def trouve_cases_communes_intelligent(ligne, sequence):
    degres, x = trouve_degres_et_x(sequence, len(ligne))
    nb_possibilitees_max = trouve_nb_possiblilitees(degres, x)
    if MODE_LOGIMAGE_PEU_DE_MEMOIRE_MAIS_PLUS_LENT:
        print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
        return trouve_cases_communes_peu_memoire(ligne, sequence, degres, x, nb_possibilitees_max)
    else:
        if nb_possibilitees_max > SEUIL_MAX_METODE_CORRECTION_RAPIDE_MOINS_MEMOIRE:
            if nb_possibilitees_max > SEUIL_MAX_METODE_CORRECTION_RAPIDE:
                set_plus_lent_moins_de_memoire(True)
            else:
                set_plus_lent_moins_de_memoire(False)
            print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
            return trouve_cases_communes_peu_memoire(ligne, sequence, degres, x, nb_possibilitees_max)
        else:
            print_correction(f'Méthode 1:         ({nb_possibilitees_max} possibilitées)')
            possibilites = trouve_cases_communes_rapide_memoire(ligne, sequence)
            if possibilites == RETURN_ERREUR_MEMOIRE:
                print_correction('Echec méthode 1 !')
                print_correction(f'Méthode 2:         ({nb_possibilitees_max} possibilitées)')
                return trouve_cases_communes_peu_memoire(ligne, sequence, degres, x, nb_possibilitees_max)
            else:
                return possibilites


# A part : def trouve_cases_communes_intelligent --> test pour ajustement seuils, methodes ...
def test_et_compare_fonctions_correction_logimage_1_et_2(nb_essais=100):
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
        nb_cases_vides = random.randint(0, nb_cases)
        for j in range(nb_cases_vides):
            num = random.randint(0, nb_cases - 1 - j)
            while not ligne[num] == CASE_INCONNUE:
                ligne[num] = CASE_INCONNUE
                num = random.randint(0, nb_cases - 1 - j)
        degres, x = trouve_degres_et_x(sequence_ligne, len(ligne))
        nb_po = trouve_nb_possiblilitees(degres, x)
        print()
        print(f'{nb_po} possibilités : {nb_cases} cases dont {nb_True} pleines' +
              f' et {nb_cases_vides} effacées, {len(sequence_ligne)} nbs dans la sequences')
        liste1 = trouve_cases_communes_peu_memoire(ligne, sequence_ligne, degres, x, nb_po)
        liste2 = trouve_cases_communes_rapide_memoire(ligne, sequence_ligne)

        if not liste1.sort() == liste2.sort():
            print("ERREUR : les deux fonctions n'ont pas trouvées le même résultat !")