"""
Orchestrateur principal pour le calcul des 33 notes annexes SYSCOHADA révisé.

Ce script coordonne le calcul de toutes les notes annexes et gère la validation de cohérence.
Il implémente:
- Chargement unique des balances avec mise en cache
- Calcul séquentiel ou parallèle des 33 notes
- Barre de progression pendant le calcul
- Validation de cohérence inter-notes
- Génération de rapport récapitulatif
- Export Excel de toutes les notes

Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# Ajouter le dossier Modules au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Modules'))

from balance_reader import BalanceReader
from coherence_validator import CoherenceValidator
from excel_exporter import ExcelExporter
from trace_manager import TraceManager


def configurer_logging():
    """Configure le système de logging avec rotation quotidienne."""
    # Créer le dossier Logs s'il n'existe pas
    logs_dir = os.path.join(os.path.dirname(__file__), 'Logs')
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configuration du logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Format des logs
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour le fichier principal (INFO et plus)
    main_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(logs_dir, 'calcul_notes_annexes.log'),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    main_handler.setLevel(logging.INFO)
    main_handler.setFormatter(formatter)
    logger.addHandler(main_handler)
    
    # Handler pour les warnings uniquement
    warning_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(logs_dir, 'calcul_notes_warnings.log'),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    warning_handler.setLevel(logging.WARNING)
    warning_handler.setFormatter(formatter)
    logger.addHandler(warning_handler)
    
    # Handler pour les erreurs uniquement
    error_handler = logging.handlers.TimedRotatingFileHandler(
        os.path.join(logs_dir, 'calcul_notes_errors.log'),
        when='midnight',
        interval=1,
        backupCount=30,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logging.info("=" * 80)
    logging.info("Système de logging configuré avec succès")
    logging.info(f"Logs sauvegardés dans: {logs_dir}")
    logging.info("=" * 80)


class CalculNotesAnnexesMain:
    """
    Orchestrateur principal pour le calcul des notes annexes.
    
    Gère:
    - Chargement unique des balances (cache)
    - Calcul des 33 notes avec barre de progression
    - Validation de cohérence inter-notes
    - Export Excel et génération de traces
    - Calcul parallèle optionnel
    """
    
    # Liste des 33 notes à calculer
    NOTES_A_CALCULER = [
        '3a', '3b', '3c', '3d', '3e',  # Immobilisations
        '4', '5', '6', '7',  # Actif circulant
        '8', '9', '10',  # Capitaux propres
        '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',  # Passif
        '21', '22', '23', '24', '25', '26', '27',  # Charges
        '28', '29', '30', '31', '32', '33'  # Produits
    ]
    
    def __init__(self, fichier_balance: str, mode_parallele: bool = False):
        """
        Initialise l'orchestrateur.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel de balances
            mode_parallele: Si True, calcule les notes en parallèle (optionnel)
        """
        self.fichier_balance = fichier_balance
        self.balance_reader = BalanceReader(fichier_balance)
        self.balances = None  # Cache des balances
        self.notes_calculees = {}
        self.mode_parallele = mode_parallele
        self.statuts_calcul = {}  # Statut de chaque note
        
        logging.info(f"Orchestrateur initialisé avec: {fichier_balance}")
        logging.info(f"Mode parallèle: {'Activé' if mode_parallele else 'Désactivé'}")
    
    def charger_balances(self) -> bool:
        """
        Charge les balances en mémoire (une seule fois - cache).
        
        Returns:
            True si le chargement a réussi
            
        Requirements: 12.2, 12.4
        """
        if self.balances is not None:
            logging.info("✓ Balances déjà en cache")
            return True
            
        try:
            logging.info("Chargement des balances...")
            debut = time.time()
            self.balances = self.balance_reader.charger_balances()
            duree = time.time() - debut
            logging.info(f"✓ Balances chargées avec succès en {duree:.2f}s")
            return True
        except Exception as e:
            logging.error(f"✗ Erreur lors du chargement des balances: {e}")
            return False
    
    def afficher_barre_progression(self, note_actuelle: int, total: int, note_nom: str, statut: str):
        """
        Affiche une barre de progression pendant le calcul.
        
        Args:
            note_actuelle: Numéro de la note en cours
            total: Nombre total de notes
            note_nom: Nom de la note
            statut: Statut du calcul (✓ ou ✗)
            
        Requirements: 12.5
        """
        pourcentage = (note_actuelle / total) * 100
        barre_longueur = 50
        rempli = int(barre_longueur * note_actuelle / total)
        barre = '█' * rempli + '░' * (barre_longueur - rempli)
        
        print(f"\r[{barre}] {pourcentage:.1f}% | Note {note_nom} {statut}", end='', flush=True)
        
        if note_actuelle == total:
            print()  # Nouvelle ligne à la fin
    
    def calculer_note_individuelle(self, numero_note: str) -> Tuple[str, pd.DataFrame, bool, str]:
        """
        Calcule une note individuelle.
        
        Args:
            numero_note: Numéro de la note (ex: '3a', '4', '21')
            
        Returns:
            Tuple (nom_note, dataframe, succès, message_erreur)
            
        Requirements: 12.3
        """
        nom_note = f"Note_{numero_note.upper()}"
        
        try:
            # Importer dynamiquement le calculateur
            module_name = f"calculer_note_{numero_note}"
            class_name = f"CalculateurNote{numero_note.upper()}"
            
            # Chemin vers le script
            script_path = os.path.join(
                os.path.dirname(__file__),
                'Scripts',
                f'{module_name}.py'
            )
            
            if not os.path.exists(script_path):
                return nom_note, None, False, f"Script {module_name}.py non trouvé"
            
            # Import dynamique
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Scripts'))
            module = __import__(module_name)
            calculateur_class = getattr(module, class_name)
            
            # Créer l'instance et calculer
            calculateur = calculateur_class(self.fichier_balance)
            
            # Utiliser les balances en cache si disponibles
            if self.balances is not None:
                calculateur.balance_n = self.balances[0]
                calculateur.balance_n1 = self.balances[1]
                calculateur.balance_n2 = self.balances[2]
            else:
                if not calculateur.charger_balances():
                    return nom_note, None, False, "Échec du chargement des balances"
            
            df = calculateur.generer_note()
            return nom_note, df, True, ""
            
        except Exception as e:
            return nom_note, None, False, str(e)
    
    def calculer_toutes_notes(self) -> Dict[str, pd.DataFrame]:
        """
        Calcule toutes les 33 notes annexes avec barre de progression.
        
        Returns:
            Dict mappant nom_note -> DataFrame
            
        Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7
        """
        # Charger les balances une seule fois
        if self.balances is None:
            if not self.charger_balances():
                return {}
        
        logging.info("=" * 80)
        logging.info("DÉBUT DU CALCUL DES 33 NOTES ANNEXES")
        logging.info("=" * 80)
        
        debut = datetime.now()
        total_notes = len(self.NOTES_A_CALCULER)
        
        if self.mode_parallele:
            # Calcul parallèle (optionnel)
            self._calculer_parallele()
        else:
            # Calcul séquentiel
            self._calculer_sequentiel()
        
        fin = datetime.now()
        duree = (fin - debut).total_seconds()
        
        # Vérifier la contrainte de performance
        if duree > 30:
            logging.warning(f"⚠ Contrainte de performance non respectée: {duree:.2f}s > 30s")
        else:
            logging.info(f"✓ Contrainte de performance respectée: {duree:.2f}s < 30s")
        
        logging.info("=" * 80)
        logging.info(f"CALCUL TERMINÉ - Durée: {duree:.2f}s")
        logging.info(f"Notes calculées: {len(self.notes_calculees)}/{total_notes}")
        logging.info("=" * 80)
        
        return self.notes_calculees
    
    def _calculer_sequentiel(self):
        """
        Calcule les notes en mode séquentiel.
        
        Requirements: 12.3, 12.5
        """
        total = len(self.NOTES_A_CALCULER)
        
        for i, numero_note in enumerate(self.NOTES_A_CALCULER, 1):
            nom_note, df, succes, erreur = self.calculer_note_individuelle(numero_note)
            
            if succes and df is not None:
                self.notes_calculees[nom_note] = df
                self.statuts_calcul[nom_note] = "✓ Succès"
                self.afficher_barre_progression(i, total, numero_note, "✓")
                logging.info(f"✓ {nom_note} calculée")
            else:
                self.statuts_calcul[nom_note] = f"✗ Échec: {erreur}"
                self.afficher_barre_progression(i, total, numero_note, "✗")
                logging.error(f"✗ {nom_note}: {erreur}")
    
    def _calculer_parallele(self):
        """
        Calcule les notes en mode parallèle (optionnel).
        
        Requirements: 12.6, 12.7
        """
        logging.info("Mode parallèle activé")
        total = len(self.NOTES_A_CALCULER)
        notes_completees = 0
        
        try:
            # Utiliser ProcessPoolExecutor pour le calcul parallèle
            with ProcessPoolExecutor(max_workers=4) as executor:
                # Soumettre tous les calculs
                futures = {
                    executor.submit(self.calculer_note_individuelle, num): num
                    for num in self.NOTES_A_CALCULER
                }
                
                # Traiter les résultats au fur et à mesure
                for future in as_completed(futures):
                    numero_note = futures[future]
                    notes_completees += 1
                    
                    try:
                        nom_note, df, succes, erreur = future.result()
                        
                        if succes and df is not None:
                            self.notes_calculees[nom_note] = df
                            self.statuts_calcul[nom_note] = "✓ Succès"
                            self.afficher_barre_progression(notes_completees, total, numero_note, "✓")
                            logging.info(f"✓ {nom_note} calculée")
                        else:
                            self.statuts_calcul[nom_note] = f"✗ Échec: {erreur}"
                            self.afficher_barre_progression(notes_completees, total, numero_note, "✗")
                            logging.error(f"✗ {nom_note}: {erreur}")
                    except Exception as e:
                        logging.error(f"✗ Erreur lors du traitement de Note_{numero_note}: {e}")
                        self.statuts_calcul[f"Note_{numero_note.upper()}"] = f"✗ Erreur: {e}"
                        
        except Exception as e:
            logging.error(f"Erreur en mode parallèle: {e}")
            logging.info("Basculement en mode séquentiel...")
            self._calculer_sequentiel()
    
    def generer_rapport_recapitulatif(self) -> str:
        """
        Génère un rapport récapitulatif HTML avec le statut de chaque note.
        
        Returns:
            Code HTML du rapport
            
        Requirements: 12.7
        """
        html = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport Récapitulatif - Notes Annexes SYSCOHADA</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-card h3 {{
            margin: 0;
            font-size: 2em;
        }}
        .stat-card p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .succes {{
            color: #27ae60;
            font-weight: bold;
        }}
        .echec {{
            color: #e74c3c;
            font-weight: bold;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Rapport Récapitulatif - Notes Annexes SYSCOHADA Révisé</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{len(self.notes_calculees)}</h3>
                <p>Notes Calculées</p>
            </div>
            <div class="stat-card">
                <h3>{len(self.NOTES_A_CALCULER)}</h3>
                <p>Notes Totales</p>
            </div>
            <div class="stat-card">
                <h3>{(len(self.notes_calculees)/len(self.NOTES_A_CALCULER)*100):.1f}%</h3>
                <p>Taux de Réussite</p>
            </div>
        </div>
        
        <h2>Statut Détaillé par Note</h2>
        <table>
            <thead>
                <tr>
                    <th>Note</th>
                    <th>Statut</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for numero_note in self.NOTES_A_CALCULER:
            nom_note = f"Note_{numero_note.upper()}"
            statut = self.statuts_calcul.get(nom_note, "Non calculée")
            classe_css = "succes" if "✓" in statut else "echec"
            
            html += f"""
                <tr>
                    <td><strong>{nom_note}</strong></td>
                    <td class="{classe_css}">{statut}</td>
                </tr>
