#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de calcul de la NOTE 6 - AUTRES CRÉANCES
Syscohada Révisé

Ce script calcule la Note 6 à partir des balances N, N-1, N-2 en utilisant
l'architecture modulaire du système de calcul automatique des notes annexes.

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


class CalculateurNote6(CalculateurNote):
    """
    Calculateur pour la Note 6 - Autres Créances.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    de la Note 6 avec les lignes d'autres créances:
    - Fournisseurs débiteurs, avances et acomptes versés
    - Personnel débiteur
    - État et collectivités publiques (créances)
    - Organismes sociaux (créances)
    - Débiteurs divers
    - Créances sur cessions d'immobilisations
    - Autres créances
    
    Mapping des comptes SYSCOHADA:
    - Comptes autres créances:
      * 40X: Fournisseurs et comptes rattachés (soldes débiteurs)
      * 42X: Personnel
      * 43X: Organismes sociaux
      * 44X: État et collectivités publiques
      * 45X: Organismes internationaux
      * 46X: Associés et groupe
      * 47X: Débiteurs et créditeurs divers
    - Comptes provisions: 49X (Provisions pour dépréciation)
    
    Note: Les autres créances peuvent faire l'objet de provisions pour dépréciation
    en cas de risque de non-recouvrement.
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 6.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel des balances
        """
        super().__init__(fichier_balance, "6", "AUTRES CRÉANCES")
        
        # Mapping des comptes pour chaque ligne de la Note 6
        self.mapping_comptes = {
            'Fournisseurs débiteurs, avances et acomptes versés': {
                'brut': ['409'],  # Fournisseurs débiteurs
                'amort': ['4909']  # Provisions pour dépréciation
            },
            'Personnel débiteur': {
                'brut': ['421', '422', '423', '424', '425', '426', '427', '428'],
                'amort': ['4921', '4922', '4923', '4924', '4925', '4926', '4927', '4928']
            },
            'État et collectivités publiques (créances)': {
                'brut': ['441', '442', '443', '444', '445', '446', '447', '448'],
                'amort': ['4941', '4942', '4943', '4944', '4945', '4946', '4947', '4948']
            },
            'Organismes sociaux (créances)': {
                'brut': ['431', '432', '433', '434', '435', '436', '437', '438'],
                'amort': ['4931', '4932', '4933', '4934', '4935', '4936', '4937', '4938']
            },
            'Débiteurs divers': {
                'brut': ['471', '472', '473', '474', '475', '476', '477', '478'],
                'amort': ['4971', '4972', '4973', '4974', '4975', '4976', '4977', '4978']
            },
            'Associés et groupe': {
                'brut': ['461', '462', '463', '464', '465', '466', '467', '468'],
                'amort': ['4961', '4962', '4963', '4964', '4965', '4966', '4967', '4968']
            },
            'Organismes internationaux': {
                'brut': ['451', '452', '453', '454', '455', '456', '457', '458'],
                'amort': ['4951', '4952', '4953', '4954', '4955', '4956', '4957', '4958']
            }
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 6 complète avec les 7 lignes et le total.
        
        Cette méthode:
        1. Calcule chaque ligne d'autres créances
        2. Calcule la ligne de total
        3. Retourne un DataFrame avec toutes les lignes
        
        Returns:
            DataFrame contenant les 8 lignes (7 lignes + total)
        """
        lignes = []
        
        # Calculer chaque ligne d'autres créances
        for libelle, comptes in self.mapping_comptes.items():
            print(f"  Calcul: {libelle}...")
            
            ligne = self.calculer_ligne_note(
                libelle=libelle,
                comptes_brut=comptes['brut'],
                comptes_amort=comptes.get('amort')
            )
            
            lignes.append(ligne)
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        # Calculer la ligne de total
        total = self.calculer_total(df)
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def calculer_total(self, df: pd.DataFrame) -> dict:
        """
        Calcule la ligne de total en sommant toutes les colonnes.
        
        Args:
            df: DataFrame contenant les lignes de détail
            
        Returns:
            Dict représentant la ligne de total
        """
        total = {
            'libelle': 'TOTAL AUTRES CRÉANCES',
            'brut_ouverture': df['brut_ouverture'].sum(),
            'augmentations': df['augmentations'].sum(),
            'diminutions': df['diminutions'].sum(),
            'brut_cloture': df['brut_cloture'].sum(),
            'amort_ouverture': df['amort_ouverture'].sum(),
            'dotations': df['dotations'].sum(),
            'reprises': df['reprises'].sum(),
            'amort_cloture': df['amort_cloture'].sum(),
            'vnc_ouverture': df['vnc_ouverture'].sum(),
            'vnc_cloture': df['vnc_cloture'].sum()
        }
        
        return total


# Point d'entrée principal
if __name__ == "__main__":
    import argparse
    
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(
        description='Calcul de la Note 6 - Autres Créances'
    )
    parser.add_argument(
        'fichier_balance',
        nargs='?',
        default='../../P000 -BALANCE DEMO N_N-1_N-2.xls',
        help='Chemin vers le fichier Excel des balances (N, N-1, N-2)'
    )
    parser.add_argument(
        '--output-html',
        default='../Tests/test_note_6.html',
        help='Chemin du fichier HTML de sortie (défaut: ../Tests/test_note_6.html)'
    )
    parser.add_argument(
        '--output-trace',
        default='../Tests/trace_note_6.json',
        help='Chemin du fichier de trace JSON (défaut: ../Tests/trace_note_6.json)'
    )
    
    args = parser.parse_args()
    
    # Créer le calculateur
    calculateur = CalculateurNote6(args.fichier_balance)
    
    # Exécuter le calcul complet
    calculateur.executer(
        fichier_html=args.output_html,
        fichier_trace=args.output_trace
    )
