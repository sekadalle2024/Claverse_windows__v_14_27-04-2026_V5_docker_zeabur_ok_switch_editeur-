# Quick Start - Note 31: Subventions d'Exploitation

## Vue d'ensemble

La Note 31 calcule les **subventions d'exploitation** reçues par l'entreprise pour les exercices N et N-1, avec analyse de la variation.

## Comptes SYSCOHADA utilisés

### Comptes 71X - Subventions d'exploitation
- **711**: Subventions d'équilibre
- **712**: Subventions de fonctionnement
- **713**: Subventions de prix
- **718**: Autres subventions d'exploitation

## Structure de la note

La note présente pour chaque type de subvention:
1. Montant de l'exercice N
2. Montant de l'exercice N-1
3. Variation N / N-1 (en valeur absolue et en %)

## Exécution rapide

### Depuis le dossier Scripts:
```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_31.py
```

### Avec un fichier de balance personnalisé:
```bash
python calculer_note_31.py "chemin/vers/balance.xlsx"
```

### Avec options de sortie personnalisées:
```bash
python calculer_note_31.py \
  --output-html "../Tests/ma_note_31.html" \
  --output-trace "../Tests/ma_trace_31.json"
```

## Fichiers générés

1. **test_note_31.html**: Tableau HTML formaté avec les subventions d'exploitation
2. **note_31_trace.json**: Fichier de traçabilité avec détail des comptes sources

## Interprétation des résultats

### Subventions d'équilibre (711)
Subventions destinées à compenser des pertes d'exploitation ou à maintenir l'équilibre financier.

### Subventions de fonctionnement (712)
Subventions pour financer des charges d'exploitation courantes.

### Subventions de prix (713)
Subventions compensant l'insuffisance de certains prix de vente.

### Autres subventions (718)
Autres types de subventions d'exploitation non classées ailleurs.

## Analyse de la variation

Une **augmentation** des subventions peut indiquer:
- Développement de nouvelles activités subventionnées
- Augmentation du soutien public
- Difficultés économiques nécessitant plus de soutien

Une **diminution** peut indiquer:
- Amélioration de la rentabilité autonome
- Fin de programmes de subventions
- Changement de politique publique

## Vérifications importantes

1. **Cohérence avec le compte de résultat**: Le total doit correspondre au poste "Subventions d'exploitation" (ligne TH)
2. **Justification des variations**: Les variations importantes doivent être documentées
3. **Conditions d'octroi**: Vérifier le respect des conditions attachées aux subventions

## Exemple de sortie console

```
================================================================================
  CALCULATEUR NOTE 31 - SUBVENTIONS D'EXPLOITATION
================================================================================

📂 Chargement des balances depuis: ../../P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 148 lignes chargées
✓ Balance N-2 : 145 lignes chargées

🔢 Calcul de la note 31...
  Calcul: Subventions d'équilibre...
    Exercice N:         500,000
    Exercice N-1:       450,000
    Variation:           50,000 (+11.1%)
  Calcul: Subventions de fonctionnement...
    Exercice N:         300,000
    Exercice N-1:       280,000
    Variation:           20,000 (+7.1%)
  Calcul: Subventions de prix...
    Exercice N:         150,000
    Exercice N-1:       150,000
    Variation:                0 (+0.0%)
  Calcul: Autres subventions d'exploitation...
    Exercice N:          50,000
    Exercice N-1:        40,000
    Variation:           10,000 (+25.0%)
✓ Note calculée: 15 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: ../Tests/test_note_31.html
✓ Fichier de trace sauvegardé: ../Tests/note_31_trace.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 31
────────────────────────────────────────────────────────────────────────────────

  Subventions d'Exploitation Exercice N:      1,000,000
  Subventions d'Exploitation Exercice N-1:      920,000
  Variation:                                      80,000
  Variation %:                                      8.7%

================================================================================
  ✓ NOTE 31 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Dépannage

### Erreur: "Aucun compte 71X trouvé"
- Vérifier que la balance contient des comptes de subventions d'exploitation
- Certaines entreprises n'ont pas de subventions

### Montants à zéro
- Normal si l'entreprise ne reçoit pas de subventions d'exploitation
- Vérifier la balance si des subventions sont attendues

### Variation importante
- Documenter les raisons de la variation
- Vérifier les pièces justificatives des subventions

## Liens avec d'autres notes

- **Compte de résultat**: Ligne TH (Subventions d'exploitation)
- **Note 14**: Subventions d'investissement (à distinguer des subventions d'exploitation)
- **Annexe fiscale**: Déclaration des subventions reçues

## Date de création
27 Avril 2026
