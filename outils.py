# coding: utf-8

FULL_SCREEN = False

# MODE_LOGIMAGE_PEU_DE_MEMOIRE_MAIS_PLUS_LENT = False
COEF_RENTABILITE_METHODE_1 = 0.2
SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE = 2000000
SEUIL_MAX_METODE_RECURSIVE_AVEC_MEMOIRE = 300000
SEUIL_MAX_CORRECTION = 1000000000  # Faisable mais TRES long ...
SEUIL_RENTABILITE_METHODE_GROSSIERE = 1000
DEGRES_X_MAX_METHODE_2_CORRECTION_LOGIMAGE = 50, 50
RETURN_ERREUR_MEMOIRE = 'erreur'
SAUVEGARDE_CASES_SI_CORRECTION_PAS_COMPLETE = True
PRINT_CORRECTION = False
AFFICHE_DETAILS_METHODE_GROSSIERE = False


def print_correction(string: str):
    if PRINT_CORRECTION:
        print(string)


TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE = 0
TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE = 1
TYPE_ACTION_TESTER_LOGIMAGE = 2
TYPE_ACTION_CORRIGER_LOGIMAGE = 3
TYPE_ACTION_COLORIER_CASE = 4
TYPE_ACTION_CRAYON = 5
TYPE_ACTION_POINTEUR = 6
TYPE_ACTION_AIDE = 7

NOIR = (0, 0, 0)
GRIS_FONCE = (50, 50, 50)
GRIS_MOYEN = (90, 90, 90)
GRIS_CLAIR = (130, 130, 130)
BLANC = (255, 255, 255)
BLEU = (0, 0, 255)
VERT = (52, 175, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 127, 0)
JAUNE = (255, 230, 0)

FPS = 70
CAPTION = 'Logimages (Quentin PALAZON)'

# SOURIS_NORMALE = ("X               ",
#                   "XX              ",
#                   "X.X             ",
#                   "X..X            ",
#                   "X...X           ",
#                   "X....X          ",
#                   "X.....X         ",
#                   "X......X        ",
#                   "X.......X       ",
#                   "X........X      ",
#                   "X.........X     ",
#                   "X......XXXXX    ",
#                   "X...X..X        ",
#                   "X..XX..X        ",
#                   "X.X  X..X       ",
#                   "XX   X..X       ",
#                   "X     X..X      ",
#                   "      X..X      ",
#                   "       XX       ",
#                   "                ",
#                   "                ",
#                   "                ",
#                   "                ",
#                   "                ")
# SOURIS_NORMALE = ("     XX         ",
#                   "    X..X        ",
#                   "    X..X        ",
#                   "    X..X        ",
#                   "    X..XXXXX    ",
#                   "    X..X..X.XX  ",
#                   " XX X..X..X.X.X ",
#                   "X..XX.........X ",
#                   "X...X.........X ",
#                   "XX.....X.X.X..X ",
#                   "  X....X.X.X..X ",
#                   "  X....X.X.X.X  ",
#                   "   X...X.X.X.X  ",
#                   "    X.......X   ",
#                   "     X......X   ",
#                   "     XXXXXXXX   ",)
# SOURIS_COLORIER_CLIC = ((16, 16), (7, 7), ("       .        ",
#                                            "      .X.       ",
#                                            "     .XXX.      ",
#                                            "    .XXXXX.     ",
#                                            "   .XXX XXX.    ",
#                                            "  .XXX   XXX.   ",
#                                            " .XXX     XXX.  ",
#                                            ".XXX       XXX. ",
#                                            " .XXX     XXX.  ",
#                                            "  .XXX   XXX.   ",
#                                            "   .XXX XXX.    ",
#                                            "    .XXXXX.     ",
#                                            "     .XXX.      ",
#                                            "      .X.       ",
#                                            "       .        ",
#                                            "                "))

