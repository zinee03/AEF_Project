import json
import os

class AEF:

  def __init__(self, states, alphabet, transitions, initial_states, final_states):

    self.states = states
    self.alphabet = alphabet
    self.transitions = transitions
    self.current_states = initial_states
    self.initial_states = initial_states
    self.final_states = final_states

  def transition(self, symbol):
    new_current_states = set()
    for state in self.current_states:
      if state in self.transitions and symbol in self.transitions[state]:
        transition_states = self.transitions[state][symbol]
        if isinstance(transition_states, list):
          new_current_states.update(transition_states)
        else:
          new_current_states.add(transition_states)
    self.current_states = new_current_states


  def is_in_final_state(self):
    return any(state in self.final_states for state in self.current_states)


  def is_automate_complet(self):
    for state in self.states:
      # Vérifier si l'état a des transitions définies
      if state not in self.transitions:
        return False  # S'il manque des transitions pour un état, retourner False
      for symbol in self.alphabet:
        if symbol not in self.transitions[
            state] or not self.transitions[state][symbol]:
          return False  # S'il manque une transition pour un symbole, ou si la transition est vide, retourner False
    return True


  def make_complete(self, file_path):
    # Créer un état puits
    sink_state = "sink_state"
    self.states.append(sink_state)

    # Ajouter des transitions pour l'état puits
    for state in self.states:
      if state != sink_state:
        for symbol in self.alphabet:
          if state not in self.transitions or symbol not in self.transitions[
              state] or not self.transitions[state][symbol]:
            # Si une transition est manquante pour un état ou un symbole, la diriger vers l'état puits
            if state not in self.transitions:
              self.transitions[state] = {}
            self.transitions[state][symbol] = sink_state

    # Ajouter des transitions pour l'état puits vers lui-même pour chaque symbole manquant
    self.transitions[sink_state] = {
        symbol: sink_state
        for symbol in self.alphabet
    }

    #Parcourir et afficher les transtions
    for state in self.transitions:
      for symbol in self.transitions[state]:
        destination = self.transitions[state][symbol]
        print(f"Transition: {state} --({symbol})--> {destination}")
    
    save_aef_to_file(self, file_path)


  def is_deterministic(aef):
    # Vérifier s'il y a un seul état initial
    if len(aef.initial_states) != 1:
      print("Votre AEF n'est pas déterministe !\n")
    
    else :# Si toutes les conditions sont satisfaites pour chaque état, l'automate est déterministe
        print("Votre AEF est déterministe !\n")


  def rendre_emonde(self, file_path):
    #Verifier qu'il est accessibles
    i = 0
    etats_accessibles = set()
    etats_non_traites = set(self.initial_states)
    while i != len(self.states):
      state = etats_non_traites.pop()
      etats_accessibles.add(state)

      if state in self.transitions:
        for symbol, transitions in self.transitions[state].items():
          etats_non_traites.update(transitions.split())

      i = i + 1

    #Verifier qu'il est co accessible
    visited_states = set()
    states_to_explore = set(self.final_states)

    while states_to_explore:
      current_state = states_to_explore.pop()
      visited_states.add(current_state)

      for state, transitions in self.transitions.items():
        for symbol, dest_states in transitions.items():
          if current_state in dest_states:
            if state not in visited_states:
              states_to_explore.add(state)

    #Verifier qu'il est emonde
    etats_emonde = set()
    etats_a_supprimer = set()

    for i in etats_accessibles:
      for j in visited_states:
        if i == j:
          etats_emonde.add(i)

    for i in self.states:
      if i not in etats_emonde:
        etats_a_supprimer.add(i)

    print("", etats_emonde)
    print("", etats_a_supprimer)

    # Supprimer les états
    for state in etats_a_supprimer:
      self.states.remove(state)
      if state in self.initial_states:
        self.initial_states.remove(state)
      if state in self.final_states:
        self.final_states.remove(state)

      transitions_to_delete = {}  # Pour stocker les clés à supprimer
      for transitions in self.transitions.values():
        for dest_state in transitions:
          if state in transitions[dest_state]:
            transitions[dest_state] = transitions[dest_state].replace(
                state, "")

            # Si la destination devient vide après le remplacement, marquez la transition à supprimer
            if not transitions[dest_state]:
              transitions_to_delete[dest_state] = transitions[dest_state]
      print("", transitions_to_delete)
      # Supprimer les transitions marquées pour suppression
      for dest_state in transitions_to_delete:
        if dest_state in self.transitions:
          del self.transitions[dest_state]

    print("", self.transitions)

    #Parcourir et afficher les transtions
    for state in self.transitions:
      for symbol in self.transitions[state]:
        destination = self.transitions[state][symbol]
        print(f"Transition: {state} --({symbol})--> {destination}")
    
    save_aef_to_file(self, file_path)
    

  def draw_AEF(self):
    print("\nReprésentation de l'AEF :\n")
    print(f"États : {', '.join(self.states)}")
    print(f"Alphabet : {', '.join(self.alphabet)}")
    print(f"États initiaux : {', '.join(self.initial_states)}")
    print(f"États finaux : {', '.join(self.final_states)}")
    print("Transitions :\n")

    # Créer un tableau vide pour stocker les transitions avec les états et les symboles
    table = [['' for _ in range(len(self.alphabet) + 1)]
             for _ in range(len(self.states) + 2)]

    # Ajouter les états en première colonne, en commençant à la deuxième ligne
    #table[1][0] = 'Transitions:'
    for i, state in enumerate(self.states):
      table[i + 2][0] = state

    # Ajouter les symboles en première ligne, en commençant à la deuxième colonne
    for i, symbol in enumerate(self.alphabet):
      table[0][i + 1] = symbol

    # Remplir le tableau avec les états correspondant aux transitions
    for i, state in enumerate(self.states):
      for j, symbol in enumerate(self.alphabet):
        if state in self.transitions and symbol in self.transitions[state]:
          transitions = self.transitions[state][symbol]
          if isinstance(transitions, list):
            table[i + 2][j + 1] = ', '.join(transitions)
          else:
            table[i + 2][j + 1] = transitions

    # Afficher le tableau
    for row in table:
      for cell in row:
        print('{:<15}'.format(cell), end='')
      print()  # Appel de la méthode pour afficher le tableau de transitions


  def complement_aef(self, file_path):
    # Inverser les états finaux et non finaux
    complement_final_states = set(self.states) - set(self.final_states)
    self.final_states = complement_final_states - set(self.initial_states)

    # Sauvegarder l'AEF modifié dans un fichier
    save_aef_to_file(self, file_path)
    return self  # Retourner l'objet AEF modifié


  def mirror_aef(self, file_path):
    # Échanger les états initiaux et finaux
    self.initial_states, self.final_states = self.final_states, self.initial_states

    # Inverser les transitions
    reversed_transitions = {
        state: {symbol: []
                for symbol in self.alphabet}
        for state in self.states
    }
    for from_state, symbols in self.transitions.items():
      for symbol, to_states in symbols.items():
        # Inverser chaque transition
        for to_state in to_states:
          reversed_transitions[to_state][symbol].append(from_state)

    self.transitions = reversed_transitions
    save_aef_to_file(self, file_path)
    return self  # Ajouter cette ligne pour retourner l'objet AEF modifié


  def concatenate_aef(self, other_aef, connecting_symbol, file_path):
    # Vérifier l'unicité des états
    if set(self.states).intersection(other_aef.states):
      print("Erreur : Conflit de noms d'états entre les deux AEFs.")
      return None

    # Unir les états des deux AEFs
    concatenated_states = set(self.states).union(other_aef.states)

    # Fusionner les alphabets des deux AEFs (et ajouter le symbole de connexion si nécessaire)
    concatenated_alphabet = set(self.alphabet).union(other_aef.alphabet)
    if connecting_symbol not in concatenated_alphabet:
      concatenated_alphabet.add(connecting_symbol)

    # Garder les transitions du premier AEF
    concatenated_transitions = self.transitions.copy()

    # Ajouter les transitions du second AEF
    for state in other_aef.transitions:
      concatenated_transitions[state] = other_aef.transitions[state]

    # Créer une unique transition spéciale entre les états finaux du premier AEF et les états initiaux du second AEF
    for final_state in self.final_states:
      concatenated_transitions[final_state][connecting_symbol] = next(
          iter(other_aef.initial_states))

    # Les états initiaux restent ceux du premier AEF et les états finaux sont ceux du second AEF
    concatenated_final_states = set(other_aef.final_states)

    # Créer le nouvel AEF concaténé
    concatenated_aef = AEF(states=concatenated_states,
                           alphabet=concatenated_alphabet,
                           transitions=concatenated_transitions,
                           initial_states=self.initial_states,
                           final_states=concatenated_final_states)

    # Sauvegarder l'AEF concaténé dans un fichier
    save_aef_to_file(concatenated_aef, file_path)
    return concatenated_aef
  
  
  def convert_to_deterministic(self, file_path):
      self.dfa = {}
      new_states_list = []
      keys_list = ["".join(self.initial_states)]
      path_list = list(self.alphabet)

      self.dfa[keys_list[0]] = {}

      for y in range(len(path_list)):
          var = "".join(self.transitions[keys_list[0][0]][path_list[y]])
          self.dfa[keys_list[0]][path_list[y]] = var
          if var not in keys_list:
              new_states_list.append(var)
              keys_list.append(var)

      while len(new_states_list) != 0:
        self.dfa[new_states_list[0]] = {}
        for _ in range(len(new_states_list[0])):
            for i in range(len(path_list)):
              temp = []
              for j in range(len(new_states_list[0])):
                  temp += self.transitions[new_states_list[0][j]][path_list[i]]
                  s = "".join(temp)
                  if s not in keys_list:
                      new_states_list.append(s)
                      keys_list.append(s)
                  self.dfa[new_states_list[0]][path_list[i]] = s

        new_states_list.remove(new_states_list[0])

      # Print the new AFD
      # print("\nPrint AFD_table: ")
      # dfa_table = pd.DataFrame(self.dfa)
      # print(dfa_table.transpose())

      dfa_states_list = list(self.dfa.keys())
      dfa_final_states = []

      for dfa_state in dfa_states_list:
          nfa_states_in_dfa_state = set()

          for state in dfa_state:
              nfa_states_in_dfa_state.update(state)

          if any(state in self.final_states for state in nfa_states_in_dfa_state):
              dfa_final_states.append(dfa_state)

      print("\nFinal state of the defined automate (AFD): ", dfa_final_states)
      print(self.dfa)
      save_aef_to_file(self, file_path)
  

  def is_accepted(self, file_path):
    if check_variables_non_empty(self, file_path) == True:
        word = input("Entrez un mot : ")
        for symbol in word:
            self.transition(symbol)

        if self.is_in_final_state():
            print(f"Le mot '{word}' est accepté.")
        else:
            print(f"Le mot '{word}' n'est pas accepté.")
    else:
        print("Aucun AEF d'enregistré !")
    
    
    


def is_file_empty(file_path):
    try:
      with open(file_path, 'r') as file:
        file_content = file.read().strip()
        return not file_content  # Renvoie True si le fichier est vide
    except FileNotFoundError:
      print(f"Le fichier '{file_path}' n'existe pas.")
    except Exception as e:
      print(f"Une erreur s'est produite lors de la lecture du fichier : {e}")


def check_variables_non_empty(aef, file_path):
    if aef == None: 
      print("Votre AEF n'est pas défini !\n")
      return False
    if is_file_empty(file_path):
      print("Le fichier est vide !")
      return False

    # Autres vérifications ici pour les variables de l'AEF
    if not aef.states or not aef.alphabet or not aef.transitions or not aef.initial_states or not aef.final_states:
      print("Certains champs de l'AEF sont vides.")
      return False
    else:
      return True


def generer_systeme_equations(aef):
  systeme = {}
  for etat in aef.states:
      left_member = f"{etat} = "
      right_member = ""
      transitions = aef.transitions.get(etat, {})
      count = 0
 
      for symbole, destination in transitions.items():
          count += 1
          right_member += f"{symbole}{destination}"
          if count < len(transitions):
              right_member += " + "
 
      if etat in aef.final_states:
          if count == 0:
              right_member = "ε"
          else:
              right_member += " + ε"
 
      systeme[etat] = left_member + right_member
 
  return systeme
 
 
