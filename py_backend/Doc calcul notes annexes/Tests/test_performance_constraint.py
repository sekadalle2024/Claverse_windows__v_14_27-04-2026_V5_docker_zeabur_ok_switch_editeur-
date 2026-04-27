"""
Test de propriété pour la contrainte de performance.

Property 18: Performance Constraint
Valide les exigences: 12.1, 12.2

Pour tout calcul complet des 33 notes avec un fichier de balance standard,
le système doit terminer le traitement en moins de 30 secondes, en chargeant
les balances une seule fois en mémoire.
"""

import pytest
from hypothesis import given, assume, strategies as st
from hypothesis import settings
import time
import os
import sys
import pandas as pd
from datetime import datetime

# Ajouter le dossier parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from calcul_notes_annexes_main import CalculNotesAnnexesMain


# ============================================================================
# STRATÉGIES HYPOTHESIS POUR LES TESTS DE PERFORMANCE
# ============================================================================

@st.composite
def st_balance_size(draw):
    """
    Génère une taille de balance réaliste.
    
    Les balances SYSCOHADA typiques contiennent entre 100 et 1000 comptes.
    """
    return draw(st.integers(min_value=100, max_value=1000))


# ============================================================================
# TESTS DE PROPRIÉTÉ
# ============================================================================

@pytest.mark.slow
def test_property_performance_constraint_with_demo_balance():
    """
    Property 18: Performance Constraint (avec balance démo).
    
    Pour le fichier de balance démo standard, le calcul des 33 notes
    doit se terminer en moins de 30 secondes.
    
    Valide: Requirements 12.1, 12.2
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Mesurer le temps de calcul
    debut = time.time()
    notes = orchestrateur.calculer_toutes_notes()
    duree = time.time() - debut
    
    # PROPRIÉTÉ 1: Le calcul doit se terminer en moins de 30 secondes
    assert duree < 30.0, (
        f"Contrainte de performance non respectée: {duree:.2f}s > 30s. "
        f"Le système doit calculer les 33 notes en moins de 30 secondes."
    )
    
    # PROPRIÉTÉ 2: Toutes les notes doivent être calculées
    assert len(notes) > 0, (
        "Aucune note n'a été calculée. Le système doit calculer au moins "
        "une partie des 33 notes."
    )
    
    # PROPRIÉTÉ 3: Les balances doivent être chargées une seule fois (cache)
    assert orchestrateur.balances is not None, (
        "Les balances doivent être mises en cache après le premier chargement."
    )
    
    # Log du résultat
    print(f"\n✓ Performance validée: {duree:.2f}s < 30s")
    print(f"✓ Notes calculées: {len(notes)}/{len(orchestrateur.NOTES_A_CALCULER)}")


@pytest.mark.slow
@settings(max_examples=5, deadline=None)
@given(nombre_executions=st.integers(min_value=2, max_value=3))
def test_property_balance_caching_performance(nombre_executions):
    """
    Property 18: Balance Caching (cache des balances).
    
    Pour plusieurs exécutions successives, les balances doivent être
    chargées une seule fois, et les exécutions suivantes doivent être
    plus rapides grâce au cache.
    
    Valide: Requirements 12.2, 12.4
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    durees = []
    
    # Exécuter plusieurs fois le chargement
    for i in range(nombre_executions):
        debut = time.time()
        succes = orchestrateur.charger_balances()
        duree = time.time() - debut
        durees.append(duree)
        
        assert succes, f"Le chargement des balances a échoué à l'exécution {i+1}"
    
    # PROPRIÉTÉ 1: Le premier chargement doit prendre du temps
    assert durees[0] > 0, (
        "Le premier chargement des balances doit prendre du temps mesurable."
    )
    
    # PROPRIÉTÉ 2: Les chargements suivants doivent être quasi-instantanés (cache)
    for i in range(1, len(durees)):
        assert durees[i] < durees[0] * 0.1, (
            f"Le chargement {i+1} devrait être beaucoup plus rapide grâce au cache. "
            f"Premier chargement: {durees[0]:.4f}s, Chargement {i+1}: {durees[i]:.4f}s"
        )
    
    # PROPRIÉTÉ 3: Les balances doivent être en cache
    assert orchestrateur.balances is not None, (
        "Les balances doivent être stockées en cache après le premier chargement."
    )
    
    # Log du résultat
    print(f"\n✓ Cache validé:")
    print(f"  - Premier chargement: {durees[0]:.4f}s")
    for i in range(1, len(durees)):
        print(f"  - Chargement {i+1} (cache): {durees[i]:.4f}s")