SOURIS_NORMALE = ((32, 32), (11, 1), ("          XXXX                  ",
                                      "         XXXXXX                 ",
                                      "        XXX..XXX                ",
                                      "        XX....XX                ",
                                      "        XX....XX                ",
                                      "        XX....XX                ",
                                      "        XX....XX                ",
                                      "        XX....XX                ",
                                      "        XX....XXXXXXXXXX        ",
                                      "        XX....XXXXXXXXXXX       ",
                                      "        XX....XX....XX.XXXXX    ",
                                      "        XX....XX....XX..XXXXX   ",
                                      "  XXXX  XX....XX....XX..XX.XXX  ",
                                      " XXXXXX XX....XX....XX..XX..XX  ",
                                      "XXX..XXXXX....XX....XX......XX  ",
                                      "XX....XXXX..................XX  ",
                                      "XX......XX..................XX  ",
                                      "XX......XX..................XX  ",
                                      "XXXX..........XX..XX..XX....XX  ",
                                      " XXXX.........XX..XX..XX....XX  ",
                                      "   XXX........XX..XX..XX...XXX  ",
                                      "    XX........XX..XX..XX...XX   ",
                                      "    XXX.......XX..XX..XX..XXX   ",
                                      "     XX.......XX..XX..XX..XX    ",
                                      "     XXX......XX..XX..XX..XX    ",
                                      "      XXX.....XX..XX.....XXX    ",
                                      "       XXX...............XX     ",
                                      "        XXX.............XX      ",
                                      "         XXX............XX      ",
                                      "          XX............XX      ",
                                      "          XXXXXXXXXXXXXXXX      ",
                                      "           XXXXXXXXXXXXXX       "))
SOURIS_NORMALE_CLIC = ((32, 32), (11, 1), ("                                ",
                                           "                                ",
                                           "                                ",
                                           "          XXXX                  ",
                                           "         XXXXXX                 ",
                                           "        XXX..XXX                ",
                                           "        XX....XX                ",
                                           "        XX.XX.XX                ",
                                           "        XX....XXXXXXXXXX        ",
                                           "        XX....XXXXXXXXXXX       ",
                                           "        XX....XX....XX.XXXXX    ",
                                           "        XX....XX....XX..XXXXX   ",
                                           "  XXXX  XX....XX....XX..XX.XXX  ",
                                           " XXXXXX XX....XX....XX..XX..XX  ",
                                           "XXX..XXXXX....XX....XX......XX  ",
                                           "XX....XXXX..................XX  ",
                                           "XX......XX..................XX  ",
                                           "XX......XX..................XX  ",
                                           "XXXX..........XX..XX..XX....XX  ",
                                           " XXXX.........XX..XX..XX....XX  ",
                                           "   XXX........XX..XX..XX...XXX  ",
                                           "    XX........XX..XX..XX...XX   ",
                                           "    XXX.......XX..XX..XX..XXX   ",
                                           "     XX.......XX..XX..XX..XX    ",
                                           "     XXX......XX..XX..XX..XX    ",
                                           "      XXX.....XX..XX.....XXX    ",
                                           "       XXX...............XX     ",
                                           "        XXX.............XX      ",
                                           "         XXX............XX      ",
                                           "          XX............XX      ",
                                           "          XXXXXXXXXXXXXXXX      ",
                                           "           XXXXXXXXXXXXXX       "))
SOURIS_COLORIER = ((16, 16), (0, 0), ("...             ",
                                      ".XX..           ",
                                      ".XXXX..         ",
                                      " .XXXXX..       ",
                                      " .XXXXXXX..     ",
                                      "  .XXXXXXXX..   ",
                                      "  .XXXXXXXXXX.. ",
                                      "   .XXXXXXXXXXX.",
                                      "   .XXXXXXXXXXX.",
                                      "    .XXXX...... ",
                                      "    .XXXX.      ",
                                      "     .XXX.      ",
                                      "     .XXX.      ",
                                      "      .XX.      ",
                                      "      .XX.      ",
                                      "       ..       ",))