def appliquer_lemme_arden(systeme, etat):
  equation = systeme[etat]
  parties = equation.split(' + ')
  partie_recursive = [part for part in parties if etat in part]
  partie_non_recursive = [part for part in parties if etat not in part]
 
  if partie_recursive:
      partie_recursive = [part.replace(etat, '') for part in partie_recursive]
      A = '+'.join(partie_recursive)
      B = '+'.join(partie_non_recursive)
      systeme[etat] = f"{A})*({B}"
  else:
      systeme[etat] = '+'.join(partie_non_recursive)
 
  return systeme
 
def substituer_expressions_resolues(systeme, etat_resolu):
  expression_resolue = systeme[etat_resolu]
  for etat in systeme:
      if etat != etat_resolu:
          systeme[etat] = systeme[etat].replace(etat_resolu, f"({expression_resolue})")
  return systeme
def generer_expression_reguliere(aef):
  systeme = generer_systeme_equations(aef)
 
  for etat in aef.states:
      systeme = appliquer_lemme_arden(systeme, etat)
 
  for etat_resolu in aef.states:
      systeme = substituer_expressions_resolues(systeme, etat_resolu)
 
  etat_initial = next(iter(aef.initial_states))
  return systeme[etat_initial]
 
def factoriser_expression_aef(expression, facteur):
    # Supprimer les égalités et les parenthèses vides
    expression = expression.replace("=", "").replace("()", "")
 
    # Diviser l'expression en parties en utilisant ' + ' comme séparateur
    parties = expression.split(' + ')
 
    # Extraire les parties qui contiennent le facteur
    parties_avec_facteur = [partie.replace(facteur, '').strip() for partie in parties if facteur in partie]
 
    # Si aucune partie ne contient le facteur, retourner l'expression originale
    if not parties_avec_facteur:
        return expression
 
    # Reconstruire l'expression factorisée
    expression_factorisee = f"{facteur}(" + ' + '.join(parties_avec_facteur) + ')'
 
    # Ajouter les parties sans le facteur à la fin de l'expression
    parties_sans_facteur = [partie for partie in parties if facteur not in partie]
    if parties_sans_facteur:
        expression_factorisee += " + " + ' + '.join(parties_sans_facteur)
 
    return expression_factorisee