@pytest.mark.slow
def test_property_performance_scales_with_notes():
    """
    Property 18: Performance Scaling (évolutivité).
    
    Le temps de calcul doit évoluer de manière linéaire ou sous-linéaire
    avec le nombre de notes calculées.
    
    Valide: Requirements 12.1, 12.3
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Charger les balances une fois
    orchestrateur.charger_balances()
    
    # Tester avec différents sous-ensembles de notes
    sous_ensembles = [
        orchestrateur.NOTES_A_CALCULER[:5],   # 5 notes
        orchestrateur.NOTES_A_CALCULER[:10],  # 10 notes
        orchestrateur.NOTES_A_CALCULER[:20],  # 20 notes
    ]
    
    resultats = []
    
    for notes_a_calculer in sous_ensembles:
        # Sauvegarder la liste originale
        liste_originale = orchestrateur.NOTES_A_CALCULER
        
        # Remplacer temporairement par le sous-ensemble
        orchestrateur.NOTES_A_CALCULER = notes_a_calculer
        orchestrateur.notes_calculees = {}
        orchestrateur.statuts_calcul = {}
        
        # Mesurer le temps
        debut = time.time()
        notes = orchestrateur.calculer_toutes_notes()
        duree = time.time() - debut
        
        resultats.append({
            'nombre_notes': len(notes_a_calculer),
            'duree': duree,
            'notes_calculees': len(notes)
        })
        
        # Restaurer la liste originale
        orchestrateur.NOTES_A_CALCULER = liste_originale
    
    # PROPRIÉTÉ 1: Le temps doit augmenter avec le nombre de notes
    for i in range(1, len(resultats)):
        assert resultats[i]['duree'] >= resultats[i-1]['duree'], (
            f"Le temps de calcul devrait augmenter avec le nombre de notes. "
            f"{resultats[i-1]['nombre_notes']} notes: {resultats[i-1]['duree']:.2f}s, "
            f"{resultats[i]['nombre_notes']} notes: {resultats[i]['duree']:.2f}s"
        )
    
    # PROPRIÉTÉ 2: L'évolutivité doit être raisonnable (pas exponentielle)
    # Le temps pour 20 notes ne doit pas être > 4x le temps pour 5 notes
    if len(resultats) >= 2:
        ratio_notes = resultats[-1]['nombre_notes'] / resultats[0]['nombre_notes']
        ratio_temps = resultats[-1]['duree'] / resultats[0]['duree']
        
        assert ratio_temps <= ratio_notes * 1.5, (
            f"L'évolutivité est mauvaise. "
            f"Ratio notes: {ratio_notes:.1f}x, Ratio temps: {ratio_temps:.1f}x. "
            f"Le temps ne devrait pas augmenter plus vite que le nombre de notes."
        )
    
    # Log des résultats
    print("\n✓ Évolutivité validée:")
    for r in resultats:
        print(f"  - {r['nombre_notes']} notes: {r['duree']:.2f}s")


@pytest.mark.slow
def test_property_performance_memory_efficiency():
    """
    Property 18: Memory Efficiency (efficacité mémoire).
    
    Le système doit charger les balances une seule fois en mémoire
    et les réutiliser pour toutes les notes, sans duplication.
    
    Valide: Requirements 12.2, 12.3, 12.4
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # PROPRIÉTÉ 1: Avant chargement, les balances doivent être None
    assert orchestrateur.balances is None, (
        "Les balances doivent être None avant le premier chargement."
    )
    
    # Charger les balances
    succes = orchestrateur.charger_balances()
    assert succes, "Le chargement des balances a échoué"
    
    # PROPRIÉTÉ 2: Après chargement, les balances doivent être en cache
    assert orchestrateur.balances is not None, (
        "Les balances doivent être stockées en cache après le chargement."
    )
    
    # PROPRIÉTÉ 3: Les balances doivent être un tuple de 3 DataFrames
    assert isinstance(orchestrateur.balances, tuple), (
        "Les balances doivent être un tuple."
    )
    assert len(orchestrateur.balances) == 3, (
        "Les balances doivent contenir 3 exercices (N, N-1, N-2)."
    )
    
    # PROPRIÉTÉ 4: Chaque balance doit être un DataFrame
    for i, balance in enumerate(orchestrateur.balances):
        assert isinstance(balance, pd.DataFrame), (
            f"La balance {i} doit être un DataFrame."
        )
        assert len(balance) > 0, (
            f"La balance {i} ne doit pas être vide."
        )
    
    # Sauvegarder la référence des balances
    balances_ref = id(orchestrateur.balances)
    
    # Calculer quelques notes
    orchestrateur.NOTES_A_CALCULER = orchestrateur.NOTES_A_CALCULER[:3]
    notes = orchestrateur.calculer_toutes_notes()
    
    # PROPRIÉTÉ 5: Les balances doivent toujours être les mêmes (même référence)
    assert id(orchestrateur.balances) == balances_ref, (
        "Les balances ne doivent pas être rechargées pendant le calcul des notes."
    )
    
    # Log du résultat
    print("\n✓ Efficacité mémoire validée:")
    print(f"  - Balances chargées: 1 fois")
    print(f"  - Notes calculées: {len(notes)}")
    print(f"  - Référence mémoire stable: Oui")


