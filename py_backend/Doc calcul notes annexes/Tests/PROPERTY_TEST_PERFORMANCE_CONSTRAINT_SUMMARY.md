# Property Test: Performance Constraint

## Overview

This property test validates **Property 18: Performance Constraint** from the design document.

**Property Statement:**
> For any complete calculation of all 33 notes with a standard balance file, the system must complete processing in less than 30 seconds, loading balances only once into memory.

**Validates Requirements:** 12.1, 12.2

## Test File

`test_performance_constraint.py`

## Property Tests Implemented

### 1. `test_property_performance_constraint_with_demo_balance()`

**Purpose:** Validates that the complete calculation of 33 notes completes within 30 seconds.

**Properties Verified:**
- ✓ Total execution time < 30 seconds
- ✓ All notes are calculated successfully
- ✓ Balances are cached after first load

**Test Strategy:**
- Uses the demo balance file (P000 -BALANCE DEMO N_N-1_N-2.xls)
- Measures total execution time for calculating all 33 notes
- Verifies cache is populated

**Expected Behavior:**
```python
duree < 30.0  # Must complete in less than 30 seconds
len(notes) > 0  # At least some notes calculated
orchestrateur.balances is not None  # Cache populated
```

### 2. `test_property_balance_caching_performance()`

**Purpose:** Validates that balances are loaded once and cached for subsequent operations.

**Properties Verified:**
- ✓ First load takes measurable time
- ✓ Subsequent loads are quasi-instantaneous (< 10% of first load)
- ✓ Balances remain in cache

**Test Strategy:**
- Uses Hypothesis to generate 2-3 execution iterations
- Measures time for each balance loading operation
- Compares first load vs cached loads

**Expected Behavior:**
```python
durees[0] > 0  # First load takes time
durees[i] < durees[0] * 0.1  # Cached loads are 10x faster
orchestrateur.balances is not None  # Cache persists
```

### 3. `test_property_performance_scales_with_notes()`

**Purpose:** Validates that performance scales linearly or sub-linearly with the number of notes.

**Properties Verified:**
- ✓ Time increases with number of notes
- ✓ Scaling is reasonable (not exponential)
- ✓ Time ratio ≤ 1.5x note count ratio

**Test Strategy:**
- Tests with subsets of 5, 10, and 20 notes
- Measures execution time for each subset
- Calculates scaling ratios

**Expected Behavior:**
```python
duree[i] >= duree[i-1]  # Time increases
ratio_temps <= ratio_notes * 1.5  # Reasonable scaling
```

### 4. `test_property_performance_memory_efficiency()`

**Purpose:** Validates that balances are loaded once and reused without duplication.

**Properties Verified:**
- ✓ Balances are None before first load
- ✓ Balances are cached after load
- ✓ Cache contains 3 DataFrames (N, N-1, N-2)
- ✓ Memory reference remains stable during calculations

**Test Strategy:**
- Checks balance state before and after loading
- Verifies cache structure (tuple of 3 DataFrames)
- Tracks memory reference ID to ensure no reloading

**Expected Behavior:**
```python
balances is None  # Before load
balances is tuple of 3 DataFrames  # After load
id(balances) == balances_ref  # Same reference throughout
```

## Unit Tests Implemented

### 1. `test_performance_constraint_unit_simple()`

**Purpose:** Simple unit test with 3 notes to verify basic performance.

**Validates:**
- Calculation of 3 notes completes in < 5 seconds
- At least one note is calculated successfully

### 2. `test_balance_caching_unit()`

**Purpose:** Unit test specifically for cache functionality.

**Validates:**
- First load populates cache
- Second load uses cache (10x faster)

## Hypothesis Configuration

```python
@settings(max_examples=5, deadline=None)
```

- **max_examples:** Limited to 5 for performance tests (they are slow)
- **deadline:** Disabled to allow long-running calculations

## Test Markers

```python
@pytest.mark.slow
```

Performance tests are marked as `slow` to allow selective execution:

```bash
# Run all tests except slow ones
pytest test_performance_constraint.py -v -m "not slow"

# Run only slow tests
pytest test_performance_constraint.py -v -m "slow"

# Run all tests
pytest test_performance_constraint.py -v
```

## Running the Tests

### Run all property tests:
```bash
cd "py_backend/Doc calcul notes annexes/Tests"
pytest test_performance_constraint.py -v
```

### Run with Hypothesis statistics:
```bash
pytest test_performance_constraint.py -v --hypothesis-show-statistics
```

### Run only fast unit tests:
```bash
pytest test_performance_constraint.py -v -m "not slow"
```

### Run with detailed output:
```bash
pytest test_performance_constraint.py -v -s
```

## Expected Output

```
test_performance_constraint.py::test_property_performance_constraint_with_demo_balance PASSED
✓ Performance validée: 18.45s < 30s
✓ Notes calculées: 33/33

test_performance_constraint.py::test_property_balance_caching_performance PASSED
✓ Cache validé:
  - Premier chargement: 0.8234s
  - Chargement 2 (cache): 0.0001s
  - Chargement 3 (cache): 0.0001s

test_performance_constraint.py::test_property_performance_scales_with_notes PASSED
✓ Évolutivité validée:
  - 5 notes: 2.34s
  - 10 notes: 4.67s
  - 20 notes: 9.12s

test_performance_constraint.py::test_property_performance_memory_efficiency PASSED
✓ Efficacité mémoire validée:
  - Balances chargées: 1 fois
  - Notes calculées: 3
  - Référence mémoire stable: Oui

test_performance_constraint.py::test_performance_constraint_unit_simple PASSED
✓ Test unitaire validé: 3 notes en 2.15s

test_performance_constraint.py::test_balance_caching_unit PASSED
✓ Cache validé: 0.8156s -> 0.0001s
```

## Dependencies

- **pytest:** Test framework
- **hypothesis:** Property-based testing library
- **pandas:** Data manipulation
- **time:** Performance measurement
- **calcul_notes_annexes_main:** Main orchestrator module

## Notes

1. **Performance tests are slow:** These tests calculate actual notes and measure real execution time, so they take longer than typical unit tests.

2. **Balance file required:** Tests require the demo balance file `P000 -BALANCE DEMO N_N-1_N-2.xls` to be present in the parent directory.

3. **Hypothesis examples limited:** Property tests use only 5 examples to keep test execution time reasonable.

4. **Markers for selective execution:** Use `-m "not slow"` to skip performance tests during rapid development.

5. **Cache validation:** Multiple tests verify that the balance caching mechanism works correctly, as this is critical for meeting the 30-second constraint.

## Success Criteria

✅ All property tests pass  
✅ Performance constraint (< 30s) is met  
✅ Balance caching works correctly  
✅ Performance scales reasonably with note count  
✅ Memory efficiency is maintained  

## Related Files

- `calcul_notes_annexes_main.py` - Main orchestrator being tested
- `test_coherence_integration.py` - Integration test for coherence validation
- `test_trace_integration.py` - Integration test for trace generation
- `.kiro/specs/calcul-notes-annexes-syscohada/design.md` - Property 18 definition
- `.kiro/specs/calcul-notes-annexes-syscohada/requirements.md` - Requirements 12.1, 12.2
