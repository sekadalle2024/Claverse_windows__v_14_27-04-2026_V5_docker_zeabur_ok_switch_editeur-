"""
Property Test: Calculation Caching

Property 19: Calculation Caching
For any calculation that is repeated with the same input data, the system must return 
cached results, and the second execution must be significantly faster than the first.

Validates: Requirements 12.4

This test verifies that:
1. Balances are loaded only once and cached
2. Repeated calculations use cached balances
3. Second execution is significantly faster than first
4. Cached results are identical to fresh calculations
"""

import pytest
import os
import sys
import time
import pandas as pd
from hypothesis import given, strategies as st, settings, assume

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from calcul_notes_annexes_main import CalculNotesAnnexesMain


# ============================================================================
# STRATEGIES HYPOTHESIS
# ============================================================================

@st.composite
def st_fichier_balance_valide(draw):
    """
    Génère un chemin vers un fichier de balance valide.
    Utilise le fichier de test existant.
    """
    # Utiliser le fichier de balance de démo
    fichier = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    assume(os.path.exists(fichier))
    
    return fichier


# ============================================================================
# PROPERTY TESTS
# ============================================================================

@given(fichier_balance=st_fichier_balance_valide())
@settings(max_examples=5, deadline=120000)  # 2 minutes par exemple
def test_property_balance_caching_single_load(fichier_balance):
    """
    Property: Les balances doivent être chargées une seule fois et mises en cache.
    
    Vérifie que:
    - Premier appel à charger_balances() charge les données
    - Appels suivants utilisent le cache
    - Le cache contient les 3 balances (N, N-1, N-2)
    """
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Premier chargement
    debut1 = time.time()
    succes1 = orchestrateur.charger_balances()
    duree1 = time.time() - debut1
    
    assert succes1, "Le premier chargement doit réussir"
    assert orchestrateur.balances is not None, "Les balances doivent être en cache"
    assert len(orchestrateur.balances) == 3, "Le cache doit contenir 3 balances (N, N-1, N-2)"
    
    # Vérifier que ce sont des DataFrames
    for i, balance in enumerate(orchestrateur.balances):
        assert isinstance(balance, pd.DataFrame), f"Balance {i} doit être un DataFrame"
        assert not balance.empty, f"Balance {i} ne doit pas être vide"
    
    # Deuxième chargement (doit utiliser le cache)
    debut2 = time.time()
    succes2 = orchestrateur.charger_balances()
    duree2 = time.time() - debut2
    
    assert succes2, "Le deuxième chargement doit réussir"
    
    # Le deuxième chargement doit être beaucoup plus rapide (utilise le cache)
    # On s'attend à ce que le cache soit au moins 10x plus rapide
    assert duree2 < duree1 / 10, \
        f"Le cache doit être significativement plus rapide: {duree2:.4f}s vs {duree1:.4f}s"
    
    # Le cache doit être quasi-instantané (< 1ms)
    assert duree2 < 0.001, \
        f"L'accès au cache doit être quasi-instantané: {duree2:.4f}s < 0.001s"


@given(fichier_balance=st_fichier_balance_valide())
@settings(max_examples=3, deadline=180000)  # 3 minutes par exemple
def test_property_calculation_uses_cache(fichier_balance):
    """
    Property: Les calculs de notes doivent utiliser les balances en cache.
    
    Vérifie que:
    - Les balances sont chargées une seule fois
    - Tous les calculs de notes utilisent le même cache
    - Pas de rechargement entre les calculs
    """
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Charger les balances
    succes = orchestrateur.charger_balances()
    assert succes, "Le chargement initial doit réussir"
    
    # Sauvegarder la référence du cache
    cache_initial = orchestrateur.balances
    assert cache_initial is not None, "Le cache doit être initialisé"
    
    # Calculer quelques notes (on teste avec 3 notes pour la rapidité)
    notes_a_tester = ['3a', '4', '8']
    
    for numero_note in notes_a_tester:
        nom_note, df, succes, erreur = orchestrateur.calculer_note_individuelle(numero_note)
        
        # Vérifier que le cache n'a pas changé
        assert orchestrateur.balances is cache_initial, \
            f"Le cache ne doit pas être rechargé pour {nom_note}"
        
        # Vérifier que les balances sont toujours les mêmes objets
        for i in range(3):
            assert orchestrateur.balances[i] is cache_initial[i], \
                f"Balance {i} ne doit pas être rechargée pour {nom_note}"


@given(fichier_balance=st_fichier_balance_valide())
@settings(max_examples=3, deadline=240000)  # 4 minutes par exemple
def test_property_repeated_calculation_faster(fichier_balance):
    """
    Property: Les calculs répétés doivent être plus rapides grâce au cache.
    
    Vérifie que:
    - Premier calcul complet (avec chargement) prend du temps
    - Calculs suivants sont plus rapides (utilisent le cache)
    - Le gain de performance est significatif (au moins 20%)
    """
    # Premier calcul (sans cache préalable)
    orchestrateur1 = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    debut1 = time.time()
    # Calculer une note (3a par exemple)
    nom_note1, df1, succes1, erreur1 = orchestrateur1.calculer_note_individuelle('3a')
    duree1 = time.time() - debut1
    
    assert succes1, f"Le premier calcul doit réussir: {erreur1}"
    assert df1 is not None, "Le premier calcul doit retourner un DataFrame"
    
    # Deuxième calcul (avec cache préchargé)
    orchestrateur2 = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Précharger le cache
    orchestrateur2.charger_balances()
    
    debut2 = time.time()
    nom_note2, df2, succes2, erreur2 = orchestrateur2.calculer_note_individuelle('3a')
    duree2 = time.time() - debut2
    
    assert succes2, f"Le deuxième calcul doit réussir: {erreur2}"
    assert df2 is not None, "Le deuxième calcul doit retourner un DataFrame"
    
    # Le deuxième calcul doit être plus rapide (au moins 20% plus rapide)
    gain_performance = (duree1 - duree2) / duree1 * 100
    
    assert duree2 < duree1, \
        f"Le calcul avec cache doit être plus rapide: {duree2:.4f}s vs {duree1:.4f}s"
    
    assert gain_performance >= 20, \
        f"Le gain de performance doit être d'au moins 20%: {gain_performance:.1f}%"
    
    # Les résultats doivent être identiques
    assert df1.shape == df2.shape, "Les DataFrames doivent avoir la même forme"
    
    # Comparer les valeurs numériques (avec tolérance pour les arrondis)
    for col in df1.columns:
        if df1[col].dtype in ['float64', 'int64']:
            assert df1[col].equals(df2[col]) or \
                   (df1[col] - df2[col]).abs().max() < 0.01, \
                   f"Les valeurs de la colonne {col} doivent être identiques"


