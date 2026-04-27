# Quick Start - API Notes Annexes SYSCOHADA

## Vue d'ensemble

L'API Notes Annexes SYSCOHADA permet de calculer automatiquement les 33 notes annexes des états financiers à partir d'un fichier Excel de balances.

## Endpoint

```
POST /api/calculer_notes_annexes
```

## Utilisation

### 1. Démarrer le backend

```bash
cd py_backend
python main.py
```

Le serveur démarre sur `http://localhost:5000`

### 2. Tester l'endpoint

#### Avec PowerShell (Windows)

```powershell
.\test-api-notes-annexes.ps1
```

#### Avec curl

```bash
curl -X POST http://localhost:5000/api/calculer_notes_annexes \
  -F "balance_file=@P000 -BALANCE DEMO N_N-1_N-2.xls" \
  -H "Content-Type: multipart/form-data"
```

#### Avec Python

```python
import requests

url = "http://localhost:5000/api/calculer_notes_annexes"
files = {"balance_file": open("P000 -BALANCE DEMO N_N-1_N-2.xls", "rb")}

response = requests.post(url, files=files)
data = response.json()

print(f"Notes calculées: {data['notes_calculees']}/{data['notes_totales']}")
print(f"Taux de cohérence: {data['taux_coherence']}%")
print(f"Durée: {data['duree_calcul']}s")
```

## Format de la requête

### Input

- **Méthode**: POST
- **Content-Type**: multipart/form-data
- **Paramètre**: `balance_file` (fichier Excel .xlsx ou .xls)

### Fichier de balance requis

Le fichier Excel doit contenir 3 onglets:
- `BALANCE N` : Balance de l'exercice en cours
- `BALANCE N-1` : Balance de l'exercice précédent
- `BALANCE N-2` : Balance de l'exercice antérieur

Chaque onglet doit avoir 8 colonnes:
1. Numéro de compte
2. Intitulé
3. Ant Débit (solde débiteur d'ouverture)
4. Ant Crédit (solde créditeur d'ouverture)
5. Débit (mouvements débiteurs)
6. Crédit (mouvements créditeurs)
7. Solde Débit (solde débiteur de clôture)
8. Solde Crédit (solde créditeur de clôture)

## Format de la réponse

### Succès (200 OK)

```json
{
  "success": true,
  "timestamp": "2026-04-27T10:30:00",
  "notes_calculees": 33,
  "notes_totales": 33,
  "taux_coherence": 98.5,
  "duree_calcul": 12.5,
  "fichier_source": "P000 -BALANCE DEMO N_N-1_N-2.xls",
  "notes": {
    "Note_3A": {
      "colonnes": [
        "Libellé",
        "Brut Ouverture",
        "Augmentations",
        "Diminutions",
        "Brut Clôture",
        "Amort Ouverture",
        "Dotations",
        "Reprises",
        "Amort Clôture",
        "VNC Ouverture",
        "VNC Clôture"
      ],
      "lignes": [
        ["Frais de recherche et de développement", 1500000, 500000, 0, 2000000, 300000, 200000, 0, 500000, 1200000, 1500000],
        ["Brevets, licences, logiciels", 800000, 200000, 0, 1000000, 400000, 100000, 0, 500000, 400000, 500000],
        ...
      ]
    },
    "Note_3B": { ... },
    ...
  },
  "statuts": {
    "Note_3A": "✓ Succès",
    "Note_3B": "✓ Succès",
    ...
  }
}
```

### Erreurs

#### 400 Bad Request
```json
{
  "detail": "Format de fichier non supporté: .pdf. Formats acceptés: .xlsx, .xls"
}
```

#### 404 Not Found
```json
{
  "detail": "Fichier ou onglet manquant: BALANCE N"
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Erreur interne lors du calcul: ..."
}
```

#### 503 Service Unavailable
```json
{
  "detail": "Service de calcul des notes annexes temporairement indisponible"
}
```

## Health Check

Vérifier la disponibilité du service:

```bash
curl http://localhost:5000/api/notes_annexes/health
```

Réponse:
```json
{
  "service": "Notes Annexes SYSCOHADA",
  "status": "available",
  "version": "1.0.0",
  "timestamp": "2026-04-27T10:30:00"
}
```

## Intégration Frontend

### Exemple React/TypeScript

```typescript
async function calculerNotesAnnexes(file: File) {
  const formData = new FormData();
  formData.append('balance_file', file);

  try {
    const response = await fetch('http://localhost:5000/api/calculer_notes_annexes', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    const data = await response.json();
    
    console.log(`Notes calculées: ${data.notes_calculees}/${data.notes_totales}`);
    console.log(`Taux de cohérence: ${data.taux_coherence}%`);
    
    // Afficher les notes dans l'interface
    Object.entries(data.notes).forEach(([noteName, noteData]) => {
      console.log(`${noteName}: ${noteData.lignes.length} lignes`);
    });
    
    return data;
  } catch (error) {
    console.error('Erreur:', error);
    throw error;
  }
}
```

### Exemple avec accordéon

```typescript
import { useState } from 'react';

function NotesAnnexesAccordion({ notes }) {
  const [expandedNote, setExpandedNote] = useState(null);

  return (
    <div className="notes-accordion">
      {Object.entries(notes).map(([noteName, noteData]) => (
        <div key={noteName} className="note-item">
          <button
            onClick={() => setExpandedNote(expandedNote === noteName ? null : noteName)}
            className="note-header"
          >
            {noteName} ({noteData.lignes.length} lignes)
          </button>
          
          {expandedNote === noteName && (
            <div className="note-content">
              <table>
                <thead>
                  <tr>
                    {noteData.colonnes.map((col, i) => (
                      <th key={i}>{col}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {noteData.lignes.map((ligne, i) => (
                    <tr key={i}>
                      {ligne.map((cell, j) => (
                        <td key={j}>{cell}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
```

## Performance

- **Durée moyenne**: 10-25 secondes pour 33 notes
- **Contrainte**: < 30 secondes (respectée)
- **Taux de cohérence attendu**: ≥ 95%

## Dépannage

### Le service n'est pas disponible (503)

Vérifier que les modules sont installés:
```bash
cd py_backend/Doc\ calcul\ notes\ annexes
pip install -r requirements.txt
```

### Erreur de format de fichier (400)

- Vérifier que le fichier est au format .xlsx ou .xls
- Vérifier que les 3 onglets existent (BALANCE N, N-1, N-2)
- Vérifier que les colonnes sont correctement nommées

### Timeout

Si le calcul prend trop de temps:
- Vérifier la taille du fichier de balance
- Vérifier les performances du serveur
- Augmenter le timeout dans la requête HTTP

## Documentation complète

Pour plus de détails, consulter:
- [Design Document](design.md)
- [Requirements Document](requirements.md)
- [Tasks Document](tasks.md)
