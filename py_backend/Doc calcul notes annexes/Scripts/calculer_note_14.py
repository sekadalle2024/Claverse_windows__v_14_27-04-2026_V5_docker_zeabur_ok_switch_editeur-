"""
Calculateur Note 14 - Dettes Fiscales

Ce module calcule la Note 14 des annexes SYSCOHADA Révisé concernant les dettes
fiscales. Il traite les comptes de la classe 44X.

Comptes SYSCOHADA concernés:
    - 441: État et autres collectivités publiques - Subventions à recevoir
    - 442: État - Impôts et taxes recouvrables sur des tiers
    - 443: Opérations particulières avec l'État
    - 444: État - Impôts sur les résultats
    - 445: État - Taxes sur le chiffre d'affaires
    - 446: État - Autres impôts et taxes
    - 447: État - Charges à payer et produits à recevoir
    - 448: État - Charges à payer et produits à recevoir (hors taxes)
    - 449: État - Créances et dettes diverses

Usage:
    python calculer_note_14.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote14(CalculateurNote):
    """Calculateur pour la Note 14 - Dettes Fiscales."""
    
    def __init__(self, fichier_balance: str):
        super().__init__(fichier_balance, "14", "Dettes Fiscales")
        
        self.mapping_comptes = {
            "État - Impôts sur les résultats": ["444"],
            "État - Taxes sur le chiffre d'affaires": ["445"],
            "État - Autres impôts et taxes": ["446"],
            "État - Charges à payer et produits à recevoir": ["447"],
            "État - Créances et dettes diverses": ["449"]
        }
    
    def calculer_ligne_dette_fiscale(self, libelle: str, comptes: list) -> Dict[str, float]:
        """Calcule une ligne de dette fiscale."""
        from account_extractor import AccountExtractor
        from movement_calculator import MovementCalculator
        
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        movement_calc = MovementCalculator()
        
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Dettes fiscales = comptes créditeurs
        solde_ouverture = soldes_n1['solde_credit']
        augmentations = soldes_n['mvt_credit']
        reglements = soldes_n['mvt_debit']
        solde_cloture = soldes_n['solde_credit']
        
        coherent, ecart = movement_calc.verifier_coherence(
            solde_ouverture, augmentations, reglements, solde_cloture
        )
        if not coherent:
            print(f"  ⚠ Incohérence détectée pour '{libelle}': écart de {ecart:.2f}")
        
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'dette_fiscale',
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
            'reglements': reglements,
            'solde_cloture': solde_cloture
        }
    
    def generer_note(self) -> pd.DataFrame:
        """Génère la Note 14 complète."""
        lignes = []
        
        print(f"  Calcul des dettes fiscales...")
        
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_dette_fiscale(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        df = pd.DataFrame(lignes)
        
        total = {
            'libelle': 'TOTAL DETTES FISCALES',
            'solde_ouverture': df['solde_ouverture'].sum(),
            'augmentations': df['augmentations'].sum(),
            'reglements': df['reglements'].sum(),
            'solde_cloture': df['solde_cloture'].sum()
        }
        
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """Génère le fichier HTML de la Note 14."""
        from html_generator import HTMLGenerator
        
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DES DETTES FISCALES', 'colonnes': ['solde_ouverture', 'augmentations', 'reglements', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE DES DETTES',
                'solde_ouverture': 'Solde début exercice',
                'augmentations': 'Nouvelles dettes',
                'reglements': 'Règlements',
                'solde_cloture': 'Solde fin exercice'
            }
        }
        
        generator = HTMLGenerator(self.titre_note, self.numero_note)
        html = generator.generer_html(df, colonnes_config)
        
        return html


def main():
    """Point d'entrée principal du script."""
    script_dir = Path(__file__).parent
    fichier_balance = script_dir.parent.parent.parent / "P000 -BALANCE DEMO N_N-1_N-2.xlsx"
    
    tests_dir = script_dir.parent / "Tests"
    fichier_html = tests_dir / "test_note_14.html"
    fichier_trace = tests_dir / "trace_note_14.json"
    
    calculateur = CalculateurNote14(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