SOURIS_DESSIN = ((16, 16), (0, 0), ("XXXX            ",
                                    "X...XX          ",
                                    "X..XXXX         ",
                                    "X.XXX.XX        ",
                                    " XXX...XX       ",
                                    " XX.....XX      ",
                                    "  XX.....XX     ",
                                    "   XX.....XX    ",
                                    "    XX.....XX   ",
                                    "     XX....XX   ",
                                    "      XX..XX.XX ",
                                    "       XXXX.XXXX",
                                    "        XX.XXXX ",
                                    "          XXXX  ",
                                    "          XXX   ",
                                    "           X    "))
SOURIS_GOMME = ((16, 16), (1, 1), ("   XXX          ",
                                   "  XX.XX         ",
                                   " XX...XX        ",
                                   "XX.....XX       ",
                                   "X.......XX      ",
                                   "XX.....X.XX     ",
                                   " XX...X...XX    ",
                                   "  XX.X...XXXX   ",
                                   "   XX...XXXXXX  ",
                                   "    XX.XXXXXXXX ",
                                   "     XXXXXXXXXXX",
                                   "      XXXXXXXXXX",
                                   "       XXXXXXXX ",
                                   "        XXXXXX  ",
                                   "         XXXX   ",
                                   "          XX    "))

COULEUR_FOND = (200, 200, 200)

LARGEUR = 1360
HAUTEUR = 700

DEFAULT_POLICE = None, 35

DEFAULT_TAILLE_GRILLE = 20, 15
MARGE_GRILLE_BORD_HAUT = 100
MARGE_GRILLE_BORD_BAS = 20
MARGE_GRILLE_BORD_DROITE = 20
MARGE_GRILLE_BORD_GAUCHE = 330
MARGE_BOUTON = 18

COULEUR_TITRE = NOIR
COULEUR_CHARGEMENT = (70, 70, 70)
TAILLE_TITRE = 80
CONTOURS_TITRE_SELECTIONNE = GRIS_MOYEN, 4
MARGE_TITRE = 15
DEFAULT_TITRE = 'Logimage'
LONGEUR_TITRE_MAX = 30

COULEUR_QUADRILLAGE = NOIR
COULEUR_CASE_PLEINE = (20, 20, 20)
COULEUR_CASE_VIDE = BLANC
COEF_TAILLE_QUADRILLAGE = 0.06
COEF_TAILLE_QUADRILLAGE_PRINCIPALE_ECART = 0.04
QUADRILLAGE_PRINCIPALE = 5
COEF_TAILLE_POLICE = 1.2
COULEUR_NB = NOIR
COEF_TAILLE_POINTS_CRAYON = 0.1
COULEUR_POINTS_CRAYON_CASE_INCONNUE = (5, 5, 50)
COULEUR_POINTS_CRAYON_CASE_PLEINE = (66, 79, 127)
COULEUR_POINTS_CRAYON_CASE_VIDE = (38, 46, 73)
COULEUR_POINTEUR = (NOIR, 90)

CASE_INCONNUE = "?"
CASE_INNEXISTANTE = 'NON'
COULEUR_CASE_INCONNUE_ROUGE = (180, 20, 20)
COULEUR_CASE_INCONNUE_BLEU = (36, 62, 165)

VITESSE_MOLETTE = 15
COEF_VITESSE_MOLETTE = 0.85
NB_COLONNES_VIGNETTES_MAX = 10

MODE_ACCUEIL = 0
MODE_CHOISI_LOGIMAGE = 1
MODE_LOGIMAGE = 2

NOM_NOUVEAU_LOGIMAGE = 'Nouveau'

TAILLE_TITRE_PRINCIPAL = 200
TITRE_MODE_ACCUEIL = "LOGIMAGE"
TITRE_MODE_CHOISI_LOGIMAGE = "Choisir un logimage ..."
TITRE_MODE_CHOISI_LOGIMAGE_CHARGEMENT = "Chargement ..."

