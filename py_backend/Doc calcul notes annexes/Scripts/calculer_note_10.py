#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de calcul de la NOTE 10 - RÉSULTAT
Syscohada Révisé

Ce script calcule la Note 10 à partir des balances N, N-1, N-2 en utilisant
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


class CalculateurNote10(CalculateurNote):
    """
    Calculateur pour la Note 10 - Résultat.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    de la Note 10 avec les mouvements du résultat:
    - Résultat en instance d'affectation
    - Résultat de l'exercice
    - Résultat net de l'exercice
    - Résultat des exercices antérieurs
    
    Mapping des comptes SYSCOHADA:
    - Comptes de résultat: 12X et 13X
      * 12: Report à nouveau
        - 121: Report à nouveau créditeur (bénéfice)
        - 129: Report à nouveau débiteur (perte)
      * 13: Résultat net de l'exercice
        - 130: Résultat en instance d'affectation
        - 131: Résultat net: Bénéfice
        - 139: Résultat net: Perte
    
    Note: Le résultat représente le bénéfice ou la perte de l'exercice.
    Cette note suit les mouvements du résultat (affectation, distribution)
    sur les 3 exercices (N, N-1, N-2).
    Les comptes de résultat ne font pas l'objet d'amortissements.
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 10.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel des balances
        """
        super().__init__(fichier_balance, "10", "RÉSULTAT")
        
        # Mapping des comptes pour chaque ligne de la Note 10
        self.mapping_comptes = {
            'Résultat en instance d\'affectation': {
                'brut': ['130'],
                'amort': None  # Pas d'amortissements pour le résultat
            },
            'Résultat net: Bénéfice': {
                'brut': ['131'],
                'amort': None
            },
            'Résultat net: Perte': {
                'brut': ['139'],
                'amort': None
            },
            'Report à nouveau créditeur': {
                'brut': ['121'],
                'amort': None
            },
            'Report à nouveau débiteur': {
                'brut': ['129'],
                'amort': None
            }
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 10 complète avec les 5 lignes et le total.
        
        Cette méthode:
        1. Calcule chaque ligne de résultat
        2. Calcule la ligne de total
        3. Retourne un DataFrame avec toutes les lignes
        
        Returns:
            DataFrame contenant les 6 lignes (5 lignes + total)
        """
        lignes = []
        
        # Calculer chaque ligne de résultat
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
            'libelle': 'TOTAL RÉSULTAT',
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
        description='Calcul de la Note 10 - Résultat'
    )
    parser.add_argument(
        'fichier_balance',
        nargs='?',
        default='../../../P000 -BALANCE DEMO N_N-1_N-2.xls',
        help='Chemin vers le fichier Excel des balances (N, N-1, N-2)'
    )
    parser.add_argument(
        '--output-html',
        default='../Tests/test_note_10.html',
        help='Chemin du fichier HTML de sortie (défaut: ../Tests/test_note_10.html)'
    )
    parser.add_argument(
        '--output-trace',
        default='../Tests/trace_note_10.json',
        help='Chemin du fichier de trace JSON (défaut: ../Tests/trace_note_10.json)'
    )
    
    args = parser.parse_args()
    
    # Créer le calculateur
    calculateur = CalculateurNote10(args.fichier_balance)
    
    # Exécuter le calcul complet
    calculateur.executer(
        fichier_html=args.output_html,
        fichier_trace=args.output_trace
    )
