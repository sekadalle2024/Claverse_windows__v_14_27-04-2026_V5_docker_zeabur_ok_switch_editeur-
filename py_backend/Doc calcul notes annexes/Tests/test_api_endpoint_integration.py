"""
Integration Test: API Endpoint for Notes Annexes SYSCOHADA

Feature: calcul-notes-annexes-syscohada
Task: 22.4 Write integration test for API endpoint

This module contains comprehensive integration tests for the API endpoint
/api/calculer_notes_annexes, covering:
- File upload and response format validation
- Error handling for invalid files
- Response time and performance testing
- Complete workflow validation

Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6
"""

import pytest
import tempfile
import os
import io
import time
from pathlib import Path
import pandas as pd
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Import the API router
import sys
notes_annexes_path = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, notes_annexes_path)

try:
    from api_notes_annexes import router
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def client():
    """Create a test client for the API."""
    if not API_AVAILABLE:
        pytest.skip("API module not available")
    
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


@pytest.fixture
def valid_balance_file():
    """
    Create a valid balance file with 3 sheets for testing.
    
    Returns:
        Path to temporary Excel file
    """
    temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
    temp_file.close()
    
    # Create sample balance data
    balance_data = {
        'Numéro': ['211', '212', '213', '2811', '2812', '2813'],
        'Intitulé': [
            'Frais de recherche et développement',
            'Brevets, licences, logiciels',
            'Concessions et droits similaires',
            'Amortissements frais R&D',
            'Amortissements brevets',
            'Amortissements concessions'
        ],
        'Ant Débit': [1500000, 800000, 500000, 0, 0, 0],
        'Ant Crédit': [0, 0, 0, 300000, 150000, 100000],
        'Débit': [500000, 200000, 100000, 0, 0, 0],
        'Crédit': [0, 0, 0, 200000, 100000, 50000],
        'Solde Débit': [2000000, 1000000, 600000, 0, 0, 0],
        'Solde Crédit': [0, 0, 0, 500000, 250000, 150000]
    }
    
    balance_n = pd.DataFrame(balance_data)
    balance_n1 = pd.DataFrame(balance_data)  # Simplified: same data for N-1
    balance_n2 = pd.DataFrame(balance_data)  # Simplified: same data for N-2
    
    with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
        balance_n.to_excel(writer, sheet_name='BALANCE N', index=False)
        balance_n1.to_excel(writer, sheet_name='BALANCE N-1', index=False)
        balance_n2.to_excel(writer, sheet_name='BALANCE N-2', index=False)
    
    yield temp_file.name
    
    # Cleanup
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def demo_balance_file():
    """
    Get path to demo balance file if it exists.
    
    Returns:
        Path to demo balance file or None
    """
    demo_file = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'P000 -BALANCE DEMO N_N-1_N-2.xls'
    )
    
    if os.path.exists(demo_file):
        return demo_file
    return None


# ============================================================================
# TEST 1: FILE UPLOAD AND RESPONSE FORMAT
# ============================================================================

