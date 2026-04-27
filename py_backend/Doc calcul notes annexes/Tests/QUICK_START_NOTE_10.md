# Quick Start - Note 10: Résultat

## Vue d'ensemble

La Note 10 présente les mouvements du résultat (bénéfice ou perte) sur trois exercices.

## Comptes concernés

- **12X**: Résultat de l'exercice
- **13X**: Résultat en instance d'affectation

## Structure de la note

| Libellé | Exercice N-2 | Exercice N-1 | Exercice N |
|---------|--------------|--------------|------------|
| Résultat de l'exercice | Montant | Montant | Montant |
| Résultat en instance d'affectation | Montant | Montant | Montant |
| **TOTAL** | **Total N-2** | **Total N-1** | **Total N** |

## Exécution rapide

### Windows PowerShell
```powershell
# Depuis la racine du projet
.\test-note-10.ps1
```

### Ligne de commande directe
```bash
# Depuis la racine du projet
cd py_backend
python "Doc calcul notes annexes/Scripts/calculer_note_10.py"
cd ..
```

## Fichiers générés

- **HTML**: `py_backend/Doc calcul notes annexes/Tests/test_note_10.html`
  - Tableau formaté avec style SYSCOHADA
  - Montants avec séparateurs de milliers
  - Ligne de total en gras

## Interprétation des résultats

### Soldes positifs (Bénéfice)
- Solde créditeur > Solde débiteur
- Indique un résultat bénéficiaire

### Soldes négatifs (Perte)
- Solde débiteur > Solde créditeur
- Indique un résultat déficitaire

### Résultat en instance d'affectation
- Résultat non encore affecté aux réserves ou distribué
- Peut provenir d'exercices antérieurs

## Vérifications à effectuer

1. **Cohérence temporelle**
   - Le résultat N-1 doit correspondre au compte de résultat N-1
   - Le résultat N doit correspondre au compte de résultat N

2. **Affectation du résultat**
   - Vérifier que le résultat en instance correspond aux décisions d'affectation
   - Contrôler la cohérence avec les mouvements de réserves (Note 9)

3. **Total**
   - Le total doit être la somme des deux lignes
   - Vérifier la cohérence avec le bilan passif

## Exemple de sortie

```
NOTE 10 - RÉSULTAT

Libellé                                    Exercice N-2    Exercice N-1    Exercice N
Résultat de l'exercice                     15 000 000      18 500 000      22 000 000
Résultat en instance d'affectation          2 000 000       1 500 000       3 000 000
TOTAL                                      17 000 000      20 000 000      25 000 000
```

## Cas particuliers

### Résultat déficitaire
- Affiché en négatif (ou entre parenthèses selon convention)
- Peut réduire les capitaux propres

### Report à nouveau
- Peut être inclus dans le résultat en instance d'affectation
- Vérifier la cohérence avec les statuts de l'entreprise

### Affectation partielle
- Une partie du résultat peut être affectée immédiatement
- Le reste reste en instance d'affectation

## Dépannage

### Erreur: Fichier de balance introuvable
```
Solution: Vérifier que P000 -BALANCE DEMO N_N-1_N-2.xlsx existe à la racine
```

### Montants à zéro
```
Cause possible: Comptes 12X ou 13X absents de la balance
Solution: Vérifier la présence des comptes dans la balance
```

### Incohérence avec le compte de résultat
```
Solution: Vérifier que le compte 12 correspond bien au résultat net
         Contrôler les écritures de clôture
```

## Prochaines étapes

Après validation de la Note 10:
1. Vérifier la cohérence avec le compte de résultat
2. Contrôler l'affectation du résultat (Note 9 - Réserves)
3. Passer à la Note 11 (Provisions)

## Support

Pour plus d'informations:
- Voir `requirements.md` - Requirement 5
- Voir `design.md` - Section Components
- Consulter le template: `calculateur_note_template.py`
