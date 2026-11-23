"""Tests de l'application. Pour les lancer :  python -m unittest"""

import os
import tempfile
import unittest

import entraide


class TestEntraide(unittest.TestCase):

    def test_ajouter_donne_des_id_croissants(self):
        annonces = []
        a1 = entraide.ajouter_annonce(annonces, "offre", "Amadou", "Cours de maths", "0600")
        a2 = entraide.ajouter_annonce(annonces, "demande", "Fatou", "Réparer un vélo", "0700")
        self.assertEqual(a1["id"], 1)
        self.assertEqual(a2["id"], 2)
        self.assertEqual(len(annonces), 2)

    def test_chercher_ignore_majuscules(self):
        annonces = []
        entraide.ajouter_annonce(annonces, "offre", "Amadou", "Cours de MATHS", "0600")
        entraide.ajouter_annonce(annonces, "offre", "Fatou", "Couture", "0700")
        resultat = entraide.chercher_annonces(annonces, "maths")
        self.assertEqual(len(resultat), 1)

    def test_resoudre_et_supprimer(self):
        annonces = []
        entraide.ajouter_annonce(annonces, "offre", "Amadou", "Jardinage", "0600")
        self.assertTrue(entraide.marquer_resolue(annonces, 1))
        self.assertTrue(annonces[0]["resolue"])
        self.assertFalse(entraide.marquer_resolue(annonces, 99))
        self.assertTrue(entraide.supprimer_annonce(annonces, 1))
        self.assertEqual(annonces, [])

    def test_sauvegarde_puis_chargement(self):
        with tempfile.TemporaryDirectory() as dossier:
            chemin = os.path.join(dossier, "annonces.json")
            annonces = []
            entraide.ajouter_annonce(annonces, "demande", "Awa", "Aide aux devoirs", "0800")
            entraide.sauvegarder_annonces(annonces, chemin)
            self.assertEqual(entraide.charger_annonces(chemin), annonces)


if __name__ == "__main__":
    unittest.main()