def ExpressionRegulierefinale (expression_finale):
       reguliere = expression_finale
       return reguliere

#def find_language(self,):
    
   # return language




def input_aef():
  print("Entrez les détails de l'Automate à États Finis :")

  states = set(
      input("Liste des états (séparés par des virgules) : ").split(','))
  alphabet = set(input("Alphabet (séparé par des virgules) : ").split(','))

  transitions = {}
  for state in states:
    transitions[state] = {}
    for symbol in alphabet:
      transition_states = input(
          f"Transitions depuis l'état '{state}' avec le symbole '{symbol}' (séparées par des virgules) : "
      )

      #transition_states = transition_states.split(',') A VERIFIER!!!!!

      transitions[state][symbol] = transition_states

  initial_states = set(
      input("Liste des états initiaux (séparés par des virgules) : ").split(','))
  final_states = set(
      input("Liste des états finaux (séparés par des virgules) : ").split(','))

  return AEF(states, alphabet, transitions, initial_states, final_states)


def load_aef_from_file(file_path):
  try:
    if file_path is None:
      print("Le chemin du fichier est vide.")
      return None

    with open(file_path, 'r') as file:
      # Lire le contenu du fichier et charger les données JSON
      file_content = file.read().strip()

      if not file_content:
        print("Le fichier est vide.")
        return None

      aef_data = json.loads(file_content)
      return AEF(**aef_data)
  except FileNotFoundError:
    print(f"Le fichier '{file_path}' n'existe pas.")
  except Exception as e:
    print(f"Une erreur s'est produite lors de la lecture du fichier: {e}")


