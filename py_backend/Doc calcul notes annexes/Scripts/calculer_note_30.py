#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de calcul de la NOTE 30 - PRODUCTION IMMOBILISÉE
Syscohada Révisé

Ce script calcule la Note 30 à partir des balances N, N-1, N-2 en utilisant
l'architecture modulaire du système de calcul automatique des notes annexes.

Note: Cette note fait partie du compte de résultat (produits) et ne comporte
pas de colonnes d'amortissement. Elle présente uniquement les mouvements
de l'exercice pour la production immobilisée (production de l'entreprise
pour elle-même, capitalisée en immobilisations).

Auteur: Système de calcul automatique des notes annexes SYSCOHADA
Date: 27 Avril 2026
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


class CalculateurNote30(CalculateurNote):
    """
    Calculateur pour la Note 30 - Production Immobilisée.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    de la Note 30 avec la production immobilisée.
    
    Mapping des comptes SYSCOHADA:
    - Comptes 72X: Production immobilisée
      * 721: Immobilisations incorporelles
      * 722: Immobilisations corporelles
      * 726: Immobilisations financières
    
    Structure de la note:
    - Production immobilisée (exercice N)
    - Production immobilisée (exercice N-1)
    - Variation N / N-1
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 30.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel des balances
        """
        super().__init__(fichier_balance, "30", "PRODUCTION IMMOBILISÉE")
        
        # Mapping des comptes pour la Note 30
        # Note: Pour les comptes de production immobilisée, on utilise les comptes 72X
        self.mapping_comptes = {
            'Production immobilisée - Immobilisations incorporelles': {
                'comptes': ['721', '7211', '7212', '7213', '7214', '7215', '7216', '7217', '7218', '7219']
            },
            'Production immobilisée - Immobilisations corporelles': {
                'comptes': ['722', '7221', '7222', '7223', '7224', '7225', '7226', '7227', '7228', '7229']
            },
            'Production immobilisée - Immobilisations financières': {
                'comptes': ['726', '7261', '7262', '7263', '7264', '7265', '7266', '7267', '7268', '7269']
            }
        }
    
    def calculer_ligne_produit(
        self,
        libelle: str,
        comptes: list,
        exercice: str = 'N'
    ) -> dict:
        """
        Calcule une ligne de produit pour un exercice donné.
        
        Pour les comptes de production immobilisée (classe 72), on extrait:
        - Le solde créditeur (produits) de l'exercice
        - Les mouvements créditeurs (augmentation des produits)
        - Les mouvements débiteurs (diminution des produits, reprises)
        
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
        
        # Pour les comptes de production immobilisée (classe 72):
        # - Le solde créditeur représente la production immobilisée de l'exercice
        # - Les mouvements créditeurs sont les productions enregistrées
        # - Les mouvements débiteurs sont les reprises/annulations
        
        montant_produit = soldes['solde_credit'] - soldes['solde_debit']
        mouvements_credit = soldes['mvt_credit']
        mouvements_debit = soldes['mvt_debit']
        
        # Enregistrer la traçabilité
        comptes_sources = []
        for compte in comptes:
            solde = extractor.extraire_solde_compte(compte)
            if solde['solde_debit'] > 0 or solde['solde_credit'] > 0:
                comptes_sources.append({
                    'compte': compte,
                    'type': 'production_immobilisee',
                    'solde_debit': solde['solde_debit'],
                    'solde_credit': solde['solde_credit'],
                    'mvt_debit': solde['mvt_debit'],
                    'mvt_credit': solde['mvt_credit']
                })
        
        self.trace_manager.enregistrer_calcul(
            libelle=f"{libelle} - Exercice {exercice}",
            montant=montant_produit,
            comptes_sources=comptes_sources
        )
        
        return {
            'libelle': libelle,
            'exercice': exercice,
            'montant_produit': montant_produit,
            'mouvements_credit': mouvements_credit,
            'mouvements_debit': mouvements_debit
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 30 complète avec la production immobilisée N et N-1.
        
        Cette méthode:
        1. Calcule la production immobilisée pour l'exercice N
        2. Calcule la production immobilisée pour l'exercice N-1
        3. Calcule la variation entre N et N-1
        4. Retourne un DataFrame avec toutes les lignes
        
        Returns:
            DataFrame contenant les lignes de la note
        """
        lignes = []
        
        # Calculer pour chaque poste de production immobilisée
        for libelle, mapping in self.mapping_comptes.items():
            print(f"  Calcul: {libelle}...")
            
            # Calculer pour l'exercice N
            ligne_n = self.calculer_ligne_produit(
                libelle=libelle,
                comptes=mapping['comptes'],
                exercice='N'
            )
            
            # Calculer pour l'exercice N-1
            ligne_n1 = self.calculer_ligne_produit(
                libelle=libelle,
                comptes=mapping['comptes'],
                exercice='N-1'
            )
            
            # Créer les lignes pour le DataFrame
            lignes.append({
                'libelle': f"{libelle} - Exercice N",
                'montant': ligne_n['montant_produit'],
                'mouvements_credit': ligne_n['mouvements_credit'],
                'mouvements_debit': ligne_n['mouvements_debit']
            })
            
            lignes.append({
                'libelle': f"{libelle} - Exercice N-1",
                'montant': ligne_n1['montant_produit'],
                'mouvements_credit': ligne_n1['mouvements_credit'],
                'mouvements_debit': ligne_n1['mouvements_debit']
            })
            
            # Calculer la variation
            variation = ligne_n['montant_produit'] - ligne_n1['montant_produit']
            variation_pct = (variation / ligne_n1['montant_produit'] * 100) if ligne_n1['montant_produit'] != 0 else 0
            
            lignes.append({
                'libelle': f"Variation N / N-1",
                'montant': variation,
                'mouvements_credit': 0,
                'mouvements_debit': 0
            })
            
            print(f"    Exercice N:   {ligne_n['montant_produit']:>15,.0f}")
            print(f"    Exercice N-1: {ligne_n1['montant_produit']:>15,.0f}")
            print(f"    Variation:    {variation:>15,.0f} ({variation_pct:+.1f}%)")
        
        # Ajouter une ligne de total
        total_n = sum([l['montant'] for l in lignes if 'Exercice N' in l['libelle'] and 'N-1' not in l['libelle']])
        total_n1 = sum([l['montant'] for l in lignes if 'Exercice N-1' in l['libelle']])
        total_variation = total_n - total_n1
        
        lignes.append({
            'libelle': 'TOTAL - Exercice N',
            'montant': total_n,
            'mouvements_credit': 0,
            'mouvements_debit': 0
        })
        
        lignes.append({
            'libelle': 'TOTAL - Exercice N-1',
            'montant': total_n1,
            'mouvements_credit': 0,
            'mouvements_debit': 0
        })
        
        lignes.append({
            'libelle': 'TOTAL - Variation N / N-1',
            'montant': total_variation,
            'mouvements_credit': 0,
            'mouvements_debit': 0
        })
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """
        Génère le fichier HTML de la note via HTML_Generator.
        
        Cette méthode surcharge la méthode de base pour adapter la structure
        aux notes de production immobilisée (pas d'amortissements).
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        from html_generator import HTMLGenerator
        
        # Configuration des colonnes pour le HTML (structure simplifiée pour produits)
        colonnes_config = {
            'groupes': [
                {'titre': 'PRODUCTION IMMOBILISÉE', 'colonnes': ['montant', 'mouvements_credit', 'mouvements_debit']}
            ],
            'en_tetes': {
                'libelle': 'EXERCICE',
                'montant': 'Montant',
                'mouvements_credit': 'Mouvements Crédit',
                'mouvements_debit': 'Mouvements Débit'
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
        
        # Extraire les montants N et N-1 (lignes de total)
        total_rows = df[df['libelle'].str.contains('TOTAL', case=False, na=False)]
        
        if len(total_rows) >= 2:
            montant_n = total_rows.iloc[0]['montant']
            montant_n1 = total_rows.iloc[1]['montant']
            variation = montant_n - montant_n1
            
            print(f"  Production Immobilisée Exercice N:    {montant_n:>15,.0f}")
            print(f"  Production Immobilisée Exercice N-1:  {montant_n1:>15,.0f}")
            print(f"  Variation:                            {variation:>15,.0f}")
            
            if montant_n1 != 0:
                variation_pct = (variation / montant_n1) * 100
                print(f"  Variation %:                          {variation_pct:>15,.1f}%")
        
        print()


# Point d'entrée principal
if __name__ == "__main__":
    import argparse
    
    # Parser les arguments de ligne de commande
    parser = argparse.ArgumentParser(
        description='Calcul de la Note 30 - Production Immobilisée'
    )
    parser.add_argument(
        'fichier_balance',
        nargs='?',
        default='../../P000 -BALANCE DEMO N_N-1_N-2.xlsx',
        help='Chemin vers le fichier Excel des balances (N, N-1, N-2)'
    )
    parser.add_argument(
        '--output-html',
        default='../Tests/test_note_30.html',
        help='Chemin du fichier HTML de sortie (défaut: ../Tests/test_note_30.html)'
    )
    parser.add_argument(
        '--output-trace',
        default='../Tests/note_30_trace.json',
        help='Chemin du fichier de trace JSON (défaut: ../Tests/note_30_trace.json)'
    )
    
    args = parser.parse_args()
    
    # Créer le calculateur
    calculateur = CalculateurNote30(args.fichier_balance)
    
    # Exécuter le calcul complet
    calculateur.executer(
        fichier_html=args.output_html,
        fichier_trace=args.output_trace
    )
