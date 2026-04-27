# Quick Start - Note 21: Achats de Marchandises

## Vue d'ensemble

La Note 21 calcule les achats de marchandises pour les exercices N et N-1, avec la variation entre les deux exercices.

## Comptes SYSCOHADA utilisés

- **601**: Achats de marchandises
- **6011-6019**: Sous-comptes d'achats de marchandises

## Structure de la note

La Note 21 présente:
1. Achats de marchandises - Exercice N
2. Achats de marchandises - Exercice N-1
3. Variation N / N-1 (montant et pourcentage)

## Exécution rapide

### Avec le fichier de balance par défaut

```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_21.py
```

### Avec un fichier de balance personnalisé

```bash
python calculer_note_21.py "chemin/vers/balance.xlsx"
```

### Avec options personnalisées

```bash
python calculer_note_21.py "balance.xlsx" \
  --output-html "mon_rapport_note_21.html" \
  --output-trace "ma_trace_note_21.json"
```

## Fichiers générés

1. **test_note_21.html**: Tableau HTML formaté de la note
2. **note_21_trace.json**: Fichier de traçabilité avec détails des calculs

## Exemple de sortie

```
================================================================================
  CALCULATEUR NOTE 21 - ACHATS DE MARCHANDISES
================================================================================

📂 Chargement des balances depuis: ../../P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 150 lignes chargées
✓ Balance N-2 : 150 lignes chargées

🔢 Calcul de la note 21...
  Calcul: Achats de marchandises...
    Exercice N:      5,000,000
    Exercice N-1:    4,500,000
    Variation:         500,000 (+11.1%)
✓ Note calculée: 3 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: ../Tests/test_note_21.html
✓ Fichier de trace sauvegardé: ../Tests/note_21_trace.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 21
────────────────────────────────────────────────────────────────────────────────

  Achats Exercice N:        5,000,000
  Achats Exercice N-1:      4,500,000
  Variation:                  500,000
  Variation %:                   11.1%

================================================================================
  ✓ NOTE 21 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Vérification des résultats

### Ouvrir le fichier HTML

```bash
# Windows
start ../Tests/test_note_21.html

# Linux/Mac
xdg-open ../Tests/test_note_21.html
```

### Consulter la trace JSON

```bash
cat ../Tests/note_21_trace.json
```

## Points de contrôle

1. **Cohérence des montants**: Vérifier que les achats N et N-1 correspondent aux comptes 60X
2. **Variation**: La variation doit être égale à (Achats N - Achats N-1)
3. **Traçabilité**: Le fichier JSON doit contenir les comptes sources pour chaque ligne

## Comptes de charges (classe 6)

Pour les comptes de charges:
- Le **solde débiteur** représente les charges de l'exercice
- Les **mouvements débiteurs** sont les charges enregistrées
- Les **mouvements créditeurs** sont les reprises/annulations

## Intégration avec d'autres notes

La Note 21 fait partie du compte de résultat et doit être cohérente avec:
- Le compte de résultat global
- Les autres notes de charges (Notes 22-27)
- Le tableau des flux de trésorerie

## Dépannage

### Erreur "Balance non trouvée"
- Vérifier le chemin du fichier de balance
- S'assurer que les onglets "BALANCE N", "BALANCE N-1", "BALANCE N-2" existent

### Montants à zéro
- Vérifier que les comptes 60X existent dans la balance
- Consulter le fichier de trace pour voir les comptes sources

### Erreur de calcul
- Vérifier la cohérence des soldes dans la balance
- Consulter les avertissements dans la console

## Prochaines étapes

Après avoir validé la Note 21, vous pouvez:
1. Calculer les autres notes de charges (Notes 22-27)
2. Intégrer dans le calcul global des 33 notes
3. Valider la cohérence inter-notes avec le Coherence_Validator
