# coding: utf-8

from logimage import *
from titre import *


class Fenetre:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(CAPTION)
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        self.running = True
        self.x_souris, self.y_souris = 0, 0
        self.titre = Titre()
        self.grille = Grille()

        self.liste_boutons = []
        nb_bouton = len(LISTE_ORDRE_BOUTONS)
        largeur_bouton = MARGE_GRILLE_BORD_GAUCHE - 2 * MARGE_BOUTON
        hauteur_bouton = (HAUTEUR - MARGE_BOUTON * (nb_bouton + 1)) / nb_bouton
        x_bouton = LARGEUR - MARGE_GRILLE_BORD_GAUCHE + MARGE_BOUTON
        for i, type_bouton in enumerate(LISTE_ORDRE_BOUTONS):
            y_bouton = int(MARGE_BOUTON + i * (hauteur_bouton + MARGE_BOUTON))
            self.liste_boutons.append(Bouton(x_bouton, y_bouton, largeur_bouton, int(hauteur_bouton), type_bouton))

    def gere_eventements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                self.titre.gere_clavier(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.grille.gere_clic(self.x_souris, self.y_souris)
                self.titre.gere_clic(self.x_souris, self.y_souris)

                for bouton in self.liste_boutons:
                    if bouton.clic(self.x_souris, self.y_souris):
                        if bouton.type == BOUTON_AJOUT_COLONNE:
                            self.grille.mode_ajout_colonne = not self.grille.mode_ajout_colonne
                            self.grille.mode_suppression_colonne = False
                            self.grille.mode_suppression_ligne = False
                            self.grille.mode_suppression_groupe_colonnes = False
                            self.grille.mode_suppression_groupe_lignes = False
                            self.grille.mode_ajout_groupe_colonnes = False
                        elif bouton.type == BOUTON_AJOUT_LIGNE:
                            self.grille.mode_ajout_ligne = not self.grille.mode_ajout_ligne
                            self.grille.mode_suppression_colonne = False
                            self.grille.mode_suppression_ligne = False
                            self.grille.mode_suppression_groupe_colonnes = False
                            self.grille.mode_suppression_groupe_lignes = False
                            self.grille.mode_ajout_groupe_lignes = False
                        elif bouton.type == BOUTON_SUPPR_COLONNE:
                            self.grille.mode_suppression_colonne = not self.grille.mode_suppression_colonne
                            self.grille.mode_ajout_colonne = False
                            self.grille.mode_ajout_ligne = False
                            self.grille.mode_ajout_groupe_colonnes = False
                            self.grille.mode_ajout_groupe_lignes = False
                            self.grille.mode_suppression_groupe_colonnes = False
                        elif bouton.type == BOUTON_SUPPR_LIGNE:
                            self.grille.mode_suppression_ligne = not self.grille.mode_suppression_ligne
                            self.grille.mode_ajout_colonne = False
                            self.grille.mode_ajout_ligne = False
                            self.grille.mode_ajout_groupe_colonnes = False
                            self.grille.mode_ajout_groupe_lignes = False
                            self.grille.mode_suppression_groupe_lignes = False
                        elif bouton.type == BOUTON_AJOUT_GROUPE_COLONNES:
                            self.grille.mode_ajout_groupe_colonnes = not self.grille.mode_ajout_groupe_colonnes
                            self.grille.mode_suppression_colonne = False
                            self.grille.mode_suppression_ligne = False
                            self.grille.mode_suppression_groupe_colonnes = False
                            self.grille.mode_suppression_groupe_lignes = False
                            self.grille.mode_ajout_colonne = False
                        elif bouton.type == BOUTON_AJOUT_GROUPE_LIGNES:
                            self.grille.mode_ajout_groupe_lignes = not self.grille.mode_ajout_groupe_lignes
                            self.grille.mode_suppression_colonne = False
                            self.grille.mode_suppression_ligne = False
                            self.grille.mode_suppression_groupe_colonnes = False
                            self.grille.mode_suppression_groupe_lignes = False
                            self.grille.mode_ajout_ligne = False
                        elif bouton.type == BOUTON_SUPPR_GROUPE_COLONNES:
                            self.grille.mode_suppression_groupe_colonnes = \
                                not self.grille.mode_suppression_groupe_colonnes
                            self.grille.mode_ajout_colonne = False
                            self.grille.mode_ajout_ligne = False
                            self.grille.mode_ajout_groupe_colonnes = False
                            self.grille.mode_ajout_groupe_lignes = False
                            self.grille.mode_suppression_colonne = False
                        elif bouton.type == BOUTON_SUPPR_GROUPE_LIGNES:
                            self.grille.mode_suppression_groupe_lignes = not self.grille.mode_suppression_groupe_lignes
                            self.grille.mode_ajout_colonne = False
                            self.grille.mode_ajout_ligne = False
                            self.grille.mode_ajout_groupe_colonnes = False
                            self.grille.mode_ajout_groupe_lignes = False
                            self.grille.mode_suppression_ligne = False
                        elif bouton.type == BOUTON_CREER_LOGIMAGE:
                            Logimage(self.grille, self.titre.texte)
                        break

            elif event.type == pygame.MOUSEMOTION:
                self.x_souris, self.y_souris = pygame.mouse.get_pos()

    def update(self):
        self.gere_eventements()

    def affiche(self):
        self.screen.fill(COULEUR_FOND)
        self.grille.affiche(self.screen)
        self.grille.affiche_select(self.screen, self.x_souris, self.y_souris)
        for bouton in self.liste_boutons:
            bouton.affiche(self.screen)
        self.titre.affiche(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
