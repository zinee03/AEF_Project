
# Projet Automate (AEF)

## Description
Ce projet implémente une classe `AEF` en Python, qui représente un automate. L'automate est constitué d'états, d'un alphabet, de transitions entre les états, d'états initiaux et d'états finaux.

## Fonctionnalités
- **Initialisation** : Créez un automate en spécifiant les états, l'alphabet, les transitions, les états initiaux et les états finaux.
- **Transition** : Effectuez des transitions d'état en fonction des symboles de l'alphabet.

## Utilisation
1. **Initialisation de l'automate** :
   Créez une instance de la classe `AEF` en passant les paramètres nécessaires (états, alphabet, etc.).
   
2. **Effectuer des transitions** :
   Utilisez la méthode `transition` avec un symbole de l'alphabet pour effectuer des transitions d'état dans l'automate.

## Exemple
```python
# Création de l'automate
aef = AEF(states, alphabet, transitions, initial_states, final_states)

# Effectuer une transition avec un symbole
aef.transition(symbol)
```
