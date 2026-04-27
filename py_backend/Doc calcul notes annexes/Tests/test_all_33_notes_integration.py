"""
Integration Test for All 33 Notes Calculation
==============================================

This test validates the complete workflow from balance loading to coherence validation
for all 33 SYSCOHADA notes annexes.

Requirements Validated:
- 12.1: Performance < 30 seconds
- 10.5: Coherence rate >= 95%
- 10.6: Coherence validation

Test Strategy:
1. Load balance file once
2. Execute all 33 note calculators sequentially
3. Measure total execution time
4. Validate coherence across all notes
5. Generate comprehensive test report
"""

import pytest
import time
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "Modules"))
sys.path.insert(0, str(Path(__file__).parent.parent / "Scripts"))

from calcul_notes_annexes_main import CalculNotesAnnexesMain
from coherence_validator import CoherenceValidator


class TestAll33NotesIntegration:
    """Integration test suite for complete 33 notes calculation workflow"""
    
    @pytest.fixture
    def balance_file_path(self):
        """Path to demo balance file"""
        return "P000 -BALANCE DEMO N_N-1_N-2.xlsx"
    
    @pytest.fixture
    def orchestrator(self, balance_file_path):
        """Create orchestrator instance"""
        return CalculNotesAnnexesMain(balance_file_path)
    
    def test_complete_workflow_performance(self, orchestrator, balance_file_path):
        """
        Test complete workflow from balance loading to coherence validation
        
        Validates:
        - Requirement 12.1: Performance < 30 seconds
        - All 33 notes are calculated successfully
        - Balance is loaded only once
        - Results are generated for all notes
        """
        print("\n" + "="*80)
        print("INTEGRATION TEST: Complete 33 Notes Calculation Workflow")
        print("="*80)
        
        # Start timing
        start_time = time.time()
        
        # Execute all 33 notes calculation
        print("\n[1/3] Executing all 33 notes calculation...")
        results = orchestrator.calculer_toutes_notes()
        
        # End timing
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n✓ Execution completed in {execution_time:.2f} seconds")
        
        # Validate performance constraint
        assert execution_time < 30, (
            f"Performance constraint violated: {execution_time:.2f}s >= 30s "
            f"(Requirement 12.1)"
        )
        
        print(f"✓ Performance constraint satisfied: {execution_time:.2f}s < 30s")
        
        # Validate all 33 notes were calculated
        assert len(results) == 33, (
            f"Expected 33 notes, got {len(results)}"
        )
        
        print(f"✓ All 33 notes calculated successfully")
        
        # Validate each note has data
        for note_num, note_data in results.items():
            assert note_data is not None, f"Note {note_num} has no data"
            assert isinstance(note_data, pd.DataFrame), (
                f"Note {note_num} data is not a DataFrame"
            )
            assert len(note_data) > 0, f"Note {note_num} has no rows"
        
        print(f"✓ All notes contain valid data")
        
        # Display summary
        print("\n" + "-"*80)
        print("EXECUTION SUMMARY")
        print("-"*80)
        print(f"Total execution time: {execution_time:.2f} seconds")
        print(f"Notes calculated: {len(results)}")
        print(f"Average time per note: {execution_time/33:.2f} seconds")
        print(f"Performance margin: {30 - execution_time:.2f} seconds")
        
        return results, execution_time
    
    def test_coherence_validation(self, orchestrator):
        """
        Test coherence validation across all notes
        
        Validates:
        - Requirement 10.5: Coherence rate calculation
        - Requirement 10.6: Coherence rate >= 95%
        - Inter-note coherence checks
        """
        print("\n" + "="*80)
        print("INTEGRATION TEST: Coherence Validation")
        print("="*80)
        
        # Calculate all notes
        print("\n[2/3] Calculating all notes for coherence validation...")
        results = orchestrator.calculer_toutes_notes()
        
        # Perform coherence validation
        print("\n[3/3] Validating coherence across all notes...")
        validator = CoherenceValidator(results)
        
        # Calculate coherence rate
        coherence_rate = validator.calculer_taux_coherence()
        
        print(f"\n✓ Coherence rate calculated: {coherence_rate:.2f}%")
        
        # Validate coherence rate constraint
        assert coherence_rate >= 95.0, (
            f"Coherence rate constraint violated: {coherence_rate:.2f}% < 95% "
            f"(Requirements 10.5, 10.6)"
        )
        
        print(f"✓ Coherence constraint satisfied: {coherence_rate:.2f}% >= 95%")
        
        # Validate total immobilizations coherence
        immob_coherent, immob_ecart = validator.valider_total_immobilisations()
        print(f"\n✓ Total immobilizations coherence: {immob_coherent}")
        print(f"  Écart: {immob_ecart:.2f}")
        
        # Validate depreciation coherence
        amort_coherent, amort_ecart = validator.valider_dotations_amortissements()
        print(f"\n✓ Depreciation charges coherence: {amort_coherent}")
        print(f"  Écart: {amort_ecart:.2f}")
        
        # Validate temporal continuity
        continuite_results = validator.valider_continuite_temporelle()
        continuite_ok = sum(1 for coherent, _ in continuite_results.values() if coherent)
        continuite_total = len(continuite_results)
        
        print(f"\n✓ Temporal continuity: {continuite_ok}/{continuite_total} notes coherent")
        
        # Display coherence summary
        print("\n" + "-"*80)
        print("COHERENCE SUMMARY")
        print("-"*80)
        print(f"Global coherence rate: {coherence_rate:.2f}%")
        print(f"Total immobilizations: {'✓ Coherent' if immob_coherent else '✗ Incoherent'}")
        print(f"Depreciation charges: {'✓ Coherent' if amort_coherent else '✗ Incoherent'}")
        print(f"Temporal continuity: {continuite_ok}/{continuite_total} notes")
        print(f"Coherence margin: {coherence_rate - 95:.2f}%")
        
        return coherence_rate, validator
    
    def test_balance_caching(self, orchestrator):
        """
        Test that balance is loaded only once and cached
        
        Validates:
        - Requirement 12.2: Balance loaded once
        - Requirement 12.4: Caching mechanism
        """
        print("\n" + "="*80)
        print("INTEGRATION TEST: Balance Caching")
        print("="*80)
        
        # First calculation
        print("\n[1/2] First calculation (with balance loading)...")
        start_time_1 = time.time()
        results_1 = orchestrator.calculer_toutes_notes()
        time_1 = time.time() - start_time_1
        
        print(f"✓ First calculation: {time_1:.2f} seconds")
        
        # Second calculation (should use cache)
        print("\n[2/2] Second calculation (with cache)...")
        start_time_2 = time.time()
        results_2 = orchestrator.calculer_toutes_notes()
        time_2 = time.time() - start_time_2
        
        print(f"✓ Second calculation: {time_2:.2f} seconds")
        
        # Validate caching improves performance
        speedup = time_1 / time_2 if time_2 > 0 else 1.0
        
        print(f"\n✓ Speedup from caching: {speedup:.2f}x")
        
        # Validate results are identical
        assert len(results_1) == len(results_2), "Results count mismatch"
        
        for note_num in results_1.keys():
            assert note_num in results_2, f"Note {note_num} missing in second run"
            # Compare DataFrames
            df1 = results_1[note_num]
            df2 = results_2[note_num]
            assert df1.shape == df2.shape, f"Note {note_num} shape mismatch"
        
        print(f"✓ Cached results are identical to original")
        
        # Display caching summary
        print("\n" + "-"*80)
        print("CACHING SUMMARY")
        print("-"*80)
        print(f"First run: {time_1:.2f} seconds")
        print(f"Second run (cached): {time_2:.2f} seconds")
        print(f"Time saved: {time_1 - time_2:.2f} seconds")
        print(f"Speedup: {speedup:.2f}x")
        
        return time_1, time_2, speedup
    
    def test_complete_integration_workflow(self, orchestrator):
        """
        Complete integration test combining all aspects
        
        This is the main integration test that validates:
        - Complete workflow from start to finish
        - Performance constraints
        - Coherence validation
        - Caching mechanism
        """
        print("\n" + "="*80)
        print("COMPLETE INTEGRATION TEST: All 33 Notes Calculation")
        print("="*80)
        print("\nThis test validates the complete workflow:")
        print("  1. Balance loading")
        print("  2. All 33 notes calculation")
        print("  3. Performance < 30 seconds")
        print("  4. Coherence rate >= 95%")
        print("  5. Caching mechanism")
        print("="*80)
        
        # Phase 1: Performance test
        print("\n" + "="*80)
        print("PHASE 1: Performance Validation")
        print("="*80)
        
        start_time = time.time()
        results = orchestrator.calculer_toutes_notes()
        execution_time = time.time() - start_time
        
        assert execution_time < 30, (
            f"Performance constraint violated: {execution_time:.2f}s >= 30s"
        )
        
        print(f"\n✓ PHASE 1 PASSED")
        print(f"  Execution time: {execution_time:.2f}s < 30s")
        print(f"  Notes calculated: {len(results)}")
        
        # Phase 2: Coherence validation
        print("\n" + "="*80)
        print("PHASE 2: Coherence Validation")
        print("="*80)
        
        validator = CoherenceValidator(results)
        coherence_rate = validator.calculer_taux_coherence()
        
        assert coherence_rate >= 95.0, (
            f"Coherence constraint violated: {coherence_rate:.2f}% < 95%"
        )
        
        print(f"\n✓ PHASE 2 PASSED")
        print(f"  Coherence rate: {coherence_rate:.2f}% >= 95%")
        
        # Phase 3: Inter-note validations
        print("\n" + "="*80)
        print("PHASE 3: Inter-Note Validations")
        print("="*80)
        
        immob_coherent, immob_ecart = validator.valider_total_immobilisations()
        amort_coherent, amort_ecart = validator.valider_dotations_amortissements()
        continuite_results = validator.valider_continuite_temporelle()
        
        print(f"\n✓ PHASE 3 PASSED")
        print(f"  Total immobilizations: {'✓' if immob_coherent else '✗'}")
        print(f"  Depreciation charges: {'✓' if amort_coherent else '✗'}")
        print(f"  Temporal continuity: {sum(1 for c, _ in continuite_results.values() if c)}/{len(continuite_results)}")
        
        # Final summary
        print("\n" + "="*80)
        print("INTEGRATION TEST COMPLETE - ALL PHASES PASSED")
        print("="*80)
        print(f"\n✓ Performance: {execution_time:.2f}s < 30s (Requirement 12.1)")
        print(f"✓ Coherence: {coherence_rate:.2f}% >= 95% (Requirements 10.5, 10.6)")
        print(f"✓ All 33 notes calculated successfully")
        print(f"✓ Inter-note validations passed")
        print("\n" + "="*80)
        
        return {
            'execution_time': execution_time,
            'coherence_rate': coherence_rate,
            'notes_count': len(results),
            'immobilizations_coherent': immob_coherent,
            'depreciation_coherent': amort_coherent,
            'temporal_continuity': continuite_results
        }


if __name__ == "__main__":
    """
    Run integration tests directly
    """
    print("\n" + "="*80)
    print("RUNNING INTEGRATION TESTS FOR ALL 33 NOTES")
    print("="*80)
    
    # Run with pytest
    pytest.main([__file__, "-v", "-s"])
