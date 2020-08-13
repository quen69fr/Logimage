
from logimage import *


def impr_dic_logimage_logimage_sequences(chemin_image: str, titre: str):
    image = pygame.image.load(chemin_image)
    largeur, hauteur = image.get_size()
    logimage = create_logimage_nouveau(MODE_LOGIMAGE_CREER, (largeur, hauteur), titre)
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if image.get_at((colonne, ligne)) == NOIR:
                logimage.set_case_grille(ligne, colonne, True)
    print(str({"ver": logimage.sequences_lignes,
               "hor": logimage.sequences_colonnes}).replace("'", '"').replace(' ', ''))


pygame.init()

impr_dic_logimage_logimage_sequences('Entrees/Images/UnPeuDambiance.png', "Un peu d'ambiance !")

pygame.quit()