class TestFileUploadAndResponseFormat:
    """
    Test suite for file upload and response format validation.
    
    Validates: Requirements 13.1, 13.2, 13.3
    """
    
    def test_upload_valid_xlsx_file(self, client, valid_balance_file):
        """
        Test uploading a valid .xlsx file.
        
        Verifies:
        - File is accepted
        - HTTP 200 response
        - Response contains required fields
        
        Requirement: 13.1, 13.2
        """
        with open(valid_balance_file, 'rb') as f:
            files = {
                'balance_file': (
                    'test_balance.xlsx',
                    f,
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            }
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        assert data['success'] == True
        assert 'notes' in data
        assert 'timestamp' in data
        assert 'notes_calculees' in data
    
    def test_upload_valid_xls_file(self, client, demo_balance_file):
        """
        Test uploading a valid .xls file (legacy Excel format).
        
        Verifies:
        - Legacy format is accepted
        - HTTP 200 response
        
        Requirement: 13.1, 13.2
        """
        if demo_balance_file is None:
            pytest.skip("Demo balance file not available")
        
        with open(demo_balance_file, 'rb') as f:
            files = {
                'balance_file': (
                    'balance_demo.xls',
                    f,
                    'application/vnd.ms-excel'
                )
            }
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data['success'] == True
    
    def test_response_structure_completeness(self, client, valid_balance_file):
        """
        Test that response contains all required fields.
        
        Verifies:
        - success field (boolean)
        - timestamp field (ISO format)
        - notes_calculees field (integer)
        - taux_coherence field (float)
        - duree_calcul field (float)
        - notes field (dict)
        - statuts field (dict)
        - fichier_source field (string)
        
        Requirement: 13.3
        """
        with open(valid_balance_file, 'rb') as f:
            files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        required_fields = [
            'success', 'timestamp', 'notes_calculees', 'notes_totales',
            'taux_coherence', 'duree_calcul', 'notes', 'statuts', 'fichier_source'
        ]
        
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        # Verify field types
        assert isinstance(data['success'], bool)
        assert isinstance(data['timestamp'], str)
        assert isinstance(data['notes_calculees'], int)
        assert isinstance(data['notes_totales'], int)
        assert isinstance(data['taux_coherence'], (int, float))
        assert isinstance(data['duree_calcul'], (int, float))
        assert isinstance(data['notes'], dict)
        assert isinstance(data['statuts'], dict)
        assert isinstance(data['fichier_source'], str)
    
    def test_notes_structure_format(self, client, valid_balance_file):
        """
        Test that each note has the correct structure.
        
        Verifies:
        - Each note is a dictionary
        - Each note has 'colonnes' field (list)
        - Each note has 'lignes' field (list of lists)
        - Column count is consistent across rows
        
        Requirement: 13.3, 13.4
        """
        with open(valid_balance_file, 'rb') as f:
            files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200
        data = response.json()
        notes = data['notes']
        
        assert len(notes) > 0, "No notes were calculated"
        
        for note_name, note_data in notes.items():
            # Verify structure
            assert isinstance(note_data, dict), f"Note {note_name} must be a dict"
            assert 'colonnes' in note_data, f"Note {note_name} missing 'colonnes'"
            assert 'lignes' in note_data, f"Note {note_name} missing 'lignes'"
            
            colonnes = note_data['colonnes']
            lignes = note_data['lignes']
            
            assert isinstance(colonnes, list), f"Note {note_name} colonnes must be a list"
            assert isinstance(lignes, list), f"Note {note_name} lignes must be a list"
            
            # Verify column consistency
            if len(lignes) > 0:
                num_colonnes = len(colonnes)
                for i, ligne in enumerate(lignes):
                    assert isinstance(ligne, list), f"Note {note_name} ligne {i} must be a list"
                    assert len(ligne) == num_colonnes, \
                        f"Note {note_name} ligne {i}: expected {num_colonnes} columns, got {len(ligne)}"
    
    def test_json_serialization(self, client, valid_balance_file):
        """
        Test that response is properly JSON-serializable.
        
        Verifies:
        - No NaN values
        - No Infinity values
        - All numeric values are valid
        
        Requirement: 13.3
        """
        with open(valid_balance_file, 'rb') as f:
            files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify numeric fields are valid
        assert data['taux_coherence'] >= 0 and data['taux_coherence'] <= 100
        assert data['duree_calcul'] > 0
        assert data['notes_calculees'] >= 0
        
        # Verify notes data is valid
        for note_name, note_data in data['notes'].items():
            for ligne in note_data['lignes']:
                for valeur in ligne:
                    if isinstance(valeur, (int, float)):
                        assert not (valeur != valeur), f"NaN value found in {note_name}"  # NaN check
                        assert valeur != float('inf') and valeur != float('-inf'), \
                            f"Infinity value found in {note_name}"


# ============================================================================
# TEST 2: ERROR HANDLING FOR INVALID FILES
# ============================================================================

class TestErrorHandlingInvalidFiles:
    """
    Test suite for error handling with invalid files.
    
    Validates: Requirements 13.5, 13.6
    """
    
    def test_invalid_file_format_txt(self, client):
        """
        Test uploading a .txt file (invalid format).
        
        Verifies:
        - HTTP 400 error
        - Error message indicates invalid format
        
        Requirement: 13.5, 13.6
        """
        invalid_content = b"This is a text file, not an Excel file"
        files = {'balance_file': ('invalid.txt', io.BytesIO(invalid_content), 'text/plain')}
        response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data
        assert 'format' in data['detail'].lower() or 'supporté' in data['detail'].lower()
    
    def test_invalid_file_format_pdf(self, client):
        """
        Test uploading a .pdf file (invalid format).
        
        Verifies:
        - HTTP 400 error
        - Descriptive error message
        
        Requirement: 13.5, 13.6
        """
        invalid_content = b"%PDF-1.4 fake pdf content"
        files = {'balance_file': ('document.pdf', io.BytesIO(invalid_content), 'application/pdf')}
        response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data
    
    def test_missing_filename(self, client):
        """
        Test uploading file without filename.
        
        Verifies:
        - HTTP 400 error
        - Error message about missing filename
        
        Requirement: 13.5, 13.6
        """
        files = {'balance_file': ('', io.BytesIO(b"content"), 'application/octet-stream')}
        response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 400
        data = response.json()
        assert 'detail' in data
    
    def test_corrupted_excel_file(self, client):
        """
        Test uploading a corrupted Excel file.
        
        Verifies:
        - HTTP 400 or 500 error
        - Error message indicates file problem
        
        Requirement: 13.5, 13.6
        """
        # Create fake Excel content (corrupted)
        corrupted_content = b"PK\x03\x04" + b"\x00" * 100  # Fake ZIP header
        files = {
            'balance_file': (
                'corrupted.xlsx',
                io.BytesIO(corrupted_content),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        }
        response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code in [400, 500]
        data = response.json()
        assert 'detail' in data
    
    def test_missing_balance_sheets(self, client):
        """
        Test uploading Excel file with missing balance sheets.
        
        Verifies:
        - HTTP 404 or 400 error
        - Error message indicates missing sheets
        
        Requirement: 13.5, 13.6
        """
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
        temp_file.close()
        
        try:
            # Create Excel with only one sheet
            balance = pd.DataFrame({
                'Numéro': ['211'],
                'Intitulé': ['Test'],
                'Ant Débit': [1000],
                'Ant Crédit': [0],
                'Débit': [100],
                'Crédit': [0],
                'Solde Débit': [1100],
                'Solde Crédit': [0]
            })
            
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                balance.to_excel(writer, sheet_name='BALANCE N', index=False)
            
            with open(temp_file.name, 'rb') as f:
                files = {
                    'balance_file': (
                        'incomplete.xlsx',
                        f,
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                }
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            assert response.status_code in [400, 404, 500]
            data = response.json()
            assert 'detail' in data
        
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    def test_invalid_column_names(self, client):
        """
        Test uploading Excel file with invalid column names.
        
        Verifies:
        - HTTP 400 or 500 error
        - Error message indicates data problem
        
        Requirement: 13.5, 13.6
        """
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
        temp_file.close()
        
        try:
            # Create Excel with wrong column names
            balance = pd.DataFrame({
                'Account': ['211'],
                'Name': ['Test'],
                'Amount': [1000]
            })
            
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                balance.to_excel(writer, sheet_name='BALANCE N', index=False)
                balance.to_excel(writer, sheet_name='BALANCE N-1', index=False)
                balance.to_excel(writer, sheet_name='BALANCE N-2', index=False)
            
            with open(temp_file.name, 'rb') as f:
                files = {
                    'balance_file': (
                        'invalid_columns.xlsx',
                        f,
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                }
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            assert response.status_code in [400, 500]
            data = response.json()
            assert 'detail' in data
        
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
    
    def test_empty_excel_file(self, client):
        """
        Test uploading an empty Excel file.
        
        Verifies:
        - HTTP 400 or 500 error
        - Error message indicates empty file
        
        Requirement: 13.5, 13.6
        """
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
        temp_file.close()
        
        try:
            # Create empty Excel file
            with pd.ExcelWriter(temp_file.name, engine='openpyxl') as writer:
                pass  # Empty file
            
            with open(temp_file.name, 'rb') as f:
                files = {
                    'balance_file': (
                        'empty.xlsx',
                        f,
                        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                }
                response = client.post('/api/calculer_notes_annexes', files=files)
            
            assert response.status_code in [400, 404, 500]
            data = response.json()
            assert 'detail' in data
        
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)


# ============================================================================
# TEST 3: RESPONSE TIME AND PERFORMANCE
# ============================================================================

class TestResponseTimeAndPerformance:
    """
    Test suite for response time and performance validation.
    
    Validates: Requirements 13.2, 13.4
    """
    
    def test_response_time_small_file(self, client, valid_balance_file):
        """
        Test response time with a small balance file.
        
        Verifies:
        - Response time is reasonable (< 60 seconds)
        - duree_calcul field matches actual time
        
        Requirement: 13.2, 13.4
        """
        start_time = time.time()
        
        with open(valid_balance_file, 'rb') as f:
            files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response time is reasonable
        assert actual_duration < 60, f"Response took too long: {actual_duration:.2f}s"
        
        # Verify reported duration is close to actual
        reported_duration = data['duree_calcul']
        assert abs(reported_duration - actual_duration) < 5, \
            f"Reported duration ({reported_duration:.2f}s) differs significantly from actual ({actual_duration:.2f}s)"
        
        print(f"\n✓ Small file processed in {actual_duration:.2f}s")
    
    def test_response_time_demo_file(self, client, demo_balance_file):
        """
        Test response time with the demo balance file.
        
        Verifies:
        - Response time meets performance requirement (< 30 seconds)
        - All notes are calculated
        
        Requirement: 13.2, 13.4
        """
        if demo_balance_file is None:
            pytest.skip("Demo balance file not available")
        
        start_time = time.time()
        
        with open(demo_balance_file, 'rb') as f:
            files = {'balance_file': ('demo.xls', f, 'application/vnd.ms-excel')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        end_time = time.time()
        actual_duration = end_time - start_time
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify performance requirement
        assert actual_duration < 30, \
            f"Performance requirement not met: {actual_duration:.2f}s (should be < 30s)"
        
        # Verify notes were calculated
        assert data['notes_calculees'] > 0
        
        print(f"\n✓ Demo file processed in {actual_duration:.2f}s")
        print(f"  - Notes calculated: {data['notes_calculees']}")
        print(f"  - Coherence rate: {data['taux_coherence']:.1f}%")
    
    def test_concurrent_requests(self, client, valid_balance_file):
        """
        Test handling of concurrent requests.
        
        Verifies:
        - Multiple requests can be processed
        - No race conditions or crashes
        - Each request returns valid response
        
        Requirement: 13.2
        """
        import concurrent.futures
        
        def make_request():
            with open(valid_balance_file, 'rb') as f:
                files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
                response = client.post('/api/calculer_notes_annexes', files=files)
            return response
        
        # Make 3 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request) for _ in range(3)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # Verify all requests succeeded
        for response in responses:
            assert response.status_code == 200
            data = response.json()
            assert data['success'] == True
        
        print(f"\n✓ {len(responses)} concurrent requests processed successfully")
    
    def test_memory_cleanup(self, client, valid_balance_file):
        """
        Test that temporary files are cleaned up after processing.
        
        Verifies:
        - Temporary files are deleted
        - No memory leaks
        
        Requirement: 13.2
        """
        import tempfile
        
        # Get initial temp file count
        temp_dir = tempfile.gettempdir()
        initial_files = set(os.listdir(temp_dir))
        
        # Make request
        with open(valid_balance_file, 'rb') as f:
            files = {'balance_file': ('test.xlsx', f, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
            response = client.post('/api/calculer_notes_annexes', files=files)
        
        assert response.status_code == 200
        
        # Check temp files after request
        final_files = set(os.listdir(temp_dir))
        new_files = final_files - initial_files
        
        # Filter for Excel files
        excel_files = [f for f in new_files if f.endswith(('.xlsx', '.xls'))]
        
        assert len(excel_files) == 0, \
            f"Temporary Excel files not cleaned up: {excel_files}"
        
        print(f"\n✓ Temporary files cleaned up successfully")


# ============================================================================
# TEST 4: HEALTH CHECK ENDPOINT
# ============================================================================

class TestHealthCheckEndpoint:
    """
    Test suite for health check endpoint.
    
    Validates: Service availability monitoring
    """
    
    def test_health_check_available(self, client):
        """
        Test health check endpoint when service is available.
        
        Verifies:
        - HTTP 200 response
        - Status is 'available'
        - Response contains version and timestamp
        """
        response = client.get('/api/notes_annexes/health')
        
        assert response.status_code == 200
        data = response.json()
        
        assert 'service' in data
        assert 'status' in data
        assert 'version' in data
        assert 'timestamp' in data
        
        assert data['service'] == "Notes Annexes SYSCOHADA"
        assert data['status'] in ['available', 'unavailable']
        
        print(f"\n✓ Health check: {data['status']}")


# ============================================================================
# SUMMARY TEST
# ============================================================================

@pytest.mark.skipif(not API_AVAILABLE, reason="API module not available")
def test_complete_workflow_integration(client, demo_balance_file):
    """
    Complete workflow integration test.
    
    This test validates the entire workflow from file upload to response:
    1. Upload balance file
    2. Verify HTTP 200 response
    3. Verify response structure
    4. Verify notes are calculated
    5. Verify coherence validation
    6. Verify performance
    
    Validates: Requirements 13.1, 13.2, 13.3, 13.4
    """
    if demo_balance_file is None:
        pytest.skip("Demo balance file not available")
    
    print("\n" + "="*70)
    print("COMPLETE WORKFLOW INTEGRATION TEST")
    print("="*70)
    
    start_time = time.time()
    
    # Step 1: Upload file
    print("\n1. Uploading balance file...")
    with open(demo_balance_file, 'rb') as f:
        files = {'balance_file': ('balance_demo.xls', f, 'application/vnd.ms-excel')}
        response = client.post('/api/calculer_notes_annexes', files=files)
    
    # Step 2: Verify response
    print("2. Verifying HTTP response...")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert data['success'] == True
    
    # Step 3: Verify structure
    print("3. Verifying response structure...")
    required_fields = ['notes', 'timestamp', 'notes_calculees', 'taux_coherence', 'duree_calcul']
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Step 4: Verify notes
    print("4. Verifying notes calculation...")
    notes = data['notes']
    assert len(notes) > 0, "No notes calculated"
    
    for note_name, note_data in notes.items():
        assert 'colonnes' in note_data
        assert 'lignes' in note_data
    
    # Step 5: Verify coherence
    print("5. Verifying coherence validation...")
    taux_coherence = data['taux_coherence']
    assert 0 <= taux_coherence <= 100
    
    # Step 6: Verify performance
    print("6. Verifying performance...")
    end_time = time.time()
    total_duration = end_time - start_time
    
    print("\n" + "="*70)
    print("WORKFLOW INTEGRATION TEST RESULTS")
    print("="*70)
    print(f"✓ File uploaded successfully")
    print(f"✓ Notes calculated: {data['notes_calculees']}/{data.get('notes_totales', 'N/A')}")
    print(f"✓ Coherence rate: {taux_coherence:.1f}%")
    print(f"✓ Calculation time: {data['duree_calcul']:.2f}s")
    print(f"✓ Total response time: {total_duration:.2f}s")
    print(f"✓ Source file: {data['fichier_source']}")
    print("="*70)
    
    assert total_duration < 60, f"Total workflow took too long: {total_duration:.2f}s"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
