# coding: utf-8

import numpy
from logimage import *


def activation_function(x: float):
    return max(0., x)


v_activation_function = numpy.vectorize(activation_function)


def activation_function_derivitive(x: float):
    return 1


v_activation_function_derivitive = numpy.vectorize(activation_function_derivitive)


def shuffle_data(data: tuple):
    entries, answers = data
    range_state = numpy.random.get_state()
    numpy.random.shuffle(entries)
    numpy.random.set_state(range_state)
    numpy.random.shuffle(answers)
    return list(entries), list(answers)


class Network:
    def __init__(self, sizes: list):
        self.sizes = sizes
        self.num_layers = len(self.sizes)

        self.weights = [numpy.random.uniform(-1., 1., (n2, n1))
                        for n1, n2 in zip(self.sizes[:-1], self.sizes[1:])]
        self.biases = [numpy.random.uniform(-1., 1., (n, 1))
                       for n in self.sizes[1:]]

    def save_network(self, path: str):
        with open(path, "w") as file:
            json.dump([self.sizes,
                       [weight.tolist() for weight in self.weights],
                       [bias.tolist() for bias in self.biases]], file)

    def load_network(self, path: str):
        with open(path, "r") as file:
            params = json.load(file)
        self.sizes = params[0]
        self.num_layers = len(self.sizes)
        self.weights = [numpy.array(weight) for weight in params[1]]
        self.biases = [numpy.array(bias) for bias in params[2]]

    def feedforward(self, entry: numpy.ndarray):
        layer = entry.reshape((self.sizes[0], 1))
        for i, weight in enumerate(self.weights):
            layer = numpy.dot(weight, layer) + self.biases[i]
            layer = v_activation_function(layer)
        return layer

    def evaluate(self, test_data: tuple, num_tests: int):
        entries, answers = shuffle_data(test_data)
        num_successes = 0
        for entry, answer in zip(entries[:num_tests], answers[:num_tests]):
            if numpy.argmax(self.feedforward(entry)) == answer:
                num_successes += 1
        return num_successes / num_tests

    def train_network(self, training_data: tuple, list_num_data: list, list_num_updates: list, list_coef_step: list):
        entries, answers = shuffle_data(training_data)
        num_tot_data = len(entries)
        idx = 0
        for num_updates, num_data, coef_step in zip(list_num_updates, list_num_data, list_coef_step):
            for _ in range(num_updates):
                if idx + num_data > num_tot_data:
                    update_images = entries[idx:num_tot_data]
                    update_answers = answers[idx:num_tot_data]
                    entries, answers = shuffle_data(training_data)
                    idx = idx + num_data - num_tot_data
                    self.update_network(update_images + entries[0:idx], update_answers + answers[0:idx], coef_step)
                else:
                    self.update_network(entries[idx:idx + num_data], answers[idx:idx + num_data], coef_step)
                    idx += num_data

    def update_network(self, entries: list, aswers: list, coef_step: float):
        delta_weights = [numpy.zeros(weight.shape) for weight in self.weights]
        delta_biases = [numpy.zeros(bias.shape) for bias in self.biases]
        for entry, answer in zip(entries, aswers):
            single_delta_weights, single_delta_biases = self.backpropagation(entry, answer)
            delta_weights = [delta_weight + single_delta_weight
                             for delta_weight, single_delta_weight in zip(delta_weights, single_delta_weights)]
            delta_biases = [delta_bias + single_delta_bias
                            for delta_bias, single_delta_bias in zip(delta_biases, single_delta_biases)]
        num_images = len(entries)
        coef = coef_step / num_images
        self.weights = [weight + coef * delta_weight for weight, delta_weight in zip(self.weights, delta_weights)]
        self.biases = [bias + coef * delta_bias for bias, delta_bias in zip(self.biases, delta_biases)]

    def backpropagation(self, entry: numpy.ndarray, answer: numpy.ndarray):
        # feedforward
        layer = entry.reshape((self.sizes[0], 1))
        neurons = []
        neurons_squeezed = [layer]
        for i, weight in enumerate(self.weights):
            layer = numpy.dot(weight, layer) + self.biases[i]
            neurons.append(layer)
            layer = v_activation_function(layer)
            neurons_squeezed.append(layer)

        # backpropagation
        delta_neurons = v_activation_function_derivitive(neurons[-1]) * (answer - neurons_squeezed[-1])
        delta_weights = [numpy.dot(delta_neurons, neurons_squeezed[-2].transpose())]
        delta_biases = [delta_neurons]

        for idx in range(2, self.num_layers):
            delta_neurons = v_activation_function_derivitive(neurons[-idx]) * \
                            numpy.dot(self.weights[-idx+1].transpose(), delta_neurons)
            delta_biases.insert(0, delta_neurons)
            delta_weights.insert(0, numpy.dot(delta_neurons, neurons_squeezed[-idx-1].transpose()))

        return delta_weights, delta_biases


