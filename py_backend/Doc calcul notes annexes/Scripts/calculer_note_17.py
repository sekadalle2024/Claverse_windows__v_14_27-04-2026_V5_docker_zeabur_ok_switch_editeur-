"""
Calculateur Note 17 - Trésorerie Passif

Ce module calcule la Note 17 des annexes SYSCOHADA Révisé concernant la trésorerie passif.
Il traite les comptes des classes 52X et 56X (découverts bancaires et concours bancaires).

Comptes SYSCOHADA concernés:
    - 521: Crédits de trésorerie
    - 525: Crédits d'escompte
    - 526: Crédits de campagne
    - 527: Autres crédits de trésorerie
    - 561: Banques - Découverts
    - 564: Banques - Intérêts courus
    - 565: Escomptes de crédits ordinaires
    - 566: Escomptes de crédits de campagne

Usage:
    python calculer_note_17.py
"""

import sys
from pathlib import Path
from typing import Dict
import pandas as pd

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from calculateur_note_template import CalculateurNote


class CalculateurNote17(CalculateurNote):
    """Calculateur pour la Note 17 - Trésorerie Passif."""
    
    def __init__(self, fichier_balance: str):
        super().__init__(fichier_balance, "17", "Trésorerie Passif")
        
        self.mapping_comptes = {
            "Crédits de trésorerie": ["521"],
            "Crédits d'escompte": ["525"],
            "Crédits de campagne": ["526"],
            "Autres crédits de trésorerie": ["527"],
            "Banques - Découverts": ["561"],
            "Banques - Intérêts courus": ["564"],
            "Escomptes de crédits ordinaires": ["565"],
            "Escomptes de crédits de campagne": ["566"]
        }
    
    def calculer_ligne_tresorerie_passif(self, libelle: str, comptes: list) -> Dict[str, float]:
        """Calcule une ligne de trésorerie passif."""
        from account_extractor import AccountExtractor
        from movement_calculator import MovementCalculator
        
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        movement_calc = MovementCalculator()
        
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        solde_ouverture = soldes_n1['solde_credit']
        augmentations = soldes_n['mvt_credit']
        remboursements = soldes_n['mvt_debit']
        solde_cloture = soldes_n['solde_credit']
        
        coherent, ecart = movement_calc.verifier_coherence(
            solde_ouverture, augmentations, remboursements, solde_cloture
        )
        if not coherent:
            print(f"  ⚠ Incohérence détectée pour '{libelle}': écart de {ecart:.2f}")
        
        comptes_sources = []
        for compte in comptes:
            solde = extractor_n.extraire_solde_compte(compte)
            comptes_sources.append({
                'compte': compte,
                'type': 'tresorerie_passif',
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
        """Génère la Note 17 complète."""
        lignes = []
        
        print(f"  Calcul de la trésorerie passif...")
        
        for libelle, comptes in self.mapping_comptes.items():
            ligne = self.calculer_ligne_tresorerie_passif(libelle, comptes)
            lignes.append(ligne)
            print(f"    ✓ {libelle}: {ligne['solde_cloture']:,.0f}")
        
        df = pd.DataFrame(lignes)
        
        total = {
            'libelle': 'TOTAL TRÉSORERIE PASSIF',
            'solde_ouverture': df['solde_ouverture'].sum(),
            'augmentations': df['augmentations'].sum(),
            'remboursements': df['remboursements'].sum(),
            'solde_cloture': df['solde_cloture'].sum()
        }
        
        df = pd.concat([df, pd.DataFrame([total])], ignore_index=True)
        
        return df
    
    def generer_html(self, df: pd.DataFrame) -> str:
        """Génère le fichier HTML de la Note 17."""
        from html_generator import HTMLGenerator
        
        colonnes_config = {
            'groupes': [
                {'titre': 'MOUVEMENTS DE LA TRÉSORERIE PASSIF', 'colonnes': ['solde_ouverture', 'augmentations', 'remboursements', 'solde_cloture']}
            ],
            'en_tetes': {
                'libelle': 'NATURE',
                'solde_ouverture': 'Solde début exercice',
                'augmentations': 'Nouveaux concours',
                'remboursements': 'Remboursements',
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
    fichier_html = tests_dir / "test_note_17.html"
    fichier_trace = tests_dir / "trace_note_17.json"
    
    calculateur = CalculateurNote17(str(fichier_balance))
    calculateur.executer(
        fichier_html=str(fichier_html),
        fichier_trace=str(fichier_trace)
    )


if __name__ == "__main__":
    main()
