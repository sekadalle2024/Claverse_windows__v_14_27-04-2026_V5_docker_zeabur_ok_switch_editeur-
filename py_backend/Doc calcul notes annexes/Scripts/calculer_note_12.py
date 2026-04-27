"""
Calculateur Note 12 - Emprunts et Dettes Financières

Ce module calcule la Note 12 des annexes SYSCOHADA Révisé concernant les emprunts
et dettes financières. Il traite les comptes de la classe 16X.

Comptes SYSCOHADA concernés:
    - 161: Emprunts obligataires
    - 162: Emprunts auprès des établissements de crédit
    - 163: Avances reçues de l'État
    - 164: Avances reçues et comptes courants bloqués
    - 165: Dépôts et cautionnements reçus
    - 166: Intérêts courus
    - 167: Emprunts et dettes assortis de conditions particulières
    - 168: Autres emprunts et dettes

Structure de la note:
    - Solde d'ouverture
    - Augmentations (nouveaux emprunts)
    - Remboursements
    - Solde de clôture

Usage:
    python calculer_note_12.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

# Ajouter le chemin du template au PYTHONPATH
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote12(CalculateurNote):
    """
    Calculateur pour la Note 12 - Emprunts et Dettes Financières.
    
    Cette classe hérite de CalculateurNote et implémente le calcul spécifique
    des emprunts et dettes financières (comptes 16X).
    """
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur de la Note 12.
        
        Args:
            fichier_balance: Chemin vers le fichier Excel de balances
        """
        super().__init__(fichier_balance, "12", "Emprunts et Dettes Financières")
        
        # Mapping des lignes de la note aux comptes SYSCOHADA
        self.mapping_comptes = {
            "Emprunts obligataires": ["161"],
            "Emprunts auprès des établissements de crédit": ["162"],
            "Avances reçues de l'État": ["163"],
            "Avances reçues et comptes courants bloqués": ["164"],
            "Dépôts et cautionnements reçus": ["165"],
            "Intérêts courus": ["166"],
            "Emprunts et dettes assortis de conditions particulières": ["167"],
            "Autres emprunts et dettes": ["168"]
        }
    
    def calculer_ligne_emprunt(self, libelle: str, comptes: list) -> Dict[str, float]:
        """
        Calcule une ligne d'emprunt avec ses mouvements.
        
        Pour les emprunts (comptes créditeurs):
        - Solde ouverture = Solde Crédit N-1
        - Augmentations = Mouvements Crédit N (nouveaux emprunts)
        - Remboursements = Mouvements Débit N (diminutions)
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
        
        # Extraire les soldes des comptes d'emprunts
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Calculer les montants (emprunts = comptes créditeurs)
        solde_ouverture = soldes_n1['solde_credit']
        augmentations = soldes_n['mvt_credit']    # Nouveaux emprunts
        remboursements = soldes_n['mvt_debit']    # Remboursements
        solde_cloture = soldes_n['solde_credit']
        
        # Vérifier la cohérence
        coherent, ecart = movement_calc.verifier_coherence(
            solde_ouverture, augmentations, remboursements, solde_cloture
        )
        if not coherent:
            print(f"  ⚠ Incohérence détectée pour '{libelle}': écart de {ecart:.2f}")
        
        # Traçabilité
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'emprunt',
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
            'augmentations': augmentations,
            'remboursements': remboursements,
            'solde_cloture': solde_cloture
        }
    
    def generer_note(self) -> pd.DataFrame:
        """
        Génère la Note 12 complète avec toutes les lignes d'emprunts.
        
        Returns:
            pd.DataFrame: DataFrame contenant toutes les lignes et le total
        """
        lignes = []
        
        print(f"  Calcul des emprunts et dettes financières...")
        
        # Calculer chaque ligne d'emprunt
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_emprunt(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        # Créer le DataFrame
        df = pd.DataFrame(lignes)
        
        # Calculer la ligne de total
        total = {
            'libelle': 'TOTAL EMPRUNTS ET DETTES FINANCIÈRES',
            'solde_ouverture': df['solde_ouverture'].sum(),
            'augmentations': df['augmentations'].sum(),
            'remboursements': df['remboursements'].sum(),
            'solde_cloture': df['solde_cloture'].sum()
        }
        
        # Ajouter le total au DataFrame
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """
        Génère le fichier HTML de la Note 12.
        
        Args:
            df: DataFrame contenant les données de la note
            
        Returns:
            str: Code HTML complet de la note
        """
        from html_generator import HTMLGenerator
        
        # Configuration des colonnes pour le HTML
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DES EMPRUNTS', 'colonnes': ['solde_ouverture', 'augmentations', 'remboursements', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE DES EMPRUNTS',
                'solde_ouverture': 'Solde début exercice',
                'augmentations': 'Nouveaux emprunts',
                'remboursements': 'Remboursements',
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
    fichier_html = tests_dir / "test_note_12.html"
    fichier_trace = tests_dir / "trace_note_12.json"
    
    # Créer et exécuter le calculateur
    calculateur = CalculateurNote12(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
