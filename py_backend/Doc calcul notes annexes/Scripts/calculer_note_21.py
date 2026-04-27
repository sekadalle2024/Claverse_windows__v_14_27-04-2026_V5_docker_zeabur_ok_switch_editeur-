#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de calcul de la NOTE 21 - ACHATS DE MARCHANDISES
Syscohada Révisé

Ce script calcule la Note 21 à partir des balances N, N-1, N-2 en utilisant
l'architecture modulaire du système de calcul automatique des notes annexes.

Note: Cette note fait partie du compte de résultat (charges) et ne comporte
pas de colonnes d'amortissement. Elle présente uniquement les mouvements
de l'exercice pour les achats de marchandises.

Auteur: Système de calcul automatique des notes annexes SYSCOHADA
Date: 26 Avril 2026
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Ajouter le chemin du template au PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote
from account_extractor import AccountExtractor
from movement_calculator import MovementCalculator


class CalculateurNote21(CalculateurNote):
    """
    Calculateur pour la Note 21 - Achats de Marchandises.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    de la Note 21 avec les achats de marchandises destinées à la revente.
    
    Mapping des comptes SYSCOHADA:
    - Comptes 60X: Achats de marchandises
      * 601: Achats de marchandises
      * 602: Achats de matières premières et fournitures liées
      * 603: Variations des stocks de marchandises
      * 604-608: Autres achats
    
    Structure de la note:
    - Achats de marchandises (exercice N)
    - Achats de marchandises (exercice N-1)
    - Variation N / N-1
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 21.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel des balances
        """
        super().__init__(fichier_balance, "21", "ACHATS DE MARCHANDISES")
        
        # Mapping des comptes pour la Note 21
        # Note: Pour les comptes de charges, on utilise uniquement les comptes 60X
        self.mapping_comptes = {
            'Achats de marchandises': {
                'comptes': ['601', '6011', '6012', '6013', '6014', '6015', '6016', '6017', '6018', '6019']
            }
        }
    
    def calculer_ligne_charge(
        self,
        libelle: str,
        comptes: list,
        exercice: str = 'N'
    ) -> dict:
        """
        Calcule une ligne de charge pour un exercice donné.
        
        Pour les comptes de charges (classe 6), on extrait:
        - Le solde débiteur (charges) de l'exercice
        - Les mouvements débiteurs (augmentation des charges)
        - Les mouvements créditeurs (diminution des charges, reprises)
        
        Args:
            libelle: Libellé de la ligne
            comptes: Liste des racines de comptes
            exercice: 'N' ou 'N-1' pour sélectionner la balance
            
        Returns:
            Dict contenant les montants calculés
        """
        # Sélectionner la balance appropriée
        if exercice == 'N':
            balance = self.balance_n
        elif exercice == 'N-1':
            balance = self.balance_n1
        else:
            raise ValueError(f"Exercice invalide: {exercice}. Utilisez 'N' ou 'N-1'")
        
        # Extracteur pour l'exercice sélectionné
        extractor = AccountExtractor(balance)
        
        # Extraire les soldes des comptes
        soldes = extractor.extraire_comptes_multiples(comptes)
        
        # Pour les comptes de charges (classe 6):
        # - Le solde débiteur représente les charges de l'exercice
        # - Les mouvements débiteurs sont les charges enregistrées
        # - Les mouvements créditeurs sont les reprises/annulations
        
        montant_charge = soldes['solde_debit'] - soldes['solde_credit']
        mouvements_debit = soldes['mvt_debit']
        mouvements_credit = soldes['mvt_credit']
        
        # Enregistrer la traçabilité
        comptes_sources = []
        for compte in comptes:
            solde = extractor.extraire_solde_compte(compte)
            if solde['solde_debit'] > 0 or solde['solde_credit'] > 0:
                comptes_sources.append({
                    'compte': compte,
                    'type': 'charge',
                    'solde_debit': solde['solde_debit'],
                    'solde_credit': solde['solde_credit'],
                    'mvt_debit': solde['mvt_debit'],
                    'mvt_credit': solde['mvt_credit']
                })
        
        self.trace_manager.enregistrer_calcul(
            libelle=f"{libelle} - Exercice {exercice}",
            montant=montant_charge,
            comptes_sources=comptes_sources
        )
        
        return {
            'libelle': libelle,
            'exercice': exercice,
            'montant_charge': montant_charge,
            'mouvements_debit': mouvements_debit,
            'mouvements_credit': mouvements_credit
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 21 complète avec les achats N et N-1.
        
        Cette méthode:
        1. Calcule les achats de marchandises pour l'exercice N
        2. Calcule les achats de marchandises pour l'exercice N-1
        3. Calcule la variation entre N et N-1
        4. Retourne un DataFrame avec les 3 lignes
        
        Returns:
            DataFrame contenant les lignes de la note
        """
        lignes = []
        
        # Calculer pour chaque poste d'achats
        for libelle, mapping in self.mapping_comptes.items():
            print(f"  Calcul: {libelle}...")
            
            # Calculer pour l'exercice N
            ligne_n = self.calculer_ligne_charge(
                libelle=libelle,
                comptes=mapping['comptes'],
                exercice='N'
            )
            
            # Calculer pour l'exercice N-1
            ligne_n1 = self.calculer_ligne_charge(
                libelle=libelle,
                comptes=mapping['comptes'],
                exercice='N-1'
            )
            
            # Créer les lignes pour le DataFrame
            lignes.append({
                'libelle': f"{libelle} - Exercice N",
                'montant': ligne_n['montant_charge'],
                'mouvements_debit': ligne_n['mouvements_debit'],
                'mouvements_credit': ligne_n['mouvements_credit']
            })
            
            lignes.append({
                'libelle': f"{libelle} - Exercice N-1",
                'montant': ligne_n1['montant_charge'],
                'mouvements_debit': ligne_n1['mouvements_debit'],
                'mouvements_credit': ligne_n1['mouvements_credit']
            })
            
            # Calculer la variation
            variation = ligne_n['montant_charge'] - ligne_n1['montant_charge']
            variation_pct = (variation / ligne_n1['montant_charge'] * 100) if ligne_n1['montant_charge'] != 0 else 0
            
            lignes.append({
                'libelle': f"Variation N / N-1",
                'montant': variation,
                'mouvements_debit': 0,
                'mouvements_credit': 0
            })
            
            print(f"    Exercice N:   {ligne_n['montant_charge']:>15,.0f}")
            print(f"    Exercice N-1: {ligne_n1['montant_charge']:>15,.0f}")
            print(f"    Variation:    {variation:>15,.0f} ({variation_pct:+.1f}%)")
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """
        Génère le fichier HTML de la note via HTML_Generator.
        
        Cette méthode surcharge la méthode de base pour adapter la structure
        aux notes de charges (pas d'amortissements).
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        from html_generator import HTMLGenerator
        
        # Configuration des colonnes pour le HTML (structure simplifiée pour charges)
        colonnes_config = {
            'groupes': [
                {'titre': 'ACHATS DE MARCHANDISES', 'colonnes': ['montant', 'mouvements_debit', 'mouvements_credit']}
            ],
            'en_tetes': {
                'libelle': 'EXERCICE',
                'montant': 'Montant',
                'mouvements_debit': 'Mouvements Débit',
                'mouvements_credit': 'Mouvements Crédit'
            }
        }
        
        generator = HTMLGenerator(self.titre_note, self.numero_note)
        html = generator.generer_html(df, colonnes_config)
        
        return html
    
    def afficher_resume(self, df: pd.DataFrame):
        """
        Affiche un résumé des calculs dans la console.
        
        Args:
            df: DataFrame contenant les données de la note
        """
        print(f"\n{'─'*80}")
        print(f"  RÉSUMÉ NOTE {self.numero_note}")
        print(f"{'─'*80}\n")
        
        # Extraire les montants N et N-1
        montant_n = df[df['libelle'].str.contains('Exercice N$', regex=True)]['montant'].sum()
        montant_n1 = df[df['libelle'].str.contains('Exercice N-1')]['montant'].sum()
        variation = montant_n - montant_n1
        
        print(f"  Achats Exercice N:    {montant_n:>15,.0f}")
        print(f"  Achats Exercice N-1:  {montant_n1:>15,.0f}")
        print(f"  Variation:            {variation:>15,.0f}")
        
        if montant_n1 != 0:
            variation_pct = (variation / montant_n1) * 100
            print(f"  Variation %:          {variation_pct:>15,.1f}%")
        
        print()


# Point d'entrée principal
if __name__ == "__main__":
    import argparse
    
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(
        description='Calcul de la Note 21 - Achats de Marchandises'
    )
    parser.add_argument(
        'fichier_balance',
        nargs='?',
        default='../../P000 -BALANCE DEMO N_N-1_N-2.xlsx',
        help='Chemin vers le fichier Excel des balances (N, N-1, N-2)'
    )
    parser.add_argument(
        '--output-html',
        default='../Tests/test_note_21.html',
        help='Chemin du fichier HTML de sortie (défaut: ../Tests/test_note_21.html)'
    )
    parser.add_argument(
        '--output-trace',
        default='../Tests/note_21_trace.json',
        help='Chemin du fichier de trace JSON (défaut: ../Tests/note_21_trace.json)'
    )
    
    args = parser.parse_args()
    
    # Créer le calculateur
    calculateur = CalculateurNote21(args.fichier_balance)
    
    # Exécuter le calcul complet
    calculateur.executer(
        fichier_html=args.output_html,
        fichier_trace=args.output_trace
    )
