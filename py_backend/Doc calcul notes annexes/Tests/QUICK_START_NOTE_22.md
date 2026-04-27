# Quick Start - Note 22: Achats de Matières Premières

## Vue d'ensemble

La Note 22 calcule les achats de matières premières et fournitures liées à partir des comptes 601 et 602 du plan comptable SYSCOHADA.

## Exécution rapide

### Option 1: Script PowerShell (Recommandé)

```powershell
.\test-note-22.ps1
```

### Option 2: Ligne de commande Python

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_22.py"
```

## Comptes utilisés

La Note 22 utilise les comptes suivants:

- **601**: Achats de marchandises (matières premières)
  - 6011 à 6019: Sous-comptes détaillés
- **602**: Achats de matières premières et fournitures liées
  - 6021 à 6029: Sous-comptes détaillés

## Structure de la note

La Note 22 présente:

1. **Achats de matières premières - Exercice N**
   - Montant total des achats de l'exercice en cours
   - Mouvements débiteurs (charges enregistrées)
   - Mouvements créditeurs (reprises/annulations)

2. **Achats de matières premières - Exercice N-1**
   - Montant total des achats de l'exercice précédent
   - Mouvements débiteurs
   - Mouvements créditeurs

3. **Variation N / N-1**
   - Différence entre les deux exercices
   - Pourcentage de variation

## Fichiers générés

Après l'exécution, les fichiers suivants sont créés:

- **HTML**: `py_backend/Doc calcul notes annexes/Tests/test_note_22.html`
  - Visualisation formatée de la note
  - Conforme au format SYSCOHADA officiel

- **Trace JSON**: `py_backend/Doc calcul notes annexes/Tests/note_22_trace.json`
  - Détail des calculs effectués
  - Comptes sources utilisés
  - Métadonnées de génération

## Visualisation

Pour ouvrir le fichier HTML généré:

```powershell
start "py_backend/Doc calcul notes annexes/Tests/test_note_22.html"
```

Ou double-cliquez sur le fichier dans l'explorateur Windows.

## Paramètres optionnels

### Spécifier un fichier de balance différent

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_22.py" "chemin/vers/balance.xlsx"
```

### Personnaliser les fichiers de sortie

```bash
python "py_backend/Doc calcul notes annexes/Scripts/calculer_note_22.py" \
  --output-html "mon_rapport.html" \
  --output-trace "ma_trace.json"
```

## Vérification des résultats

### Contrôles à effectuer

1. **Cohérence des montants**
   - Vérifier que les montants N et N-1 sont cohérents avec les balances
   - Vérifier que la variation = Montant N - Montant N-1

2. **Comptes sources**
   - Consulter le fichier trace JSON pour voir les comptes utilisés
   - Vérifier que tous les comptes 601 et 602 pertinents sont inclus

3. **Format HTML**
   - Vérifier que le tableau est bien formaté
   - Vérifier que les montants sont alignés et lisibles

## Dépannage

### Erreur: "Fichier de balance non trouvé"

Vérifiez que le fichier `P000 -BALANCE DEMO N_N-1_N-2.xlsx` est présent à la racine du projet.

### Erreur: "Module non trouvé"

Assurez-vous que tous les modules sont présents dans le dossier `Modules/`:
- `balance_reader.py`
- `account_extractor.py`
- `movement_calculator.py`
- `html_generator.py`
- `trace_manager.py`

### Montants à zéro

Si tous les montants sont à zéro, vérifiez que:
- Les comptes 601 et 602 existent dans la balance
- Les onglets "BALANCE N" et "BALANCE N-1" sont présents dans le fichier Excel

## Intégration avec les autres notes

La Note 22 fait partie du compte de résultat (charges). Elle doit être cohérente avec:

- **Note 21**: Achats de marchandises (comptes 601)
- **Note 23**: Autres achats (comptes 604-608)
- **Compte de résultat**: Total des achats

## Prochaines étapes

Après avoir validé la Note 22, vous pouvez:

1. Exécuter la Note 23 (Autres Achats)
2. Vérifier la cohérence inter-notes avec le Coherence_Validator
3. Générer le rapport complet des 33 notes

## Support

Pour plus d'informations:
- Consultez le fichier `requirements.md` pour les spécifications détaillées
- Consultez le fichier `design.md` pour l'architecture du système
- Consultez les tests d'intégration dans `Tests/`

---

**Date de création**: 26 Avril 2026  
**Version**: 1.0  
**Statut**: ✓ Implémenté et testé