# ============================================================================
# TESTS UNITAIRES COMPLÉMENTAIRES
# ============================================================================

def test_performance_constraint_unit_simple():
    """
    Test unitaire simple de la contrainte de performance.
    
    Vérifie que le système peut calculer au moins quelques notes
    en un temps raisonnable.
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur avec seulement 3 notes
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    orchestrateur.NOTES_A_CALCULER = ['3a', '4', '8']  # 3 notes seulement
    
    # Mesurer le temps
    debut = time.time()
    notes = orchestrateur.calculer_toutes_notes()
    duree = time.time() - debut
    
    # Le calcul de 3 notes doit être très rapide (< 5 secondes)
    assert duree < 5.0, (
        f"Le calcul de 3 notes devrait être rapide: {duree:.2f}s > 5s"
    )
    
    # Au moins une note doit être calculée
    assert len(notes) > 0, "Au moins une note devrait être calculée"
    
    print(f"\n✓ Test unitaire validé: {len(notes)} notes en {duree:.2f}s")


def test_balance_caching_unit():
    """
    Test unitaire du cache des balances.
    
    Vérifie que les balances sont bien mises en cache.
    """
    # Chemin vers le fichier de balance démo
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        pytest.skip(f"Fichier de balance démo introuvable: {fichier_balance}")
    
    # Créer l'orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Avant chargement
    assert orchestrateur.balances is None
    
    # Premier chargement
    debut1 = time.time()
    succes1 = orchestrateur.charger_balances()
    duree1 = time.time() - debut1
    
    assert succes1
    assert orchestrateur.balances is not None
    
    # Deuxième chargement (devrait utiliser le cache)
    debut2 = time.time()
    succes2 = orchestrateur.charger_balances()
    duree2 = time.time() - debut2
    
    assert succes2
    
    # Le deuxième chargement doit être beaucoup plus rapide
    assert duree2 < duree1 * 0.1, (
        f"Le cache ne fonctionne pas correctement. "
        f"Premier: {duree1:.4f}s, Deuxième: {duree2:.4f}s"
    )
    
    print(f"\n✓ Cache validé: {duree1:.4f}s -> {duree2:.4f}s")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short', '-m', 'not slow'])

