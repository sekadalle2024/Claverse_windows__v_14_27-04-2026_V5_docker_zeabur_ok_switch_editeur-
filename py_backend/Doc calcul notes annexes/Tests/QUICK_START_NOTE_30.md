# Quick Start - Note 30: Production Immobilisée

## Vue d'ensemble

La Note 30 calcule la **Production Immobilisée** à partir des comptes de la classe 72X du plan comptable SYSCOHADA révisé.

## Comptes utilisés

| Compte | Description |
|--------|-------------|
| 721    | Production immobilisée - Immobilisations incorporelles |
| 722    | Production immobilisée - Immobilisations corporelles |
| 726    | Production immobilisée - Immobilisations financières |

## Exécution rapide

### Depuis le dossier Scripts

```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_30.py
```

### Depuis la racine du projet

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_30.py"
```

### Avec PowerShell (test-note-30.ps1)

```powershell
.\test-note-30.ps1
```

## Fichiers générés

- **HTML**: `py_backend/Doc calcul notes annexes/Tests/test_note_30.html`
- **Trace JSON**: `py_backend/Doc calcul notes annexes/Tests/note_30_trace.json`

## Structure de la note

La Note 30 présente:

1. **Production immobilisée - Immobilisations incorporelles**
   - Exercice N
   - Exercice N-1
   - Variation N / N-1

2. **Production immobilisée - Immobilisations corporelles**
   - Exercice N
   - Exercice N-1
   - Variation N / N-1

3. **Production immobilisée - Immobilisations financières**
   - Exercice N
   - Exercice N-1
   - Variation N / N-1

4. **TOTAL**
   - Exercice N
   - Exercice N-1
   - Variation N / N-1

## Colonnes du tableau

| Colonne | Description |
|---------|-------------|
| Exercice | Libellé de la ligne (N, N-1, Variation) |
| Montant | Montant de la production immobilisée |
| Mouvements Crédit | Productions enregistrées |
| Mouvements Débit | Reprises/annulations |

## Exemple de sortie console

```
════════════════════════════════════════════════════════════════════════════════
  CALCUL NOTE 30 - PRODUCTION IMMOBILISÉE
════════════════════════════════════════════════════════════════════════════════

✓ Balances chargées avec succès
  - Balance N:   1234 comptes
  - Balance N-1: 1234 comptes
  - Balance N-2: 1234 comptes

  Calcul: Production immobilisée - Immobilisations incorporelles...
    Exercice N:           500,000
    Exercice N-1:         450,000
    Variation:             50,000 (+11.1%)

  Calcul: Production immobilisée - Immobilisations corporelles...
    Exercice N:         2,000,000
    Exercice N-1:       1,800,000
    Variation:           200,000 (+11.1%)

  Calcul: Production immobilisée - Immobilisations financières...
    Exercice N:                 0
    Exercice N-1:               0
    Variation:                  0 (+0.0%)

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 30
────────────────────────────────────────────────────────────────────────────────

  Production Immobilisée Exercice N:        2,500,000
  Production Immobilisée Exercice N-1:      2,250,000
  Variation:                                  250,000
  Variation %:                                   11.1%

✓ Fichier HTML généré: ../Tests/test_note_30.html
✓ Fichier de trace généré: ../Tests/note_30_trace.json

════════════════════════════════════════════════════════════════════════════════
  NOTE 30 CALCULÉE AVEC SUCCÈS
════════════════════════════════════════════════════════════════════════════════
```

## Validation des résultats

### Vérifications automatiques

Le script effectue les vérifications suivantes:
- ✓ Chargement des 3 balances (N, N-1, N-2)
- ✓ Extraction des comptes 72X
- ✓ Calcul des montants pour N et N-1
- ✓ Calcul de la variation
- ✓ Génération du HTML conforme SYSCOHADA
- ✓ Traçabilité complète des calculs

### Vérifications manuelles

1. Ouvrir le fichier HTML généré
2. Vérifier que les montants correspondent aux comptes 72X de la balance
3. Vérifier la cohérence entre N et N-1
4. Vérifier que la variation = N - N-1

## Dépannage

### Erreur: "Balance non trouvée"
- Vérifier que le fichier `P000 -BALANCE DEMO N_N-1_N-2.xlsx` existe
- Vérifier le chemin relatif depuis le script

### Erreur: "Onglet manquant"
- Vérifier que les onglets "BALANCE N", "BALANCE N-1", "BALANCE N-2" existent
- Vérifier l'orthographe exacte des noms d'onglets

### Montants à zéro
- Normal si l'entreprise n'a pas de production immobilisée
- Vérifier les comptes 72X dans la balance

## Intégration

Ce script fait partie du système de calcul automatique des 33 notes annexes SYSCOHADA révisé.

### Modules utilisés
- `calculateur_note_template.py`: Classe de base
- `account_extractor.py`: Extraction des comptes
- `movement_calculator.py`: Calcul des mouvements
- `html_generator.py`: Génération HTML
- `trace_manager.py`: Traçabilité

### Prochaines étapes
- Note 31: Subventions d'Exploitation
- Note 32: Reprises de Provisions
- Note 33: Produits Financiers

## Références

- **Requirements**: 5.1, 5.2, 5.3, 5.4
- **Design**: Section "Calculateur_Note (Template)"
- **Plan comptable**: SYSCOHADA Révisé - Classe 72
