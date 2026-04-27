# Quick Start - Note 25 (Charges de Personnel)

## Vue d'ensemble

La Note 25 présente le détail des charges de personnel (comptes 66X) pour les exercices N et N-1.

## Structure de la Note 25

### Comptes utilisés (66X)

| Ligne | Comptes | Description |
|-------|---------|-------------|
| Salaires et traitements | 661 | Rémunérations du personnel |
| Primes et gratifications | 662 | Primes diverses |
| Congés payés | 663 | Provisions pour congés payés |
| Indemnités de préavis et de licenciement | 664 | Indemnités de rupture |
| Charges sociales | 665, 666, 667, 668 | Cotisations sociales |
| Autres charges de personnel | 669 | Autres charges |

### Colonnes du tableau

1. **Libellé**: Description de la charge
2. **Exercice N**: Montant de l'exercice en cours
3. **Exercice N-1**: Montant de l'exercice précédent

## Exécution rapide

### Windows PowerShell

```powershell
# Depuis la racine du projet
python py_backend/"Doc calcul notes annexes"/Scripts/calculer_note_25.py
```

### Bash/Linux

```bash
# Depuis la racine du projet
python3 py_backend/"Doc calcul notes annexes"/Scripts/calculer_note_25.py
```

## Fichiers générés

- **Emplacement**: `py_backend/Doc calcul notes annexes/Tests/test_note_25.html`
- **Format**: Tableau HTML avec style SYSCOHADA
- **Contenu**: 6 lignes de détail + 1 ligne de total

## Vérification des résultats

### Points à vérifier

1. ✓ Toutes les catégories de charges de personnel sont présentes
2. ✓ Les montants N et N-1 sont cohérents
3. ✓ Le total correspond à la somme des lignes
4. ✓ Les montants correspondent aux comptes 66X de la balance

### Exemple de résultat attendu

```
NOTE 25 - CHARGES DE PERSONNEL
═══════════════════════════════════════════════════════════════

Libellé                                    Exercice N    Exercice N-1
─────────────────────────────────────────────────────────────────────
Salaires et traitements                    15 000 000    14 000 000
Primes et gratifications                    2 500 000     2 200 000
Congés payés                                1 200 000     1 100 000
Indemnités de préavis et de licenciement      500 000       450 000
Charges sociales                            5 800 000     5 400 000
Autres charges de personnel                   300 000       250 000
─────────────────────────────────────────────────────────────────────
TOTAL CHARGES DE PERSONNEL                 25 300 000    23 400 000
═══════════════════════════════════════════════════════════════
```

## Dépannage

### Erreur: Fichier de balance introuvable

**Solution**: Vérifiez que le fichier `P000 -BALANCE DEMO N_N-1_N-2.xlsx` existe à la racine du projet.

### Erreur: Module non trouvé

**Solution**: Vérifiez que tous les modules sont présents dans `py_backend/Doc calcul notes annexes/Modules/`.

### Montants à zéro

**Cause possible**: Aucun compte 66X dans la balance de démonstration.
**Solution**: Vérifiez la présence des comptes 66X dans la balance.

## Prochaines étapes

Après avoir validé la Note 25, vous pouvez passer à:
- **Note 26**: Dotations aux Amortissements (comptes 681X)
- **Note 27**: Dotations aux Provisions (comptes 691X)

## Informations techniques

- **Requirement**: 5.1, 5.2, 5.3, 5.4
- **Comptes**: 66X (Charges de personnel)
- **Type**: Note de compte de résultat (Charges)
- **Calcul**: Solde débiteur - Solde créditeur