def save_aef_to_file(aef, file_path):
  try:
    with open(file_path, 'w') as file:
      # Convertir les listes en dictionnaires pour l'enregistrement JSON
      transitions = {}
      for state, symbols in aef.transitions.items():
        transitions[state] = {
            symbol: trans
            for symbol, trans in symbols.items()
        }
      json.dump(
          {
              "states": list(aef.states),
              "alphabet": list(aef.alphabet),
              "transitions": aef.transitions,
              "initial_states": list(aef.initial_states),
              "final_states": list(aef.final_states)
          },
          file,
          indent=2)
    print(f"L'AEF a été enregistré avec succès dans le fichier '{file_path}'.")
  except Exception as e:
    print(f"Une erreur s'est produite lors de l'enregistrement de l'AEF : {e}")


def save_aef(aef):
  if aef is None:
    aef = input_aef()

  file_path = input("Entrez le chemin du fichier pour enregistrer l'AEF : ")
  save_aef_to_file(aef, file_path)
  return aef


def modify_aef(aef):
  print("Que souhaitez vous modifier dans l'AEF ?\n1. Etats\n2. Alphabet\n3. Transitions\n4. Etats initiaux\n5. Etats finaux\n")

  choice = input("Sélectionnez ce que vous souhaitez modifier : ")

  if choice == '1':
    aef.states = set(
        input("Nouvelle liste des états (séparés par des virgules) : ").split(','))
    print("Vous venez de modifier les états de l'AEF, vous devez donc maintenant modifier les transitions :")
    transitions = {}
    for state in aef.states:
      transitions[state] = {}
      for symbol in aef.alphabet:
        transition_state = input(
            f"Nouvelle transition depuis l'état '{state}' avec le symbole '{symbol}' : "
        )
        transitions[state][symbol] = transition_state
    aef.transitions = transitions
    print("Vous avez modifié les états de l'AEF, vous devez donc préciser lesquels sont initiaux/finaux :\n")
    aef.initial_states = set(
        input("Nouvelle liste des états initiaux (séparés par des virgules) :").split(','))
    aef.final_states = set(
        input("Nouvelle liste des états finaux (séparés par des virgules) :").split(','))
    
  elif choice == '2':
    aef.alphabet = set(input("Nouvel alphabet (séparé par des virugles) : ").split(','))
    print("\nVous venez de modifier l'alphabet de l'AEF, vous devez donc maintenant modifier les transitions :")
    transitions = {}
    for state in aef.states:
      transitions[state] = {}
      for symbol in aef.alphabet:
        transition_state = input(
            f"Nouvelle transition depuis l'état '{state}' avec le symbole '{symbol}' : "
        )
        transitions[state][symbol] = transition_state
    aef.transitions = transitions

  elif choice == '3':
    transitions = {}
    for state in aef.states:
      transitions[state] = {}
      for symbol in aef.alphabet:
        transition_state = input(
            f"Nouvelle transition depuis l'état '{state}' avec le symbole '{symbol}' : "
        )
        transitions[state][symbol] = transition_state
    aef.transitions = transitions

  elif choice == '4':
    aef.initial_states = set(
        input("Nouvelle liste des états initiaux (séparés par des virgules) :").
        split(','))
    
  elif choice == '5':
    aef.final_states = set(
        input("Nouvelle liste des états finaux (séparés par des virgules) :").
        split(','))
    
  else:
    print("Choix invalide. Aucune modification effectuée. ")


