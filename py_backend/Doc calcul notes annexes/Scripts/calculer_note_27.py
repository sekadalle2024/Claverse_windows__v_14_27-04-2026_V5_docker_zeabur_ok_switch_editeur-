#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculateur pour Note 27 - Dotations aux Provisions (SYSCOHADA)

Cette note présente les dotations aux provisions de l'exercice.

Structure:
- Dotations aux provisions pour risques et charges
- Dotations aux provisions pour dépréciation des immobilisations
- Dotations aux provisions pour dépréciation des stocks
- Dotations aux provisions pour dépréciation des créances
- Total des dotations aux provisions

Comptes concernés:
- 6911: Dotations aux provisions pour risques et charges
- 6912: Dotations aux provisions pour dépréciation des immobilisations
- 6913: Dotations aux provisions pour dépréciation des stocks
- 6914: Dotations aux provisions pour dépréciation des créances
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Any

# Ajouter le chemin du module parent
module_path = Path(__file__).resolve().parent.parent / "Modules"
sys.path.insert(0, str(module_path))

from balance_reader import BalanceReader
from account_extractor import AccountExtractor
from mapping_manager import MappingManager
from html_generator import HTMLGenerator
from excel_exporter import ExcelExporter
from trace_manager import TraceManager


class CalculateurNote27:
    """
    Calculateur pour la Note 27 - Dotations aux Provisions.
    """

    # Mapping des comptes pour Note 27
    MAPPING_COMPTES = {
        "dotations_risques_charges": ["6911"],
        "dotations_depreciation_immobilisations": ["6912"],
        "dotations_depreciation_stocks": ["6913"],
        "dotations_depreciation_creances": ["6914"]
    }

    def __init__(self, balance_file: str, exercice_n: str, exercice_n1: str):
        """
        Initialise le calculateur.

        Args:
            balance_file: Chemin vers le fichier de balance
            exercice_n: Libellé de l'exercice N
            exercice_n1: Libellé de l'exercice N-1
        """
        self.balance_reader = BalanceReader(balance_file)
        self.account_extractor = AccountExtractor(self.balance_reader)
        self.mapping_manager = MappingManager(self.MAPPING_COMPTES)
        self.html_generator = HTMLGenerator()
        self.excel_exporter = ExcelExporter()
        self.trace_manager = TraceManager()
        self.exercice_n = exercice_n
        self.exercice_n1 = exercice_n1

    def calculer(self) -> Dict[str, Any]:
        """
        Calcule les dotations aux provisions.

        Returns:
            Dictionnaire contenant les données calculées
        """
        # Extraire les comptes
        comptes_data = self.account_extractor.extraire_comptes(
            list(self.mapping_manager.get_all_accounts())
        )

        # Calculer les dotations par catégorie
        dotations_risques_n = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_risques_charges"], "N"
        )
        dotations_risques_n1 = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_risques_charges"], "N-1"
        )

        dotations_immob_n = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_immobilisations"], "N"
        )
        dotations_immob_n1 = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_immobilisations"], "N-1"
        )

        dotations_stocks_n = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_stocks"], "N"
        )
        dotations_stocks_n1 = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_stocks"], "N-1"
        )

        dotations_creances_n = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_creances"], "N"
        )
        dotations_creances_n1 = self._calculer_solde(
            comptes_data, self.MAPPING_COMPTES["dotations_depreciation_creances"], "N-1"
        )

        # Calculer le total
        total_n = (dotations_risques_n + dotations_immob_n + 
                   dotations_stocks_n + dotations_creances_n)
        total_n1 = (dotations_risques_n1 + dotations_immob_n1 + 
                    dotations_stocks_n1 + dotations_creances_n1)

        # Tracer les calculs
        self.trace_manager.add_trace(
            "Note 27",
            "Dotations risques et charges N",
            dotations_risques_n,
            f"Somme des comptes {self.MAPPING_COMPTES['dotations_risques_charges']}"
        )
        self.trace_manager.add_trace(
            "Note 27",
            "Dotations dépréciation immobilisations N",
            dotations_immob_n,
            f"Somme des comptes {self.MAPPING_COMPTES['dotations_depreciation_immobilisations']}"
        )
        self.trace_manager.add_trace(
            "Note 27",
            "Dotations dépréciation stocks N",
            dotations_stocks_n,
            f"Somme des comptes {self.MAPPING_COMPTES['dotations_depreciation_stocks']}"
        )
        self.trace_manager.add_trace(
            "Note 27",
            "Dotations dépréciation créances N",
            dotations_creances_n,
            f"Somme des comptes {self.MAPPING_COMPTES['dotations_depreciation_creances']}"
        )
        self.trace_manager.add_trace(
            "Note 27",
            "Total dotations provisions N",
            total_n,
            "Somme de toutes les dotations aux provisions"
        )

        # Construire le résultat
        resultat = {
            "note": "Note 27",
            "titre": "Dotations aux Provisions",
            "exercice_n": self.exercice_n,
            "exercice_n1": self.exercice_n1,
            "lignes": [
                {
                    "libelle": "Dotations aux provisions pour risques et charges",
                    "n": dotations_risques_n,
                    "n1": dotations_risques_n1,
                    "comptes": self.MAPPING_COMPTES["dotations_risques_charges"]
                },
                {
                    "libelle": "Dotations aux provisions pour dépréciation des immobilisations",
                    "n": dotations_immob_n,
                    "n1": dotations_immob_n1,
                    "comptes": self.MAPPING_COMPTES["dotations_depreciation_immobilisations"]
                },
                {
                    "libelle": "Dotations aux provisions pour dépréciation des stocks",
                    "n": dotations_stocks_n,
                    "n1": dotations_stocks_n1,
                    "comptes": self.MAPPING_COMPTES["dotations_depreciation_stocks"]
                },
                {
                    "libelle": "Dotations aux provisions pour dépréciation des créances",
                    "n": dotations_creances_n,
                    "n1": dotations_creances_n1,
                    "comptes": self.MAPPING_COMPTES["dotations_depreciation_creances"]
                },
                {
                    "libelle": "Total des dotations aux provisions",
                    "n": total_n,
                    "n1": total_n1,
                    "total": True
                }
            ],
            "traces": self.trace_manager.get_all_traces()
        }

        return resultat

    def _calculer_solde(self, comptes_data: Dict, comptes: List[str], periode: str) -> float:
        """
        Calcule le solde pour une liste de comptes.

        Args:
            comptes_data: Données des comptes
            comptes: Liste des comptes
            periode: 'N' ou 'N-1'

        Returns:
            Solde calculé
        """
        solde = 0.0
        for compte in comptes:
            if compte in comptes_data:
                if periode == "N":
                    # Pour les charges, on prend le solde débiteur
                    solde += comptes_data[compte].get("solde_debiteur_n", 0.0)
                else:
                    solde += comptes_data[compte].get("solde_debiteur_n1", 0.0)
        return solde

    def generer_html(self, data: Dict[str, Any]) -> str:
        """
        Génère le HTML pour la note.

        Args:
            data: Données calculées

        Returns:
            Code HTML
        """
        return self.html_generator.generer_note_standard(data)

    def exporter_excel(self, data: Dict[str, Any], output_file: str):
        """
        Exporte les données vers Excel.

        Args:
            data: Données calculées
            output_file: Chemin du fichier de sortie
        """
        self.excel_exporter.exporter_note(data, output_file)


def main():
    """
    Fonction principale pour tester le calculateur.
    """
    # Exemple d'utilisation
    balance_file = "chemin/vers/balance.xlsx"
    exercice_n = "2024"
    exercice_n1 = "2023"

    calculateur = CalculateurNote27(balance_file, exercice_n, exercice_n1)
    resultat = calculateur.calculer()

    # Afficher le résultat
    print(f"\n{resultat['titre']}")
    print("=" * 80)
    for ligne in resultat["lignes"]:
        print(f"{ligne['libelle']:60} {ligne['n']:>15,.2f} {ligne['n1']:>15,.2f}")

    # Générer HTML
    html = calculateur.generer_html(resultat)
    print("\nHTML généré avec succès")

    # Exporter vers Excel
    # calculateur.exporter_excel(resultat, "note_27.xlsx")
    # print("Export Excel réussi")


if __name__ == "__main__":
    main()
