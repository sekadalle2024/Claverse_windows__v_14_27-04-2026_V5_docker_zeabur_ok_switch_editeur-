"""
Calculateur Note 16 - Autres Dettes

Ce module calcule la Note 16 des annexes SYSCOHADA Révisé concernant les autres dettes.
Il traite les comptes des classes 46X et 47X.

Comptes SYSCOHADA concernés:
    - 461: Associés - Capital à rembourser
    - 462: Associés - Comptes courants
    - 463: Associés - Opérations faites en commun
    - 464: Associés - Dividendes à payer
    - 465: Associés - Créances sur cessions d'immobilisations
    - 467: Créditeurs divers
    - 471: Comptes d'attente créditeurs
    - 472: Comptes transitoires ou d'attente créditeurs
    - 475: Créances sur cessions d'immobilisations
    - 476: Charges constatées d'avance
    - 477: Produits constatés d'avance
    - 478: Écarts de conversion - Passif

Usage:
    python calculer_note_16.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote16(CalculateurNote):
    """Calculateur pour la Note 16 - Autres Dettes."""
    
    def __init__(self, fichier_balance: str):
        super().__init__(fichier_balance, "16", "Autres Dettes")
        
        self.mapping_comptes = {
            "Associés - Capital à rembourser": ["461"],
            "Associés - Comptes courants": ["462"],
            "Associés - Dividendes à payer": ["464"],
            "Créditeurs divers": ["467"],
            "Comptes d'attente créditeurs": ["471"],
            "Comptes transitoires créditeurs": ["472"]
        }
    
    def calculer_ligne_autre_dette(self, libelle: str, comptes: list) -> Dict[str, float]:
        """Calcule une ligne d'autre dette."""
        from account_extractor import AccountExtractor
        from movement_calculator import MovementCalculator
        
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        movement_calc = MovementCalculator()
        
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        solde_ouverture = soldes_n1['solde_credit']
        augmentations = soldes_n['mvt_credit']
        diminutions = soldes_n['mvt_debit']
        solde_cloture = soldes_n['solde_credit']
        
        coherent, ecart = movement_calc.verifier_coherence(
            solde_ouverture, augmentations, diminutions, solde_cloture
        )
        if not coherent:
            print(f"  ⚠ Incohérence détectée pour '{libelle}': écart de {ecart:.2f}")
        
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'autre_dette',
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
            'diminutions': diminutions,
            'solde_cloture': solde_cloture
        }
    
    def generer_note(self) -> pd.DataFrame:
        """Génère la Note 16 complète."""
        lignes = []
        
        print(f"  Calcul des autres dettes...")
        
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_autre_dette(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        df = pd.DataFrame(lignes)
        
        total = {
            'libelle': 'TOTAL AUTRES DETTES',
            'solde_ouverture': df['solde_ouverture'].sum(),
            'augmentations': df['augmentations'].sum(),
            'diminutions': df['diminutions'].sum(),
            'solde_cloture': df['solde_cloture'].sum()
        }
        
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """Génère le fichier HTML de la Note 16."""
        from html_generator import HTMLGenerator
        
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DES AUTRES DETTES', 'colonnes': ['solde_ouverture', 'augmentations', 'diminutions', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE DES DETTES',
                'solde_ouverture': 'Solde début exercice',
                'augmentations': 'Augmentations',
                'diminutions': 'Diminutions',
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
    fichier_html = tests_dir / "test_note_16.html"
    fichier_trace = tests_dir / "trace_note_16.json"
    
    calculateur = CalculateurNote16(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
