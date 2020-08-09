# coding: utf-8

from logimage import *


def creer_logimage_a_partir_png(chemin_image: str, titre: str):
    image = pygame.image.load(chemin_image)
    largeur, hauteur = image.get_size()
    logimage = create_logimage_nouveau(MODE_LOGIMAGE_CREER, (largeur, hauteur), titre)
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if image.get_at((colonne, ligne)) == NOIR:
                logimage.set_case_grille(ligne, colonne, True)
    logimage.sauvegarde_logimage()


def creer_logimage_a_partir_txt(chemin_texte: str, titre: str):
    liste_nbs_colonnes = []
    liste_nbs_lignes = []
    mode = 0
    with open(chemin_texte) as texte:
        for ligne in texte:
            if mode == 0:
                if 'columns' in ligne:
                    mode = 1
                    continue
            elif mode == 1:
                if 'rows' in ligne:
                    mode = 2
                    continue
                if len(ligne) > 1:
                    colonne_nbs = []
                    for lettre in ligne.split(' '):
                        if len(lettre) > 0:
                            colonne_nbs.append(int(lettre))
                    liste_nbs_colonnes.append(colonne_nbs)
            else:
                if len(ligne) > 1:
                    ligne_nbs = []
                    for lettre in ligne.split(' '):
                        if len(lettre) > 0:
                            ligne_nbs.append(int(lettre))
                    liste_nbs_lignes.append(ligne_nbs)

    largeur, hauteur = len(liste_nbs_colonnes), len(liste_nbs_lignes)
    logimage = create_logimage_nouveau(MODE_LOGIMAGE_RENTRE, (largeur, hauteur), titre)
    for i, ligne in enumerate(liste_nbs_lignes):
        for case in ligne:
            logimage.add_case_sequence_ligne(i, case)
    for j, colonne in enumerate(liste_nbs_colonnes):
        for case in colonne:
            logimage.add_case_sequence_colonne(j, case)

    logimage.sauvegarde_logimage()


pygame.init()
creer_logimage_a_partir_png('Entrees/jazz_orchestra_puzzle.png', "Un peu d'ambiance !")