def delete_aef(file_path):
  try:
    os.remove(file_path)
    print(f"L'AEF du fichier '{file_path}' a été supprimé avec succès.")
  except FileNotFoundError:
    print(f"Le fichier '{file_path}' n'existe pas.")
  except Exception as e:
    print(f"Une erreur s'est produite lors de la suppression de l'AEF : {e}")


def product_aef(aef1, aef2):
  # Créer les états du produit en combinant les états des deux AEFs
  product_states = [(state1, state2) for state1 in aef1.states
                    for state2 in aef2.states]

  # Créer les transitions du produit
  product_transitions = {}
  for state1, state2 in product_states:
    product_transitions[(state1, state2)] = {}

    for symbol in aef1.alphabet:
      # Vérifier si les transitions existent dans l'AEF1 et l'AEF2
      transition1 = aef1.transitions[state1][
          symbol] if state1 in aef1.transitions and symbol in aef1.transitions[
              state1] else None
      transition2 = aef2.transitions[state2][
          symbol] if state2 in aef2.transitions and symbol in aef2.transitions[
              state2] else None

      # Ajouter la transition au produit
      product_transitions[(state1, state2)][symbol] = (transition1,
                                                       transition2)

  # Créer les états initiaux et finaux du produit
  product_initial_states = [(aef1_initial, aef2_initial)
                            for aef1_initial in aef1.initial_states
                            for aef2_initial in aef2.initial_states]
  product_final_states = [(aef1_final, aef2_final)
                          for aef1_final in aef1.final_states
                          for aef2_final in aef2.final_states]

  # Créer une nouvelle instance d'AEF pour le produit
  product_aef = AEF(
      states=product_states,
      alphabet=aef1.alphabet,  # L'alphabet commun
      transitions=product_transitions,
      initial_states=product_initial_states,
      final_states=product_final_states)

  return product_aef



def other_options(aef, file_path):
  print("Options supplémentaires :\n8. Vérifier si un mot est reconnu par un AEF\n9. Vérifier si un automate est complet\n10. Rendre un automate complet\n11. Vérifier si un automate est déterministe\n12. Rendre un automate deterministe\n13. Autre\n0. Revenir au menu\n")

  choice = input("\nSélectionner ce que vous voulez faire :")

  if choice == '8':
    aef.is_accepted(file_path)
    
  elif choice == '9':
    if check_variables_non_empty(aef, file_path):
        if aef.is_automate_complet() == True:
            print("L'automate est bien complet !\n")
        else:
            print("L'automate n'est pas complet !\n")

  elif choice == '10':
    if check_variables_non_empty(aef, file_path):
        if aef.is_automate_complet() == True:
            print("L'automate est deja complet !\n")
        else:
            aef.make_complete(file_path)
            print("Votre automate est désormais complet !\n")
    

  elif choice == '11':
    aef.is_deterministic()

  elif choice == '12':
    aef.convert_to_deterministic(file_path)

  elif choice == '13':
    other_other_options(aef, file_path)

  elif choice == '0':
    main(aef)  # Retour au menu principal

  else:
    print("Choix invalide. Veuillez choisir une option valide.")
    other_options(aef, file_path)


