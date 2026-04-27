"""
Calculateur Note 18 - Charges Constatées d'Avance

Ce module calcule la Note 18 des annexes SYSCOHADA Révisé concernant les charges constatées d'avance.
Il traite le compte 476 (Charges constatées d'avance).

Comptes SYSCOHADA concernés:
    - 476: Charges constatées d'avance

Usage:
    python calculer_note_18.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote18(CalculateurNote):
    """Calculateur pour la Note 18 - Charges Constatées d'Avance."""
    
    def __init__(self, fichier_balance: str):
        super().__init__(fichier_balance, "18", "Charges Constatées d'Avance")
        
        self.mapping_comptes = {
            "Charges constatées d'avance": ["476"]
        }
    
    def calculer_ligne_charges_avance(self, libelle: str, comptes: list) -> Dict[str, float]:
        """Calcule une ligne de charges constatées d'avance."""
        from account_extractor import AccountExtractor
        from movement_calculator import MovementCalculator
        
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        movement_calc = MovementCalculator()
        
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Pour les charges constatées d'avance (compte d'actif), on utilise les soldes débiteurs
        solde_ouverture = soldes_n1['solde_debit']
        augmentations = soldes_n['mvt_debit']
        diminutions = soldes_n['mvt_credit']
        solde_cloture = soldes_n['solde_debit']
        
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
                'type': 'charges_avance',
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
        """Génère la Note 18 complète."""
        lignes = []
        
        print(f"  Calcul des charges constatées d'avance...")
        
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_charges_avance(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        df = pd.DataFrame(lignes)
        
        # Pas de ligne de total pour une seule ligne
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """Génère le fichier HTML de la Note 18."""
        from html_generator import HTMLGenerator
        
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DES CHARGES CONSTATÉES D\'AVANCE', 'colonnes': ['solde_ouverture', 'augmentations', 'diminutions', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE',
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
    fichier_html = tests_dir / "test_note_18.html"
    fichier_trace = tests_dir / "trace_note_18.json"
    
    calculateur = CalculateurNote18(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