"""
        
        html += f"""
            </tbody>
        </table>
        
        <p class="timestamp">Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
        return html
    
    def valider_coherence(self) -> float:
        """
        Valide la cohérence inter-notes.
        
        Returns:
            Taux de cohérence global (0-100)
            
        Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7
        """
        if not self.notes_calculees:
            logging.warning("Aucune note calculée pour la validation")
            return 0.0
        
        logging.info("Validation de la cohérence inter-notes...")
        validator = CoherenceValidator(self.notes_calculees)
        taux = validator.calculer_taux_coherence()
        
        # Émettre une alerte si taux < 95%
        if taux < 95.0:
            logging.warning(f"⚠ ALERTE CRITIQUE: Taux de cohérence {taux:.1f}% < 95%")
        else:
            logging.info(f"✓ Taux de cohérence acceptable: {taux:.1f}% >= 95%")
        
        # Générer le rapport
        rapport_html = validator.generer_rapport_coherence()
        fichier_rapport = os.path.join(
            os.path.dirname(__file__),
            'Tests',
            'rapport_coherence.html'
        )
        
        os.makedirs(os.path.dirname(fichier_rapport), exist_ok=True)
        with open(fichier_rapport, 'w', encoding='utf-8') as f:
            f.write(rapport_html)
        
        logging.info(f"✓ Rapport de cohérence sauvegardé: {fichier_rapport}")
        
        return taux
    
    def generer_traces(self):
        """
        Génère les fichiers de trace pour toutes les notes calculées.
        Enregistre les calculs, métadonnées et gère l'historique.
        
        Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7
        """
        logging.info("=" * 80)
        logging.info("GÉNÉRATION DES TRACES")
        logging.info("=" * 80)
        
        traces_generees = 0
        traces_echouees = 0
        
        for nom_note, df in self.notes_calculees.items():
            try:
                # Extraire le numéro de la note
                numero = nom_note.replace('Note_', '').lower()
                
                trace_manager = TraceManager(numero)
                
                # Enregistrer les métadonnées
                import hashlib
                with open(self.fichier_balance, 'rb') as f:
                    hash_md5 = hashlib.md5(f.read()).hexdigest()
                
                trace_manager.enregistrer_metadata(
                    self.fichier_balance,
                    hash_md5
                )
                
                # Enregistrer les calculs pour chaque ligne de la note
                if df is not None and not df.empty:
                    for idx, row in df.iterrows():
                        # Extraire le libellé (première colonne généralement)
                        libelle = str(row.iloc[0]) if len(row) > 0 else f"Ligne {idx}"
                        
                        # Enregistrer les montants de la ligne
                        montants = {}
                        for col_name, value in row.items():
                            if col_name != row.index[0]:  # Skip libellé column
                                try:
                                    montants[str(col_name)] = float(value) if pd.notna(value) else 0.0
                                except (ValueError, TypeError):
                                    montants[str(col_name)] = 0.0
                        
                        # Enregistrer le calcul (sans comptes sources détaillés pour l'instant)
                        if montants:
                            # Prendre le premier montant comme représentatif
                            montant_principal = list(montants.values())[0] if montants else 0.0
                            trace_manager.enregistrer_calcul(
                                libelle=libelle,
                                montant=montant_principal,
                                comptes_sources=[]  # Les comptes sources seraient ajoutés par les calculateurs individuels
                            )
                    
                    # Ajouter le total si présent (dernière ligne généralement)
                    if len(df) > 0:
                        derniere_ligne = df.iloc[-1]
                        total_data = {}
                        for col_name, value in derniere_ligne.items():
                            if col_name != derniere_ligne.index[0]:
                                try:
                                    total_data[str(col_name)] = float(value) if pd.notna(value) else 0.0
                                except (ValueError, TypeError):
                                    total_data[str(col_name)] = 0.0
                        
                        if total_data:
                            trace_manager.ajouter_total(total_data)
                
                # Sauvegarder la trace
                fichier_trace = os.path.join(
                    os.path.dirname(__file__),
                    'Tests',
                    f'trace_note_{numero}.json'
                )
                trace_manager.sauvegarder_trace(fichier_trace)
                
                # Gérer l'historique (garder les 10 dernières)
                trace_manager.gerer_historique(max_historique=10)
                
                traces_generees += 1
                logging.info(f"✓ Trace générée: {nom_note}")
                
            except Exception as e:
                traces_echouees += 1
                logging.warning(f"✗ Impossible de générer la trace pour {nom_note}: {e}")
        
        logging.info("=" * 80)
        logging.info(f"TRACES GÉNÉRÉES: {traces_generees}/{len(self.notes_calculees)}")
        if traces_echouees > 0:
            logging.warning(f"Traces échouées: {traces_echouees}")
        logging.info("=" * 80)
    
    def exporter_excel(self, fichier_sortie: str = None) -> bool:
        """
        Exporte toutes les notes vers Excel.
        
        Args:
            fichier_sortie: Nom du fichier Excel (optionnel)
            
        Returns:
            True si l'export a réussi
            
        Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7
        """
        if not self.notes_calculees:
            logging.warning("Aucune note à exporter")
            return False
        
        logging.info("Export des notes vers Excel...")
        
        # Nom par défaut avec timestamp
        if fichier_sortie is None:
            timestamp = datetime.now().strftime('%Y%m%d')
            fichier_sortie = f"Notes_Annexes_Calculees_{timestamp}.xlsx"
        
        # Chemin complet
        chemin_sortie = os.path.join(
            os.path.dirname(__file__),
            'Tests',
            fichier_sortie
        )
        
        exporter = ExcelExporter(chemin_sortie)
        exporter.exporter_toutes_notes(self.notes_calculees)
        
        succes = exporter.sauvegarder()
        
        if succes:
            logging.info(f"✓ Export Excel réussi: {chemin_sortie}")
        else:
            logging.error("✗ Échec de l'export Excel")
        
        return succes