def other_other_options(aef, file_path):
  print("\nOptions supplémentaires: \n15. Complément d'un AEF\n16. Miroir d'un AEF\n17. Produit de deux AEF\n18. Concaténation de deux AEF\n19. Rendre emonde\n20. Generer expression réguliere\n")

  choice = input("\nSélectionnez ce que vous voulez faire : ")

  if choice == '15':
    if check_variables_non_empty(aef, file_path):
      aef.complement_aef(file_path)
      print("Complément appliqué sur votre AEF !\n")
      print("Voici votre nouvel AEF :\n")
      aef.draw_AEF()

  elif choice == '16':
    if check_variables_non_empty(aef, file_path):
      aef.mirror_aef(file_path)  # Modifier l'instance aef avec le retour de mirror_aef()
      print("Effet miroir appliqué sur votre AEF")
      print("Voici votre nouvel AEF :\n")
      aef.draw_AEF()
    else:
      print("Aucun AEF n'est défini.")

  elif choice == '17':
    print("\n")
    file_path_aef1 = input(
        "Entrez le chemin du fichier pour le premier AEF : ")
    file_path_aef2 = input(
        "Entrez le chemin du fichier pour le deuxième AEF : ")

    aef1 = load_aef_from_file(file_path_aef1)
    aef2 = load_aef_from_file(file_path_aef2)

    if check_variables_non_empty(aef1, file_path_aef1) and check_variables_non_empty(aef2, file_path_aef2):
      product_result = product_aef(aef1, aef2)
      print("\nAEF produit")
      print("États du produit:", product_result.states)
      print("Transitions du produit:", product_result.transitions)
      print("États initiaux du produit:", product_result.initial_states)
      print("États finaux du produit:", product_result.final_states)
    else:
      print("L'un des AEFs n'est pas défini.")

  elif choice == '18':
    print('Concaténation de deux AEF sélectionnée.')
    file_path_aef1 = input(
        "Entrez le chemin du fichier pour le premier AEF : ")
    file_path_aef2 = input("Entrez le chemin du fichier pour le second AEF : ")

    aef1 = load_aef_from_file(file_path_aef1)
    aef2 = load_aef_from_file(file_path_aef2)

    if check_variables_non_empty(aef1, file_path) and check_variables_non_empty(aef2, file_path):
      connecting_symbol = input(
          "Entrez le symbole de connexion pour relier les deux AEFs : ")
      file_path_concatenated = input(
          "Entrez le chemin du fichier pour enregistrer l'AEF concaténé : ")

      concatenated_aef = aef1.concatenate_aef(aef2, connecting_symbol,
                                              file_path_concatenated)
      if check_variables_non_empty(concatenated_aef, file_path):
        print('Les AEF ont été concaténés et sauvegardés.')
        print("\nVoici l'AEF concaténé :\n")
        concatenated_aef.draw_AEF()
      else:
        print("Erreur lors de la concaténation des AEFs.")
    else:
      print(
          "Les fichiers sont vides et/ou l'aef n'est pas défini !\n"
      )
  elif choice == '19':
    aef.rendre_emonde(file_path)
  elif choice == '20':
      file_path = input("Entrez le chemin du fichier de l'AEF pour générer l'expression régulière : ")
      aef = load_aef_from_file(file_path)
      if aef:
          # Générer le système d'équations
          systeme_equations = generer_systeme_equations(aef)
 
          # Afficher les équations pour chaque état
          print("Système d'équations généré :")
          for etat, equation in systeme_equations.items():
              print(f"{etat}: {equation}")
 
          # Identifier et résoudre l'équation de l'état qui n'est pas final
          equation_q2_resolue = ""
          for etat, equation in systeme_equations.items():
              if 'ε' not in equation:
                  print(f"L'équation pour l'état non final {etat} est : {equation}")
                  B = input(f"Pour l'état {etat}, entrez l'expression pour B (Arden solution de l’équation X = BX + C est X = B∗C) : ")
                  C = input(f"Pour l'état {etat}, entrez l'expression pour C (Arden solution de l’équation X = BX + C est X = B∗C) : ")
                  equation_q2_resolue = f"{B}*({C})"
                  print(f"L'équation résolue pour l'état est : {etat} = {equation_q2_resolue}")
                  break
 
          # Remplacer l'occurrence de q2 dans l'équation de q1 par l'équation résolue de q2
          if equation_q2_resolue:
              equation_q1 = systeme_equations.get('q1', '')
              equation_q1_modifiee = equation_q1.replace("q2", equation_q2_resolue)
              print(f"L'équation modifiée pour l'état final  :  = {equation_q1_modifiee}")
 
              # Demander le facteur commun pour la factorisation
              facteur = input("Entrez le facteur commun pour la factorisation (par exemple, q1) : ")
              equation_q1_factorisee = factoriser_expression_aef(equation_q1_modifiee, facteur)
              print(f"Expression factorisée : {equation_q1_factorisee}")
 
              print("Appliquer le lemme d'Arden sur l'expression factorisée.")
              B_nouveau = input("Entrez pour la nouvelle expression le B  : ")
              C_nouveau = input("Entrez pour la nouvelle expression le C : ")
 
              # Appliquer le lemme d'Arden
              expression_finale = f"{B_nouveau}*({C_nouveau})"
              print(f"L'expression régulière après application du lemme d'Arden est : {expression_finale}")
          else:
              print("Aucune équation résolue pour q2 n'a été trouvée.")
      else:
              print(f"Impossible de charger l")
  
  elif choice == '21':
     # Appel à la méthode find_language
    language = aef.find_language()
    print("Le langage reconnu par l'automate est :", language)
      
  else:
    print("Choix invalide. Veuillez choisir une option valide.")
    other_other_options(aef, file_path)

  
  
