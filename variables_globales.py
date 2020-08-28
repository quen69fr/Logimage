# coding: utf-8

action_logimage_ligne_possible = None
action_logimage_colonne_possible = None
action_test_creation = False
action_corriger_logimage = False
action_colorier_case = False
action_logimage_mode_crayon = False
action_pointeur = False
action_aide = False


def reset_variables_globales():
    global action_logimage_ligne_possible
    global action_logimage_colonne_possible
    global action_test_creation
    global action_corriger_logimage
    global action_colorier_case
    global action_logimage_mode_crayon
    global action_pointeur
    global action_aide
    action_logimage_ligne_possible = None
    action_logimage_colonne_possible = None
    action_test_creation = False
    action_corriger_logimage = False
    action_colorier_case = False
    action_logimage_mode_crayon = False
    action_pointeur = False
    action_aide = False


def get_action_logimage_ligne_possible():
    global action_logimage_ligne_possible
    return action_logimage_ligne_possible


def set_action_logimage_ligne_possible(valeur):
    global action_logimage_ligne_possible
    action_logimage_ligne_possible = valeur


def get_action_logimage_colonne_possible():
    global action_logimage_colonne_possible
    return action_logimage_colonne_possible


def set_action_logimage_colonne_possible(valeur):
    global action_logimage_colonne_possible
    action_logimage_colonne_possible = valeur


def get_action_test_creation():
    global action_test_creation
    return action_test_creation


def set_action_test_creation(valeur):
    global action_test_creation
    action_test_creation = valeur


def get_action_corriger_logimage():
    global action_corriger_logimage
    return action_corriger_logimage


def set_action_corriger_logimage(valeur):
    global action_corriger_logimage
    action_corriger_logimage = valeur


def get_action_colorier_case():
    global action_colorier_case
    return action_colorier_case


def set_action_colorier_case(valeur):
    global action_colorier_case
    action_colorier_case = valeur


def get_action_logimage_mode_crayon():
    global action_logimage_mode_crayon
    return action_logimage_mode_crayon


def set_action_logimage_mode_crayon(valeur):
    global action_logimage_mode_crayon
    action_logimage_mode_crayon = valeur


def get_action_pointeur():
    global action_pointeur
    return action_pointeur


def set_action_pointeur(valeur):
    global action_pointeur
    action_pointeur = valeur


def get_action_aide():
    global action_aide
    return action_aide


def set_action_aide(valeur):
    global action_aide
    action_aide = valeur
