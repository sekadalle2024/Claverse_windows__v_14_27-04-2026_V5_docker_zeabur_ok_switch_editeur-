# Quick Start - Test d'Intégration Coherence_Validator

## Vue d'ensemble

Ce guide permet de tester rapidement l'intégration du `Coherence_Validator` dans l'orchestrateur principal.

## Tâche 21.2 - Intégration Coherence_Validator

### Fonctionnalités implémentées

✅ **1. Appel du validateur après calcul des notes**
- Le validateur est appelé automatiquement dans `main()` après `calculer_toutes_notes()`
- Méthode: `orchestrateur.valider_coherence()`

✅ **2. Génération du rapport HTML de cohérence**
- Fichier généré: `Tests/rapport_coherence.html`
- Contient les validations détaillées et le taux de cohérence global

✅ **3. Émission d'alertes si taux < 95%**
- Alerte critique loggée si `taux_coherence < 95.0%`
- Message: `⚠ ALERTE CRITIQUE: Taux de cohérence X.X% < 95%`

## Exécution des tests

### Test d'intégration complet

```powershell
# Depuis le dossier Tests/
python test_coherence_integration.py
```

### Test avec l'orchestrateur complet

```powershell
# Depuis le dossier racine Doc calcul notes annexes/
python calcul_notes_annexes_main.py
```

## Vérifications

### 1. Vérifier que le validateur est appelé

Dans `calcul_notes_annexes_main.py`, ligne ~650:

```python
if notes:
    # Valider la cohérence
    taux_coherence = orchestrateur.valider_coherence()
```

### 2. Vérifier la génération du rapport

Après exécution, vérifier que le fichier existe:

```
Tests/rapport_coherence.html
```

### 3. Vérifier les alertes dans les logs

Consulter le fichier de log:

```
Logs/calcul_notes_annexes.log
```

Rechercher:
- `✓ Taux de cohérence acceptable: X.X% >= 95%` (si OK)
- `⚠ ALERTE CRITIQUE: Taux de cohérence X.X% < 95%` (si problème)

## Workflow complet dans main()

```python
def main():
    # 1. Configuration
    configurer_logging()
    
    # 2. Création orchestrateur
    orchestrateur = CalculNotesAnnexesMain(fichier_balance)
    
    # 3. Calcul des 33 notes
    notes = orchestrateur.calculer_toutes_notes()
    
    if notes:
        # 4. ✅ VALIDATION DE COHÉRENCE (Task 21.2)
        taux_coherence = orchestrateur.valider_coherence()
        
        # 5. Génération des traces
        orchestrateur.generer_traces()
        
        # 6. Export Excel
        orchestrateur.exporter_excel()
        
        # 7. Rapport récapitulatif
        rapport_html = orchestrateur.generer_rapport_recapitulatif()
```

## Méthode valider_coherence()

### Implémentation (lignes 488-525)

```python
def valider_coherence(self) -> float:
    """
    Valide la cohérence inter-notes.
    
    Returns:
        Taux de cohérence global (0-100)
    """
    # 1. Créer le validateur avec toutes les notes
    validator = CoherenceValidator(self.notes_calculees)
    
    # 2. Calculer le taux de cohérence
    taux = validator.calculer_taux_coherence()
    
    # 3. Émettre alerte si taux < 95%
    if taux < 95.0:
        logging.warning(f"⚠ ALERTE CRITIQUE: Taux de cohérence {taux:.1f}% < 95%")
    else:
        logging.info(f"✓ Taux de cohérence acceptable: {taux:.1f}% >= 95%")
    
    # 4. Générer le rapport HTML
    rapport_html = validator.generer_rapport_coherence()
    fichier_rapport = 'Tests/rapport_coherence.html'
    
    with open(fichier_rapport, 'w', encoding='utf-8') as f:
        f.write(rapport_html)
    
    logging.info(f"✓ Rapport de cohérence sauvegardé: {fichier_rapport}")
    
    return taux
```

## Validations effectuées par CoherenceValidator

1. **Total immobilisations** (Notes 3A-3E vs Bilan Actif)
2. **Dotations amortissements** (Notes 3A-3E vs Compte de Résultat)
3. **Continuité temporelle** (Solde Clôture N-1 = Solde Ouverture N)
4. **Taux de cohérence global** (% de validations avec écart < 1%)

## Fichiers générés

Après exécution complète:

```
Tests/
├── rapport_coherence.html          # ✅ Rapport de cohérence détaillé
├── rapport_recapitulatif.html      # Rapport récapitulatif général
├── Notes_Annexes_Calculees_YYYYMMDD.xlsx  # Export Excel
└── trace_note_*.json               # Traces de calcul

Logs/
├── calcul_notes_annexes.log        # ✅ Log principal avec alertes
├── calcul_notes_warnings.log       # Warnings uniquement
└── calcul_notes_errors.log         # Erreurs uniquement
```

## Exemple de sortie console

```
[2026-04-27 10:30:15] [INFO] Validation de la cohérence inter-notes...
[2026-04-27 10:30:15] [INFO] ✓ Taux de cohérence acceptable: 97.3% >= 95%
[2026-04-27 10:30:15] [INFO] ✓ Rapport de cohérence sauvegardé: Tests/rapport_coherence.html
```

Ou en cas de problème:

```
[2026-04-27 10:30:15] [WARNING] ⚠ ALERTE CRITIQUE: Taux de cohérence 92.1% < 95%
[2026-04-27 10:30:15] [INFO] ✓ Rapport de cohérence sauvegardé: Tests/rapport_coherence.html
```

## Requirements validés

- ✅ **10.1**: Validation total immobilisations
- ✅ **10.2**: Validation dotations amortissements
- ✅ **10.3**: Validation continuité temporelle
- ✅ **10.4**: Détection incohérences avec rapport d'écart
- ✅ **10.5**: Calcul taux de cohérence global
- ✅ **10.6**: Alerte si taux < 95%
- ✅ **10.7**: Rapport de cohérence HTML sauvegardé

## Statut

✅ **Task 21.2 COMPLÉTÉE**

L'intégration du Coherence_Validator dans l'orchestrateur est complète et fonctionnelle.
