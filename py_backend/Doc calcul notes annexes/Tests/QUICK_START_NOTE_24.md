# Quick Start - Note 24: Services Extérieurs

## Vue d'ensemble

La Note 24 calcule les services extérieurs (comptes 61X et 62X) pour les exercices N et N-1, avec calcul de la variation.

## Exécution rapide

```powershell
# Depuis le dossier racine du projet
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_24.py"
```

## Comptes SYSCOHADA utilisés

### Services extérieurs A (61X)
- 611: Sous-traitance générale
- 612: Redevances de crédit-bail
- 613: Locations
- 614: Charges locatives
- 615: Entretien et réparations
- 616: Primes d'assurances
- 617: Études et recherches
- 618: Divers
- 619: Rabais obtenus

### Services extérieurs B (62X)
- 621: Personnel extérieur
- 622: Rémunérations d'intermédiaires
- 623: Publicité
- 624: Transports
- 625: Déplacements et missions
- 626: Frais postaux et télécommunications
- 627: Services bancaires
- 628: Cotisations
- 629: Rabais obtenus

## Structure de sortie

Le fichier HTML généré contient:
- Services extérieurs - Exercice N
- Services extérieurs - Exercice N-1
- Variation N / N-1 (montant et %)

## Fichiers générés

- `test_note_24.html`: Tableau HTML formaté
- `note_24_trace.json`: Traçabilité des calculs

## Validation

✓ Vérifier que les montants N et N-1 sont cohérents
✓ Vérifier que la variation est correctement calculée
✓ Vérifier que tous les comptes 61X et 62X sont inclus

## Exemple de résultat

```
Services Exercice N:      5,250,000
Services Exercice N-1:    4,800,000
Variation:                  450,000
Variation %:                   9.4%
```