MODE_LOGIMAGE_FAIT = 0
MODE_LOGIMAGE_CREER = 1
MODE_LOGIMAGE_RENTRE = 2
MODE_LOGIMAGE_IMPR = 3
MODE_LOGIMAGE_CORRECTION = 4

ACTION_SUPR_1 = 0
ACTION_SUPR_GROUPE = 1
ACTION_ADD_1 = 2
ACTION_ADD_GROUPE = 3

LISTE_ORDRE_VALEUR_CASE_CLIC = [CASE_INCONNUE, True, False]

BOUTON_MODE_LOGIMAGE_FAIT = -1
BOUTON_MODE_LOGIMAGE_CREER = -2
BOUTON_MODE_LOGIMAGE_RENTRE = -3
BOUTON_MODE_LOGIMAGE_IMPR = -4
BOUTON_REVENIR_ACCUEIL = -5
BOUTON_FULL_SCREEN = -6

BOUTON_SUPPR_LIGNE = 0
BOUTON_SUPPR_COLONNE = 1
BOUTON_SUPPR_GROUPE_LIGNES = 2
BOUTON_SUPPR_GROUPE_COLONNES = 3
BOUTON_AJOUT_LIGNE = 4
BOUTON_AJOUT_COLONNE = 5
BOUTON_AJOUT_GROUPE_LIGNES = 6
BOUTON_AJOUT_GROUPE_COLONNES = 7
BOUTON_TESTER_LOGIMAGE_CREATION = 8
BOUTON_SAUVEGARDER_LOGIMAGE = 9
BOUTON_CORRIGER_LOGIMAGE = 10
BOUTON_AIDE = 11
BOUTON_ENLEVE_ERREURS_LOGIMAGE = 12
BOUTON_RECOMMENCER_LOGIMAGE = 13
BOUTON_RETOUR_SANS_ERREUR = 14
BOUTON_COLORIER_UNE_CASE = 15
BOUTON_AFFICHER_CORRECTION = 16
BOUTON_CRAYON = 17
BOUTON_EFFACER_TOUT_CRAYON = 18
BOUTON_POINTEUR = 19

STYLE_BOUTON_VERT = ((0, 40, 3), (90, 135, 95), 3, (None, 35))
STYLE_BOUTON_ROUGE = ((96, 0, 0), (181, 99, 99), 3, (None, 35))
STYLE_BOUTON_NOIR_FIN = (NOIR, (70, 70, 70), 3, (None, 35))
STYLE_BOUTON_NOIR = (NOIR, (70, 70, 70), 5, (None, 35))
STYLE_BOUTON_ENORME = (NOIR, (70, 70, 70), 5, (None, 70))
STYLE_BOUTON_BLEU = ((19, 30, 73), (104, 116, 165), 3, (None, 35))

STYLE_VIGNETTE_LOGIMAGE = (NOIR, (240, 240, 240), 0.015, (None, 0.2))
COULEUR_SECONDAIRE_VIGNETTE = GRIS_FONCE

PARAM_BOUTON_TEXTE = 0
PARAM_BOUTON_STYLE = 1
PARAM_BOUTON_TYPE_ACTION = 2
PARAM_BOUTON_VALEUR = 3
PARAM_BOUTON_RACCOURCI = 4

