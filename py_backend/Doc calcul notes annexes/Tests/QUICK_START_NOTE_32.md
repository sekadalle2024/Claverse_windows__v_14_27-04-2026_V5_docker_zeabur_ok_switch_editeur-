# Quick Start - Note 32: Reprises de Provisions

## Vue d'ensemble

La Note 32 présente les **reprises de provisions** de l'exercice, c'est-à-dire les provisions antérieurement constituées qui sont devenues sans objet ou excédentaires.

## Comptes concernés

| Compte | Libellé |
|--------|---------|
| 7911 | Reprises de provisions pour risques et charges |
| 7912 | Reprises de provisions pour dépréciation des immobilisations |
| 7913 | Reprises de provisions pour dépréciation des stocks |
| 7914 | Reprises de provisions pour dépréciation des créances |

## Structure de la note

La note comprend 4 catégories de reprises plus un total:

1. **Reprises de provisions pour risques et charges** (compte 7911)
2. **Reprises de provisions pour dépréciation des immobilisations** (compte 7912)
3. **Reprises de provisions pour dépréciation des stocks** (compte 7913)
4. **Reprises de provisions pour dépréciation des créances** (compte 7914)
5. **TOTAL DES REPRISES DE PROVISIONS**

## Exécution rapide

### Windows PowerShell
```powershell
.\test-note-32.ps1
```

### Python direct
```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_32.py"
```

## Fichiers générés

Après exécution, vous trouverez:

- **test_note_32.html** - Tableau HTML formaté de la note
- **trace_note_32.json** - Fichier de traçabilité des calculs

## Format de sortie

Le tableau HTML contient 3 colonnes:

| NATURE DES REPRISES | Exercice N | Exercice N-1 |
|---------------------|------------|--------------|
| Reprises de provisions pour risques et charges | XXX | XXX |
| Reprises de provisions pour dépréciation des immobilisations | XXX | XXX |
| Reprises de provisions pour dépréciation des stocks | XXX | XXX |
| Reprises de provisions pour dépréciation des créances | XXX | XXX |
| **TOTAL DES REPRISES DE PROVISIONS** | **XXX** | **XXX** |

## Logique de calcul

Pour chaque catégorie de reprises:

1. **Extraction des comptes 791X** - Les comptes de reprises de provisions
2. **Calcul du solde créditeur** - Les reprises sont des produits (créditeurs)
3. **Inversion du signe** - Pour afficher des montants positifs
4. **Sommation** - Total de toutes les catégories

### Formule

```
Reprises N = |Solde Crédit N - Solde Débit N|
```

Les reprises de provisions sont des produits qui viennent augmenter le résultat de l'exercice.

## Relation avec d'autres notes

- **Note 27 (Dotations aux Provisions)** - Les dotations constituent les provisions
- **Note 32 (Reprises de Provisions)** - Les reprises annulent les provisions devenues sans objet
- **Compte de résultat** - Les reprises sont des produits d'exploitation

## Vérifications automatiques

Le calculateur effectue:

✓ Chargement des 3 balances (N, N-1, N-2)  
✓ Extraction des comptes 791X  
✓ Calcul des soldes créditeurs  
✓ Traçabilité complète des calculs  
✓ Génération HTML conforme SYSCOHADA  

## Exemple de résultat

```
================================================================================
  CALCULATEUR NOTE 32 - Reprises de Provisions
================================================================================

📂 Chargement des balances depuis: P000 -BALANCE DEMO N_N-1_N-2.xlsx
✓ Balance N   : 150 lignes chargées
✓ Balance N-1 : 145 lignes chargées
✓ Balance N-2 : 140 lignes chargées

🔢 Calcul de la note 32...
  ✓ Reprises de provisions pour risques et charges:        500,000 (N) |        450,000 (N-1)
  ✓ Reprises de provisions pour dépréciation des immobilisations:        300,000 (N) |        280,000 (N-1)
  ✓ Reprises de provisions pour dépréciation des stocks:        150,000 (N) |        120,000 (N-1)
  ✓ Reprises de provisions pour dépréciation des créances:        200,000 (N) |        180,000 (N-1)
  ────────────────────────────────────────────────────────────────
  ✓ TOTAL:      1,150,000 (N) |      1,030,000 (N-1)
✓ Note calculée: 5 lignes

📄 Génération du HTML...
✓ HTML généré

✓ Fichier HTML sauvegardé: test_note_32.html
✓ Fichier de trace sauvegardé: trace_note_32.json

────────────────────────────────────────────────────────────────────────────────
  RÉSUMÉ NOTE 32
────────────────────────────────────────────────────────────────────────────────

  Nombre de catégories: 4
  Total reprises N:           1,150,000
  Total reprises N-1:         1,030,000
  Variation:                    120,000

================================================================================
  ✓ NOTE 32 CALCULÉE AVEC SUCCÈS EN 0.45s
================================================================================
```

## Dépannage

### Erreur: Balance non trouvée
- Vérifiez que le fichier `P000 -BALANCE DEMO N_N-1_N-2.xlsx` existe
- Vérifiez le chemin relatif depuis le script

### Erreur: Module non trouvé
- Vérifiez que tous les modules sont dans `py_backend/Doc calcul notes annexes/Modules/`
- Vérifiez que `__init__.py` existe dans le dossier Modules

### Montants à zéro
- Vérifiez que les comptes 791X existent dans la balance
- Vérifiez que les comptes ont des soldes créditeurs (reprises = produits)

## Prochaines étapes

Après avoir testé la Note 32:

1. ✓ Vérifier le fichier HTML généré
2. ✓ Consulter le fichier de trace JSON
3. ✓ Comparer avec la Note 27 (Dotations aux Provisions)
4. → Passer à la Note 33 (Produits Financiers)

## Support

Pour plus d'informations:
- Consultez `requirements.md` pour les exigences détaillées
- Consultez `design.md` pour l'architecture
- Consultez `tasks.md` pour le plan d'implémentation
