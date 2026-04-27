# Quick Start - Note 23: Autres Achats

## Vue d'ensemble

Ce guide vous permet de tester rapidement le calculateur de la **Note 23 - Autres Achats** du système SYSCOHADA Révisé.

## Prérequis

- Python 3.8+
- Modules installés: pandas, openpyxl
- Fichier de balance: `P000 -BALANCE DEMO N_N-1_N-2.xlsx`

## Exécution rapide

### Option 1: Script PowerShell (Recommandé)

```powershell
.\test-note-23.ps1
```

### Option 2: Ligne de commande Python

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_23.py"
```

### Option 3: Avec paramètres personnalisés

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_23.py" \
    "chemin/vers/balance.xlsx" \
    --output-html "chemin/sortie.html" \
    --output-trace "chemin/trace.json"
```

## Comptes SYSCOHADA utilisés

La Note 23 calcule les **Autres Achats** à partir des comptes suivants:

| Compte | Description |
|--------|-------------|
| 604 | Achats stockés - Matières et fournitures consommables |
| 605 | Achats stockés - Emballages |
| 606 | Achats non stockés de matières et fournitures |
| 607 | Achats de marchandises |
| 608 | Achats d'emballages |

## Structure de la note

La Note 23 présente:

1. **Autres achats - Exercice N**: Montant total des autres achats de l'exercice en cours
2. **Autres achats - Exercice N-1**: Montant total des autres achats de l'exercice précédent
3. **Variation N / N-1**: Différence entre les deux exercices (montant et pourcentage)

## Fichiers générés

Après exécution, les fichiers suivants sont créés:

- **HTML**: `py_backend/Doc calcul notes annexes/Tests/test_note_23.html`
  - Visualisation formatée de la note
  - Conforme au format SYSCOHADA officiel
  
- **Trace JSON**: `py_backend/Doc calcul notes annexes/Tests/note_23_trace.json`
  - Traçabilité complète des calculs
  - Comptes sources utilisés
  - Métadonnées de génération

## Visualisation du résultat

### Windows

```powershell
start "py_backend/Doc calcul notes annexes/Tests/test_note_23.html"
```

### Linux/Mac

```bash
xdg-open "py_backend/Doc calcul notes annexes/Tests/test_note_23.html"
```

## Exemple de sortie console

```
================================================================================
  CALCULATEUR NOTE 23 - AUTRES ACHATS
================================================================================

📂 Chargement des balances depuis: ../../P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 150 lignes chargées
✓ Balance N-2 : 150 lignes chargées

🔢 Calcul de la note 23...
  Calcul: Autres achats...
    Exercice N:       5,250,000
    Exercice N-1:     4,800,000
    Variation:          450,000 (+9.4%)
✓ Note calculée: 3 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: ../Tests/test_note_23.html
✓ Fichier de trace sauvegardé: ../Tests/note_23_trace.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 23
────────────────────────────────────────────────────────────────────────────────

  Achats Exercice N:        5,250,000
  Achats Exercice N-1:      4,800,000
  Variation:                  450,000
  Variation %:                   9.4%

================================================================================
  ✓ NOTE 23 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Validation des résultats

### Vérifications automatiques

Le calculateur effectue automatiquement:

1. ✓ Chargement des 3 balances (N, N-1, N-2)
2. ✓ Extraction des comptes 604, 605, 606, 607, 608
3. ✓ Calcul des montants pour N et N-1
4. ✓ Calcul de la variation
5. ✓ Génération HTML conforme SYSCOHADA
6. ✓ Traçabilité complète

### Vérifications manuelles recommandées

1. Ouvrir le fichier HTML généré
2. Vérifier que les montants sont cohérents
3. Comparer avec les balances sources
4. Vérifier le calcul de variation

## Dépannage

### Erreur: Module non trouvé

```bash
pip install pandas openpyxl
```

### Erreur: Fichier de balance non trouvé

Vérifier que le fichier `P000 -BALANCE DEMO N_N-1_N-2.xlsx` existe à la racine du projet.

### Erreur: Onglet manquant

Le fichier de balance doit contenir 3 onglets:
- BALANCE N
- BALANCE N-1
- BALANCE N-2

## Intégration dans le workflow complet

Cette note fait partie du système complet de calcul des 33 notes annexes SYSCOHADA. Pour calculer toutes les notes:

```bash
python "py_backend/Doc calcul notes annexes/calcul_notes_annexes_main.py"
```

## Support

Pour plus d'informations:
- Voir `py_backend/Doc calcul notes annexes/README.md`
- Consulter les requirements: `.kiro/specs/calcul-notes-annexes-syscohada/requirements.md`
- Consulter le design: `.kiro/specs/calcul-notes-annexes-syscohada/design.md`

---

**Date de création**: 26 Avril 2026  
**Version**: 1.0  
**Statut**: ✓ Opérationnel
