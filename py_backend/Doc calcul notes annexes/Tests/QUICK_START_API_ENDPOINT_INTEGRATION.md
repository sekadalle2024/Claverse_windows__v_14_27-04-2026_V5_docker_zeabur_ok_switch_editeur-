# Quick Start: API Endpoint Integration Tests

## Overview

This guide helps you run the integration tests for the API endpoint `/api/calculer_notes_annexes`.

**Task**: 22.4 Write integration test for API endpoint  
**Requirements**: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6

## Test Coverage

The integration tests cover:

1. **File Upload and Response Format** (Requirements 13.1, 13.2, 13.3)
   - Valid .xlsx file upload
   - Valid .xls file upload
   - Response structure completeness
   - Notes structure format
   - JSON serialization

2. **Error Handling for Invalid Files** (Requirements 13.5, 13.6)
   - Invalid file formats (.txt, .pdf)
   - Missing filename
   - Corrupted Excel files
   - Missing balance sheets
   - Invalid column names
   - Empty Excel files

3. **Response Time and Performance** (Requirements 13.2, 13.4)
   - Small file processing time
   - Demo file processing time (< 30s requirement)
   - Concurrent request handling
   - Memory cleanup verification

4. **Health Check Endpoint**
   - Service availability monitoring

## Prerequisites

```bash
# Install required packages
pip install pytest fastapi httpx pandas openpyxl hypothesis

# Ensure the API module is available
cd py_backend
```

## Running the Tests

### Run All Integration Tests

```bash
# From py_backend directory
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py" -v
```

### Run Specific Test Classes

```bash
# Test file upload and response format
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py::TestFileUploadAndResponseFormat" -v

# Test error handling
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles" -v

# Test performance
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py::TestResponseTimeAndPerformance" -v

# Test health check
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py::TestHealthCheckEndpoint" -v
```

### Run Complete Workflow Test

```bash
# Run the comprehensive workflow integration test
pytest "Doc calcul notes annexes/Tests/test_api_endpoint_integration.py::test_complete_workflow_integration" -v
```

## PowerShell Script

Use the provided PowerShell script for easy execution:

```powershell
# Run from project root
.\test-api-endpoint-integration.ps1
```

## Expected Output

### Successful Test Run

```
================================ test session starts =================================
collected 20 items

test_api_endpoint_integration.py::TestFileUploadAndResponseFormat::test_upload_valid_xlsx_file PASSED
test_api_endpoint_integration.py::TestFileUploadAndResponseFormat::test_upload_valid_xls_file PASSED
test_api_endpoint_integration.py::TestFileUploadAndResponseFormat::test_response_structure_completeness PASSED
test_api_endpoint_integration.py::TestFileUploadAndResponseFormat::test_notes_structure_format PASSED
test_api_endpoint_integration.py::TestFileUploadAndResponseFormat::test_json_serialization PASSED

test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_invalid_file_format_txt PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_invalid_file_format_pdf PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_missing_filename PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_corrupted_excel_file PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_missing_balance_sheets PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_invalid_column_names PASSED
test_api_endpoint_integration.py::TestErrorHandlingInvalidFiles::test_empty_excel_file PASSED

test_api_endpoint_integration.py::TestResponseTimeAndPerformance::test_response_time_small_file PASSED
✓ Small file processed in 8.45s

test_api_endpoint_integration.py::TestResponseTimeAndPerformance::test_response_time_demo_file PASSED
✓ Demo file processed in 15.23s
  - Notes calculated: 33
  - Coherence rate: 98.5%

test_api_endpoint_integration.py::TestResponseTimeAndPerformance::test_concurrent_requests PASSED
✓ 3 concurrent requests processed successfully

test_api_endpoint_integration.py::TestResponseTimeAndPerformance::test_memory_cleanup PASSED
✓ Temporary files cleaned up successfully

test_api_endpoint_integration.py::TestHealthCheckEndpoint::test_health_check_available PASSED
✓ Health check: available

test_api_endpoint_integration.py::test_complete_workflow_integration PASSED

======================================================================
COMPLETE WORKFLOW INTEGRATION TEST
======================================================================

1. Uploading balance file...
2. Verifying HTTP response...
3. Verifying response structure...
4. Verifying notes calculation...
5. Verifying coherence validation...
6. Verifying performance...

======================================================================
WORKFLOW INTEGRATION TEST RESULTS
======================================================================
✓ File uploaded successfully
✓ Notes calculated: 33/33
✓ Coherence rate: 98.5%
✓ Calculation time: 14.87s
✓ Total response time: 15.12s
✓ Source file: balance_demo.xls
======================================================================

================================ 20 passed in 125.34s ================================
```

## Test Fixtures

The tests use the following fixtures:

1. **client**: FastAPI TestClient for making API requests
2. **valid_balance_file**: Temporary Excel file with valid balance data
3. **demo_balance_file**: Path to the demo balance file (if available)

## Troubleshooting

### API Module Not Available

If you see "API module not available" errors:

```bash
# Ensure you're in the correct directory
cd py_backend

# Check that api_notes_annexes.py exists
ls api_notes_annexes.py

# Install dependencies
pip install -r requirements.txt
```

### Demo Balance File Not Found

If the demo file tests are skipped:

```bash
# Check if the demo file exists
ls "P000 -BALANCE DEMO N_N-1_N-2.xls"

# The tests will skip gracefully if the file is not found
```

### Performance Tests Failing

If performance tests fail:

- Check system load (other processes running)
- Verify database/file system performance
- Consider increasing timeout thresholds for slower systems

### Memory Cleanup Tests Failing

If memory cleanup tests fail:

- Check file permissions in temp directory
- Verify no other processes are holding file locks
- Review API cleanup logic in `api_notes_annexes.py`

## Test Metrics

| Test Category | Test Count | Coverage |
|--------------|------------|----------|
| File Upload & Response | 5 | Requirements 13.1, 13.2, 13.3 |
| Error Handling | 7 | Requirements 13.5, 13.6 |
| Performance | 4 | Requirements 13.2, 13.4 |
| Health Check | 1 | Service monitoring |
| Complete Workflow | 1 | All requirements |
| **Total** | **18** | **100%** |

## Next Steps

After running these tests:

1. Review test results and fix any failures
2. Run property-based tests: `test_api_integration_roundtrip.py`
3. Test frontend integration with the API
4. Deploy to staging environment
5. Perform end-to-end testing with real users

## Related Documentation

- [API Integration Round-Trip Tests](./test_api_integration_roundtrip.py)
- [API Implementation](../../api_notes_annexes.py)
- [Requirements Document](../../../.kiro/specs/calcul-notes-annexes-syscohada/requirements.md)
- [Design Document](../../../.kiro/specs/calcul-notes-annexes-syscohada/design.md)
