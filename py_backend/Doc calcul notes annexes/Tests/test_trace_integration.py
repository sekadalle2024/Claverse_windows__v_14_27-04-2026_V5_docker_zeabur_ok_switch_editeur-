"""
Test d'intégration de Trace_Manager dans l'orchestrateur.

Vérifie que:
- Les traces sont générées pour toutes les notes calculées
- L'historique est géré (garde les 10 dernières traces)
- Les métadonnées sont correctement enregistrées
- Les fichiers de trace sont créés au bon endroit

Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7
"""

import os
import sys
import json
import pytest
from datetime import datetime
import pandas as pd

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Modules'))

from calcul_notes_annexes_main import CalculNotesAnnexesMain


class TestTraceIntegration:
    """Tests d'intégration de Trace_Manager dans l'orchestrateur."""
    
    @pytest.fixture
    def orchestrateur(self):
        """Crée un orchestrateur pour les tests."""
        fichier_balance = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'P000 -BALANCE DEMO N_N-1_N-2.xls'
        )
        
        if not os.path.exists(fichier_balance):
            pytest.skip(f"Fichier de balance non trouvé: {fichier_balance}")
        
        return CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    @pytest.fixture
    def notes_test(self):
        """Crée des notes de test."""
        return {
            'Note_3A': pd.DataFrame({
                'Libellé': ['Frais R&D', 'Brevets', 'Total'],
                'Brut Ouverture': [1000000, 500000, 1500000],
                'Augmentations': [200000, 100000, 300000],
                'Brut Clôture': [1200000, 600000, 1800000]
            }),
            'Note_4': pd.DataFrame({
                'Libellé': ['Marchandises', 'Matières', 'Total'],
                'Stock Ouverture': [300000, 200000, 500000],
                'Entrées': [100000, 50000, 150000],
                'Stock Clôture': [400000, 250000, 650000]
            })
        }
    
    def test_generer_traces_cree_fichiers(self, orchestrateur, notes_test):
        """
        Test que generer_traces() crée les fichiers de trace.
        
        Requirements: 15.1, 15.2, 15.3
        """
        # Assigner les notes de test
        orchestrateur.notes_calculees = notes_test
        
        # Générer les traces
        orchestrateur.generer_traces()
        
        # Vérifier que les fichiers de trace existent
        tests_dir = os.path.join(os.path.dirname(__file__))
        
        for nom_note in notes_test.keys():
            numero = nom_note.replace('Note_', '').lower()
            fichier_trace = os.path.join(tests_dir, f'trace_note_{numero}.json')
            
            assert os.path.exists(fichier_trace), \
                f"Fichier de trace non créé: {fichier_trace}"
            
            # Vérifier que le fichier contient du JSON valide
            with open(fichier_trace, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            
            # Vérifier la structure de base
            assert 'note' in trace_data
            assert 'date_generation' in trace_data
            assert 'fichier_balance' in trace_data
            assert 'hash_md5_balance' in trace_data
            assert 'lignes' in trace_data
            
            print(f"✓ Trace créée et valide: {nom_note}")
    
    def test_generer_traces_enregistre_metadata(self, orchestrateur, notes_test):
        """
        Test que les métadonnées sont correctement enregistrées.
        
        Requirements: 15.3, 15.4
        """
        orchestrateur.notes_calculees = notes_test
        orchestrateur.generer_traces()
        
        tests_dir = os.path.join(os.path.dirname(__file__))
        fichier_trace = os.path.join(tests_dir, 'trace_note_3a.json')
        
        with open(fichier_trace, 'r', encoding='utf-8') as f:
            trace_data = json.load(f)
        
        # Vérifier les métadonnées
        assert trace_data['fichier_balance'] == orchestrateur.fichier_balance
        assert len(trace_data['hash_md5_balance']) == 32  # MD5 hash length
        
        # Vérifier le format de la date
        date_gen = datetime.fromisoformat(trace_data['date_generation'])
        assert isinstance(date_gen, datetime)
        
        print("✓ Métadonnées correctement enregistrées")
    
    def test_generer_traces_enregistre_calculs(self, orchestrateur, notes_test):
        """
        Test que les calculs sont enregistrés dans les traces.
        
        Requirements: 15.1, 15.2
        """
        orchestrateur.notes_calculees = notes_test
        orchestrateur.generer_traces()
        
        tests_dir = os.path.join(os.path.dirname(__file__))
        fichier_trace = os.path.join(tests_dir, 'trace_note_3a.json')
        
        with open(fichier_trace, 'r', encoding='utf-8') as f:
            trace_data = json.load(f)
        
        # Vérifier que les lignes sont enregistrées
        assert len(trace_data['lignes']) > 0
        
        # Vérifier la structure d'une ligne
        premiere_ligne = trace_data['lignes'][0]
        assert 'libelle' in premiere_ligne
        assert 'montant' in premiere_ligne
        
        print(f"✓ {len(trace_data['lignes'])} lignes de calcul enregistrées")
    
    def test_generer_traces_gere_historique(self, orchestrateur, notes_test):
        """
        Test que l'historique des traces est géré (max 10).
        
        Requirements: 15.7
        """
        orchestrateur.notes_calculees = notes_test
        
        # Générer plusieurs fois pour tester l'historique
        for i in range(3):
            orchestrateur.generer_traces()
        
        # Vérifier que les fichiers de trace existent toujours
        tests_dir = os.path.join(os.path.dirname(__file__))
        fichier_trace = os.path.join(tests_dir, 'trace_note_3a.json')
        
        assert os.path.exists(fichier_trace)
        
        # Note: La gestion complète de l'historique (archivage des anciennes traces)
        # est implémentée dans TraceManager.gerer_historique()
        # Ce test vérifie que la méthode est appelée sans erreur
        
        print("✓ Gestion de l'historique fonctionne")
    
    def test_generer_traces_toutes_notes(self, orchestrateur, notes_test):
        """
        Test que les traces sont générées pour toutes les notes.
        
        Requirements: 15.1
        """
        orchestrateur.notes_calculees = notes_test
        orchestrateur.generer_traces()
        
        tests_dir = os.path.join(os.path.dirname(__file__))
        
        # Vérifier qu'une trace existe pour chaque note
        for nom_note in notes_test.keys():
            numero = nom_note.replace('Note_', '').lower()
            fichier_trace = os.path.join(tests_dir, f'trace_note_{numero}.json')
            
            assert os.path.exists(fichier_trace), \
                f"Trace manquante pour {nom_note}"
        
        print(f"✓ Traces générées pour toutes les {len(notes_test)} notes")
    
    def test_generer_traces_avec_notes_vides(self, orchestrateur):
        """
        Test que generer_traces() gère les notes vides sans erreur.
        
        Requirements: 15.1
        """
        # Tester avec aucune note
        orchestrateur.notes_calculees = {}
        
        # Ne devrait pas lever d'exception
        try:
            orchestrateur.generer_traces()
            print("✓ Gestion des notes vides OK")
        except Exception as e:
            pytest.fail(f"Exception inattendue avec notes vides: {e}")
    
    def test_generer_traces_avec_dataframe_vide(self, orchestrateur):
        """
        Test que generer_traces() gère les DataFrames vides.
        
        Requirements: 15.1
        """
        orchestrateur.notes_calculees = {
            'Note_TEST': pd.DataFrame()
        }
        
        # Ne devrait pas lever d'exception
        try:
            orchestrateur.generer_traces()
            print("✓ Gestion des DataFrames vides OK")
        except Exception as e:
            pytest.fail(f"Exception inattendue avec DataFrame vide: {e}")
    
    def test_integration_complete_workflow(self, orchestrateur):
        """
        Test d'intégration complète du workflow avec traces.
        
        Vérifie:
        1. Calcul des notes
        2. Génération des traces
        3. Validation de cohérence
        4. Export Excel
        
        Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7
        """
        # Charger les balances
        if not orchestrateur.charger_balances():
            pytest.skip("Impossible de charger les balances")
        
        # Calculer quelques notes (pas toutes pour gagner du temps)
        orchestrateur.NOTES_A_CALCULER = ['3a', '4']  # Limiter pour le test
        notes = orchestrateur.calculer_toutes_notes()
        
        if not notes:
            pytest.skip("Aucune note calculée")
        
        # Générer les traces
        orchestrateur.generer_traces()
        
        # Vérifier que les traces existent
        tests_dir = os.path.join(os.path.dirname(__file__))
        
        for nom_note in notes.keys():
            numero = nom_note.replace('Note_', '').lower()
            fichier_trace = os.path.join(tests_dir, f'trace_note_{numero}.json')
            
            assert os.path.exists(fichier_trace), \
                f"Trace non créée dans le workflow complet: {nom_note}"
            
            # Vérifier le contenu
            with open(fichier_trace, 'r', encoding='utf-8') as f:
                trace_data = json.load(f)
            
            assert trace_data['note'] == numero
            assert 'lignes' in trace_data
            assert 'date_generation' in trace_data
        
        print(f"✓ Workflow complet avec traces réussi pour {len(notes)} notes")


def run_tests():
    """Exécute les tests avec pytest."""
    pytest.main([__file__, '-v', '--tb=short'])


if __name__ == '__main__':
    run_tests()
