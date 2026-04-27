# Quick Start - Note 27: Dotations aux Provisions

## Vue d'ensemble

La Note 27 présente les dotations aux provisions de l'exercice, ventilées par nature de provision.

## Structure de la note

```
Note 27 - Dotations aux Provisions
├── Dotations aux provisions pour risques et charges (6911)
├── Dotations aux provisions pour dépréciation des immobilisations (6912)
├── Dotations aux provisions pour dépréciation des stocks (6913)
├── Dotations aux provisions pour dépréciation des créances (6914)
└── Total des dotations aux provisions
```

## Comptes utilisés

| Catégorie | Comptes | Description |
|-----------|---------|-------------|
| Risques et charges | 6911 | Dotations aux provisions pour risques et charges |
| Dépréciation immobilisations | 6912 | Dotations aux provisions pour dépréciation des immobilisations |
| Dépréciation stocks | 6913 | Dotations aux provisions pour dépréciation des stocks |
| Dépréciation créances | 6914 | Dotations aux provisions pour dépréciation des créances |

## Utilisation

### Exemple basique

```python
from calculer_note_27 import CalculateurNote27

# Initialiser le calculateur
calculateur = CalculateurNote27(
    balance_file="balance.xlsx",
    exercice_n="2024",
    exercice_n1="2023"
)

# Calculer la note
resultat = calculateur.calculer()

# Afficher les résultats
for ligne in resultat["lignes"]:
    print(f"{ligne['libelle']}: {ligne['n']:,.2f}")
```

### Génération HTML

```python
# Générer le HTML
html = calculateur.generer_html(resultat)

# Sauvegarder dans un fichier
with open("note_27.html", "w", encoding="utf-8") as f:
    f.write(html)
```

### Export Excel

```python
# Exporter vers Excel
calculateur.exporter_excel(resultat, "note_27.xlsx")
```

## Format de sortie

```python
{
    "note": "Note 27",
    "titre": "Dotations aux Provisions",
    "exercice_n": "2024",
    "exercice_n1": "2023",
    "lignes": [
        {
            "libelle": "Dotations aux provisions pour risques et charges",
            "n": 250000.00,
            "n1": 200000.00,
            "comptes": ["6911"]
        },
        {
            "libelle": "Dotations aux provisions pour dépréciation des immobilisations",
            "n": 150000.00,
            "n1": 120000.00,
            "comptes": ["6912"]
        },
        {
            "libelle": "Dotations aux provisions pour dépréciation des stocks",
            "n": 80000.00,
            "n1": 75000.00,
            "comptes": ["6913"]
        },
        {
            "libelle": "Dotations aux provisions pour dépréciation des créances",
            "n": 120000.00,
            "n1": 100000.00,
            "comptes": ["6914"]
        },
        {
            "libelle": "Total des dotations aux provisions",
            "n": 600000.00,
            "n1": 495000.00,
            "total": True
        }
    ]
}
```

## Tests

### Lancer les tests

```bash
# Test unitaire
python -m pytest test_note_27.py -v

# Test avec couverture
python -m pytest test_note_27.py --cov=calculer_note_27

# Test d'intégration
python test_note_27_integration.py
```

### Script PowerShell

```powershell
.\test-note-27.ps1
```

## Règles de calcul

### Dotations aux provisions pour risques et charges
- Compte 6911: Provisions pour litiges, garanties, restructurations, etc.
- Solde débiteur (charge)

### Dotations aux provisions pour dépréciation des immobilisations
- Compte 6912: Provisions pour dépréciation des immobilisations
- Solde débiteur (charge)

### Dotations aux provisions pour dépréciation des stocks
- Compte 6913: Provisions pour dépréciation des stocks
- Solde débiteur (charge)

### Dotations aux provisions pour dépréciation des créances
- Compte 6914: Provisions pour créances douteuses
- Solde débiteur (charge)

### Total
- Somme de toutes les dotations aux provisions

## Contrôles de cohérence

1. **Cohérence avec le bilan**:
   - Les dotations doivent correspondre à l'augmentation des provisions au passif

2. **Cohérence avec le compte de résultat**:
   - Les dotations doivent correspondre aux charges de provisions

3. **Évolution N/N-1**:
   - Analyser les variations significatives par catégorie

4. **Cohérence avec les reprises**:
   - Comparer avec la Note 32 (Reprises de provisions)

## Traçabilité

Le calculateur génère automatiquement des traces pour:
- Dotations risques et charges N
- Dotations dépréciation immobilisations N
- Dotations dépréciation stocks N
- Dotations dépréciation créances N
- Total des dotations provisions N

## Exemple de résultat

```
Note 27 - Dotations aux Provisions
================================================================================
Dotations aux provisions pour risques et charges                  250,000.00    200,000.00
Dotations aux provisions pour dépréciation des immobilisations    150,000.00    120,000.00
Dotations aux provisions pour dépréciation des stocks              80,000.00     75,000.00
Dotations aux provisions pour dépréciation des créances           120,000.00    100,000.00
--------------------------------------------------------------------------------
Total des dotations aux provisions                                600,000.00    495,000.00
================================================================================
```

## Liens avec d'autres notes

- **Note 11**: Provisions (mouvements des provisions)
- **Note 32**: Reprises de provisions
- **Compte de résultat**: Charges d'exploitation et financières

## Références

- Requirements: 5.1, 5.2, 5.3, 5.4
- SYSCOHADA: Comptes 691X
- Task: 18.7