DIC_BOUTONS = {
    PARAM_BOUTON_TEXTE: {
        BOUTON_MODE_LOGIMAGE_FAIT: 'Faire un logimage',
        BOUTON_MODE_LOGIMAGE_CREER: 'Créer un logimage',
        BOUTON_MODE_LOGIMAGE_RENTRE: 'Rentrer un logimage',
        BOUTON_MODE_LOGIMAGE_IMPR: 'Imprimer un logimage',
        BOUTON_REVENIR_ACCUEIL: '< ACCUEIL',
        BOUTON_FULL_SCREEN: 'Plein écran',
        BOUTON_SUPPR_LIGNE: 'Supprimer 1 ligne',
        BOUTON_SUPPR_COLONNE: 'Supprimer 1 colonne',
        BOUTON_SUPPR_GROUPE_LIGNES: f'Supprimer {QUADRILLAGE_PRINCIPALE} lignes',
        BOUTON_SUPPR_GROUPE_COLONNES: f'Supprimer {QUADRILLAGE_PRINCIPALE} colonnes',
        BOUTON_AJOUT_LIGNE: 'Ajouter 1 ligne',
        BOUTON_AJOUT_COLONNE: 'Ajouter 1 colonne',
        BOUTON_AJOUT_GROUPE_LIGNES: f'Ajouter {QUADRILLAGE_PRINCIPALE} lignes',
        BOUTON_AJOUT_GROUPE_COLONNES: f'Ajouter {QUADRILLAGE_PRINCIPALE} colonnes',
        BOUTON_TESTER_LOGIMAGE_CREATION: 'Tester le Logimage',
        BOUTON_SAUVEGARDER_LOGIMAGE: 'Sauvegarder',
        BOUTON_CORRIGER_LOGIMAGE: 'Voir les erreurs',
        BOUTON_AIDE: 'Aide',
        BOUTON_ENLEVE_ERREURS_LOGIMAGE: 'Enlever les erreurs',
        BOUTON_RECOMMENCER_LOGIMAGE: 'Tout effacer',
        BOUTON_RETOUR_SANS_ERREUR: 'Retour avant erreurs',
        BOUTON_COLORIER_UNE_CASE: 'Colorier une case',
        BOUTON_AFFICHER_CORRECTION: 'Tout corriger',
        BOUTON_CRAYON: 'Prendre le crayon',
        BOUTON_EFFACER_TOUT_CRAYON: 'Effacer le crayon',
        BOUTON_POINTEUR: 'Mettre le pointeur'
    },
    PARAM_BOUTON_STYLE: {
        BOUTON_MODE_LOGIMAGE_FAIT: STYLE_BOUTON_ENORME,
        BOUTON_MODE_LOGIMAGE_CREER: STYLE_BOUTON_ENORME,
        BOUTON_MODE_LOGIMAGE_RENTRE: STYLE_BOUTON_ENORME,
        BOUTON_MODE_LOGIMAGE_IMPR: STYLE_BOUTON_ENORME,
        BOUTON_REVENIR_ACCUEIL: STYLE_BOUTON_NOIR,
        BOUTON_FULL_SCREEN: STYLE_BOUTON_NOIR,
        BOUTON_SUPPR_LIGNE: STYLE_BOUTON_ROUGE,
        BOUTON_SUPPR_COLONNE: STYLE_BOUTON_ROUGE,
        BOUTON_SUPPR_GROUPE_LIGNES: STYLE_BOUTON_ROUGE,
        BOUTON_SUPPR_GROUPE_COLONNES: STYLE_BOUTON_ROUGE,
        BOUTON_AJOUT_LIGNE: STYLE_BOUTON_VERT,
        BOUTON_AJOUT_COLONNE: STYLE_BOUTON_VERT,
        BOUTON_AJOUT_GROUPE_LIGNES: STYLE_BOUTON_VERT,
        BOUTON_AJOUT_GROUPE_COLONNES: STYLE_BOUTON_VERT,
        BOUTON_TESTER_LOGIMAGE_CREATION: STYLE_BOUTON_NOIR_FIN,
        BOUTON_SAUVEGARDER_LOGIMAGE: STYLE_BOUTON_NOIR,
        BOUTON_CORRIGER_LOGIMAGE: STYLE_BOUTON_ROUGE,
        BOUTON_AIDE: STYLE_BOUTON_VERT,
        BOUTON_ENLEVE_ERREURS_LOGIMAGE: STYLE_BOUTON_ROUGE,
        BOUTON_RECOMMENCER_LOGIMAGE: STYLE_BOUTON_BLEU,
        BOUTON_RETOUR_SANS_ERREUR: STYLE_BOUTON_VERT,
        BOUTON_COLORIER_UNE_CASE: STYLE_BOUTON_VERT,
        BOUTON_AFFICHER_CORRECTION: STYLE_BOUTON_VERT,
        BOUTON_CRAYON: STYLE_BOUTON_BLEU,
        BOUTON_EFFACER_TOUT_CRAYON: STYLE_BOUTON_BLEU,
        BOUTON_POINTEUR: STYLE_BOUTON_BLEU
    },
    PARAM_BOUTON_TYPE_ACTION: {
        BOUTON_MODE_LOGIMAGE_FAIT: None,
        BOUTON_MODE_LOGIMAGE_CREER: None,
        BOUTON_MODE_LOGIMAGE_RENTRE: None,
        BOUTON_MODE_LOGIMAGE_IMPR: None,
        BOUTON_REVENIR_ACCUEIL: None,
        BOUTON_FULL_SCREEN: None,
        BOUTON_SUPPR_LIGNE: TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE,
        BOUTON_SUPPR_COLONNE: TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE,
        BOUTON_SUPPR_GROUPE_LIGNES: TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE,
        BOUTON_SUPPR_GROUPE_COLONNES: TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE,
        BOUTON_AJOUT_LIGNE: TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE,
        BOUTON_AJOUT_COLONNE: TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE,
        BOUTON_AJOUT_GROUPE_LIGNES: TYPE_ACTION_LOGIMAGE_LIGNE_POSSIBLE,
        BOUTON_AJOUT_GROUPE_COLONNES: TYPE_ACTION_LOGIMAGE_COLONNE_POSSIBLE,
        BOUTON_TESTER_LOGIMAGE_CREATION: TYPE_ACTION_TESTER_LOGIMAGE,
        BOUTON_SAUVEGARDER_LOGIMAGE: None,
        BOUTON_CORRIGER_LOGIMAGE: TYPE_ACTION_CORRIGER_LOGIMAGE,
        BOUTON_AIDE: TYPE_ACTION_AIDE,
        BOUTON_ENLEVE_ERREURS_LOGIMAGE: None,
        BOUTON_RECOMMENCER_LOGIMAGE: None,
        BOUTON_RETOUR_SANS_ERREUR: None,
        BOUTON_COLORIER_UNE_CASE: TYPE_ACTION_COLORIER_CASE,
        BOUTON_AFFICHER_CORRECTION: None,
        BOUTON_CRAYON: TYPE_ACTION_CRAYON,
        BOUTON_EFFACER_TOUT_CRAYON: None,
        BOUTON_POINTEUR: TYPE_ACTION_POINTEUR
    },
    PARAM_BOUTON_VALEUR: {
        BOUTON_MODE_LOGIMAGE_FAIT: None,
        BOUTON_MODE_LOGIMAGE_CREER: None,
        BOUTON_MODE_LOGIMAGE_RENTRE: None,
        BOUTON_MODE_LOGIMAGE_IMPR: None,
        BOUTON_REVENIR_ACCUEIL: None,
        BOUTON_FULL_SCREEN: None,
        BOUTON_SUPPR_LIGNE: ACTION_SUPR_1,
        BOUTON_SUPPR_COLONNE: ACTION_SUPR_1,
        BOUTON_SUPPR_GROUPE_LIGNES: ACTION_SUPR_GROUPE,
        BOUTON_SUPPR_GROUPE_COLONNES: ACTION_SUPR_GROUPE,
        BOUTON_AJOUT_LIGNE: ACTION_ADD_1,
        BOUTON_AJOUT_COLONNE: ACTION_ADD_1,
        BOUTON_AJOUT_GROUPE_LIGNES: ACTION_ADD_GROUPE,
        BOUTON_AJOUT_GROUPE_COLONNES: ACTION_ADD_GROUPE,
        BOUTON_TESTER_LOGIMAGE_CREATION: None,
        BOUTON_SAUVEGARDER_LOGIMAGE: None,
        BOUTON_CORRIGER_LOGIMAGE: None,
        BOUTON_AIDE: None,
        BOUTON_ENLEVE_ERREURS_LOGIMAGE: None,
        BOUTON_RECOMMENCER_LOGIMAGE: None,
        BOUTON_RETOUR_SANS_ERREUR: None,
        BOUTON_COLORIER_UNE_CASE: None,
        BOUTON_AFFICHER_CORRECTION: None,
        BOUTON_CRAYON: None,
        BOUTON_EFFACER_TOUT_CRAYON: None,
        BOUTON_POINTEUR: None
    },
    PARAM_BOUTON_RACCOURCI: {
        BOUTON_MODE_LOGIMAGE_FAIT: 'L',
        BOUTON_MODE_LOGIMAGE_CREER: 'C',
        BOUTON_MODE_LOGIMAGE_RENTRE: 'R',
        BOUTON_MODE_LOGIMAGE_IMPR: 'I',
        BOUTON_REVENIR_ACCUEIL: 'A',
        BOUTON_FULL_SCREEN: 'F',
        BOUTON_SUPPR_LIGNE: None,
        BOUTON_SUPPR_COLONNE: None,
        BOUTON_SUPPR_GROUPE_LIGNES: None,
        BOUTON_SUPPR_GROUPE_COLONNES: None,
        BOUTON_AJOUT_LIGNE: None,
        BOUTON_AJOUT_COLONNE: None,
        BOUTON_AJOUT_GROUPE_LIGNES: None,
        BOUTON_AJOUT_GROUPE_COLONNES: None,
        BOUTON_TESTER_LOGIMAGE_CREATION: 'T',
        BOUTON_SAUVEGARDER_LOGIMAGE: 'S',
        BOUTON_CORRIGER_LOGIMAGE: 'V',
        BOUTON_AIDE: 'H',
        BOUTON_ENLEVE_ERREURS_LOGIMAGE: None,
        BOUTON_RECOMMENCER_LOGIMAGE: None,
        BOUTON_RETOUR_SANS_ERREUR: None,
        BOUTON_COLORIER_UNE_CASE: 'I',
        BOUTON_AFFICHER_CORRECTION: None,
        BOUTON_CRAYON: 'C',
        BOUTON_EFFACER_TOUT_CRAYON: 'E',
        BOUTON_POINTEUR: 'P'
    }
}

