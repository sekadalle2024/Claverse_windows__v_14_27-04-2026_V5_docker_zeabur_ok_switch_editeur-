#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de calcul de la NOTE 29 - VENTES DE PRODUITS FINIS
Syscohada Révisé

Ce script calcule la Note 29 à partir des balances N, N-1, N-2 en utilisant
l'architecture modulaire du système de calcul automatique des notes annexes.

Note: Cette note fait partie du compte de résultat (produits) et ne comporte
pas de colonnes d'amortissement. Elle présente uniquement les mouvements
de l'exercice pour les ventes de produits finis.

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


class CalculateurNote29(CalculateurNote):
    """
    Calculateur pour la Note 29 - Ventes de Produits Finis.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    de la Note 29 avec les ventes de produits finis.
    
    Mapping des comptes SYSCOHADA:
    - Comptes 701, 702, 703: Ventes de produits finis
      * 701: Ventes de produits finis
      * 702: Ventes de produits intermédiaires
      * 703: Ventes de produits résiduels
    
    Structure de la note:
    - Ventes de produits finis (exercice N)
    - Ventes de produits finis (exercice N-1)
    - Variation N / N-1
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 29.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel des balances
        """
        super().__init__(fichier_balance, "29", "VENTES DE PRODUITS FINIS")
        
        # Mapping des comptes pour la Note 29
        # Note: Pour les comptes de produits, on utilise les comptes 701, 702, 703
        self.mapping_comptes = {
            'Ventes de produits finis': {
                'comptes': ['701', '7011', '7012', '7013', '7014', '7015', '7016', '7017', '7018', '7019']
            },
            'Ventes de produits intermédiaires': {
                'comptes': ['702', '7021', '7022', '7023', '7024', '7025', '7026', '7027', '7028', '7029']
            },
            'Ventes de produits résiduels': {
                'comptes': ['703', '7031', '7032', '7033', '7034', '7035', '7036', '7037', '7038', '7039']
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
        
        Pour les comptes de produits (classe 7), on extrait:
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
        
        # Pour les comptes de produits (classe 7):
        # - Le solde créditeur représente les produits de l'exercice
        # - Les mouvements créditeurs sont les produits enregistrés
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
                    'type': 'produit',
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
        Génère la Note 29 complète avec les ventes N et N-1.
        
        Cette méthode:
        1. Calcule les ventes de produits finis pour l'exercice N
        2. Calcule les ventes de produits finis pour l'exercice N-1
        3. Calcule la variation entre N et N-1
        4. Retourne un DataFrame avec toutes les lignes
        
        Returns:
            DataFrame contenant les lignes de la note
        """
        lignes = []
        
        # Calculer pour chaque poste de ventes
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
        aux notes de produits (pas d'amortissements).
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        from html_generator import HTMLGenerator
        
        # Configuration des colonnes pour le HTML (structure simplifiée pour produits)
        colonnes_config = {
            'groupes': [
                {'titre': 'VENTES DE PRODUITS FINIS', 'colonnes': ['montant', 'mouvements_credit', 'mouvements_debit']}
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
            
            print(f"  Ventes Exercice N:    {montant_n:>15,.0f}")
            print(f"  Ventes Exercice N-1:  {montant_n1:>15,.0f}")
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
        description='Calcul de la Note 29 - Ventes de Produits Finis'
    )
    parser.add_argument(
        'fichier_balance',
        nargs='?',
        default='../../P000 -BALANCE DEMO N_N-1_N-2.xlsx',
        help='Chemin vers le fichier Excel des balances (N, N-1, N-2)'
    )
    parser.add_argument(
        '--output-html',
        default='../Tests/test_note_29.html',
        help='Chemin du fichier HTML de sortie (défaut: ../Tests/test_note_29.html)'
    )
    parser.add_argument(
        '--output-trace',
        default='../Tests/note_29_trace.json',
        help='Chemin du fichier de trace JSON (défaut: ../Tests/note_29_trace.json)'
    )
    
    args = parser.parse_args()
    
    # Créer le calculateur
    calculateur = CalculateurNote29(args.fichier_balance)
    
    # Exécuter le calcul complet
    calculateur.executer(
        fichier_html=args.output_html,
        fichier_trace=args.output_trace
    )
