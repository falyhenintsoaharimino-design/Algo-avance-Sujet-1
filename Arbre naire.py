"""
Projet Algorithmique Avancee - Sujet 1 : Arbre n-aire
Script unique regroupant les 4 parties du travail de groupe.

"""


# PARTIE 1 - Erwan : Structure de donnees de base

class Noeud:
    """noeud de l'arbre n-aire."""

    def __init__(self, valeur):
        self.valeur = valeur
        self.enfants = [] 

    def ajouter_enfant(self, noeud_enfant):
        """Ajoute un noeud deja cree comme enfant direct de ce noeud."""
        self.enfants.append(noeud_enfant)

    def est_feuille(self):
        """Un noeud est une feuille s'il n'a aucun enfant."""
        return len(self.enfants) == 0

    def __repr__(self):
        return f"Noeud({self.valeur!r})"


class ArbreNaire:
    """Represente l'arbre n-aire complet, a partir de sa racine."""

    def __init__(self, valeur_racine):
        self.racine = Noeud(valeur_racine)

    def ajouter_enfant(self, valeur_parent, valeur_enfant):
        """Cherche le noeud dont la valeur est `valeur_parent` et lui
        ajoute un nouvel enfant portant `valeur_enfant`.

        Retourne True si l'ajout a reussi, False si le parent n'a pas
        ete trouve dans l'arbre.
        """
        parent = self._trouver_noeud(self.racine, valeur_parent)
        if parent is None:
            return False
        parent.ajouter_enfant(Noeud(valeur_enfant))
        return True

    def _trouver_noeud(self, noeud_courant, valeur_cherchee):
        """Recherche interne recursive utilisee pour construire l'arbre.
        La partie 2 fournit la recherche complete destinee a l'utilisateur.
        """
        if noeud_courant.valeur == valeur_cherchee:
            return noeud_courant
        for enfant in noeud_courant.enfants:
            resultat = self._trouver_noeud(enfant, valeur_cherchee)
            if resultat is not None:
                return resultat
        return None


def construire_arbre_exemple():
    """Construit un petit arbre d'exemple."""
    arbre = ArbreNaire("Racine")
    arbre.ajouter_enfant("Racine", "Enfant1")
    arbre.ajouter_enfant("Racine", "Enfant2")
    arbre.ajouter_enfant("Racine", "Enfant3")
    arbre.ajouter_enfant("Enfant1", "PetitFils1")
    arbre.ajouter_enfant("Enfant1", "PetitFils2")
    return arbre


# PARTIE 2 - Faly : Parcours et recherche

def parcours_prefixe(noeud):
    """Parcours en profondeur : le noeud est visite AVANT ses enfants.
    """
    if noeud is None:
        return []

    resultat = [noeud.valeur]
    for enfant in noeud.enfants:
        resultat.extend(parcours_prefixe(enfant))
    return resultat


def parcours_postfixe(noeud):
    """Parcours en profondeur : le noeud est visite APRES tous ses enfants.
    """
    if noeud is None:
        return []

    resultat = []
    for enfant in noeud.enfants:
        resultat.extend(parcours_postfixe(enfant))
    resultat.append(noeud.valeur)
    return resultat


def parcours_largeur(racine):
    """Parcours en largeur (BFS), niveau par niveau.
    """
    if racine is None:
        return []

    resultat = []
    file_attente = [racine]

    while file_attente:
        noeud_courant = file_attente.pop(0)
        resultat.append(noeud_courant.valeur)
        file_attente.extend(noeud_courant.enfants)

    return resultat


def rechercher(racine, valeur_cherchee):
    """Recherche une valeur dans l'arbre a partir de la racine.
    Reutilise le parcours prefixe : on s'arrete des qu'on trouve la
    valeur. Renvoie le Noeud trouve, ou None si absent.
    """
    if racine is None:
        return None

    if racine.valeur == valeur_cherchee:
        return racine

    for enfant in racine.enfants:
        resultat = rechercher(enfant, valeur_cherchee)
        if resultat is not None:
            return resultat

    return None


# PARTIE 3 - Faly : Ameliorations

def hauteur(noeud):
    """Hauteur de l'arbre (nombre d'arcs jusqu'a la feuille la plus
    profonde). Un noeud seul (feuille) a une hauteur de 0.
    """
    if noeud is None or noeud.est_feuille():
        return 0

    hauteurs_enfants = [hauteur(enfant) for enfant in noeud.enfants]
    return 1 + max(hauteurs_enfants)


def compter_noeuds(noeud):
    """Compte le nombre total de noeuds dans le sous-arbre."""
    if noeud is None:
        return 0

    total = 1
    for enfant in noeud.enfants:
        total += compter_noeuds(enfant)
    return total


