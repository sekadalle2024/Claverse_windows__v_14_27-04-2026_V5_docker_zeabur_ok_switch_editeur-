#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculateur pour Note 32 - Reprises de Provisions (SYSCOHADA Révisé)

Cette note présente les reprises de provisions de l'exercice, qui correspondent
aux provisions antérieurement constituées et devenues sans objet ou excédentaires.

Structure de la note:
- Reprises de provisions pour risques et charges
- Reprises de provisions pour dépréciation des immobilisations
- Reprises de provisions pour dépréciation des stocks
- Reprises de provisions pour dépréciation des créances
- Total des reprises de provisions

Comptes concernés (classe 791X):
- 7911: Reprises de provisions pour risques et charges
- 7912: Reprises de provisions pour dépréciation des immobilisations
- 7913: Reprises de provisions pour dépréciation des stocks
- 7914: Reprises de provisions pour dépréciation des créances

Référence: Plan comptable SYSCOHADA révisé
"""

import sys
import os
from pathlib import Path
from typing import Dict, List
import pandas as pd

# Ajouter le chemin des modules au PYTHONPATH
current_dir = Path(__file__).parent
modules_dir = current_dir.parent / "Modules"
sys.path.insert(0, str(modules_dir))

from balance_reader import BalanceReader
from account_extractor import AccountExtractor
from movement_calculator import MovementCalculator
from html_generator import HTMLGenerator
from trace_manager import TraceManager


class CalculateurNote32:
    """
    Calculateur pour la Note 32 - Reprises de Provisions.
    
    Cette classe calcule les reprises de provisions de l'exercice en extrayant
    les soldes des comptes 791X et en les présentant selon la structure
    officielle de la note annexe SYSCOHADA.
    
    Attributes:
        fichier_balance (str): Chemin vers le fichier Excel de balances
        numero_note (str): Numéro de la note ("32")
        titre_note (str): Titre de la note
        balance_n (pd.DataFrame): Balance de l'exercice N
        balance_n1 (pd.DataFrame): Balance de l'exercice N-1
        mapping_comptes (Dict): Mapping des lignes aux comptes 791X
        trace_manager (TraceManager): Gestionnaire de traçabilité
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 32.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel de balances
        """
        self.fichier_balance = fichier_balance
        self.numero_note = "32"
        self.titre_note = "Reprises de Provisions"
        
        # DataFrames des balances
        self.balance_n = None
        self.balance_n1 = None
        self.balance_n2 = None
        
        # Mapping des comptes pour Note 32 (Reprises de provisions - compte 791X)
        self.mapping_comptes = {
            "Reprises de provisions pour risques et charges": ["7911"],
            "Reprises de provisions pour dépréciation des immobilisations": ["7912"],
            "Reprises de provisions pour dépréciation des stocks": ["7913"],
            "Reprises de provisions pour dépréciation des créances": ["7914"]
        }
        
        # Gestionnaire de traçabilité
        self.trace_manager = TraceManager(self.numero_note)
        
        print(f"\n{'='*80}")
        print(f"  CALCULATEUR NOTE {self.numero_note} - {self.titre_note}")
        print(f"{'='*80}\n")
    
    def charger_balances(self) -> bool:
        """
        Charge les balances des 3 exercices (N, N-1, N-2) via Balance_Reader.
        
        Returns:
            bool: True si le chargement est réussi, False sinon
        """
        try:
            print(f"📂 Chargement des balances depuis: {self.fichier_balance}")
            
            reader = BalanceReader(self.fichier_balance)
            self.balance_n, self.balance_n1, self.balance_n2 = reader.charger_balances()
            
            print(f"✓ Balance N   : {len(self.balance_n)} lignes chargées")
            print(f"✓ Balance N-1 : {len(self.balance_n1)} lignes chargées")
            print(f"✓ Balance N-2 : {len(self.balance_n2)} lignes chargées")
            print()
            
            # Enregistrer les métadonnées
            import hashlib
            with open(self.fichier_balance, 'rb') as f:
                hash_md5 = hashlib.md5(f.read()).hexdigest()
            self.trace_manager.enregistrer_metadata(self.fichier_balance, hash_md5)
            
            return True
            
        except Exception as e:
            print(f"✗ Erreur lors du chargement des balances: {str(e)}")
            return False
    
    def calculer_ligne_note(self, libelle: str, comptes: List[str]) -> Dict[str, float]:
        """
        Calcule une ligne de la note (reprises pour une catégorie).
        
        Pour les reprises de provisions (produits), on extrait le solde créditeur
        des comptes 791X qui représente le montant des reprises de l'exercice.
        
        Args:
            libelle: Libellé de la ligne
            comptes: Liste des racines de comptes (ex: ["7911"])
            
        Returns:
            Dict contenant le libellé et les montants N et N-1
        """
        # Extracteurs pour chaque exercice
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        
        # Calculateur de mouvements
        movement_calc = MovementCalculator()
        
        # Extraire les soldes des comptes de reprises
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Pour les reprises (produits - compte 791X), on prend le solde créditeur
        # qui représente le montant des reprises de provisions de l'exercice
        montant_n = movement_calc.calculer_solde_cloture(
            soldes_n['solde_debit'],
            soldes_n['solde_credit']
        )
        
        montant_n1 = movement_calc.calculer_solde_cloture(
            soldes_n1['solde_debit'],
            soldes_n1['solde_credit']
        )
        
        # Les reprises sont des produits (créditeurs), donc on inverse le signe
        # pour avoir des montants positifs
        montant_n = abs(montant_n)
        montant_n1 = abs(montant_n1)
        
        # Traçabilité
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'reprise_provision',
                'solde_debit_n': solde['solde_debit'],
                'solde_credit_n': solde['solde_credit']
            })
        
        self.trace_manager.enregistrer_calcul(
            libelle=libelle,
            montant=montant_n,
            comptes_sources=comptes_sources
        )
        
        return {
            'libelle': libelle,
            'montant_n': montant_n,
            'montant_n1': montant_n1,
            'comptes': comptes
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la note complète avec toutes les lignes et le total.
        
        Returns:
            pd.DataFrame: DataFrame contenant toutes les lignes de la note
        """
        print(f"🔢 Calcul de la note {self.numero_note}...")
        
        lignes = []
        
        # Calculer chaque ligne de la note
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_note(libelle, comptes)
            lignes.append(ligne)
            print(f"  ✓ {libelle}: {ligne['montant_n']:>15,.0f} (N) | {ligne['montant_n1']:>15,.0f} (N-1)")
        
        # Calculer le total
        total_n = sum(ligne['montant_n'] for ligne in lignes)
        total_n1 = sum(ligne['montant_n1'] for ligne in lignes)
        
        lignes.append({
            'libelle': 'TOTAL DES REPRISES DE PROVISIONS',
            'montant_n': total_n,
            'montant_n1': total_n1,
            'comptes': [],
            'total': True
        })
        
        print(f"  {'─'*60}")
        print(f"  ✓ TOTAL: {total_n:>15,.0f} (N) | {total_n1:>15,.0f} (N-1)")
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """
        Génère le fichier HTML de la note via HTML_Generator.
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        # Configuration des colonnes pour le HTML
        colonnes_config = {
            'colonnes': ['libelle', 'montant_n', 'montant_n1'],
            'en_tetes': {
                'libelle': 'NATURE DES REPRISES',
                'montant_n': 'Exercice N',
                'montant_n1': 'Exercice N-1'
            },
            'alignements': {
                'libelle': 'left',
                'montant_n': 'right',
                'montant_n1': 'right'
            },
            'formats': {
                'montant_n': 'montant',
                'montant_n1': 'montant'
            }
        }
        
        generator = HTMLGenerator(self.titre_note, self.numero_note)
        html = generator.generer_html(df, colonnes_config)
        
        return html
    
    def sauvegarder_html(self, html: str, fichier_sortie: str):
        """
        Sauvegarde le fichier HTML généré.
        
        Args:
            html: Code HTML à sauvegarder
            fichier_sortie: Chemin du fichier de sortie
        """
        try:
            output_dir = Path(fichier_sortie).parent
            output_dir.mkdir(parents=True, exist_ok=True)
            
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                f.write(html)
            
            print(f"✓ Fichier HTML sauvegardé: {fichier_sortie}")
            
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde du HTML: {str(e)}")
    
    def sauvegarder_trace(self, fichier_sortie: str):
        """
        Sauvegarde le fichier de trace JSON.
        
        Args:
            fichier_sortie: Chemin du fichier de trace
        """
        try:
            self.trace_manager.sauvegarder_trace(fichier_sortie)
            print(f"✓ Fichier de trace sauvegardé: {fichier_sortie}")
            
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde de la trace: {str(e)}")
    
    def afficher_resume(self, df: pd.DataFrame):
        """
        Affiche un résumé des calculs dans la console.
        
        Args:
            df: DataFrame contenant les données de la note
        """
        print(f"\n{'─'*80}")
        print(f"  RÉSUMÉ NOTE {self.numero_note}")
        print(f"{'─'*80}\n")
        
        # Ligne de total (dernière ligne)
        total = df.iloc[-1]
        
        print(f"  Nombre de catégories: {len(df) - 1}")
        print(f"  Total reprises N:     {total['montant_n']:>15,.0f}")
        print(f"  Total reprises N-1:   {total['montant_n1']:>15,.0f}")
        print(f"  Variation:            {total['montant_n'] - total['montant_n1']:>15,.0f}")
        print()
    
    def executer(self, fichier_html: str = None, fichier_trace: str = None):
        """
        Exécute le calcul complet de la note (méthode principale).
        
        Args:
            fichier_html: Chemin du fichier HTML de sortie (optionnel)
            fichier_trace: Chemin du fichier de trace JSON (optionnel)
        """
        from datetime import datetime
        start_time = datetime.now()
        
        # Étape 1: Charger les balances
        if not self.charger_balances():
            print("✗ Échec du chargement des balances. Arrêt du traitement.")
            return
        
        # Étape 2: Générer la note
        df_note = self.generer_note()
        print(f"✓ Note calculée: {len(df_note)} lignes")
        print()
        
        # Étape 3: Générer le HTML
        print(f"📄 Génération du HTML...")
        html = self.generer_html(df_note)
        print(f"✓ HTML généré")
        print()
        
        # Étape 4: Sauvegarder les fichiers
        if fichier_html:
            self.sauvegarder_html(html, fichier_html)
        
        if fichier_trace:
            self.sauvegarder_trace(fichier_trace)
        
        # Étape 5: Afficher le résumé
        self.afficher_resume(df_note)
        
        # Durée totale
        end_time = datetime.now()
        duree = (end_time - start_time).total_seconds()
        
        print(f"{'='*80}")
        print(f"  ✓ NOTE {self.numero_note} CALCULÉE AVEC SUCCÈS EN {duree:.2f}s")
        print(f"{'='*80}\n")


# Point d'entrée pour les tests
if __name__ == "__main__":
    # Chemin vers le fichier de balance de démonstration
    # Essayer plusieurs chemins possibles
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / "P000 -BALANCE DEMO N_N-1_N-2.xlsx",
        Path(__file__).parent.parent.parent / "BALANCES_N_N1_N2.xlsx",
        Path(__file__).parent.parent.parent / "Balance excel.xlsx"
    ]
    
    balance_file = None
    for path in possible_paths:
        if path.exists():
            balance_file = path
            break
    
    if balance_file is None:
        print("✗ Aucun fichier de balance trouvé. Chemins testés:")
        for path in possible_paths:
            print(f"  - {path}")
        sys.exit(1)
    
    # Chemins de sortie
    output_dir = Path(__file__).parent.parent / "Tests"
    fichier_html = output_dir / "test_note_32.html"
    fichier_trace = output_dir / "trace_note_32.json"
    
    # Créer et exécuter le calculateur
    calculateur = CalculateurNote32(str(balance_file))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )
