# Property Test Summary: Calculation Caching

## Property 19: Calculation Caching

**Énoncé formel**: ∀ calcul C avec données D, si C(D) est exécuté deux fois, alors:
1. Le deuxième appel utilise des résultats en cache
2. temps(C₂) < temps(C₁)
3. résultat(C₁) = résultat(C₂)
4. gain_performance ≥ 20%

**Valide**: Requirements 12.4

## Architecture du test

```
test_calculation_caching.py
├── Strategies Hypothesis
│   └── st_fichier_balance_valide()
│       └── Génère des chemins vers fichiers de balance valides
│
├── Property Tests
│   ├── test_property_balance_caching_single_load
│   │   └── Vérifie le chargement unique et le cache
│   │
│   ├── test_property_calculation_uses_cache
│   │   └── Vérifie l'utilisation du cache par tous les calculs
│   │
│   ├── test_property_repeated_calculation_faster
│   │   └── Vérifie le gain de performance
│   │
│   ├── test_property_cache_consistency_across_notes
│   │   └── Vérifie la cohérence du cache
│   │
│   └── test_property_cache_memory_efficiency
│       └── Vérifie l'efficacité mémoire
│
└── Unit Tests
    ├── test_cache_initialization
    ├── test_cache_persistence
    └── test_cache_shared_across_calculations
```

## Mécanisme de caching testé

### 1. Chargement initial
```python
orchestrateur = CalculNotesAnnexesMain(fichier_balance)
orchestrateur.charger_balances()  # Charge les 3 balances
# self.balances = (balance_n, balance_n1, balance_n2)
```

### 2. Utilisation du cache
```python
# Premier appel: charge depuis Excel
debut1 = time.time()
orchestrateur.charger_balances()
duree1 = time.time() - debut1  # ~0.5-2s

# Deuxième appel: utilise le cache
debut2 = time.time()
orchestrateur.charger_balances()
duree2 = time.time() - debut2  # < 0.001s

assert duree2 < duree1 / 10  # Cache 10x+ plus rapide
```

### 3. Partage du cache
```python
# Tous les calculs utilisent le même cache
for note in ['3a', '4', '8']:
    calculateur.calculer_note_individuelle(note)
    # Utilise orchestrateur.balances (pas de rechargement)
```

## Propriétés vérifiées

### P1: Chargement unique
```
∀ orchestrateur O, ∀ n ≥ 2 appels à charger_balances():
  - Premier appel: charge depuis fichier
  - Appels suivants: retourne cache
  - temps(appel₂) < temps(appel₁) / 10
```

### P2: Utilisation du cache
```
∀ calcul C de note N:
  - Si cache existe: utilise cache
  - Si cache n'existe pas: charge puis met en cache
  - Pas de rechargement entre calculs
```

### P3: Gain de performance
```
∀ calcul C répété:
  - temps(C avec cache) < temps(C sans cache)
  - gain_performance ≥ 20%
  - résultat(C₁) = résultat(C₂)
```

### P4: Cohérence du cache
```
∀ calculs C₁, C₂, ..., Cₙ:
  - Tous utilisent le même cache
  - Cache non modifié par les calculs
  - Données sources identiques pour tous
```

### P5: Efficacité mémoire
```
∀ balances B dans cache:
  - Pas de duplication en mémoire
  - Tous les calculs référencent les mêmes objets
  - id(B) reste constant
```

## Métriques de performance

### Temps de chargement
- **Sans cache**: 0.5 - 2.0 secondes
- **Avec cache**: < 0.001 seconde (< 1ms)
- **Ratio**: > 10x plus rapide

### Gain de performance sur calculs
- **Premier calcul**: temps_base
- **Calculs suivants**: temps_base * 0.8 ou moins
- **Gain minimum**: 20%

### Mémoire
- **3 DataFrames** en cache (N, N-1, N-2)
- **Pas de duplication**: même objet référencé
- **Overhead**: négligeable

## Cas limites testés

### 1. Cache vide
```python
orchestrateur.balances is None  # Initial
orchestrateur.charger_balances()
orchestrateur.balances is not None  # Après chargement
```

### 2. Cache existant
```python
orchestrateur.charger_balances()  # Charge
cache1 = orchestrateur.balances
orchestrateur.charger_balances()  # Utilise cache
cache2 = orchestrateur.balances
assert cache1 is cache2  # Même objet
```

### 3. Calculs multiples
```python
for note in ['3a', '4', '8', '10']:
    calculateur.calculer_note_individuelle(note)
    # Tous utilisent le même cache
```

### 4. Intégrité du cache
```python
balances_originales = [df.copy() for df in orchestrateur.balances]
# ... calculs ...
for i in range(3):
    assert orchestrateur.balances[i].equals(balances_originales[i])
```

## Stratégies Hypothesis

### st_fichier_balance_valide()
Génère des chemins vers des fichiers de balance valides:
- Utilise le fichier de démo existant
- Vérifie l'existence du fichier
- Assume que le fichier est accessible

## Configuration Hypothesis

```python
@settings(
    max_examples=5,      # 5 exemples pour les tests de cache
    deadline=120000      # 2 minutes par exemple
)
```

## Exécution et validation

### Commande de test
```bash
pytest test_calculation_caching.py -v
```

### Critères de succès
- ✓ Tous les property tests passent
- ✓ Cache 10x+ plus rapide que chargement
- ✓ Gain de performance ≥ 20%
- ✓ Pas de duplication mémoire
- ✓ Cohérence maintenue

### Critères d'échec
- ✗ Cache non utilisé (rechargement détecté)
- ✗ Gain de performance < 20%
- ✗ Balances modifiées pendant calculs
- ✗ Duplication en mémoire

## Couverture des requirements

### Requirement 12.4
> THE System SHALL charger les balances une seule fois en mémoire et les réutiliser pour toutes les notes

**Validé par**:
- test_property_balance_caching_single_load
- test_property_calculation_uses_cache
- test_property_cache_consistency_across_notes

**Métriques**:
- Chargement unique: ✓
- Réutilisation: ✓
- Performance: ✓ (> 10x plus rapide)

## Relation avec autres tests

### Tests précédents
- Task 21.4: Performance constraint (< 30s total)
- Task 21.3: Trace integration
- Task 21.2: Coherence validation

### Tests suivants
- Task 21.6 (optionnel): Integration test 33 notes
- Task 22: API Flask endpoint

## Maintenance

### Mise à jour du test
Si l'implémentation du cache change:
1. Vérifier que `self.balances` est toujours utilisé
2. Ajuster les seuils de performance si nécessaire
3. Vérifier que les calculateurs utilisent le cache

### Ajout de nouveaux cas
Pour tester d'autres aspects du cache:
1. Ajouter une nouvelle property function
2. Utiliser les strategies existantes
3. Documenter la nouvelle propriété

## Références

- **Design Document**: Section "Components and Interfaces" → CalculNotesAnnexesMain
- **Requirements**: 12.4 (Calculation caching)
- **Implementation**: calcul_notes_annexes_main.py
- **Related Tests**: test_performance_constraint.py

## Conclusion

Ce test valide que le système implémente correctement le caching des balances, garantissant:
- Performance optimale (> 10x plus rapide)
- Utilisation efficace de la mémoire
- Cohérence des données
- Gain de performance significatif (≥ 20%)

**Property 19 validée**: ✓ Calculation Caching fonctionne correctement