def compter_feuilles(noeud):
    """Compte le nombre de feuilles (noeuds sans enfant) dans le sous-arbre."""
    if noeud is None:
        return 0

    if noeud.est_feuille():
        return 1

    total = 0
    for enfant in noeud.enfants:
        total += compter_feuilles(enfant)
    return total


def supprimer_noeud(arbre, valeur_a_supprimer):
    """Supprime le noeud portant `valeur_a_supprimer` de l'arbre.

    Choix de conception : les enfants du noeud supprime sont
    reattaches a son parent (plutot que supprimes en cascade), pour
    ne pas perdre le reste de l'arbre.

    Renvoie True si la suppression a reussi, False sinon (valeur
    introuvable, ou tentative de suppression de la racine).
    """
    if arbre.racine.valeur == valeur_a_supprimer:
        return False

    return _supprimer_recursif(arbre.racine, valeur_a_supprimer)


def _supprimer_recursif(noeud_parent, valeur_a_supprimer):
    for i, enfant in enumerate(noeud_parent.enfants):
        if enfant.valeur == valeur_a_supprimer:
            noeud_parent.enfants.pop(i)
            noeud_parent.enfants.extend(enfant.enfants)
            return True
        if _supprimer_recursif(enfant, valeur_a_supprimer):
            return True
    return False


def afficher_arbre(noeud, prefixe="", est_dernier=True):
    """Affiche l'arbre dans la console avec une indentation visuelle,
    """
    if noeud is None:
        return

    connecteur = "`-- " if est_dernier else "|-- "
    print(prefixe + connecteur + str(noeud.valeur))

    nouveau_prefixe = prefixe + ("    " if est_dernier else "|   ")
    nb_enfants = len(noeud.enfants)
    for index, enfant in enumerate(noeud.enfants):
        est_dernier_enfant = index == nb_enfants - 1
        afficher_arbre(enfant, nouveau_prefixe, est_dernier_enfant)


# PARTIE 4 - Rado : Integration, tests et interface

def executer_tests():
    """Verification automatique que les 3 parties fonctionnent bien
    ensemble.
    """
    print("=== Tests automatiques ===")
    arbre = construire_arbre_exemple()

    assert compter_noeuds(arbre.racine) == 6, "Le nombre de noeuds attendu est 6"
    assert hauteur(arbre.racine) == 2, "La hauteur attendue est 2"
    assert compter_feuilles(arbre.racine) == 4, "Le nombre de feuilles attendu est 4"

    resultat_recherche = rechercher(arbre.racine, "PetitFils1")
    assert resultat_recherche is not None, "PetitFils1 doit etre trouve"

    resultat_absent = rechercher(arbre.racine, "Fantome")
    assert resultat_absent is None, "Une valeur absente ne doit rien renvoyer"

    print("Tous les tests sont passes avec succes.\n")


def menu():
    """Menu interactif en console pour manipuler l'arbre."""
    arbre = construire_arbre_exemple()

    while True:
        print("\n--- Menu Arbre n-aire ---")
        print("1. Afficher l'arbre")
        print("2. Parcours prefixe")
        print("3. Parcours postfixe")
        print("4. Parcours en largeur (suffixe)")
        print("5. Rechercher une valeur")
        print("6. Ajouter un enfant")
        print("7. Supprimer un noeud")
        print("8. Statistiques (hauteur, noeuds, feuilles)")
        print("0. Quitter")

        choix = input("Votre choix : ").strip()

        if choix == "1":
            afficher_arbre(arbre.racine)
        elif choix == "2":
            print(parcours_prefixe(arbre.racine))
        elif choix == "3":
            print(parcours_postfixe(arbre.racine))
        elif choix == "4":
            print(parcours_largeur(arbre.racine))
        elif choix == "5":
            valeur = input("Valeur a chercher : ").strip()
            resultat = rechercher(arbre.racine, valeur)
            print("Trouve :", resultat if resultat else "aucun resultat")
        elif choix == "6":
            parent = input("Valeur du parent existant : ").strip()
            nouvel_enfant = input("Valeur du nouvel enfant : ").strip()
            ok = arbre.ajouter_enfant(parent, nouvel_enfant)
            print("Ajout reussi." if ok else "Parent introuvable.")
        elif choix == "7":
            valeur = input("Valeur du noeud a supprimer : ").strip()
            ok = supprimer_noeud(arbre, valeur)
            print("Suppression reussie." if ok else "Suppression impossible (introuvable ou racine).")
        elif choix == "8":
            print("Hauteur :", hauteur(arbre.racine))
            print("Nombre de noeuds :", compter_noeuds(arbre.racine))
            print("Nombre de feuilles :", compter_feuilles(arbre.racine))
        elif choix == "0":
            print("Fin du programme.")
            break
        else:
            print("Choix invalide, reessayez.")


if __name__ == "__main__":
    executer_tests()
    menu()