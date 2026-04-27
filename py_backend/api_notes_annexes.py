"""
API Flask pour le calcul automatique des notes annexes SYSCOHADA révisé.

Ce module expose un endpoint POST pour calculer les 33 notes annexes
à partir d'un fichier Excel de balances uploadé.

Endpoint: POST /api/calculer_notes_annexes
Input: Fichier Excel (multipart/form-data)
Output: JSON avec toutes les notes calculées

Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6
"""

import logging
import os
import sys
import tempfile
import traceback
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd

# Ajouter le chemin vers le module de calcul des notes annexes
notes_annexes_path = os.path.join(os.path.dirname(__file__), 'Doc calcul notes annexes')
sys.path.insert(0, notes_annexes_path)
sys.path.insert(0, os.path.join(notes_annexes_path, 'Modules'))

try:
    from calcul_notes_annexes_main import CalculNotesAnnexesMain
    NOTES_ANNEXES_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Module calcul_notes_annexes_main non disponible: {e}")
    NOTES_ANNEXES_AVAILABLE = False

# Configuration du logger
logger = logging.getLogger(__name__)

# Créer le router FastAPI
router = APIRouter(prefix="/api", tags=["Notes Annexes SYSCOHADA"])


def dataframe_to_dict(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convertit un DataFrame pandas en dictionnaire JSON-serializable.
    
    Args:
        df: DataFrame à convertir
        
    Returns:
        Dict avec structure {colonnes: [...], lignes: [[...]]}
    """
    if df is None or df.empty:
        return {"colonnes": [], "lignes": []}
    
    # Convertir les valeurs NaN en None pour la sérialisation JSON
    df_clean = df.fillna(0)
    
    return {
        "colonnes": df_clean.columns.tolist(),
        "lignes": df_clean.values.tolist()
    }


@router.post("/calculer_notes_annexes")
async def calculer_notes_annexes(
    balance_file: UploadFile = File(..., description="Fichier Excel de balances (N, N-1, N-2)")
):
    """
    Calcule les 33 notes annexes SYSCOHADA révisé à partir d'un fichier de balances.
    
    **Processus:**
    1. Réception du fichier Excel uploadé
    2. Validation du format du fichier
    3. Calcul des 33 notes annexes via l'orchestrateur
    4. Validation de cohérence inter-notes
    5. Retour des résultats en JSON
    
    **Input:**
    - balance_file: Fichier Excel (.xlsx ou .xls) contenant les balances N, N-1, N-2
    
    **Output:**
    ```json
    {
        "success": true,
        "timestamp": "2026-04-27T10:30:00",
        "notes_calculees": 33,
        "taux_coherence": 98.5,
        "duree_calcul": 12.5,
        "notes": {
            "Note_3A": {
                "colonnes": ["Libellé", "Brut Ouverture", ...],
                "lignes": [["Frais R&D", 1500000, ...], ...]
            },
            ...
        },
        "statuts": {
            "Note_3A": "✓ Succès",
            ...
        }
    }
    ```
    
    **Codes d'erreur:**
    - 400: Format de fichier invalide ou données manquantes
    - 404: Onglets de balance manquants
    - 500: Erreur interne lors du calcul
    - 503: Module de calcul non disponible
    
    Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6
    """
    # Vérifier que le module est disponible
    if not NOTES_ANNEXES_AVAILABLE:
        logger.error("Module calcul_notes_annexes_main non disponible")
        raise HTTPException(
            status_code=503,
            detail="Service de calcul des notes annexes temporairement indisponible"
        )
    
    # Vérifier le type de fichier
    if not balance_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Nom de fichier manquant"
        )
    
    file_ext = Path(balance_file.filename).suffix.lower()
    if file_ext not in ['.xlsx', '.xls']:
        raise HTTPException(
            status_code=400,
            detail=f"Format de fichier non supporté: {file_ext}. Formats acceptés: .xlsx, .xls"
        )
    
    # Créer un fichier temporaire pour sauvegarder l'upload
    temp_file = None
    try:
        # Lire le contenu du fichier uploadé
        contents = await balance_file.read()
        
        # Créer un fichier temporaire avec l'extension appropriée
        with tempfile.NamedTemporaryFile(
            mode='wb',
            suffix=file_ext,
            delete=False
        ) as temp_file:
            temp_file.write(contents)
            temp_file_path = temp_file.name
        
        logger.info(f"Fichier reçu: {balance_file.filename} ({len(contents)} bytes)")
        logger.info(f"Fichier temporaire créé: {temp_file_path}")
        
        # Démarrer le chronomètre
        debut = datetime.now()
        
        # Créer l'orchestrateur et calculer les notes
        try:
            orchestrateur = CalculNotesAnnexesMain(
                fichier_balance=temp_file_path,
                mode_parallele=False  # Mode séquentiel pour la stabilité
            )
            
            # Calculer toutes les notes
            notes_calculees = orchestrateur.calculer_toutes_notes()
            
            if not notes_calculees:
                raise HTTPException(
                    status_code=500,
                    detail="Aucune note n'a pu être calculée. Vérifiez le format du fichier de balances."
                )
            
            # Valider la cohérence
            taux_coherence = orchestrateur.valider_coherence()
            
            # Calculer la durée
            fin = datetime.now()
            duree = (fin - debut).total_seconds()
            
            # Convertir les DataFrames en dictionnaires
            notes_json = {}
            for nom_note, df in notes_calculees.items():
                notes_json[nom_note] = dataframe_to_dict(df)
            
            # Préparer la réponse
            response = {
                "success": True,
                "timestamp": debut.isoformat(),
                "notes_calculees": len(notes_calculees),
                "notes_totales": len(orchestrateur.NOTES_A_CALCULER),
                "taux_coherence": round(taux_coherence, 2),
                "duree_calcul": round(duree, 2),
                "notes": notes_json,
                "statuts": orchestrateur.statuts_calcul,
                "fichier_source": balance_file.filename
            }
            
            logger.info(f"✓ Calcul réussi: {len(notes_calculees)} notes en {duree:.2f}s")
            logger.info(f"✓ Taux de cohérence: {taux_coherence:.1f}%")
            
            return JSONResponse(content=response)
            
        except FileNotFoundError as e:
            logger.error(f"Fichier non trouvé: {e}")
            raise HTTPException(
                status_code=404,
                detail=f"Fichier ou onglet manquant: {str(e)}"
            )
        
        except ValueError as e:
            logger.error(f"Erreur de validation: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Données invalides: {str(e)}"
            )
        
        except Exception as e:
            logger.error(f"Erreur lors du calcul: {e}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail=f"Erreur interne lors du calcul: {str(e)}"
            )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Erreur inattendue: {str(e)}"
        )
    
    finally:
        # Nettoyer le fichier temporaire
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Fichier temporaire supprimé: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Impossible de supprimer le fichier temporaire: {e}")


@router.get("/notes_annexes/health")
async def health_check():
    """
    Vérifie la disponibilité du service de calcul des notes annexes.
    
    Returns:
        Status du service et informations de version
    """
    return {
        "service": "Notes Annexes SYSCOHADA",
        "status": "available" if NOTES_ANNEXES_AVAILABLE else "unavailable",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