LISTE_ORDRE_BOUTONS_MODE = {
    MODE_LOGIMAGE_CREER: [
        BOUTON_AJOUT_LIGNE,
        BOUTON_AJOUT_COLONNE,
        BOUTON_AJOUT_GROUPE_LIGNES,
        BOUTON_AJOUT_GROUPE_COLONNES,
        BOUTON_SUPPR_LIGNE,
        BOUTON_SUPPR_COLONNE,
        BOUTON_SUPPR_GROUPE_LIGNES,
        BOUTON_SUPPR_GROUPE_COLONNES,
        BOUTON_TESTER_LOGIMAGE_CREATION,
        BOUTON_SAUVEGARDER_LOGIMAGE
    ],
    MODE_LOGIMAGE_RENTRE: [
        BOUTON_AJOUT_LIGNE,
        BOUTON_AJOUT_COLONNE,
        BOUTON_AJOUT_GROUPE_LIGNES,
        BOUTON_AJOUT_GROUPE_COLONNES,
        BOUTON_SUPPR_LIGNE,
        BOUTON_SUPPR_COLONNE,
        BOUTON_SUPPR_GROUPE_LIGNES,
        BOUTON_SUPPR_GROUPE_COLONNES,
        BOUTON_TESTER_LOGIMAGE_CREATION,
        BOUTON_SAUVEGARDER_LOGIMAGE
    ],
    MODE_LOGIMAGE_FAIT: [
        BOUTON_CORRIGER_LOGIMAGE,
        BOUTON_ENLEVE_ERREURS_LOGIMAGE,
        BOUTON_RETOUR_SANS_ERREUR,
        BOUTON_AFFICHER_CORRECTION,
        BOUTON_AIDE,
        BOUTON_COLORIER_UNE_CASE,
        BOUTON_RECOMMENCER_LOGIMAGE,
        BOUTON_CRAYON,
        BOUTON_EFFACER_TOUT_CRAYON,
        BOUTON_POINTEUR,
        BOUTON_SAUVEGARDER_LOGIMAGE
    ]
}

