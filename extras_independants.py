# coding: utf-8

from logimage import *


def creer_logimage_a_partir_png(chemin_image: str, titre: str, save_erreur=False):
    # Images : https://fr.goobix.com/jeux-en-ligne/nonograms/?s=-
    image = pygame.image.load(chemin_image)
    largeur, hauteur = image.get_size()
    logimage = create_logimage_nouveau(MODE_LOGIMAGE_CREER, (largeur, hauteur), titre)
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if image.get_at((colonne, ligne)) == NOIR:
                logimage.set_case_grille(ligne, colonne, True)
    if logimage.teste_coherence_sequences:
        if logimage.sauvegarde_logimage('Entrees/ImagesReussies/'):
            if logimage.possible:
                if logimage.faisable:
                    print(f'{titre} --> FAISABLE : {logimage.titre.titre_sauvegarde} !')
                else:
                    print(f'{titre} --> INFAISABLE : {logimage.titre.titre_sauvegarde}')
            else:
                print(f'{titre} --> INCOHERENT --> Théoriquement impossible !!')
            return True
        else:
            if save_erreur:
                pygame.image.save(image, f'Entrees/ImagesPasReussies/{logimage.titre.titre_sauvegarde[:-5]}.png')
                print(f'{titre} --> ECHEC : {logimage.titre.titre_sauvegarde[:-5]}.png (saved)')
            else:
                print(f'{titre} --> ECHEC : {logimage.titre.titre_sauvegarde[:-5]}.png (not saved)')
            return False
    else:
        pygame.image.save(image, f'Entrees/ImagesIncohérentes/{logimage.titre.titre_sauvegarde[:-5]}.png')
        print(f'{titre} --> INCOHERENT : {logimage.titre.titre_sauvegarde[:-5]}.png (saved)')
        return True


def impr_dic_logimage_logimage_sequences(chemin_image: str, titre: str):
    # Correcteur : http://a.teall.info/nonogram/
    image = pygame.image.load(chemin_image)
    largeur, hauteur = image.get_size()
    logimage = create_logimage_nouveau(MODE_LOGIMAGE_CREER, (largeur, hauteur), titre)
    for ligne in range(hauteur):
        for colonne in range(largeur):
            if image.get_at((colonne, ligne)) == NOIR:
                logimage.set_case_grille(ligne, colonne, True)
    print(str({"ver": logimage.sequences_lignes,
               "hor": logimage.sequences_colonnes}).replace("'", '"').replace(' ', ''))


