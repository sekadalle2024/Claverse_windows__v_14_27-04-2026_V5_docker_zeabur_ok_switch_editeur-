# Quick Start - Note 29: Ventes de Produits Finis

## Vue d'ensemble

La Note 29 calcule les ventes de produits finis à partir des comptes SYSCOHADA 701, 702, 703.

## Comptes utilisés

- **701**: Ventes de produits finis
- **702**: Ventes de produits intermédiaires  
- **703**: Ventes de produits résiduels

## Exécution rapide

### Depuis le dossier Scripts

```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_29.py
```

### Avec un fichier de balance personnalisé

```bash
python calculer_note_29.py "chemin/vers/balance.xlsx"
```

### Avec options de sortie personnalisées

```bash
python calculer_note_29.py \
  --output-html "../Tests/ma_note_29.html" \
  --output-trace "../Tests/ma_trace_29.json"
```

## Fichiers générés

- **test_note_29.html**: Tableau HTML formaté de la note
- **note_29_trace.json**: Fichier de traçabilité des calculs

## Structure de la note

La Note 29 présente:

1. **Ventes de produits finis - Exercice N**
2. **Ventes de produits finis - Exercice N-1**
3. **Variation N / N-1**
4. **Ventes de produits intermédiaires - Exercice N**
5. **Ventes de produits intermédiaires - Exercice N-1**
6. **Variation N / N-1**
7. **Ventes de produits résiduels - Exercice N**
8. **Ventes de produits résiduels - Exercice N-1**
9. **Variation N / N-1**
10. **TOTAL - Exercice N**
11. **TOTAL - Exercice N-1**
12. **TOTAL - Variation N / N-1**

## Colonnes calculées

- **Montant**: Solde créditeur net (produits)
- **Mouvements Crédit**: Produits enregistrés
- **Mouvements Débit**: Reprises/annulations

## Validation

Le script affiche:
- ✓ Nombre de lignes chargées pour chaque balance
- ✓ Montants calculés pour chaque poste
- ✓ Variation N / N-1 en valeur et pourcentage
- ✓ Résumé avec totaux

## Exemple de sortie console

```
================================================================================
  CALCULATEUR NOTE 29 - VENTES DE PRODUITS FINIS
================================================================================

📂 Chargement des balances depuis: ../../P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 150 lignes chargées
✓ Balance N-2 : 150 lignes chargées

🔢 Calcul de la note 29...
  Calcul: Ventes de produits finis...
    Exercice N:       5,000,000
    Exercice N-1:     4,500,000
    Variation:          500,000 (+11.1%)
  Calcul: Ventes de produits intermédiaires...
    Exercice N:       1,200,000
    Exercice N-1:     1,100,000
    Variation:          100,000 (+9.1%)
  Calcul: Ventes de produits résiduels...
    Exercice N:         300,000
    Exercice N-1:       250,000
    Variation:           50,000 (+20.0%)
✓ Note calculée: 12 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: ../Tests/test_note_29.html
✓ Fichier de trace sauvegardé: ../Tests/note_29_trace.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 29
────────────────────────────────────────────────────────────────────────────────

  Ventes Exercice N:        6,500,000
  Ventes Exercice N-1:      5,850,000
  Variation:                  650,000
  Variation %:                  +11.1%

================================================================================
  ✓ NOTE 29 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Dépannage

### Erreur: Balance non trouvée
- Vérifiez le chemin vers le fichier Excel
- Assurez-vous que les onglets "BALANCE N", "BALANCE N-1", "BALANCE N-2" existent

### Erreur: Comptes manquants
- Normal si l'entreprise n'a pas de ventes de produits finis
- Les montants seront à zéro

### Erreur: Module non trouvé
```bash
# Assurez-vous d'être dans le bon dossier
cd "py_backend/Doc calcul notes annexes/Scripts"
```

## Intégration

Pour intégrer dans un workflow automatisé:

```python
from calculer_note_29 import CalculateurNote29

calculateur = CalculateurNote29("chemin/vers/balance.xlsx")
calculateur.executer(
    fichier_html="sortie/note_29.html",
    fichier_trace="sortie/note_29_trace.json"
)
```

## Prochaines étapes

- Vérifier le fichier HTML généré dans un navigateur
- Consulter le fichier de trace JSON pour l'audit
- Intégrer dans le calcul des 33 notes via l'orchestrateur principal
