# Quick Start - Note 18: Charges Constatées d'Avance

## Vue d'ensemble

La Note 18 calcule les mouvements des charges constatées d'avance (compte 476).

## Comptes SYSCOHADA concernés

- **476**: Charges constatées d'avance

## Structure de la note

La note présente:
- Solde début exercice
- Augmentations (nouvelles charges constatées d'avance)
- Diminutions (charges imputées à l'exercice)
- Solde fin exercice

## Exécution rapide

```powershell
# Depuis la racine du projet
.\test-note-18.ps1
```

Ou directement:

```powershell
cd py_backend
python "Doc calcul notes annexes/Scripts/calculer_note_18.py"
```

## Fichiers générés

- **HTML**: `py_backend/Doc calcul notes annexes/Tests/test_note_18.html`
- **Trace**: `py_backend/Doc calcul notes annexes/Tests/trace_note_18.json`

## Validation

Le calculateur vérifie automatiquement:
- ✓ Cohérence comptable: Solde clôture = Solde ouverture + Augmentations - Diminutions
- ✓ Traçabilité complète des calculs

## Exemple de sortie

```
========================================
CALCUL NOTE 18 - CHARGES CONSTATÉES D'AVANCE
========================================

Chargement des balances...
  ✓ Balance N chargée: 150 comptes
  ✓ Balance N-1 chargée: 145 comptes
  ✓ Balance N-2 chargée: 140 comptes

Calcul de la Note 18...
  Calcul des charges constatées d'avance...
    ✓ Charges constatées d'avance: 250,000

Génération du fichier HTML...
  ✓ HTML généré: test_note_18.html

Sauvegarde de la trace...
  ✓ Trace sauvegardée: trace_note_18.json

========================================
✓ NOTE 18 CALCULÉE AVEC SUCCÈS
========================================
```

## Particularités

- **Compte d'actif**: Les charges constatées d'avance sont un compte d'actif (solde débiteur)
- **Régularisation**: Représente des charges payées d'avance qui concernent l'exercice suivant
- **Exemples**: Loyers payés d'avance, assurances, abonnements

## Dépendances

- Balance_Reader
- Account_Extractor
- Movement_Calculator
- HTML_Generator
- Trace_Manager

## Conformité SYSCOHADA

✓ Conforme au plan comptable SYSCOHADA Révisé
✓ Format de présentation officiel respecté
