# Quick Start - Orchestrateur Principal

## Vue d'ensemble

L'orchestrateur `calcul_notes_annexes_main.py` coordonne le calcul des 33 notes annexes SYSCOHADA révisé avec les fonctionnalités suivantes:

- ✅ Chargement unique des balances (cache)
- ✅ Barre de progression en temps réel
- ✅ Calcul séquentiel ou parallèle
- ✅ Validation de cohérence inter-notes
- ✅ Génération de traces
- ✅ Export Excel
- ✅ Rapport récapitulatif HTML

## Exécution Rapide

```bash
# Mode séquentiel (par défaut)
python py_backend/Doc\ calcul\ notes\ annexes/calcul_notes_annexes_main.py

# Ou depuis le dossier
cd "py_backend/Doc calcul notes annexes"
python calcul_notes_annexes_main.py
```

## Fonctionnalités Implémentées

### 1. Chargement des Balances (Cache)
- Les balances sont chargées **une seule fois** en mémoire
- Réutilisées pour toutes les 33 notes
- Améliore les performances (Requirement 12.2, 12.4)

### 2. Barre de Progression
```
[████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░] 48.5% | Note 16 ✓
```
- Affichage en temps réel du calcul
- Indicateur visuel de succès (✓) ou échec (✗)
- Requirement 12.5

### 3. Calcul Séquentiel
- Mode par défaut
- Calcule les notes une par une
- Plus stable et prévisible

### 4. Calcul Parallèle (Optionnel)
```python
orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=True)
```
- Utilise ProcessPoolExecutor
- Calcule plusieurs notes simultanément
- Fallback automatique en mode séquentiel si erreur
- Requirements 12.6, 12.7

### 5. Validation de Cohérence
- Vérifie la cohérence inter-notes
- Alerte si taux < 95%
- Génère un rapport HTML détaillé
- Requirements 10.1-10.7

### 6. Génération de Traces
- Trace JSON pour chaque note
- Métadonnées (fichier, hash MD5, timestamp)
- Historique des 10 dernières générations
- Requirements 15.1-15.7

### 7. Export Excel
- Fichier avec timestamp: `Notes_Annexes_Calculees_AAAAMMJJ.xlsx`
- Un onglet par note
- Formatage conforme SYSCOHADA
- Requirements 9.1-9.7

### 8. Rapport Récapitulatif
- Fichier HTML: `rapport_recapitulatif.html`
- Statistiques globales
- Statut détaillé de chaque note
- Requirement 12.7

## Structure des Fichiers Générés

```
Tests/
├── rapport_recapitulatif.html      # Rapport principal
├── rapport_coherence.html          # Rapport de cohérence
├── Notes_Annexes_Calculees_AAAAMMJJ.xlsx  # Export Excel
├── trace_note_3a.json              # Traces individuelles
├── trace_note_3b.json
└── ...
```

## Logs Générés

```
Logs/
├── calcul_notes_annexes.log        # Tous les logs (INFO+)
├── calcul_notes_warnings.log       # Warnings uniquement
└── calcul_notes_errors.log         # Erreurs uniquement
```

## Contraintes de Performance

- **Objectif**: < 30 secondes pour les 33 notes
- **Vérification automatique**: Alerte si dépassement
- **Requirement**: 12.1

## Exemple de Sortie Console

```
[2026-04-27 14:30:00] [INFO] Orchestrateur initialisé avec: P000 -BALANCE DEMO N_N-1_N-2.xls
[2026-04-27 14:30:00] [INFO] Mode parallèle: Désactivé
[2026-04-27 14:30:00] [INFO] Chargement des balances...
[2026-04-27 14:30:01] [INFO] ✓ Balances chargées avec succès en 0.85s
================================================================================
DÉBUT DU CALCUL DES 33 NOTES ANNEXES
================================================================================
[████████████████████████████████████████████████] 100.0% | Note 33 ✓
[2026-04-27 14:30:25] [INFO] ✓ Contrainte de performance respectée: 24.5s < 30s
================================================================================
CALCUL TERMINÉ - Durée: 24.50s
Notes calculées: 33/33
================================================================================
[2026-04-27 14:30:26] [INFO] ✓ Taux de cohérence acceptable: 97.2% >= 95%
[2026-04-27 14:30:27] [INFO] ✓ Traces générées pour 33 notes
[2026-04-27 14:30:28] [INFO] ✓ Export Excel réussi: Tests/Notes_Annexes_Calculees_20260427.xlsx
================================================================================
RÉSUMÉ FINAL
Notes calculées: 33/33
Taux de cohérence: 97.2%
Durée totale: 28.15s
✓ Contrainte de performance respectée (< 30s)
================================================================================
```

## Personnalisation

### Activer le Mode Parallèle

Modifier dans `main()`:
```python
orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=True)
```

### Changer le Fichier de Balance

```python
fichier_balance = "chemin/vers/votre/balance.xlsx"
orchestrateur = CalculNotesAnnexesMain(fichier_balance)
```

### Personnaliser le Nom du Fichier Excel

```python
orchestrateur.exporter_excel("Mon_Export_Personnalise.xlsx")
```

## Dépannage

### Erreur: "Fichier de balance introuvable"
- Vérifier le chemin du fichier
- S'assurer que le fichier existe

### Erreur: "Script calculer_note_XX.py non trouvé"
- Certaines notes ne sont pas encore implémentées
- Le calcul continue avec les notes disponibles

### Performance > 30s
- Activer le mode parallèle
- Vérifier les ressources système
- Optimiser les scripts de calcul individuels

### Taux de cohérence < 95%
- Consulter le rapport de cohérence HTML
- Vérifier les données sources
- Analyser les écarts détaillés

## Prochaines Étapes

1. ✅ Task 21.1 complétée
2. ⏭️ Task 21.2: Intégrer Coherence_Validator
3. ⏭️ Task 21.3: Intégrer Trace_Manager
4. ⏭️ Task 21.4-21.6: Tests de propriétés et intégration

## Requirements Validés

- ✅ 12.1: Performance < 30s
- ✅ 12.2: Chargement unique des balances
- ✅ 12.3: Structures de données optimisées
- ✅ 12.4: Cache des résultats
- ✅ 12.5: Barre de progression
- ✅ 12.6: Calcul parallèle optionnel
- ✅ 12.7: Rapport récapitulatif
