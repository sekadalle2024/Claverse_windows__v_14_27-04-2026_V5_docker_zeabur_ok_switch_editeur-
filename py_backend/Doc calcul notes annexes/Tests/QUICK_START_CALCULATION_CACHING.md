# Quick Start - Property Test: Calculation Caching

## Vue d'ensemble

Ce test valide la **Property 19: Calculation Caching** qui garantit que les calculs répétés utilisent des résultats en cache et sont significativement plus rapides.

## Exécution rapide

```powershell
# Depuis le dossier racine du projet
cd py_backend/Doc calcul notes annexes/Tests
pytest test_calculation_caching.py -v
```

## Ce qui est testé

### Property 19: Calculation Caching

**Énoncé**: Pour tout calcul répété avec les mêmes données d'entrée, le système doit retourner des résultats en cache, et la deuxième exécution doit être significativement plus rapide que la première.

**Valide**: Requirements 12.4

### Tests de propriétés

1. **test_property_balance_caching_single_load**
   - Les balances sont chargées une seule fois
   - Les appels suivants utilisent le cache
   - Le cache est au moins 10x plus rapide
   - L'accès au cache est quasi-instantané (< 1ms)

2. **test_property_calculation_uses_cache**
   - Tous les calculs utilisent le même cache
   - Pas de rechargement entre les calculs
   - Les références mémoire restent identiques

3. **test_property_repeated_calculation_faster**
   - Premier calcul avec chargement prend du temps
   - Calculs suivants sont plus rapides (gain ≥ 20%)
   - Les résultats sont identiques

4. **test_property_cache_consistency_across_notes**
   - Le cache reste cohérent à travers tous les calculs
   - Les balances ne sont jamais modifiées
   - Tous les calculs utilisent les mêmes données sources

5. **test_property_cache_memory_efficiency**
   - Pas de duplication en mémoire
   - Tous les calculs référencent les mêmes objets
   - Pas de copie inutile des données

## Résultats attendus

```
✓ test_property_balance_caching_single_load - PASSED
  - Cache 10x+ plus rapide que le chargement initial
  - Accès cache < 1ms

✓ test_property_calculation_uses_cache - PASSED
  - Même cache utilisé pour toutes les notes
  - Pas de rechargement détecté

✓ test_property_repeated_calculation_faster - PASSED
  - Gain de performance ≥ 20%
  - Résultats identiques

✓ test_property_cache_consistency_across_notes - PASSED
  - Balances non modifiées
  - Cohérence maintenue

✓ test_property_cache_memory_efficiency - PASSED
  - Pas de duplication mémoire
  - Références identiques
```

## Interprétation des résultats

### ✓ Tous les tests passent
Le système implémente correctement le caching:
- Les balances sont chargées une seule fois
- Le cache est utilisé efficacement
- Les performances sont optimisées
- La cohérence est maintenue

### ✗ Échec: Cache non utilisé
Si `test_property_calculation_uses_cache` échoue:
- Les balances sont rechargées à chaque calcul
- Vérifier que `self.balances` est bien utilisé
- Vérifier que les calculateurs utilisent le cache

### ✗ Échec: Performance insuffisante
Si `test_property_repeated_calculation_faster` échoue:
- Le gain de performance est < 20%
- Le cache n'est peut-être pas utilisé
- Vérifier l'implémentation du cache

### ✗ Échec: Incohérence du cache
Si `test_property_cache_consistency_across_notes` échoue:
- Les balances sont modifiées pendant les calculs
- Risque de résultats incorrects
- Vérifier que les calculs ne modifient pas les DataFrames

## Commandes utiles

```powershell
# Exécuter uniquement les property tests
pytest test_calculation_caching.py -k "property" -v

# Exécuter avec plus d'exemples Hypothesis
pytest test_calculation_caching.py --hypothesis-show-statistics

# Exécuter avec timeout étendu
pytest test_calculation_caching.py --timeout=600

# Voir les détails de performance
pytest test_calculation_caching.py -v -s
```

## Dépendances

- pytest
- hypothesis
- pandas
- Modules: balance_reader, calcul_notes_annexes_main
- Fichier: P000 -BALANCE DEMO N_N-1_N-2.xls

## Durée d'exécution

- Tests property: ~5-10 minutes (avec Hypothesis)
- Tests unitaires: ~10-30 secondes
- Total: ~10-15 minutes

## Prochaines étapes

Après validation de ce test:
1. ✓ Task 21.5 complétée
2. → Passer à Task 21.6 (optionnel): Integration test pour les 33 notes
3. → Continuer avec Task 22: API Flask endpoint

## Notes importantes

- Le cache est implémenté dans `CalculNotesAnnexesMain.balances`
- Le chargement se fait via `charger_balances()`
- Les calculateurs individuels utilisent le cache s'il existe
- Le cache contient 3 DataFrames (N, N-1, N-2)
- Requirement 12.4 validé par ces tests
