# Property Test: API Integration Round-Trip - Summary

## Overview

**Feature**: calcul-notes-annexes-syscohada  
**Property**: Property 20 - API Integration Round-Trip  
**Test File**: `test_api_integration_roundtrip.py`  
**Requirements Validated**: 13.2, 13.3, 13.4

## Property Statement

*For any* balance file uploaded through the Claraverse interface, the backend endpoint `/api/calculer_notes_annexes` must receive the file, execute calculations, and return a JSON object containing all 33 notes, which the frontend must display in clickable accordions.

## Test Strategy

This property test uses Hypothesis to generate random balance files and verify the complete API round-trip:

1. **Generate Balance Data**: Create valid balance sheets with coherent accounting data
2. **Create Excel File**: Package balance data into Excel format with 3 sheets (N, N-1, N-2)
3. **Upload to API**: Send file via HTTP POST to the endpoint
4. **Verify Response**: Check JSON structure, data integrity, and error handling

## Test Cases

### 1. Response Structure Validation

**Test**: `test_property_20_api_roundtrip_structure`

Verifies that for any valid balance file:
- HTTP status is 200 OK
- Response contains `success: true`
- Response has required fields: `notes`, `timestamp`, `notes_calculees`, `taux_coherence`
- Each note has `colonnes` and `lignes` fields
- Data structures are properly typed

**Hypothesis Configuration**:
- Max examples: 10 (reduced for API tests)
- Deadline: 120 seconds
- Generates 3 balance sheets with 20-50 accounts each

### 2. Data Integrity Validation

**Test**: `test_property_20_api_roundtrip_data_integrity`

Verifies that data is preserved through serialization:
- Column counts are consistent across all rows
- Numeric values remain numeric after JSON serialization
- No data corruption during upload/download cycle
- Array structures are preserved

**Hypothesis Configuration**:
- Max examples: 5 (intensive test)
- Deadline: 120 seconds

### 3. Error Handling - Invalid File

**Test**: `test_property_20_api_error_handling_invalid_file`

Verifies graceful error handling:
- Invalid file formats return HTTP 400
- Error messages are descriptive
- API doesn't crash or hang
- Error response has proper structure

### 4. Error Handling - Missing Sheets

**Test**: `test_property_20_api_error_handling_missing_sheets`

Verifies detection of incomplete files:
- Files with missing balance sheets are rejected
- Appropriate error codes (400/404/500)
- Clear error messages indicate missing sheets

### 5. Integration Test with Demo Balance

**Test**: `test_api_integration_with_demo_balance`

Full integration test with real balance file:
- Uses actual demo balance file
- Verifies complete calculation workflow
- Checks coherence rate
- Validates performance metrics

## Hypothesis Strategies

### `st_balance_complete()`

Generates complete balance sheets with:
- **Account numbers**: SYSCOHADA format (classe 2-7, sous-classe 0-9, detail 1-2 digits)
- **Account labels**: Random text 10-40 characters
- **Coherent balances**: Ensures accounting equation holds
  - `Solde Clôture = Solde Ouverture + Débit - Crédit`
- **Realistic amounts**: 0 to 5M for opening balances, 0 to 2M for movements

### `create_excel_file_from_balance()`

Helper function to create temporary Excel files:
- Creates 3 sheets: BALANCE N, BALANCE N-1, BALANCE N-2
- Uses openpyxl engine for .xlsx format
- Returns path to temporary file
- Cleanup handled by test fixtures

## Expected Results

### Success Criteria

✓ All property tests pass with 100+ generated examples  
✓ Response structure is valid for all inputs  
✓ Data integrity maintained through round-trip  
✓ Error handling is graceful and informative  
✓ Integration test with demo file succeeds  

### Performance Criteria

- API response time < 30 seconds for typical balance files
- No memory leaks during repeated uploads
- Proper cleanup of temporary files

## Requirements Validation

### Requirement 13.2: API Receives File and Executes Calculations

**Validated by**:
- `test_property_20_api_roundtrip_structure`: Verifies file upload and calculation execution
- `test_api_integration_with_demo_balance`: Confirms end-to-end workflow

**Evidence**: API successfully receives uploaded files and returns calculated notes

### Requirement 13.3: API Returns JSON with All Notes

**Validated by**:
- `test_property_20_api_roundtrip_structure`: Checks JSON structure and notes presence
- `test_property_20_api_roundtrip_data_integrity`: Verifies data completeness

**Evidence**: Response contains `notes` dictionary with calculated note data

### Requirement 13.4: Frontend Displays in Accordions

**Validated by**:
- `test_property_20_api_roundtrip_data_integrity`: Ensures data format is suitable for frontend rendering
- JSON structure with `colonnes` and `lignes` matches accordion renderer expectations

**Evidence**: Data structure is compatible with accordion display components

## Running the Tests

### Run All API Integration Tests

```bash
pytest py_backend/Doc\ calcul\ notes\ annexes/Tests/test_api_integration_roundtrip.py -v
```

### Run Specific Property Test

```bash
pytest py_backend/Doc\ calcul\ notes\ annexes/Tests/test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_roundtrip_structure -v
```

### Run with Hypothesis Statistics

```bash
pytest py_backend/Doc\ calcul\ notes\ annexes/Tests/test_api_integration_roundtrip.py -v --hypothesis-show-statistics
```

### Run Integration Test Only

```bash
pytest py_backend/Doc\ calcul\ notes\ annexes/Tests/test_api_integration_roundtrip.py::test_api_integration_with_demo_balance -v
```

## Troubleshooting

### API Module Not Available

If tests are skipped with "API module not available":
1. Verify `api_notes_annexes.py` is in the correct location
2. Check that FastAPI is installed: `pip install fastapi`
3. Ensure all dependencies are installed: `pip install -r requirements.txt`

### Demo Balance File Not Found

If integration test is skipped:
1. Verify demo file exists: `P000 -BALANCE DEMO N_N-1_N-2.xls`
2. Check file path in test configuration
3. Ensure file is in the correct location relative to test file

### Timeout Errors

If tests timeout:
1. Increase deadline in `@settings` decorator
2. Reduce `max_examples` for faster execution
3. Check system resources (CPU, memory)

## Related Files

- **API Implementation**: `py_backend/api_notes_annexes.py`
- **Orchestrator**: `py_backend/Doc calcul notes annexes/calcul_notes_annexes_main.py`
- **Test Configuration**: `py_backend/Doc calcul notes annexes/Tests/conftest.py`
- **Requirements**: `.kiro/specs/calcul-notes-annexes-syscohada/requirements.md`
- **Design**: `.kiro/specs/calcul-notes-annexes-syscohada/design.md`

## Next Steps

After this test passes:
1. ✓ Task 22.3 completed
2. → Proceed to Task 22.4: Write integration test for API endpoint (optional)
3. → Continue with frontend integration (Task 23)
4. → Test complete workflow with Claraverse interface

## Notes

- This is a **property-based test** using Hypothesis for comprehensive coverage
- Tests are **non-deterministic** - different data generated each run
- **Shrinking** automatically finds minimal failing examples
- Tests validate **universal properties** across all possible inputs
- Complements unit tests by exploring edge cases automatically