TAILLE_LOGIMAGE_CORRECTION_NEURAL_NETWORK = 50
LISTE_LAYERS_CORRECTION_NEURAL_NETWORK = [TAILLE_LOGIMAGE_CORRECTION_NEURAL_NETWORK * 2, 50, 20, 1]
NOM_FICHIER_SAVE_NETWORK = "neural_network_logimages_50x50.json"


def RATE_ANSWER(nb_cases_trouvees: int, duree: float):
    if duree <= 0.000001:
        return 100000
    return max(nb_cases_trouvees / duree, 100000)


def ligne_to_numpy_array_entry(ligne, correction):
    return numpy.array([0 if case == CASE_INCONNUE else 1 for case in ligne] + [case for case in correction])


def rate_to_numpy_array_answer(rate: float):
    return numpy.array([[rate]])


def new_network():
    return Network(LISTE_LAYERS_CORRECTION_NEURAL_NETWORK)


def load_network(network: Network = None):
    if network is None:
        return new_network().load_network(NOM_FICHIER_SAVE_NETWORK)
    return network.load_network(NOM_FICHIER_SAVE_NETWORK)


def train_network(network: Network, lignes: list, corrections: list,
                  liste_nb_cases_trouvees: list, liste_durees: list):
    network.train_network(([ligne_to_numpy_array_entry(ligne, correction)
                            for ligne, correction in zip(lignes, corrections)],
                           [rate_to_numpy_array_answer(RATE_ANSWER(nb_cases_trouvees, duree))
                            for nb_cases_trouvees, duree in zip(liste_nb_cases_trouvees, liste_durees)]),
                          [10, 50, 100], [2000, 200, 120], [5, 10, 15])


def rate_ligne(network: Network, ligne: list, correction: list):
    return float(network.feedforward(ligne_to_numpy_array_entry(ligne, correction))[0][0])


