# Quick Start: API Integration Round-Trip Property Test

## What This Test Does

Validates that the API endpoint `/api/calculer_notes_annexes` correctly handles file uploads, calculates notes, and returns valid JSON responses for **any** balance file.

## Requirements

- Python 3.9+
- FastAPI
- Hypothesis
- pytest
- pandas
- openpyxl

## Installation

```bash
# Install dependencies
pip install fastapi hypothesis pytest pandas openpyxl python-multipart

# Or use requirements file
pip install -r requirements.txt
```

## Run the Test

### Quick Test (5 examples)

```bash
cd py_backend
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py" -v
```

### Full Test (100 examples)

```bash
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py" -v --hypothesis-show-statistics
```

### Run Specific Test

```bash
# Test response structure
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_roundtrip_structure" -v

# Test data integrity
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_roundtrip_data_integrity" -v

# Test error handling
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_error_handling_invalid_file" -v

# Integration test with demo file
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py::test_api_integration_with_demo_balance" -v
```

## Expected Output

```
============================= test session starts ==============================
collected 5 items

test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_roundtrip_structure PASSED [ 20%]
test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_roundtrip_data_integrity PASSED [ 40%]
test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_error_handling_invalid_file PASSED [ 60%]
test_api_integration_roundtrip.py::TestAPIIntegrationRoundTrip::test_property_20_api_error_handling_missing_sheets PASSED [ 80%]
test_api_integration_roundtrip.py::test_api_integration_with_demo_balance PASSED [100%]

✓ API Integration Test Passed:
  - Notes calculated: 33
  - Coherence rate: 98.5%
  - Duration: 12.3s

============================== 5 passed in 45.23s ===============================
```

## What Gets Tested

### 1. Response Structure ✓
- HTTP 200 status code
- JSON with `success: true`
- Required fields: `notes`, `timestamp`, `taux_coherence`
- Each note has `colonnes` and `lignes`

### 2. Data Integrity ✓
- Column counts consistent
- Numeric values preserved
- No data corruption
- Array structures intact

### 3. Error Handling ✓
- Invalid files return HTTP 400
- Missing sheets detected
- Descriptive error messages
- No crashes or hangs

### 4. Integration ✓
- Real balance file processing
- Complete calculation workflow
- Coherence validation
- Performance metrics

## Troubleshooting

### "API module not available"

```bash
# Check FastAPI installation
pip install fastapi python-multipart

# Verify api_notes_annexes.py exists
ls py_backend/api_notes_annexes.py
```

### "Demo balance file not found"

```bash
# Check file location
ls "py_backend/P000 -BALANCE DEMO N_N-1_N-2.xls"

# Or skip integration test
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py" -v -k "not demo_balance"
```

### Tests timeout

```bash
# Increase timeout
pytest "Doc calcul notes annexes/Tests/test_api_integration_roundtrip.py" -v --timeout=300
```

## Understanding the Output

### Hypothesis Statistics

When using `--hypothesis-show-statistics`:

```
- test_property_20_api_roundtrip_structure:
  - Passed: 10 examples
  - Shrinks: 0
  - Duration: 23.4s
```

- **Examples**: Number of random inputs tested
- **Shrinks**: Minimal failing examples found (0 = all passed)
- **Duration**: Total test time

### Property Test Results

✓ **PASSED** = Property holds for all generated examples  
✗ **FAILED** = Property violated, minimal example shown  
⊘ **SKIPPED** = Test skipped (missing dependencies)

## Next Steps

1. ✓ Verify all tests pass
2. → Review test coverage report
3. → Run integration test with demo file
4. → Proceed to frontend integration (Task 23)

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest test_api_integration_roundtrip.py -v` | Run all tests |
| `pytest test_api_integration_roundtrip.py -v -k structure` | Test structure only |
| `pytest test_api_integration_roundtrip.py -v -k integrity` | Test data integrity |
| `pytest test_api_integration_roundtrip.py -v -k error` | Test error handling |
| `pytest test_api_integration_roundtrip.py -v -k demo` | Integration test |
| `pytest test_api_integration_roundtrip.py --hypothesis-show-statistics` | Show Hypothesis stats |

## Files Created

- `test_api_integration_roundtrip.py` - Property test implementation
- `PROPERTY_TEST_API_INTEGRATION_ROUNDTRIP_SUMMARY.md` - Detailed documentation
- `QUICK_START_API_INTEGRATION_ROUNDTRIP.md` - This file

## Property Validated

**Property 20**: For any balance file uploaded, the API receives it, calculates notes, and returns valid JSON containing all notes for frontend display.

**Requirements**: 13.2, 13.3, 13.4
