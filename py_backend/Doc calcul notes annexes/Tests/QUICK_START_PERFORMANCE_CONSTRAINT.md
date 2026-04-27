# Quick Start: Performance Constraint Property Test

## What This Test Does

Validates that the system calculates all 33 SYSCOHADA notes in **less than 30 seconds** with **single balance loading**.

## Prerequisites

1. Demo balance file must exist:
   ```
   py_backend/P000 -BALANCE DEMO N_N-1_N-2.xls
   ```

2. Python dependencies installed:
   ```bash
   pip install pytest hypothesis pandas openpyxl
   ```

## Run the Test

### Option 1: Run All Tests (Recommended First Time)

```bash
cd "py_backend/Doc calcul notes annexes/Tests"
pytest test_performance_constraint.py -v
```

### Option 2: Run Only Fast Unit Tests

```bash
pytest test_performance_constraint.py -v -m "not slow"
```

### Option 3: Run Only Slow Property Tests

```bash
pytest test_performance_constraint.py -v -m "slow"
```

### Option 4: Run with Detailed Output

```bash
pytest test_performance_constraint.py -v -s
```

## Expected Results

### ✅ Success Output

```
test_performance_constraint.py::test_property_performance_constraint_with_demo_balance PASSED
✓ Performance validée: 18.45s < 30s
✓ Notes calculées: 33/33

test_performance_constraint.py::test_property_balance_caching_performance PASSED
✓ Cache validé:
  - Premier chargement: 0.8234s
  - Chargement 2 (cache): 0.0001s

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

======================== 6 passed in 45.23s ========================
```

### ❌ Failure Example

```
FAILED test_performance_constraint.py::test_property_performance_constraint_with_demo_balance
AssertionError: Contrainte de performance non respectée: 35.67s > 30s.
Le système doit calculer les 33 notes en moins de 30 secondes.
```

## What Each Test Validates

| Test | Validates | Time |
|------|-----------|------|
| `test_property_performance_constraint_with_demo_balance` | Complete 33 notes < 30s | ~20s |
| `test_property_balance_caching_performance` | Cache works correctly | ~5s |
| `test_property_performance_scales_with_notes` | Linear scaling | ~15s |
| `test_property_performance_memory_efficiency` | Single load, no duplication | ~5s |
| `test_performance_constraint_unit_simple` | 3 notes < 5s | ~3s |
| `test_balance_caching_unit` | Cache 10x faster | ~2s |

## Troubleshooting

### Problem: "Fichier de balance démo introuvable"

**Solution:** Ensure the balance file exists:
```bash
# Check if file exists
ls "py_backend/P000 -BALANCE DEMO N_N-1_N-2.xls"

# If missing, copy from the correct location
```

### Problem: "Performance constraint not met (> 30s)"

**Possible causes:**
1. Slow disk I/O
2. Insufficient memory
3. Other processes consuming CPU
4. Missing calculator scripts

**Solutions:**
- Close other applications
- Run on a faster machine
- Check that all 33 calculator scripts exist in `Scripts/` folder

### Problem: "ModuleNotFoundError: No module named 'calcul_notes_annexes_main'"

**Solution:** Run from the correct directory:
```bash
cd "py_backend/Doc calcul notes annexes/Tests"
pytest test_performance_constraint.py -v
```

### Problem: Tests are too slow

**Solution:** Run only fast unit tests:
```bash
pytest test_performance_constraint.py -v -m "not slow"
```

## Understanding the Output

### Performance Metrics

```
✓ Performance validée: 18.45s < 30s
```
- **18.45s:** Actual execution time
- **< 30s:** Required constraint
- **✓:** Test passed

### Cache Metrics

```
✓ Cache validé:
  - Premier chargement: 0.8234s
  - Chargement 2 (cache): 0.0001s
```
- **0.8234s:** Time to load from disk
- **0.0001s:** Time to retrieve from cache (8000x faster!)

### Scaling Metrics

```
✓ Évolutivité validée:
  - 5 notes: 2.34s
  - 10 notes: 4.67s
  - 20 notes: 9.12s
```
- Shows linear scaling (doubling notes ≈ doubles time)
- Good performance characteristic

## Next Steps

After this test passes:

1. ✅ **Task 21.4 Complete** - Performance constraint validated
2. ➡️ **Task 21.5** - Write property test for calculation caching (optional)
3. ➡️ **Task 21.6** - Write integration test for all 33 notes (optional)

## Related Documentation

- `PROPERTY_TEST_PERFORMANCE_CONSTRAINT_SUMMARY.md` - Detailed test documentation
- `test_coherence_integration.py` - Coherence validation tests
- `test_trace_integration.py` - Trace generation tests
- `QUICK_START_ORCHESTRATOR.md` - Orchestrator usage guide

## Quick Commands Reference

```bash
# Run all tests
pytest test_performance_constraint.py -v

# Run fast tests only
pytest test_performance_constraint.py -v -m "not slow"

# Run with statistics
pytest test_performance_constraint.py -v --hypothesis-show-statistics

# Run with detailed output
pytest test_performance_constraint.py -v -s

# Run specific test
pytest test_performance_constraint.py::test_performance_constraint_unit_simple -v
```

## Success Checklist

- [ ] All 6 tests pass
- [ ] Performance < 30 seconds
- [ ] Cache works (10x+ speedup)
- [ ] Scaling is linear
- [ ] Memory efficiency validated
- [ ] No errors or warnings

---

**Property Validated:** ✅ Property 18 - Performance Constraint  
**Requirements Validated:** ✅ 12.1, 12.2  
**Test File:** `test_performance_constraint.py`
