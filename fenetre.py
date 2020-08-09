# coding: utf-8

from logimage import *
import math


class Fenetre:
    def __init__(self):
        pygame.display.set_caption(CAPTION)
        self.full_screen = FULL_SCREEN
        self.screen = None
        self.update_full_screen()
        self.running = True
        self.x_souris, self.y_souris = 0, 0
        self.mouse_button_down = False

        self.mode = MODE_ACCUEIL

        self.logimage = None
        self.liste_boutons_logimage = []

        self.bouton_revenir_accueil = Bouton(MARGE_BOUTON, MARGE_BOUTON, int(TAILLE_TITRE * 2.4),
                                             int(TAILLE_TITRE * 0.85 - MARGE_BOUTON), BOUTON_REVENIR_ACCUEIL)
        self.bouton_full_screen = Bouton(MARGE_BOUTON, MARGE_BOUTON, int(TAILLE_TITRE * 2.4),
                                         int(TAILLE_TITRE * 0.85 - MARGE_BOUTON), BOUTON_FULL_SCREEN)

        self.boutons_accueil = []
        nb_boutons_accueil = len(LISTE_BOUTON_ACCUEIL)
        largeur_bouton = LARGEUR // 2.2
        hauteur_bouton = HAUTEUR // (nb_boutons_accueil + 3)
        x_bouton = int(LARGEUR / 2 - largeur_bouton / 2)
        y_bouton = int((HAUTEUR - TAILLE_TITRE_PRINCIPAL) / 2 - hauteur_bouton * (nb_boutons_accueil / 2) -
                       MARGE_BOUTON * 2 + TAILLE_TITRE_PRINCIPAL)
        for bouton in LISTE_BOUTON_ACCUEIL:
            self.boutons_accueil.append(Bouton(x_bouton, y_bouton, largeur_bouton, hauteur_bouton, bouton))
            y_bouton += hauteur_bouton + MARGE_BOUTON

        self.liste_vignettes_choisi_logimage = []

        self.mode_logimage = None

    def update_full_screen(self):
        if self.full_screen:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

    def new_logimage(self, logimage: Logimage):
        self.logimage = logimage
        reset_variables_globales()
        self.mode = MODE_LOGIMAGE

        self.liste_boutons_logimage = []
        nb_bouton = len(LISTE_ORDRE_BOUTONS_MODE[self.mode])
        if nb_bouton > 0:
            largeur_bouton = MARGE_GRILLE_BORD_GAUCHE - 2 * MARGE_BOUTON
            hauteur_bouton = (HAUTEUR - MARGE_BOUTON * (nb_bouton + 1)) / nb_bouton
            x_bouton = LARGEUR - MARGE_GRILLE_BORD_GAUCHE + MARGE_BOUTON
            for i, type_bouton in enumerate(LISTE_ORDRE_BOUTONS_MODE[self.logimage.mode_logimage]):
                y_bouton = int(MARGE_BOUTON + i * (hauteur_bouton + MARGE_BOUTON))
                self.liste_boutons_logimage.append(Bouton(x_bouton, y_bouton, largeur_bouton,
                                                          int(hauteur_bouton), type_bouton))

    def mode_choisi_logimage(self):
        self.mode = MODE_CHOISI_LOGIMAGE
        liste_vignettes = []
        for titre_sauvegarde_logimage in os.listdir(NOM_DOSSIER_SAUVEGARDE):
            with open(NOM_DOSSIER_SAUVEGARDE + titre_sauvegarde_logimage, "r") as sauvegarde_logimage:
                dict_logimage = json.load(sauvegarde_logimage)
                if (dict_logimage[PARAM_LOGIMAGE_POSSIBLE] and dict_logimage[PARAM_LOGIMAGE_FAISABLE] and
                    not dict_logimage[PARAM_LOGIMAGE_MODE] == MODE_LOGIMAGE_FAIT) or \
                        self.mode_logimage == dict_logimage[PARAM_LOGIMAGE_MODE]:
                    liste_vignettes.append((titre_sauvegarde_logimage,
                                            dict_logimage[PARAM_LOGIMAGE_NOM],
                                            dict_logimage[PARAM_LOGIMAGE_DIMENTIONS],
                                            dict_logimage[PARAM_LOGIMAGE_POSSIBLE],
                                            dict_logimage[PARAM_LOGIMAGE_FAISABLE],
                                            dict_logimage[PARAM_LOGIMAGE_MODE] == MODE_LOGIMAGE_FAIT))
        liste_vignettes.sort(key=lambda logimage: 0 if logimage[5] else 1 if not logimage[3]
                             else (logimage[2][0] * logimage[2][1]) if logimage[4] else 2)
        if self.mode_logimage == MODE_LOGIMAGE_CREER or self.mode_logimage == MODE_LOGIMAGE_RENTRE:
            liste_vignettes.insert(0, (NOM_NOUVEAU_LOGIMAGE, NOM_NOUVEAU_LOGIMAGE, None, None, None, False))
        if len(liste_vignettes) == 0:
            self.mode = MODE_ACCUEIL
            return
        nb_vignettes = len(liste_vignettes)
        nb_colonnes = math.ceil(math.sqrt(nb_vignettes))
        x_min = MARGE_BOUTON * 2
        y_min = int(MARGE_BOUTON + TAILLE_TITRE * 0.85)
        hauteur = (HAUTEUR - MARGE_BOUTON - y_min) // nb_colonnes - MARGE_BOUTON
        largeur = (LARGEUR - MARGE_BOUTON - x_min) // nb_colonnes - MARGE_BOUTON
        self.liste_vignettes_choisi_logimage = []
        i = 0
        for ligne in range(nb_colonnes):
            for colonne in range(nb_colonnes):
                nom, titre, dimentions, possible, faisable, sauvegarde = liste_vignettes[i]
                self.liste_vignettes_choisi_logimage.append(
                    VignetteLogimage(nom, (x_min + colonne * (largeur + MARGE_BOUTON),
                                           y_min + ligne * (hauteur + MARGE_BOUTON), largeur, hauteur),
                                     titre, dimentions, possible, faisable, sauvegarde))
                i += 1
                if i >= nb_vignettes:
                    return

    def fait_actions_boutons(self, bouton):
        if self.mode == MODE_ACCUEIL:
            if bouton.type == BOUTON_MODE_LOGIMAGE_CREER:
                self.mode_logimage = MODE_LOGIMAGE_CREER
            elif bouton.type == BOUTON_MODE_LOGIMAGE_RENTRE:
                self.mode_logimage = MODE_LOGIMAGE_RENTRE
            elif bouton.type == BOUTON_MODE_LOGIMAGE_IMPR:
                self.mode_logimage = MODE_LOGIMAGE_IMPR
            else:
                self.mode_logimage = MODE_LOGIMAGE_FAIT
            self.mode_choisi_logimage()
        elif self.mode == MODE_LOGIMAGE:
            if bouton.type_action == TYPE_ACTION_TESTER_LOGIMAGE:
                if get_action_test_creation():
                    set_action_test_creation(False)
                else:
                    self.logimage.corrige_logimage()
                    set_action_test_creation(True)
            else:
                set_action_test_creation(False)
            if bouton.type == BOUTON_SAUVEGARDER_LOGIMAGE:
                self.logimage.sauvegarde_logimage()
            elif bouton.type == BOUTON_RECOMMENCER_LOGIMAGE:
                self.logimage.mettre_toutes_cases_valeur(CASE_INCONNUE)
                self.logimage.efface_tout_crayon()
                reset_variables_globales()
            elif bouton.type == BOUTON_RETOUR_SANS_ERREUR:
                self.logimage.reprendre_dernier_cases_sans_erreurs()
            elif bouton.type == BOUTON_CORRIGER_ERREURS_LOGIMAGE:
                self.logimage.corrige_erreurs()
            elif bouton.type == BOUTON_ENLEVE_ERREURS_LOGIMAGE:
                self.logimage.enleve_erreurs()
            elif bouton.type == BOUTON_AFFICHER_CORRECTION:
                self.logimage.tout_corriger()
            elif bouton.type == BOUTON_COLORIER_UNE_CASE:
                set_action_logimage_mode_crayon(False)
            elif bouton.type == BOUTON_CRAYON:
                set_action_colorier_case(False)
            elif bouton.type == BOUTON_EFFACER_TOUT_CRAYON:
                set_action_colorier_case(False)
                self.logimage.efface_tout_crayon()

    def gere_eventements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if not (self.mode == MODE_LOGIMAGE and self.logimage.titre.selectinne):
                    if event.key == 97:  # Q
                        self.running = False
                        break
                if self.bouton_full_screen.gere_clavier(event):
                    self.full_screen = not self.full_screen
                    self.update_full_screen()
                if self.mode == MODE_ACCUEIL:
                    for bouton in self.boutons_accueil:
                        if bouton.gere_clavier(event):
                            self.fait_actions_boutons(bouton)
                            break
                elif self.mode == MODE_CHOISI_LOGIMAGE:
                    if self.bouton_revenir_accueil.gere_clavier(event):
                        self.mode = MODE_ACCUEIL
                        continue
                else:
                    if self.logimage.titre.selectinne:
                        self.logimage.titre.gere_clavier(event)
                    else:
                        if self.bouton_revenir_accueil.gere_clavier(event):
                            self.mode = MODE_ACCUEIL
                            continue
                        if self.mode == MODE_LOGIMAGE:
                            for bouton in self.liste_boutons_logimage:
                                if bouton.gere_clavier(event):
                                    self.fait_actions_boutons(bouton)
                                    break

            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_down = False
                if self.mode == MODE_ACCUEIL:
                    if self.bouton_full_screen.clic(self.x_souris, self.y_souris):
                        self.full_screen = not self.full_screen
                        self.update_full_screen()
                    for bouton in self.boutons_accueil:
                        if bouton.clic(self.x_souris, self.y_souris):
                            self.fait_actions_boutons(bouton)
                else:
                    if self.bouton_revenir_accueil.clic(self.x_souris, self.y_souris):
                        self.mode = MODE_ACCUEIL
                        break
                    if self.mode == MODE_CHOISI_LOGIMAGE:
                        for vignette in self.liste_vignettes_choisi_logimage:
                            if vignette.clic(self.x_souris, self.y_souris):
                                if self.mode_logimage == MODE_LOGIMAGE_IMPR:
                                    impr_logimage_sauvegarde(vignette.nom)
                                else:
                                    if vignette.nom == NOM_NOUVEAU_LOGIMAGE:
                                        self.new_logimage(create_logimage_nouveau(self.mode_logimage))
                                    else:
                                        self.new_logimage(create_logimage_sauvegarde(vignette.nom, self.mode_logimage))
                                break
                    else:
                        sens = -1 if (event.button == 3 or event.button == 5) else 1
                        if self.mode_logimage in [MODE_LOGIMAGE_CREER, MODE_LOGIMAGE_RENTRE]:
                            self.logimage.titre.gere_clic(self.x_souris, self.y_souris)
                        self.logimage.gere_clic_up(self.x_souris, self.y_souris, sens)

                        if sens == 1:
                            for bouton in self.liste_boutons_logimage:
                                if bouton.clic(self.x_souris, self.y_souris):
                                    self.fait_actions_boutons(bouton)
                                    break
                        else:
                            set_action_test_creation(False)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                sens = -1 if (event.button == 3 or event.button == 5) else 1
                self.mouse_button_down = sens
                if self.mode == MODE_LOGIMAGE and (event.button == 4 or event.button == 5):
                    self.logimage.gere_clic_down(self.x_souris, self.y_souris, sens)

            elif event.type == pygame.MOUSEMOTION:
                self.x_souris, self.y_souris = pygame.mouse.get_pos()

        if self.mouse_button_down:
            if self.mode == MODE_LOGIMAGE:
                self.logimage.gere_clic_down(self.x_souris, self.y_souris, self.mouse_button_down)

    def update(self):
        self.gere_eventements()

    def affiche(self):
        self.screen.fill(COULEUR_FOND)
        if self.mode == MODE_ACCUEIL:
            affiche_texte(TITRE_MODE_ACCUEIL, LARGEUR // 2, int(TAILLE_TITRE_PRINCIPAL * 0.24), self.screen,
                          taille=TAILLE_TITRE_PRINCIPAL, couleur=COULEUR_TITRE, x_0gauche_1centre_2droite=1)
            for bouton in self.boutons_accueil:
                bouton.affiche(self.screen)
            self.bouton_full_screen.affiche(self.screen)
        else:
            self.bouton_revenir_accueil.affiche(self.screen)
            if self.mode == MODE_CHOISI_LOGIMAGE:
                affiche_texte(TITRE_MODE_CHOISI_LOGIMAGE, LARGEUR // 2, int(TAILLE_TITRE * 0.2), self.screen,
                              taille=TAILLE_TITRE, couleur=COULEUR_TITRE, x_0gauche_1centre_2droite=1)
                for vignette in self.liste_vignettes_choisi_logimage:
                    vignette.affiche(self.screen)
            else:
                self.logimage.affiche(self.screen)
                self.logimage.affiche_actions(self.screen, self.x_souris, self.y_souris)
                for bouton in self.liste_boutons_logimage:
                    bouton.affiche(self.screen)
                self.logimage.titre.affiche(self.screen)
        pygame.display.update()
        pygame.time.Clock().tick(FPS)
