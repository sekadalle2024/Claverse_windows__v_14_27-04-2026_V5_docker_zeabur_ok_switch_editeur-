"""
Test de propriété pour la formule de calcul des VNC.

Property 9: VNC Calculation Formula
Valide les exigences: 4.1, 4.2, 4.6

Pour toute ligne d'immobilisation, le VNC_Calculator doit calculer:
- VNC_Ouverture = Brut_Ouverture - Amortissement_Ouverture
- VNC_Cloture = Brut_Cloture - Amortissement_Cloture
- Les deux VNC doivent être non-négatives
"""

import pytest
from hypothesis import given, assume, strategies as st
from hypothesis import settings
import pandas as pd

from Modules.vnc_calculator import VNCCalculator


# ============================================================================
# STRATÉGIES HYPOTHESIS POUR LES TESTS VNC
# ============================================================================

@st.composite
def st_immobilisation_valide(draw):
    """
    Génère une ligne d'immobilisation avec VNC valides (>= 0).
    
    Cette stratégie garantit que:
    - Brut >= Amortissement (pour VNC >= 0)
    - Tous les montants sont positifs
    """
    # Générer les valeurs brutes
    brut_ouverture = draw(st.floats(
        min_value=0,
        max_value=100000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    brut_cloture = draw(st.floats(
        min_value=0,
        max_value=100000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    # Générer les amortissements (toujours <= brut pour VNC >= 0)
    amort_ouverture = draw(st.floats(
        min_value=0,
        max_value=brut_ouverture,
        allow_nan=False,
        allow_infinity=False
    ))
    
    amort_cloture = draw(st.floats(
        min_value=0,
        max_value=brut_cloture,
        allow_nan=False,
        allow_infinity=False
    ))
    
    return {
        'brut_ouverture': brut_ouverture,
        'brut_cloture': brut_cloture,
        'amort_ouverture': amort_ouverture,
        'amort_cloture': amort_cloture
    }


@st.composite
def st_immobilisation_vnc_negative(draw):
    """
    Génère une ligne d'immobilisation avec VNC négative (cas anormal).
    
    Cette stratégie génère intentionnellement des cas où:
    - Amortissement > Brut (VNC < 0)
    """
    # Générer les valeurs brutes
    brut_ouverture = draw(st.floats(
        min_value=0,
        max_value=100000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    brut_cloture = draw(st.floats(
        min_value=0,
        max_value=100000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    # Générer les amortissements (> brut pour VNC < 0)
    # Ajouter au moins 1000 pour garantir une VNC négative significative
    amort_ouverture = draw(st.floats(
        min_value=brut_ouverture + 1000,
        max_value=brut_ouverture + 50000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    amort_cloture = draw(st.floats(
        min_value=brut_cloture + 1000,
        max_value=brut_cloture + 50000000,
        allow_nan=False,
        allow_infinity=False
    ))
    
    return {
        'brut_ouverture': brut_ouverture,
        'brut_cloture': brut_cloture,
        'amort_ouverture': amort_ouverture,
        'amort_cloture': amort_cloture
    }


@st.composite
def st_balance_avec_immobilisations(draw):
    """
    Génère une balance contenant des comptes d'immobilisations.
    
    Cette stratégie crée une balance avec:
    - Des comptes de brut (classe 2X)
    - Des comptes d'amortissement (classe 28X, 29X)
    """
    # Générer le numéro de compte de brut
    classe_brut = draw(st.sampled_from(['21', '22', '23', '24', '25', '26', '27']))
    sous_classe = draw(st.integers(min_value=0, max_value=9))
    numero_brut = f"{classe_brut}{sous_classe}"
    
    # Générer le numéro de compte d'amortissement correspondant
    numero_amort = f"28{sous_classe}"
    
    # Générer les montants
    immob = draw(st_immobilisation_valide())
    
    # Calculer les mouvements cohérents
    mvt_brut_debit = immob['brut_cloture'] - immob['brut_ouverture']
    mvt_brut_credit = 0.0
    if mvt_brut_debit < 0:
        mvt_brut_credit = -mvt_brut_debit
        mvt_brut_debit = 0.0
    
    mvt_amort_credit = immob['amort_cloture'] - immob['amort_ouverture']
    mvt_amort_debit = 0.0
    if mvt_amort_credit < 0:
        mvt_amort_debit = -mvt_amort_credit
        mvt_amort_credit = 0.0
    
    comptes = [
        {
            'Numéro': numero_brut,
            'Intitulé': f"Immobilisation {numero_brut}",
            'Ant Débit': immob['brut_ouverture'],
            'Ant Crédit': 0.0,
            'Débit': mvt_brut_debit,
            'Crédit': mvt_brut_credit,
            'Solde Débit': immob['brut_cloture'],
            'Solde Crédit': 0.0
        },
        {
            'Numéro': numero_amort,
            'Intitulé': f"Amortissement {numero_amort}",
            'Ant Débit': 0.0,
            'Ant Crédit': immob['amort_ouverture'],
            'Débit': mvt_amort_debit,
            'Crédit': mvt_amort_credit,
            'Solde Débit': 0.0,
            'Solde Crédit': immob['amort_cloture']
        }
    ]
    
    return pd.DataFrame(comptes), numero_brut, numero_amort, immob


# ============================================================================
# TESTS DE PROPRIÉTÉ
# ============================================================================

@given(immob=st_immobilisation_valide())
@settings(max_examples=100, deadline=60000)
def test_property_vnc_ouverture_formula(immob):
    """
    Property 9: VNC Ouverture Calculation Formula.
    
    Pour toute ligne d'immobilisation, le VNC_Calculator doit calculer:
    VNC_Ouverture = Brut_Ouverture - Amortissement_Ouverture
    
    Valide: Requirement 4.1
    """
    calc = VNCCalculator()
    
    vnc_ouverture = calc.calculer_vnc_ouverture(
        immob['brut_ouverture'],
        immob['amort_ouverture']
    )
    
    # PROPRIÉTÉ: La formule doit être exacte
    vnc_attendu = immob['brut_ouverture'] - immob['amort_ouverture']
    assert vnc_ouverture == vnc_attendu, (
        f"VNC Ouverture incorrect: "
        f"Brut={immob['brut_ouverture']:.2f}, "
        f"Amort={immob['amort_ouverture']:.2f}, "
        f"VNC attendu={vnc_attendu:.2f}, "
        f"VNC obtenu={vnc_ouverture:.2f}"
    )


@given(immob=st_immobilisation_valide())
@settings(max_examples=100, deadline=60000)
def test_property_vnc_cloture_formula(immob):
    """
    Property 9: VNC Clôture Calculation Formula.
    
    Pour toute ligne d'immobilisation, le VNC_Calculator doit calculer:
    VNC_Cloture = Brut_Cloture - Amortissement_Cloture
    
    Valide: Requirement 4.2
    """
    calc = VNCCalculator()
    
    vnc_cloture = calc.calculer_vnc_cloture(
        immob['brut_cloture'],
        immob['amort_cloture']
    )
    
    # PROPRIÉTÉ: La formule doit être exacte
    vnc_attendu = immob['brut_cloture'] - immob['amort_cloture']
    assert vnc_cloture == vnc_attendu, (
        f"VNC Clôture incorrect: "
        f"Brut={immob['brut_cloture']:.2f}, "
        f"Amort={immob['amort_cloture']:.2f}, "
        f"VNC attendu={vnc_attendu:.2f}, "
        f"VNC obtenu={vnc_cloture:.2f}"
    )


@given(immob=st_immobilisation_valide())
@settings(max_examples=100, deadline=60000)
def test_property_vnc_non_negative_valid_case(immob):
    """
    Property 9: VNC Non-Negative (cas valide).
    
    Pour toute ligne d'immobilisation valide (Brut >= Amortissement),
    les VNC calculées doivent être non-négatives.
    
    Valide: Requirement 4.6
    """
    calc = VNCCalculator()
    
    vnc_ouverture = calc.calculer_vnc_ouverture(
        immob['brut_ouverture'],
        immob['amort_ouverture']
    )
    
    vnc_cloture = calc.calculer_vnc_cloture(
        immob['brut_cloture'],
        immob['amort_cloture']
    )
    
    # PROPRIÉTÉ: Les VNC doivent être >= 0
    assert vnc_ouverture >= 0, (
        f"VNC Ouverture doit être non-négative. "
        f"Brut={immob['brut_ouverture']:.2f}, "
        f"Amort={immob['amort_ouverture']:.2f}, "
        f"VNC={vnc_ouverture:.2f}"
    )
    
    assert vnc_cloture >= 0, (
        f"VNC Clôture doit être non-négative. "
        f"Brut={immob['brut_cloture']:.2f}, "
        f"Amort={immob['amort_cloture']:.2f}, "
        f"VNC={vnc_cloture:.2f}"
    )
    
    # PROPRIÉTÉ: La validation doit réussir
    valide_ouverture, _ = calc.valider_vnc(vnc_ouverture, "Test Ouverture")
    valide_cloture, _ = calc.valider_vnc(vnc_cloture, "Test Clôture")
    
    assert valide_ouverture, "La validation VNC Ouverture devrait réussir"
    assert valide_cloture, "La validation VNC Clôture devrait réussir"


@given(immob=st_immobilisation_vnc_negative())
@settings(max_examples=100, deadline=60000)
def test_property_vnc_negative_detection(immob):
    """
    Property 9: VNC Negative Detection (cas anormal).
    
    Pour toute ligne d'immobilisation avec Amortissement > Brut,
    le VNC_Calculator doit détecter la VNC négative et émettre un avertissement.
    
    Valide: Requirement 4.6, 4.7
    """
    calc = VNCCalculator()
    
    vnc_ouverture = calc.calculer_vnc_ouverture(
        immob['brut_ouverture'],
        immob['amort_ouverture']
    )
    
    vnc_cloture = calc.calculer_vnc_cloture(
        immob['brut_cloture'],
        immob['amort_cloture']
    )
    
    # PROPRIÉTÉ: Les VNC doivent être négatives
    assert vnc_ouverture < 0, (
        f"VNC Ouverture devrait être négative. "
        f"Brut={immob['brut_ouverture']:.2f}, "
        f"Amort={immob['amort_ouverture']:.2f}, "
        f"VNC={vnc_ouverture:.2f}"
    )
    
    assert vnc_cloture < 0, (
        f"VNC Clôture devrait être négative. "
        f"Brut={immob['brut_cloture']:.2f}, "
        f"Amort={immob['amort_cloture']:.2f}, "
        f"VNC={vnc_cloture:.2f}"
    )
    
    # PROPRIÉTÉ: La validation doit échouer et retourner un message
    valide_ouverture, message_ouverture = calc.valider_vnc(
        vnc_ouverture,
        "Test Ouverture"
    )
    valide_cloture, message_cloture = calc.valider_vnc(
        vnc_cloture,
        "Test Clôture"
    )
    
    assert not valide_ouverture, "La validation VNC Ouverture devrait échouer"
    assert not valide_cloture, "La validation VNC Clôture devrait échouer"
    
    assert len(message_ouverture) > 0, "Un message d'avertissement devrait être retourné"
    assert len(message_cloture) > 0, "Un message d'avertissement devrait être retourné"
    
    assert "négative" in message_ouverture.lower(), (
        "Le message devrait mentionner 'négative'"
    )
    assert "négative" in message_cloture.lower(), (
        "Le message devrait mentionner 'négative'"
    )


@given(data=st_balance_avec_immobilisations())
@settings(max_examples=100, deadline=60000)
def test_property_vnc_extraction_dotations_reprises(data):
    """
    Property 9: VNC Calculation with Dotations and Reprises.
    
    Pour toute balance contenant des comptes d'immobilisations,
    le VNC_Calculator doit extraire correctement les dotations et reprises.
    
    Valide: Requirements 4.4, 4.5
    """
    balance, numero_brut, numero_amort, immob = data
    
    calc = VNCCalculator()
    
    # Extraire les dotations (mouvements crédit des comptes 28X)
    dotations = calc.extraire_dotations([numero_amort], balance)
    
    # Extraire les reprises (mouvements débit des comptes 28X)
    reprises = calc.extraire_reprises([numero_amort], balance)
    
    # Récupérer les mouvements réels du compte d'amortissement
    compte_amort = balance[balance['Numéro'] == numero_amort].iloc[0]
    mvt_credit_attendu = compte_amort['Crédit']
    mvt_debit_attendu = compte_amort['Débit']
    
    # PROPRIÉTÉ: Les dotations doivent correspondre aux mouvements crédit
    assert dotations == mvt_credit_attendu, (
        f"Dotations incorrectes: "
        f"Attendu={mvt_credit_attendu:.2f}, "
        f"Obtenu={dotations:.2f}"
    )
    
    # PROPRIÉTÉ: Les reprises doivent correspondre aux mouvements débit
    assert reprises == mvt_debit_attendu, (
        f"Reprises incorrectes: "
        f"Attendu={mvt_debit_attendu:.2f}, "
        f"Obtenu={reprises:.2f}"
    )
    
    # PROPRIÉTÉ: Les dotations et reprises doivent être >= 0
    assert dotations >= 0, "Les dotations doivent être non-négatives"
    assert reprises >= 0, "Les reprises doivent être non-négatives"


@given(
    brut=st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False),
    amort=st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=100, deadline=60000)
def test_property_vnc_formula_symmetry(brut, amort):
    """
    Property 9: VNC Formula Symmetry.
    
    Les formules de VNC Ouverture et VNC Clôture doivent être identiques
    (même formule appliquée à des moments différents).
    
    Valide: Requirements 4.1, 4.2
    """
    calc = VNCCalculator()
    
    # Calculer VNC avec les mêmes valeurs pour ouverture et clôture
    vnc_ouverture = calc.calculer_vnc_ouverture(brut, amort)
    vnc_cloture = calc.calculer_vnc_cloture(brut, amort)
    
    # PROPRIÉTÉ: Les deux formules doivent donner le même résultat
    # pour les mêmes entrées
    assert vnc_ouverture == vnc_cloture, (
        f"Les formules VNC Ouverture et Clôture doivent être identiques. "
        f"Brut={brut:.2f}, Amort={amort:.2f}, "
        f"VNC Ouverture={vnc_ouverture:.2f}, "
        f"VNC Clôture={vnc_cloture:.2f}"
    )
    
    # PROPRIÉTÉ: Le résultat doit être égal à Brut - Amort
    vnc_attendu = brut - amort
    assert vnc_ouverture == vnc_attendu, (
        f"VNC doit être égal à Brut - Amort. "
        f"Attendu={vnc_attendu:.2f}, "
        f"Obtenu={vnc_ouverture:.2f}"
    )


@given(
    brut_ouverture=st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False),
    augmentations=st.floats(min_value=0, max_value=5e7, allow_nan=False, allow_infinity=False),
    diminutions=st.floats(min_value=0, max_value=5e7, allow_nan=False, allow_infinity=False),
    amort_ouverture=st.floats(min_value=0, max_value=1e8, allow_nan=False, allow_infinity=False),
    dotations=st.floats(min_value=0, max_value=5e7