LISTE_BOUTON_ACCUEIL = [BOUTON_MODE_LOGIMAGE_FAIT,
                        BOUTON_MODE_LOGIMAGE_CREER,
                        BOUTON_MODE_LOGIMAGE_RENTRE,
                        BOUTON_MODE_LOGIMAGE_IMPR]

COULEUR_SUPPRESSION = ROUGE, 130
COULEUR_AJOUT = VERT, 150
COEF_ECART_TAILLE_TRAI_AJOUT = 0.2

TAILLE_POLICE_GROSSE_CENTREE = 170
COULEUR_ECHEC = (127, 0, 0)
COULEUR_SUCCES = (0, 127, 25)

COULEUR_CASES_ERREUR = (255, 0, 0), 180

TEXTE_BRAVO = 'BRAVO !'
TEXTE_PATIENTER_AIDE = 'Un instant ...'
TEXTE_VOIR_ERREUR_AIDE = 'Voir les erreurs !'
TAILLE_TEXTE_ACTION_CENTRE = 160

TEXTE_IMPOSSIBLE = 'IMPOSSIBLE !'
TEXTE_FAISABLE = 'FAISABLE !'
TEXTE_INFAISABLE = 'INFAISABLE ...'
TEXTE_SAUVEGARDE = 'En cours ...'

