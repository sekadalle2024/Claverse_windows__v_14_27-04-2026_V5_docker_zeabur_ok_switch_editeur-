# Quick Start - Note 19: Produits Constatés d'Avance

## Overview
This calculator generates Note 19 of the SYSCOHADA financial statement annexes, covering deferred income (Produits constatés d'avance).

## Account Mapping
- **477**: Produits constatés d'avance (Deferred income)

## Key Features
- Calculates movements for deferred income
- Tracks opening balance, increases, decreases, and closing balance
- Generates HTML output with SYSCOHADA-compliant formatting
- Creates JSON trace file for audit purposes

## Usage

### Prerequisites
Ensure you have a balance file at: `P000 -BALANCE DEMO N_N-1_N-2.xlsx`

### Run the Calculator
```bash
cd "py_backend/Doc calcul notes annexes/Scripts"
python calculer_note_19.py
```

### Expected Output
1. **HTML File**: `../Tests/test_note_19.html` - Visual representation of Note 19
2. **Trace File**: `../Tests/trace_note_19.json` - Detailed calculation trace

## Calculation Logic

### For Deferred Income (Liability Account)
- **Opening Balance**: Credit balance from N-1
- **Increases**: Credit movements in N
- **Decreases**: Debit movements in N
- **Closing Balance**: Credit balance in N

### Coherence Check
The calculator verifies: `Closing Balance = Opening Balance + Increases - Decreases`

## Output Structure

### HTML Table Columns
1. **NATURE**: Description (Produits constatés d'avance)
2. **Solde début exercice**: Opening balance
3. **Augmentations**: Increases during the period
4. **Diminutions**: Decreases during the period
5. **Solde fin exercice**: Closing balance

## Testing

### Quick Test
```powershell
# From project root
./test-note-19.ps1
```

This will:
- Execute the calculator
- Display results in console
- Open the HTML file in your browser
- Verify trace file creation

## Requirements Validated
- ✓ Requirement 5.1: Script structure follows template
- ✓ Requirement 5.2: Mapping for account 477 defined
- ✓ Requirement 5.3: Calculation logic implemented
- ✓ Requirement 5.4: HTML generation functional

## Notes
- Deferred income is a **liability account** (credit balance)
- Increases are recorded as **credits** (revenue received in advance)
- Decreases are recorded as **debits** (revenue recognized)
- Single line item (no subtotals needed)

## Troubleshooting

### Balance File Not Found
Ensure the balance file exists at the root level:
```
ClaraVerse/
  └── P000 -BALANCE DEMO N_N-1_N-2.xlsx
```

### Import Errors
Make sure you're running from the Scripts directory or that the module path is correctly set.

### Coherence Warnings
If you see coherence warnings, verify the balance file data for account 477.
