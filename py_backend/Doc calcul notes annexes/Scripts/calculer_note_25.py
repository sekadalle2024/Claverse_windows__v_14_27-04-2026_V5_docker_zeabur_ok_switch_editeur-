#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Calculateur Note 25 - Charges de Personnel
Génère la note annexe 25 pour les charges de personnel (comptes 66X)
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier Modules au path
modules_path = Path(__file__).parent.parent / "Modules"
sys.path.insert(0, str(modules_path))

from balance_reader import BalanceReader
from account_extractor import AccountExtractor
from movement_calculator import MovementCalculator
from html_generator import HTMLGenerator


class CalculateurNote25:
    """Calculateur pour la Note 25 - Charges de Personnel"""
    
    def __init__(self, fichier_balance: str):
        """
        Initialise le calculateur
        
        Args:
            fichier_balance: Chemin vers le fichier Excel de balances
        """
        self.fichier_balance = fichier_balance
        self.balance_n = None
        self.balance_n1 = None
        self.balance_n2 = None
        
        # Mapping des comptes pour les charges de personnel (66X)
        self.mapping_comptes = {
            "Salaires et traitements": {
                "comptes": ["661"]
            },
            "Primes et gratifications": {
                "comptes": ["662"]
            },
            "Congés payés": {
                "comptes": ["663"]
            },
            "Indemnités de préavis et de licenciement": {
                "comptes": ["664"]
            },
            "Charges sociales": {
                "comptes": ["665", "666", "667", "668"]
            },
            "Autres charges de personnel": {
                "comptes": ["669"]
            }
        }
    
    def charger_balances(self) -> bool:
        """
        Charge les balances des 3 exercices
        
        Returns:
            True si le chargement a réussi, False sinon
        """
        try:
            print("📂 Chargement des balances...")
            reader = BalanceReader(self.fichier_balance)
            self.balance_n, self.balance_n1, self.balance_n2 = reader.charger_balances()
            print("✓ Balances chargées avec succès")
            return True
        except Exception as e:
            print(f"✗ Erreur lors du chargement des balances: {e}")
            return False
    
    def calculer_ligne_note(self, libelle: str, comptes: list) -> dict:
        """
        Calcule une ligne de la note
        
        Args:
            libelle: Libellé de la ligne
            comptes: Liste des racines de comptes
            
        Returns:
            Dictionnaire avec les valeurs calculées
        """
        # Extraction des comptes pour N et N-1
        extractor_n = AccountExtractor(self.balance_n)
        extractor_n1 = AccountExtractor(self.balance_n1)
        
        # Extraire les soldes pour les comptes multiples
        soldes_n = extractor_n.extraire_comptes_multiples(comptes)
        soldes_n1 = extractor_n1.extraire_comptes_multiples(comptes)
        
        # Calculer les montants
        calculator = MovementCalculator()
        
        # Pour les charges, on utilise le solde débiteur (les charges sont au débit)
        montant_n = soldes_n['solde_debit'] - soldes_n['solde_credit']
        montant_n1 = soldes_n1['solde_debit'] - soldes_n1['solde_credit']
        
        return {
            'libelle': libelle,
            'montant_n': montant_n,
            'montant_n1': montant_n1
        }
    
    def generer_note(self) -> list:
        """
        Génère la note complète avec toutes les lignes
        
        Returns:
            Liste de dictionnaires représentant les lignes de la note
        """
        print("\n📊 Calcul de la Note 25 - Charges de Personnel...")
        
        lignes = []
        total_n = 0
        total_n1 = 0
        
        # Calculer chaque ligne
        for libelle, config in self.mapping_comptes.items():
            print(f"  Calcul: {libelle}...")
            ligne = self.calculer_ligne_note(libelle, config['comptes'])
            lignes.append(ligne)
            total_n += ligne['montant_n']
            total_n1 += ligne['montant_n1']
        
        # Ajouter la ligne de total
        lignes.append({
            'libelle': 'TOTAL CHARGES DE PERSONNEL',
            'montant_n': total_n,
            'montant_n1': total_n1
        })
        
        print(f"✓ Note 25 calculée: {len(lignes)-1} lignes + total")
        return lignes
    
    def generer_html(self, lignes: list) -> str:
        """
        Génère le HTML de la note
        
        Args:
            lignes: Liste des lignes de la note
            
        Returns:
            Code HTML
        """
        print("\n🎨 Génération du HTML...")
        
        # Configuration des colonnes
        colonnes_config = {
            'titre': 'NOTE 25 - CHARGES DE PERSONNEL',
            'colonnes': [
                {'nom': 'Libellé', 'largeur': '60%'},
                {'nom': 'Exercice N', 'largeur': '20%'},
                {'nom': 'Exercice N-1', 'largeur': '20%'}
            ]
        }
        
        # Créer le générateur HTML
        generator = HTMLGenerator(
            titre_note="NOTE 25 - CHARGES DE PERSONNEL",
            numero_note="25"
        )
        
        # Construire le tableau HTML
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{colonnes_config['titre']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #2980b9;
        }}
        td {{
            padding: 10px;
            border: 1px solid #ddd;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #f0f0f0;
        }}
        .montant {{
            text-align: right;
            font-family: 'Courier New', monospace;
        }}
        .total {{
            font-weight: bold;
            background-color: #e8f4f8 !important;
        }}
        .total td {{
            border-top: 2px solid #3498db;
            padding-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{colonnes_config['titre']}</h1>
        <table>
            <thead>
                <tr>
"""
        
        # Ajouter les en-têtes
        for col in colonnes_config['colonnes']:
            html += f"                    <th style='width: {col['largeur']}'>{col['nom']}</th>\n"
        
        html += """                </tr>
            </thead>
            <tbody>
"""
        
        # Ajouter les lignes
        for ligne in lignes:
            is_total = 'TOTAL' in ligne['libelle']
            row_class = ' class="total"' if is_total else ''
            
            html += f"                <tr{row_class}>\n"
            html += f"                    <td>{ligne['libelle']}</td>\n"
            html += f"                    <td class='montant'>{generator.formater_montant(ligne['montant_n'])}</td>\n"
            html += f"                    <td class='montant'>{generator.formater_montant(ligne['montant_n1'])}</td>\n"
            html += "                </tr>\n"
        
        html += """            </tbody>
        </table>
    </div>
</body>
</html>"""
        
        print("✓ HTML généré")
        return html
    
    def sauvegarder_html(self, html: str, fichier_sortie: str):
        """
        Sauvegarde le HTML dans un fichier
        
        Args:
            html: Code HTML
            fichier_sortie: Chemin du fichier de sortie
        """
        try:
            with open(fichier_sortie, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"✓ Fichier sauvegardé: {fichier_sortie}")
        except Exception as e:
            print(f"✗ Erreur lors de la sauvegarde: {e}")


def main():
    """Fonction principale"""
    print("=" * 70)
    print("CALCULATEUR NOTE 25 - CHARGES DE PERSONNEL")
    print("=" * 70)
    
    # Chemins des fichiers
    script_dir = Path(__file__).parent
    balance_file = script_dir.parent.parent.parent / "P000 -BALANCE DEMO N_N-1_N-2.xlsx"
    output_file = script_dir.parent / "Tests" / "test_note_25.html"
    
    # Créer le dossier Tests s'il n'existe pas
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📁 Fichier balance: {balance_file}")
    print(f"📁 Fichier sortie: {output_file}")
    
    # Vérifier que le fichier de balance existe
    if not balance_file.exists():
        print(f"\n✗ ERREUR: Fichier de balance introuvable: {balance_file}")
        return
    
    # Créer le calculateur
    calculateur = CalculateurNote25(str(balance_file))
    
    # Charger les balances
    if not calculateur.charger_balances():
        return
    
    # Générer la note
    lignes = calculateur.generer_note()
    
    # Générer le HTML
    html = calculateur.generer_html(lignes)
    
    # Sauvegarder
    calculateur.sauvegarder_html(html, str(output_file))
    
    print("\n" + "=" * 70)
    print("✓ TRAITEMENT TERMINÉ AVEC SUCCÈS")
    print("=" * 70)
    print(f"\n📄 Ouvrez le fichier dans votre navigateur:")
    print(f"   {output_file.absolute()}")


if __name__ == "__main__":
    main()