class Logimage50x50NeuralNatwork(Logimage):
    def create_trainig_data(self, liste_lignes, liste_corrections, liste_nb_cases_trouvees, liste_durees):
        if self.corrige is None or not self.possible or not self.faisable:
            return
        clear_possibilitees_pour_x_sur_n()

        self.logimage_correction_progressive = Logimage([[CASE_INCONNUE for _ in range(self.nb_colonnes)]
                                                         for _ in range(self.nb_lignes)], self.sequences_lignes,
                                                        self.sequences_colonnes, MODE_LOGIMAGE_CORRECTION, None,
                                                        f'CORRECTION : {self.titre.texte}', 'Inutile')
        cases = self.logimage_correction_progressive.cases
        cases_ordonnees_colonnes = self.logimage_correction_progressive.cases_ordonnees_colonnes

        self.possible = self.teste_coherence_sequences()

        self.nb_etapes_ordinateur = 0

        lignes_colonnes_a_tester = {}
        liste_lignes_colonnes_a_tester_grossierement = []
        for i in range(self.nb_lignes):
            lignes_colonnes_a_tester[(True, i)] = calcul_score_ligne(cases[i], self.sequences_lignes[i])
            liste_lignes_colonnes_a_tester_grossierement.append((True, i))
        for j in range(self.nb_colonnes):
            lignes_colonnes_a_tester[(False, j)] = calcul_score_ligne(cases_ordonnees_colonnes[j],
                                                                      self.sequences_colonnes[j])
            liste_lignes_colonnes_a_tester_grossierement.append((False, j))

        while len(lignes_colonnes_a_tester) > 0:
            ligne_ou_pas, n = min(lignes_colonnes_a_tester,
                                  key=lambda key: lignes_colonnes_a_tester[key][0] * COEF_RENTABILITE_METHODE_1
                                  if (lignes_colonnes_a_tester[key][1] and
                                      lignes_colonnes_a_tester[key][0] < SEUIL_MAX_METODE_RECURSIVE_SANS_MEMOIRE)
                                  else lignes_colonnes_a_tester[key][0])
            nb_possibilites, methode_1_ou_2 = lignes_colonnes_a_tester[(ligne_ou_pas, n)]
            if nb_possibilites < SEUIL_RENTABILITE_METHODE_GROSSIERE or \
                    len(liste_lignes_colonnes_a_tester_grossierement) == 0:
                del lignes_colonnes_a_tester[(ligne_ou_pas, n)]
                if (ligne_ou_pas, n) in liste_lignes_colonnes_a_tester_grossierement:
                    liste_lignes_colonnes_a_tester_grossierement.remove((ligne_ou_pas, n))
                methode_grossiere = False
            elif len(liste_lignes_colonnes_a_tester_grossierement) == 0:
                break
            else:
                ligne_ou_pas, n = liste_lignes_colonnes_a_tester_grossierement[0]
                del liste_lignes_colonnes_a_tester_grossierement[0]
                methode_grossiere = True
            self.logimage_correction_progressive.ligne_ou_colonne_en_cours = ligne_ou_pas, n

            if ligne_ou_pas:
                ligne = cases[n]
                liste_nbs = self.sequences_lignes[n]

                if CASE_INCONNUE not in ligne:
                    continue

                if methode_grossiere:
                    liste_cases_communes = trouve_cases_communes_grossierement(ligne, liste_nbs)
                else:
                    liste_cases_communes = trouve_cases_communes_intelligent(ligne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                un_seul_bloc = False
                if len(liste_cases_communes) > 0:
                    un_seul_bloc = test_cases_inconnues_d_un_seul_bloc(ligne)
                    self.nb_etapes_ordinateur += 1
                    for j, valeur in liste_cases_communes:
                        self.logimage_correction_progressive.set_case_grille(n, j, valeur)
                        lignes_colonnes_a_tester[(False, j)] = \
                            calcul_score_ligne(cases_ordonnees_colonnes[j], self.sequences_colonnes[j])
                        if (False, j) not in liste_lignes_colonnes_a_tester_grossierement:
                            liste_lignes_colonnes_a_tester_grossierement.append((False, j))
                        if not un_seul_bloc:
                            un_seul_bloc = test_cases_inconnues_d_un_seul_bloc(ligne)
                if methode_grossiere and (True, n) in lignes_colonnes_a_tester and un_seul_bloc:
                    del lignes_colonnes_a_tester[(True, n)]

            else:
                colonne = cases_ordonnees_colonnes[n]
                liste_nbs = self.sequences_colonnes[n]
                if CASE_INCONNUE not in colonne:
                    continue

                if methode_grossiere:
                    liste_cases_communes = trouve_cases_communes_grossierement(colonne, liste_nbs)
                else:
                    liste_cases_communes = trouve_cases_communes_intelligent(colonne, liste_nbs,
                                                                             methode_1_ou_2, nb_possibilites)

                un_seul_bloc = False
                if len(liste_cases_communes) > 0:
                    un_seul_bloc = test_cases_inconnues_d_un_seul_bloc(colonne)
                    self.nb_etapes_ordinateur += 1
                    for i, valeur in liste_cases_communes:
                        self.logimage_correction_progressive.set_case_grille(i, n, valeur)
                        lignes_colonnes_a_tester[(True, i)] = \
                            calcul_score_ligne(cases[i], self.sequences_lignes[i])
                        if (True, i) not in liste_lignes_colonnes_a_tester_grossierement:
                            liste_lignes_colonnes_a_tester_grossierement.append((True, i))
                        if not un_seul_bloc:
                            un_seul_bloc = test_cases_inconnues_d_un_seul_bloc(colonne)
                if methode_grossiere and (False, n) in lignes_colonnes_a_tester and un_seul_bloc:
                    del lignes_colonnes_a_tester[(False, n)]

        for (ligne_ou_pas, num), (nb_possibilites, methode_1_ou_2) in lignes_colonnes_a_tester.items():
            if ligne_ou_pas:
                ligne = cases[num]
                correction = self.corrige[num]
                sequence = self.sequences_lignes[num]
            else:
                ligne = cases_ordonnees_colonnes[num]
                correction = [li[num] for li in self.corrige]
                sequence = self.sequences_colonnes[num]

            t0 = time.time()
            liste_lignes.append(ligne)
            liste_corrections.append(correction)
            liste_nb_cases_trouvees.append(len(trouve_cases_communes_intelligent(ligne, sequence,
                                                                                 methode_1_ou_2,
                                                                                 nb_possibilites)))
            liste_durees.append(time.time() - t0)
