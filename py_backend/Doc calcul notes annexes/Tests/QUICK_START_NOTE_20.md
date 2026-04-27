# Quick Start - Note 20: Écarts de Conversion Passif

## Vue d'ensemble

La Note 20 calcule les écarts de conversion passif (gains latents) selon le référentiel SYSCOHADA Révisé. Elle traite le compte 478 qui enregistre les gains latents de change sur les créances et dettes en devises.

## Comptes SYSCOHADA concernés

- **478**: Écarts de conversion - Passif (gains latents)

## Structure de la note

La Note 20 présente les mouvements des écarts de conversion passif:

| NATURE | Solde début exercice | Augmentations | Diminutions | Solde fin exercice |
|--------|---------------------|---------------|-------------|-------------------|
| Écarts de conversion - Passif | ... | ... | ... | ... |

## Exécution rapide

### Option 1: Exécution directe

```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_20.py
```

### Option 2: Via PowerShell (depuis la racine)

```powershell
.\test-note-20.ps1
```

## Fichiers générés

Après exécution, les fichiers suivants sont créés dans `py_backend/Doc calcul notes annexes/Tests/`:

1. **test_note_20.html**: Tableau HTML formaté de la Note 20
2. **trace_note_20.json**: Fichier de traçabilité avec détail des calculs

## Interprétation des résultats

### Écarts de conversion passif (compte 478)

Les écarts de conversion passif représentent les **gains latents** sur les créances et dettes en devises:

- **Augmentations**: Nouveaux gains latents constatés (réévaluation favorable)
- **Diminutions**: Réalisation ou annulation de gains latents
- **Solde créditeur**: Gains latents non réalisés au passif du bilan

### Exemple de lecture

```
Écarts de conversion - Passif
  Solde début exercice:    50 000
  Augmentations:          120 000  (nouveaux gains latents)
  Diminutions:             30 000  (gains réalisés ou annulés)
  Solde fin exercice:     140 000  (gains latents au bilan)
```

## Contrôles de cohérence

Le calculateur vérifie automatiquement:

1. **Équation comptable**: Solde clôture = Solde ouverture + Augmentations - Diminutions
2. **Valeurs positives**: Les écarts de conversion passif sont normalement créditeurs
3. **Traçabilité**: Tous les montants sont tracés vers leurs comptes sources

## Particularités comptables

### Nature des écarts de conversion passif

- **Gains latents**: Non réalisés, inscrits au passif par prudence
- **Traitement fiscal**: Généralement non imposables tant que non réalisés
- **Symétrie**: Correspondent aux pertes latentes à l'actif (compte 47X)

### Lien avec d'autres notes

- **Note 3E**: Écarts de conversion actif (pertes latentes)
- **Compte de résultat**: Gains/pertes de change réalisés

## Dépannage

### Problème: Solde nul

Si le solde est à zéro, cela peut signifier:
- Aucune créance/dette en devises
- Pas de variation de change favorable
- Gains latents réalisés pendant l'exercice

### Problème: Incohérence détectée

Si un message d'incohérence apparaît:
1. Vérifier les mouvements du compte 478 dans la balance
2. Contrôler la cohérence avec les écarts de conversion actif
3. Vérifier les écritures de réévaluation des devises

## Références SYSCOHADA

- **Plan comptable**: Compte 478 - Écarts de conversion - Passif
- **Principe**: Prudence (gains latents au passif)
- **Liasse officielle**: Note annexe 20

## Prochaines étapes

Après validation de la Note 20:
- Continuer avec les Notes 21-33 (Charges et Produits)
- Vérifier la cohérence avec la Note 3E (Écarts de conversion actif)
- Intégrer dans le calcul global des 33 notes
