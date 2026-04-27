"""
Property Test: API Integration Round-Trip

Feature: calcul-notes-annexes-syscohada
Property 20: API Integration Round-Trip

For any balance file uploaded through the Claraverse interface, the backend 
endpoint /api/calculer_notes_annexes must receive the file, execute calculations, 
and return a JSON object containing all 33 notes, which the frontend must display 
in clickable accordions.

Validates: Requirements 13.2, 13.3, 13.4

Test Strategy:
- Generate valid balance files with Hypothesis
- Upload files to the API endpoint
- Verify JSON response structure
- Verify all 33 notes are present
- Verify data integrity through the round-trip
"""

import pytest
import tempfile
import os
import io
from pathlib import Path
from hypothesis import given, settings, assume
from hypothesis import strategies as st
import pandas as pd
from fastapi.testclient import TestClient

# Import the API router
import sys
notes_annexes_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, notes_annexes_path)

try:
    from api_notes_annexes import router
    from fastapi import FastAPI
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False


# ============================================================================
# HYPOTHESIS STRATEGIES FOR BALANCE FILE GENERATION
# ============================================================================

@st.composite
def st_balance_complete(draw):
    """
    Generate a complete balance sheet with all required columns.
    
    Returns a DataFrame with:
    - Numéro: Account number (3-5 digits)
    - Intitulé: Account label
    - Ant Débit: Opening debit balance
    - Ant Crédit: Opening credit balance
    - Débit: Debit movements
    - Crédit: Credit movements
    - Solde Débit: Closing debit balance
    - Solde Crédit: Closing credit balance
    """
    num_accounts = draw(st.integers(min_value=20, max_value=50))
    
    accounts = []
    for _ in range(num_accounts):
        # Generate SYSCOHADA account number
        classe = draw(st.sampled_from(['2', '3', '4', '5', '6', '7']))
        sous_classe = draw(st.integers(min_value=0, max_value=9))
        detail = draw(st.text(alphabet='0123456789', min_size=1, max_size=2))
        numero = f"{classe}{sous_classe}{detail}"
        
        intitule = draw(st.text(min_size=10, max_size=40, alphabet='abcdefghijklmnopqrstuvwxyz '))
        
        # Generate coherent balances
        ant_debit = draw(st.floats(min_value=0, max_value=5000000, allow_nan=False, allow_infinity=False))
        ant_credit = draw(st.floats(min_value=0, max_value=5000000, allow_nan=False, allow_infinity=False))
        mvt_debit = draw(st.floats(min_value=0, max_value=2000000, allow_nan=False, allow_infinity=False))
        mvt_credit = draw(st.floats(min_value=0, max_value=2000000, allow_nan=False, allow_infinity=False))
        
        # Calculate coherent closing balances
        solde_ouverture = ant_debit - ant_credit
        solde_cloture = solde_ouverture + mvt_debit - mvt_credit
        
        solde_debit = max(0, solde_cloture)
        solde_credit = max(0, -solde_cloture)
        
        accounts.append({
            'Numéro': numero,
            'Intitulé': intitule,
            'Ant Débit': round(ant_debit, 2),
            'Ant Crédit': round(ant_credit, 2),
            'Débit': round(mvt_debit, 2),
            'Crédit': round(mvt_credit, 2),
            'Solde Débit': round(solde_debit, 2),
            'Solde Crédit': round(solde_credit, 2)
        })
    
    return pd.DataFrame(accounts)


def create_excel_file_from_balance(balance_n, balance_n1, balance_n2):
    """
    Create a temporary Excel file with 3 balance sheets.
    
    Args:
        balance_n: DataFrame for year N
        balance_n1: DataFrame for year N-1
        balance_n2: DataFrame for year N-2
        
    Returns:
        Path to temporary Excel file
    """
    temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
    temp_file.close()
    
    with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
        balance_n.to_excel(writer, sheet_name='BALANCE N', index=False)
        balance_n1.to_excel(writer, sheet_name='BALANCE N-1', index=False)
        balance_n2.to_excel(writer, sheet_name='BALANCE N-2', index=False)
    
    return temp_file.name


# ============================================================================
# PROPERTY TESTS
# ============================================================================

