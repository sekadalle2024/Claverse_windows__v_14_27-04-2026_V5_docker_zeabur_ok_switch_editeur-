# Quick Start - Note 28: Ventes de Marchandises

## Vue d'ensemble

La Note 28 calcule les ventes de marchandises pour les exercices N et N-1, avec analyse de la variation.

## Comptes SYSCOHADA utilisés

- **701**: Ventes de marchandises
- **7011-7019**: Sous-comptes de ventes de marchandises

## Structure de la note

La note présente:
1. Ventes de marchandises - Exercice N
2. Ventes de marchandises - Exercice N-1
3. Variation N / N-1 (montant et pourcentage)

## Exécution rapide

### Depuis le dossier Scripts:

```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_28.py
```

### Avec un fichier de balance personnalisé:

```bash
python calculer_note_28.py "chemin/vers/balance.xlsx"
```

### Avec options de sortie personnalisées:

```bash
python calculer_note_28.py \
  --output-html "../Tests/ma_note_28.html" \
  --output-trace "../Tests/ma_trace_28.json"
```

## Fichiers générés

1. **test_note_28.html**: Tableau HTML formaté avec les ventes
2. **note_28_trace.json**: Fichier de traçabilité avec détails des calculs

## Interprétation des résultats

### Montants positifs
- Indiquent des ventes de marchandises (normal pour compte 701)
- Plus le montant est élevé, plus le chiffre d'affaires marchandises est important

### Variation N / N-1
- **Positive**: Augmentation des ventes (croissance)
- **Négative**: Diminution des ventes (décroissance)
- **Pourcentage**: Taux de croissance ou décroissance

## Exemple de sortie console

```
================================================================================
  CALCULATEUR NOTE 28 - VENTES DE MARCHANDISES
================================================================================

📂 Chargement des balances depuis: ../../P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 148 lignes chargées
✓ Balance N-2 : 145 lignes chargées

🔢 Calcul de la note 28...
  Calcul: Ventes de marchandises...
    Exercice N:       25,000,000
    Exercice N-1:     22,000,000
    Variation:         3,000,000 (+13.6%)
✓ Note calculée: 3 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: ../Tests/test_note_28.html
✓ Fichier de trace sauvegardé: ../Tests/note_28_trace.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 28
────────────────────────────────────────────────────────────────────────────────

  Ventes Exercice N:        25,000,000
  Ventes Exercice N-1:      22,000,000
  Variation:                 3,000,000
  Variation %:                   +13.6%

================================================================================
  ✓ NOTE 28 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Vérifications à effectuer

1. **Cohérence avec le compte de résultat**: Les ventes N doivent correspondre au poste "Ventes de marchandises" du compte de résultat
2. **Évolution logique**: La variation doit être cohérente avec l'activité de l'entreprise
3. **Mouvements créditeurs**: Doivent être supérieurs aux mouvements débiteurs (les ventes sont créditées)

## Dépannage

### Erreur "Balance non trouvée"
- Vérifier le chemin du fichier Excel
- Vérifier que les onglets "BALANCE N", "BALANCE N-1", "BALANCE N-2" existent

### Montants à zéro
- Vérifier que les comptes 701 existent dans la balance
- Vérifier que les comptes ont des mouvements créditeurs

### Variation incohérente
- Comparer avec les données du compte de résultat
- Vérifier les soldes N-1 dans la balance

## Prochaines étapes

Après la Note 28, vous pouvez calculer:
- **Note 29**: Ventes de produits finis
- **Note 30**: Production immobilisée
- **Note 31**: Subventions d'exploitation

## Support

Pour plus d'informations, consultez:
- `calculateur_note_template.py`: Documentation de la classe de base
- `requirements.md`: Exigences détaillées
- `design.md`: Architecture du système