COTE_CASE_IMPR = 50
HAUTEUR_BANDEAU_TITRE_IMPR = 200
TAILLE_TEXTE_TITRE_IMPR = 180
MARGE_COTE_IMPR = 10
TEXTE_NB_ETAPES_IMPR = "Nombre d'étapes : "
# BORNES_CATEGORIES = [200, 300, 400, 600, 700, 900, 1100, 1300, 1500, 2000]
# BORNES_CATEGORIES = [200, 300, 400, 600, 700, 900, 1000, 1200, 1300, 1500, 1800, 2500]
BORNES_CATEGORIES = list(range(50, 1050, 50)) + list(range(1100, 2400, 100)) + [2500, 3000]
CATEGORIE_INFAISABLE = -1
CATEGORIE_IMPOSSIBLE = -2
CATEGORIE_PNG = -3
TEXTE_CATEGORIE_IMPOSSIBLE = "Impossibles"
TEXTE_CATEGORIE_INFAISABLE = "Infaisables"
TEXTE_CATEGORIE_PNG = "Images PNG"

# NOM_DOSSIER_SAUVEGARDE = 'Logimages/'
# NOM_DOSSIER_SAUVEGARDE = 'LogimagesGoobix/'
# NOM_DOSSIER_SAUVEGARDE = 'LogimagesPixNCross/'
NOM_DOSSIER_SAUVEGARDE = 'LogimagesGriddlers/'
NOM_DOSSIER_ENTREES_PNG = 'Entrees/ImagesPng/'
NOM_DOSSIER_IMPR = 'ImagesSortie/'
NOM_FICHIER_SAUVEGARDE = 'derniereSauvegarde.json'
NOM_DOSSIER_SAUVEGARDE_IMAGES_INF_ERREURS = 'Entrees/ImagesInfaisablesErreurs/'
NOM_DOSSIER_SAUVEGARDE_IMAGES_INFAISABLES = 'Entrees/ImagesInfaisables/'
NOM_DOSSIER_SAUVEGARDE_IMAGES_IMPOSSIBLES = 'Entrees/ImagesImpossibles/'

SUPLEMENT_NOM_FICHIER_VIERGE = '-Vierge'
SUPLEMENT_NOM_FICHIER_CORRECTION = '-Correction'

FORMAT_FICHIER_IMPR = '.png'