def main():
    """
    Point d'entrée principal.
    
    Exécute le workflow complet:
    1. Chargement des balances (cache)
    2. Calcul des 33 notes avec progression
    3. Validation de cohérence
    4. Génération des traces
    5. Export Excel
    6. Rapport récapitulatif
    """
    # Configurer le logging
    configurer_logging()
    
    # Chemin vers le fichier de balance
    fichier_balance = os.path.join(
        os.path.dirname(__file__),
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    # Vérifier que le fichier existe
    if not os.path.exists(fichier_balance):
        logging.error(f"Fichier de balance introuvable: {fichier_balance}")
        return
    
    # Créer l'orchestrateur (mode séquentiel par défaut)
    # Pour activer le mode parallèle: mode_parallele=True
    orchestrateur = CalculNotesAnnexesMain(fichier_balance, mode_parallele=False)
    
    # Calculer toutes les notes
    debut_total = time.time()
    notes = orchestrateur.calculer_toutes_notes()
    duree_total = time.time() - debut_total
    
    if notes:
        # Valider la cohérence
        taux_coherence = orchestrateur.valider_coherence()
        
        # Générer les traces
        orchestrateur.generer_traces()
        
        # Exporter vers Excel
        orchestrateur.exporter_excel()
        
        # Générer le rapport récapitulatif
        rapport_html = orchestrateur.generer_rapport_recapitulatif()
        fichier_rapport = os.path.join(
            os.path.dirname(__file__),
            'Tests',
            'rapport_recapitulatif.html'
        )
        
        os.makedirs(os.path.dirname(fichier_rapport), exist_ok=True)
        with open(fichier_rapport, 'w', encoding='utf-8') as f:
            f.write(rapport_html)
        
        logging.info(f"✓ Rapport récapitulatif sauvegardé: {fichier_rapport}")
        
        # Résumé final
        logging.info("=" * 80)
        logging.info("RÉSUMÉ FINAL")
        logging.info(f"Notes calculées: {len(notes)}/{len(orchestrateur.NOTES_A_CALCULER)}")
        logging.info(f"Taux de cohérence: {taux_coherence:.1f}%")
        logging.info(f"Durée totale: {duree_total:.2f}s")
        
        if duree_total < 30:
            logging.info("✓ Contrainte de performance respectée (< 30s)")
        else:
            logging.warning(f"⚠ Contrainte de performance non respectée ({duree_total:.2f}s > 30s)")
        
        logging.info("=" * 80)
    else:
        logging.error("Aucune note n'a pu être calculée")


if __name__ == "__main__":
    main()
