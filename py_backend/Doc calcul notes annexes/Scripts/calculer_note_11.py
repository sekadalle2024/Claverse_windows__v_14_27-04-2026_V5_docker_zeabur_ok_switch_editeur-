"""
Calculateur Note 11 - Provisions

Ce module calcule la Note 11 des annexes SYSCOHADA Révisé concernant les provisions.
Il traite les comptes de la classe 19X (provisions pour risques et charges).

Comptes SYSCOHADA concernés:
    - 191: Provisions pour litiges
    - 192: Provisions pour garanties données aux clients
    - 193: Provisions pour pertes sur marchés
    - 194: Provisions pour pertes de change
    - 195: Provisions pour impôts
    - 196: Provisions pour pensions et obligations similaires
    - 197: Provisions pour restructurations
    - 198: Autres provisions pour risques et charges

Structure de la note:
    - Solde d'ouverture
    - Dotations de l'exercice
    - Reprises de l'exercice
    - Solde de clôture

Usage:
    python calculer_note_11.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

# Ajouter le chemin du template au PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote11(CalculateurNote):
    """
    Calculateur pour la Note 11 - Provisions.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    des provisions (comptes 19X). Les provisions sont des passifs dont l'échéance
    ou le montant est incertain.
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 11.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel de balances
        """
        super().__init__(fichier_balance, "11", "Provisions pour Risques et Charges")
        
        # Mapping des lignes de la note aux comptes SYSCOHADA
        self.mapping_comptes = {
            "Provisions pour litiges": ["191"],
            "Provisions pour garanties données aux clients": ["192"],
            "Provisions pour pertes sur marchés": ["193"],
            "Provisions pour pertes de change": ["194"],
            "Provisions pour impôts": ["195"],
            "Provisions pour pensions et obligations similaires": ["196"],
            "Provisions pour restructurations": ["197"],
            "Autres provisions pour risques et charges": ["198"]
        }
    
    def calculer_ligne_provision(self, libelle: str, comptes: list) -> Dict[str, float]:
        """
        Calcule une ligne de provision avec ses mouvements.
        
        Pour les provisions (comptes créditeurs):
        - Solde ouverture = Solde Crédit N-1
        - Dotations = Mouvements Crédit N (augmentations)
        - Reprises = Mouvements Débit N (diminutions)
        - Solde clôture = Solde Crédit N
        
        Args:
            libelle: Libellé de la ligne
            comptes: Liste des racines de comptes
            
        Returns:
            Dict contenant les 4 colonnes calculées
        """
        from account_extractor import AccountExtractor
        from movement_calculator import MovementCalculator
        
        # Extracteurs pour chaque exercice
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        
        # Calculateur de mouvements
        movement_calc = MovementCalculator()
        
        # Extraire les soldes des comptes de provisions
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Calculer les montants (provisions = comptes créditeurs)
        solde_ouverture = soldes_n1['solde_credit']
        dotations = soldes_n['mvt_credit']  # Augmentations
        reprises = soldes_n['mvt_debit']    # Diminutions
        solde_cloture = soldes_n['solde_credit']
        
        # Vérifier la cohérence: Solde clôture = Solde ouverture + Dotations - Reprises
        coherent, ecart = movement_calc.verifier_coherence(
            solde_ouverture, dotations, reprises, solde_cloture
        )
        if not coherent:
            print(f"  ⚠ Incohérence détectée pour '{libelle}': écart de {ecart:.2f}")
        
        # Traçabilité
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'provision',
                'solde_debit_n': solde['solde_debit'],
                'solde_credit_n': solde['solde_credit']
            })
        
        self.trace_manager.enregistrer_calcul(
            libelle=libelle,
            montant=solde_cloture,
            comptes_sources=comptes_sources
        )
        
        return {
            'libelle': libelle,
            'solde_ouverture': solde_ouverture,
            'dotations': dotations,
            'reprises': reprises,
            'solde_cloture': solde_cloture
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 11 complète avec toutes les lignes de provisions.
        
        Returns:
            pd.DataFrame: DataFrame contenant toutes les lignes et le total
        """
        lignes = []
        
        print(f"  Calcul des provisions...")
        
        # Calculer chaque ligne de provision
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_provision(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        # Calculer la ligne de total
        total = {
            'libelle': 'TOTAL PROVISIONS',
            'solde_ouverture': df['solde_ouverture'].sum(),
            'dotations': df['dotations'].sum(),
            'reprises': df['reprises'].sum(),
            'solde_cloture': df['solde_cloture'].sum()
        }
        
        # Ajouter le total au DataFrame
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """
        Génère le fichier HTML de la Note 11.
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        from html_generator import HTMLGenerator
        
        # Configuration des colonnes pour le HTML
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DES PROVISIONS', 'colonnes': ['solde_ouverture', 'dotations', 'reprises', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE DES PROVISIONS',
                'solde_ouverture': 'Solde début exercice',
                'dotations': 'Dotations',
                'reprises': 'Reprises',
                'solde_cloture': 'Solde fin exercice'
            }
        }
        
        generator = HTMLGenerator(self.titre_note, self.numero_note)
        html = generator.generer_html(df, colonnes_config)
        
        return html


def main():
    """Point d'entrée principal du script."""
    # Chemin vers le fichier de balance (relatif au script)
    script_dir = Path(__file__).parent
    fichier_balance = script_dir.parent.parent.parent / "P000 -BALANCE DEMO N_N-1_N-2.xlsx"
    
    # Chemins de sortie
    tests_dir = script_dir.parent / "Tests"
    fichier_html = tests_dir / "test_note_11.html"
    fichier_trace = tests_dir / "trace_note_11.json"
    
    # Créer et exécuter le calculateur
    calculateur = CalculateurNote11(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