def main(aef):
  file_path = None  # Initialiser le chemin du fichier à None
  while True:
    print("\nBIENVENUE DANS L'INTERFACE TEXTUEL D'AEF !\n\nMenu :\n1. Saisir et sauvegarder un nouvel AEF\n2. Charger un AEF à partir d'un fichier\n3. Modifier un AEF\n4. Supprimer un AEF\n5. Changer de fichier\n6. Afficher l'AEF\n7. Autre\n0. Quitter\n")

    choice = input("Sélectionnez ce que vous voulez faire :\n")

    if choice == '1':
      aef = None
      aef = save_aef(aef)  # Sauvegarder le nouvel AEF et récupérer l'instance de l'AEF

    elif choice == '2':
      file_path = input("Entrez le chemin du fichier : ")
      aef = load_aef_from_file(file_path)

    elif choice == '3':
      if file_path:
        aef = load_aef_from_file(file_path)
        if check_variables_non_empty(aef, file_path):
          print("AEF chargé avec succès.")
          modify_aef(aef)
          save_file = input(
              "Voulez-vous enregistrer les modifications dans un nouveau fichier ? (oui/non) : "
          ).lower()
          if save_file == 'oui' or save_file == 'yes':
            new_file_path = input("Entrez le chemin du nouveau fichier : ")
            save_aef_to_file(aef, new_file_path)
          else:
            save_aef_to_file(aef, file_path)

      else:
        print("Aucun fichier n'est actuellement chargé.")

    elif choice == '4':
      if is_file_empty(file_path) == False:
        delete_aef(file_path)
        file_path = None  # Réinitialisation du chemin du fichier après suppression
      else:
        print("Aucun fichier n'est actuellement chargé ou le fichier est vide !\n")

    elif choice == '5':
      new_file_path = input("Entrez le nouveau chemin du fichier JSON : ")
      aef = load_aef_from_file(new_file_path)
      if check_variables_non_empty(aef, new_file_path):
        file_path = new_file_path  # Retourner le nouvel AEF et son chemin de fichier
      else:
        print(
            "Aucun AEF n'est actuellement défini, vous allez à présent en entrer un :"
        )
        aef = input_aef()

    elif choice == '6':
      if check_variables_non_empty(aef, file_path):
        aef.draw_AEF()
      else:
        print("Aucun AEF n'est actuellement chargé ou le fichier est vide.")

    elif choice == '7':
      if check_variables_non_empty(aef, file_path):
        other_options(aef, file_path)
      else:
        print("Aucun AEF n'est actuellement chargé ou le fichier est vide.")

    elif choice == '0':
      break  # Sortie de la boucle, fin du programme
    else:
      print("Choix invalide. Veuillez choisir une option valide.")


if __name__ == "__main__":
  aef = None
  main(aef)