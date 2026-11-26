"""
Application d'entraide communautaire (PESTAL).

Chaque membre de la communauté peut :
  - proposer son aide (ex : « Je peux donner des cours de maths »)
  - demander de l'aide (ex : « Je cherche quelqu'un pour réparer un vélo »)
  - voir toutes les annonces, chercher par mot-clé
  - marquer une annonce comme résolue, ou la supprimer

Les annonces sont sauvegardées dans le fichier « annonces.json »,
donc elles ne sont pas perdues quand on ferme le programme.

Pour lancer l'application :  python entraide.py
"""

import json
import os
from datetime import date

# Nom du fichier où on enregistre les annonces
FICHIER = "annonces.json"


# ---------------------------------------------------------------------------
# 1) Sauvegarde et chargement des données
# ---------------------------------------------------------------------------

def charger_annonces(fichier=FICHIER):
    """Lit les annonces depuis le fichier JSON. Renvoie une liste."""
    if not os.path.exists(fichier):
        return []  # pas encore de fichier : on commence avec une liste vide
    with open(fichier, "r", encoding="utf-8") as f:
        return json.load(f)


def sauvegarder_annonces(annonces, fichier=FICHIER):
    """Écrit la liste des annonces dans le fichier JSON."""
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(annonces, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# 2) Les actions sur les annonces (sans input/print : faciles à tester)
# ---------------------------------------------------------------------------

def ajouter_annonce(annonces, type_annonce, auteur, titre, contact):
    """Ajoute une annonce et la renvoie.
    type_annonce vaut « offre » ou « demande »."""
    # Le nouvel identifiant = le plus grand identifiant existant + 1
    nouvel_id = max([a["id"] for a in annonces], default=0) + 1
    annonce = {
        "id": nouvel_id,
        "type": type_annonce,
        "auteur": auteur,
        "titre": titre,
        "contact": contact,
        "date": date.today().isoformat(),
        "resolue": False,
    }
    annonces.append(annonce)
    return annonce


def chercher_annonces(annonces, mot_cle):
    """Renvoie les annonces dont le titre ou l'auteur contient le mot-clé."""
    mot_cle = mot_cle.lower()
    return [
        a for a in annonces
        if mot_cle in a["titre"].lower() or mot_cle in a["auteur"].lower()
    ]


def trouver_annonce(annonces, id_annonce):
    """Renvoie l'annonce qui a cet identifiant, ou None si elle n'existe pas."""
    for a in annonces:
        if a["id"] == id_annonce:
            return a
    return None


def marquer_resolue(annonces, id_annonce):
    """Marque une annonce comme résolue. Renvoie True si ça a marché."""
    annonce = trouver_annonce(annonces, id_annonce)
    if annonce is None:
        return False
    annonce["resolue"] = True
    return True


def supprimer_annonce(annonces, id_annonce):
    """Supprime une annonce. Renvoie True si ça a marché."""
    annonce = trouver_annonce(annonces, id_annonce)
    if annonce is None:
        return False
    annonces.remove(annonce)
    return True


# ---------------------------------------------------------------------------
# 3) L'interface dans le terminal (menus, questions, affichage)
# ---------------------------------------------------------------------------

def afficher_annonces(annonces):
    """Affiche joliment une liste d'annonces."""
    if not annonces:
        print("  (aucune annonce)")
        return
    for a in annonces:
        etiquette = "OFFRE  " if a["type"] == "offre" else "DEMANDE"
        etat = " ✔ résolue" if a["resolue"] else ""
        print(f"  #{a['id']} [{etiquette}] {a['titre']}{etat}")
        print(f"       par {a['auteur']} le {a['date']} — contact : {a['contact']}")


def demander_texte(question):
    """Pose une question et refuse les réponses vides."""
    while True:
        reponse = input(question).strip()
        if reponse:
            return reponse
        print("  Merci d'écrire quelque chose.")


def demander_numero(question):
    """Pose une question et renvoie un nombre entier (ou None si invalide)."""
    reponse = input(question).strip()
    if reponse.isdigit():
        return int(reponse)
    print("  Ce n'est pas un numéro valide.")
    return None


def menu():
    """Boucle principale : affiche le menu jusqu'à ce qu'on quitte."""
    annonces = charger_annonces()

    while True:
        print("\n===== ENTRAIDE COMMUNAUTAIRE =====")
        print("1. Voir toutes les annonces")
        print("2. Proposer mon aide")
        print("3. Demander de l'aide")
        print("4. Chercher une annonce")
        print("5. Marquer une annonce comme résolue")
        print("6. Supprimer une annonce")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            afficher_annonces(annonces)

        elif choix in ("2", "3"):
            type_annonce = "offre" if choix == "2" else "demande"
            auteur = demander_texte("Votre nom : ")
            titre = demander_texte("Décrivez votre annonce : ")
            contact = demander_texte("Comment vous contacter (téléphone, email...) : ")
            annonce = ajouter_annonce(annonces, type_annonce, auteur, titre, contact)
            sauvegarder_annonces(annonces)
            print(f"  Annonce #{annonce['id']} enregistrée. Merci !")

        elif choix == "4":
            mot_cle = demander_texte("Mot-clé : ")
            afficher_annonces(chercher_annonces(annonces, mot_cle))

        elif choix == "5":
            numero = demander_numero("Numéro de l'annonce : ")
            if numero is not None:
                if marquer_resolue(annonces, numero):
                    sauvegarder_annonces(annonces)
                    print("  Annonce marquée comme résolue.")
                else:
                    print("  Annonce introuvable.")

        elif choix == "6":
            numero = demander_numero("Numéro de l'annonce : ")
            if numero is not None:
                if supprimer_annonce(annonces, numero):
                    sauvegarder_annonces(annonces)
                    print("  Annonce supprimée.")
                else:
                    print("  Annonce introuvable.")

        elif choix == "0":
            print("Au revoir et merci pour votre entraide !")
            break

        else:
            print("  Choix inconnu, tapez un chiffre entre 0 et 6.")


# Ce bloc s'exécute seulement quand on lance « python entraide.py »
if __name__ == "__main__":
    menu()