@given(fichier_balance=st_fichier_balance_valide())
@settings(max_examples=2, deadline=300000)  # 5 minutes par exemple
def test_property_cache_consistency_across_notes(fichier_balance):
    """
    Property: Le cache doit rester cohérent à travers tous les calculs de notes.
    
    Vérifie que:
    - Le cache est partagé entre tous les calculs
    - Les balances ne sont jamais modifiées
    - Tous les calculs utilisent les mêmes données sources
    """
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Charger les balances
    succes = orchestrateur.charger_balances()
    assert succes, "Le chargement doit réussir"
    
    # Créer des copies des balances pour vérifier qu'elles ne sont pas modifiées
    balances_originales = [df.copy() for df in orchestrateur.balances]
    
    # Calculer plusieurs notes
    notes_a_tester = ['3a', '4', '8']
    
    for numero_note in notes_a_tester:
        nom_note, df, succes, erreur = orchestrateur.calculer_note_individuelle(numero_note)
        
        if succes and df is not None:
            # Vérifier que les balances en cache n'ont pas été modifiées
            for i in range(3):
                assert orchestrateur.balances[i].equals(balances_originales[i]), \
                    f"Balance {i} ne doit pas être modifiée par le calcul de {nom_note}"
                
                # Vérifier que la forme n'a pas changé
                assert orchestrateur.balances[i].shape == balances_originales[i].shape, \
                    f"La forme de Balance {i} ne doit pas changer"
                
                # Vérifier que les colonnes n'ont pas changé
                assert list(orchestrateur.balances[i].columns) == list(balances_originales[i].columns), \
                    f"Les colonnes de Balance {i} ne doivent pas changer"


@given(fichier_balance=st_fichier_balance_valide())
@settings(max_examples=2, deadline=180000)  # 3 minutes par exemple
def test_property_cache_memory_efficiency(fichier_balance):
    """
    Property: Le cache doit être efficace en mémoire (pas de duplication).
    
    Vérifie que:
    - Les balances ne sont pas dupliquées en mémoire
    - Tous les calculs référencent les mêmes objets
    - Pas de copie inutile des données
    """
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Charger les balances
    succes = orchestrateur.charger_balances()
    assert succes, "Le chargement doit réussir"
    
    # Sauvegarder les IDs des objets en mémoire
    ids_originaux = [id(df) for df in orchestrateur.balances]
    
    # Calculer plusieurs notes
    notes_a_tester = ['3a', '4']
    
    for numero_note in notes_a_tester:
        nom_note, df, succes, erreur = orchestrateur.calculer_note_individuelle(numero_note)
        
        # Vérifier que les IDs des balances n'ont pas changé
        # (pas de copie, même objet en mémoire)
        ids_actuels = [id(df) for df in orchestrateur.balances]
        
        assert ids_actuels == ids_originaux, \
            f"Les balances ne doivent pas être copiées pour {nom_note}"


# ============================================================================
# TESTS UNITAIRES COMPLÉMENTAIRES
# ============================================================================

def test_cache_initialization():
    """Test que le cache est correctement initialisé à None."""
    fichier = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    if not os.path.exists(fichier):
        pytest.skip("Fichier de balance non disponible")
    
    orchestrateur = CalculNotesAnnexesMain(fichier, mode_parallele=False)
    
    # Le cache doit être None au départ
    assert orchestrateur.balances is None, "Le cache doit être None à l'initialisation"


def test_cache_persistence():
    """Test que le cache persiste entre les appels."""
    fichier = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    if not os.path.exists(fichier):
        pytest.skip("Fichier de balance non disponible")
    
    orchestrateur = CalculNotesAnnexesMain(fichier, mode_parallele=False)
    
    # Premier chargement
    orchestrateur.charger_balances()
    cache1 = orchestrateur.balances
    
    # Deuxième chargement
    orchestrateur.charger_balances()
    cache2 = orchestrateur.balances
    
    # Les deux doivent pointer vers le même objet
    assert cache1 is cache2, "Le cache doit persister entre les appels"


def test_cache_shared_across_calculations():
    """Test que le cache est partagé entre tous les calculs."""
    fichier = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    if not os.path.exists(fichier):
        pytest.skip("Fichier de balance non disponible")
    
    orchestrateur = CalculNotesAnnexesMain(fichier, mode_parallele=False)
    orchestrateur.charger_balances()
    
    cache_initial = orchestrateur.balances
    
    # Calculer une note
    orchestrateur.calculer_note_individuelle('3a')
    
    # Le cache doit être le même
    assert orchestrateur.balances is cache_initial, \
        "Le cache doit être partagé entre les calculs"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