liste = [('Entrees/Images/AuBordDeLeau.png', "Au bord de l'eau"),
         ('Entrees/Images/AuReveil.png', 'Au reveil !'),
         ('Entrees/Images/Baballe.png', 'Baballe'),
         ('Entrees/Images/BaladeEn.png', 'Balade en ...'),
         ('Entrees/Images/BallonEnÉquilibre.png', 'Ballon en équilibre'),
         ('Entrees/Images/Beugleuse.png', 'Beugleuse'),
         ('Entrees/Images/CélèbrePirate.png', 'Célèbre pirate'),
         ('Entrees/Images/DansLaPrairie.png', 'Dans la prairie ...'),
         ('Entrees/Images/DeGarde.png', '... de garde'),
         ('Entrees/Images/DePirates.png', '... de pirates'),
         ('Entrees/Images/Donald.png', 'Donald'),
         ('Entrees/Images/Egypte.png', 'Egypte'),
         ('Entrees/Images/EnMer1.png', 'En mer'),
         ('Entrees/Images/EnMontagne.png', 'En montagne'),
         ('Entrees/Images/EnRoute.png', 'En route !'),
         ('Entrees/Images/FaireLePlein.png', 'Faire le plein'),
         ('Entrees/Images/Footing.png', 'Footing ...'),
         ('Entrees/Images/GrandeAssiette.png', 'Grande assiette'),
         ('Entrees/Images/GrandRapace.png', 'Grand rapace'),
         ('Entrees/Images/GrosseCorne.png', 'Grosse corne'),
         ('Entrees/Images/GrosseVoiture.png', 'Grosse voiture'),
         ('Entrees/Images/Guerrier.png', 'Guerrier'),
         ('Entrees/Images/HouHouHooouuuu.png', 'Hou-hou-houuu'),
         ('Entrees/Images/JeuDe.png', 'Jeu de ...'),
         ('Entrees/Images/JeuneJoueur.png', 'Jeune joueur'),
         ('Entrees/Images/JoliesBouclesDoreille.png', "Jolies boucles d'oreille"),
         ('Entrees/Images/LabourerUnChamp.png', 'Labourer un champ'),
         ('Entrees/Images/LeCorbeauEtLe.png', 'Le carbeau et le ...'),
         ('Entrees/Images/LePlusGrandFelin.png', 'Le plus grand félin !'),
         ('Entrees/Images/Londres.png', 'Londres'),
         ('Entrees/Images/LumièreDansLocéan.png', "Lumière dans l'océan"),
         ('Entrees/Images/MoyenAge.png', 'Moyen Age'),
         ('Entrees/Images/OiseauMajestueux.png', 'Oiseau majestueux'),
         ('Entrees/Images/Paradisiaque.png', 'Paradisiaque'),
         ('Entrees/Images/Paysage.png', 'Paysage'),
         ('Entrees/Images/RoiDeLaSavane.png', 'Roi de la savane'),
         ('Entrees/Images/SportIndividuel.png', 'Sport individuel'),
         ('Entrees/Images/SurLaBanquise.png', 'Sur la banquise'),
         ('Entrees/Images/TasDeBoue.png', 'Tas de boue'),
         ('Entrees/Images/TournoisDuMoyenAge.png', 'Tournoi au Moyen Age'),
         ('Entrees/Images/TraverserDeLaManche.png', 'Traversée de la Manche'),
         ('Entrees/Images/UneÉlectrique.png', 'Une ... élecrtique'),
         ('Entrees/Images/UnGrandCompagnon.png', 'Un grand compagnon'),
         ('Entrees/Images/UnNoirEtBlanc.png', 'Noir et blanc'),
         ('Entrees/Images/UnToutPetit.png', 'Un tout petit ...'),
         ('Entrees/Images/AuClairDeLune.png', 'Au clair de la Lune'),
         ('Entrees/Images/Cartes.png', 'Cartes ...'),
         ('Entrees/Images/EnMilieuUrbain.png', 'En milieu urbain'),
         ('Entrees/Images/JolieFleure.png', 'Jolie fleure'),
         ('Entrees/Images/ManifiqueOiseau.png', 'Manifique oiseau'),
         ('Entrees/Images/OursEnPeluche.png', 'Ours en peluche'),
         ('Entrees/Images/QuelSon.png', 'Quel son !'),
         ('Entrees/Images/Sherif.png', 'Shérif'),
         ('Entrees/Images/SportSurLherbe.png', 'Sport sur herbe'),
         ('Entrees/Images/UnPeuDambiance.png', "Un peu d'ambiance !"),
         ('Entrees/Images/UnPeuDePatience.png', 'Un peu de patience')]

# liste = []
# for chemin in ['Entrees/Images', 'Entrees/Images2']:
#     for img in os.listdir(chemin):
#         liste.append((f'{chemin}/{img}', input(f'{img} : ')))

pygame.init()

# for chemin, titre_logimage in liste:
#     creer_logimage_a_partir_png(chemin, titre_logimage)

# impr_dic_logimage_logimage_sequences('Entrees/Images/UnPeuDambiance.png', "Un peu d'ambiance !")
# creer_logimage_a_partir_png('Entrees/Images/UnPeuDambiance.png', "Un peu d'ambiance !")

pygame.quit()