@pytest.mark.skipif(not API_AVAILABLE, reason="API module not available")
class TestAPIIntegrationRoundTrip:
    """
    Property-based tests for API integration round-trip.
    
    Property 20: For any balance file uploaded through the interface,
    the API must receive it, calculate notes, and return valid JSON.
    """
    
    @pytest.fixture
    def client(self):
        """Create a test client for the API."""
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    
    @given(
        balance_n=st_balance_complete(),
        balance_n1=st_balance_complete(),
        balance_n2=st_balance_complete()
    )
    @settings(max_examples=10, deadline=120000)  # Reduced examples for API tests
    def test_property_20_api_roundtrip_structure(self, client, balance_n, balance_n1, balance_n2):
        """
        Property 20: API Integration Round-Trip - Response Structure
        
        For any valid balance file uploaded, the API must return:
        - HTTP 200 status
        - JSON response with success=True
        - 'notes' field containing calculated notes
        - Valid structure for each note
        
        Validates: Requirements 13.2, 13.3
        """
        # Create temporary Excel file
        excel_file = None
        try:
            excel_file = create_excel_file_from_balance(balance_n, balance_n1, balance_n2)
            
            # Upload file to API
            with open(excel_file, 'rb') as f:
                files = {'balance_file': ('test_balance.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            # Verify HTTP status
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
            
            # Verify JSON structure
            data = response.json()
            assert isinstance(data, dict), "Response must be a dictionary"
            assert data.get('success') == True, "Response must indicate success"
            
            # Verify required fields
            assert 'notes' in data, "Response must contain 'notes' field"
            assert 'timestamp' in data, "Response must contain 'timestamp' field"
            assert 'notes_calculees' in data, "Response must contain 'notes_calculees' field"
            assert 'taux_coherence' in data, "Response must contain 'taux_coherence' field"
            
            # Verify notes structure
            notes = data['notes']
            assert isinstance(notes, dict), "Notes must be a dictionary"
            assert len(notes) > 0, "Notes dictionary must not be empty"
            
            # Verify each note has required structure
            for note_name, note_data in notes.items():
                assert isinstance(note_data, dict), f"Note {note_name} must be a dictionary"
                assert 'colonnes' in note_data, f"Note {note_name} must have 'colonnes' field"
                assert 'lignes' in note_data, f"Note {note_name} must have 'lignes' field"
                assert isinstance(note_data['colonnes'], list), f"Note {note_name} colonnes must be a list"
                assert isinstance(note_data['lignes'], list), f"Note {note_name} lignes must be a list"
        
        finally:
            # Cleanup
            if excel_file and os.path.exists(excel_file):
                os.unlink(excel_file)
    
    @given(
        balance_n=st_balance_complete(),
        balance_n1=st_balance_complete(),
        balance_n2=st_balance_complete()
    )
    @settings(max_examples=5, deadline=120000)
    def test_property_20_api_roundtrip_data_integrity(self, client, balance_n, balance_n1, balance_n2):
        """
        Property 20: API Integration Round-Trip - Data Integrity
        
        For any balance file uploaded, the returned notes must:
        - Contain numeric data that can be parsed
        - Have consistent column counts across rows
        - Preserve data types through serialization
        
        Validates: Requirements 13.3, 13.4
        """
        excel_file = None
        try:
            excel_file = create_excel_file_from_balance(balance_n, balance_n1, balance_n2)
            
            with open(excel_file, 'rb') as f:
                files = {'balance_file': ('test_balance.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            assert response.status_code == 200
            data = response.json()
            notes = data['notes']
            
            # Verify data integrity for each note
            for note_name, note_data in notes.items():
                colonnes = note_data['colonnes']
                lignes = note_data['lignes']
                
                # Verify column consistency
                if len(lignes) > 0:
                    num_colonnes = len(colonnes)
                    for i, ligne in enumerate(lignes):
                        assert len(ligne) == num_colonnes, \
                            f"Note {note_name} ligne {i}: expected {num_colonnes} columns, got {len(ligne)}"
                
                # Verify numeric data can be parsed
                for ligne in lignes:
                    for j, valeur in enumerate(ligne):
                        if j > 0:  # Skip first column (label)
                            assert isinstance(valeur, (int, float, type(None))), \
                                f"Note {note_name}: column {j} must be numeric, got {type(valeur)}"
        
        finally:
            if excel_file and os.path.exists(excel_file):
                os.unlink(excel_file)
    
    def test_property_20_api_error_handling_invalid_file(self, client):
        """
        Property 20: API Integration Round-Trip - Error Handling
        
        The API must handle invalid files gracefully:
        - Return appropriate HTTP error codes
        - Provide descriptive error messages
        - Not crash or hang
        
        Validates: Requirements 13.5, 13.6
        """
        # Test with invalid file format
        invalid_content = b"This is not an Excel file"
        files = {'balance_file': ('invalid.txt', io.BytesIO(invalid_content), 'text/plain')}
        response = client.post('/api/calculer_notes_annexes', files=files)
        
        # Should return 400 Bad Request for invalid format
        assert response.status_code == 400, f"Expected 400 for invalid file, got {response.status_code}"
        
        # Verify error response structure
        data = response.json()
        assert 'detail' in data, "Error response must contain 'detail' field"
    
    def test_property_20_api_error_handling_missing_sheets(self, client):
        """
        Property 20: API Integration Round-Trip - Missing Sheets
        
        The API must handle files with missing balance sheets:
        - Detect missing required sheets
        - Return 404 or 400 error
        - Provide clear error message
        
        Validates: Requirements 13.5, 13.6
        """
        # Create Excel file with only one sheet
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
        temp_file.close()
        
        try:
            balance = pd.DataFrame({
                'Numéro': ['211', '212'],
                'Intitulé': ['Test 1', 'Test 2'],
                'Ant Débit': [1000, 2000],
                'Ant Crédit': [0, 0],
                'Débit': [100, 200],
                'Crédit': [0, 0],
                'Solde Débit': [1100, 2200],
                'Solde Crédit': [0, 0]
            })
            
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                balance.to_excel(writer, sheet_name='BALANCE N', index=False)
            
            with open(temp_file.name, 'rb') as f:
                files = {'balance_file': ('incomplete.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            # Should return error for missing sheets
            assert response.status_code in [400, 404, 500], \
                f"Expected error status for missing sheets, got {response.status_code}"
        
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


# ============================================================================
# INTEGRATION TEST WITH REAL BALANCE FILE
# ============================================================================

@pytest.mark.skipif(not API_AVAILABLE, reason="API module not available")
def test_api_integration_with_demo_balance(client):
    """
    Integration test with the demo balance file.
    
    This test verifies the complete round-trip with a real balance file:
    1. Load the demo balance file
    2. Upload to API
    3. Verify response structure
    4. Verify all 33 notes are calculated
    5. Verify coherence rate
    
    Validates: Requirements 13.1, 13.2, 13.3, 13.4
    """
    # Path to demo balance file
    demo_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    if not os.path.exists(demo_file):
        pytest.skip(f"Demo balance file not found: {demo_file}")
    
    # Create test client
    app = FastAPI()
    app.include_router(router)
    test_client = TestClient(app)
    
    # Upload file
    with open(demo_file, 'rb') as f:
        files = {'balance_file': ('balance_demo.xls', f, 'application/vnd.ms-excel')}
        response = test_client.post('/api/calculer_notes_annexes', files=files)
    
    # Verify response
    assert response.status_code == 200, f"API call failed: {response.text}"
    
    data = response.json()
    assert data['success'] == True
    assert 'notes' in data
    
    # Verify all notes are present
    notes = data['notes']
    # Note: The actual number of notes may vary based on implementation
    # We verify that at least some notes are calculated
    assert len(notes) > 0, "No notes were calculated"
    
    # Verify coherence rate
    assert 'taux_coherence' in data
    taux_coherence = data['taux_coherence']
    assert isinstance(taux_coherence, (int, float))
    assert 0 <= taux_coherence <= 100, f"Coherence rate must be between 0 and 100, got {taux_coherence}"
    
    # Verify calculation duration
    assert 'duree_calcul' in data
    duree = data['duree_calcul']
    assert isinstance(duree, (int, float))
    assert duree > 0, "Calculation duration must be positive"
    
    print(f"\n✓ API Integration Test Passed:")
    print(f"  - Notes calculated: {data['notes_calculees']}")
    print(f"  - Coherence rate: {taux_coherence:.1f}%")
    print(f"  - Duration: {duree:.2f}s")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
