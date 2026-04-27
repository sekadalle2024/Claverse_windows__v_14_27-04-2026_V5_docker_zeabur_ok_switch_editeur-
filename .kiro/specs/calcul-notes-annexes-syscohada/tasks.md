# Implementation Plan: Calcul Automatique des Notes Annexes SYSCOHADA Révisé

## Overview

This implementation plan creates a modular Python system to automate the calculation and generation of 33 SYSCOHADA financial statement annexes. The system reads 8-column balance sheets for 3 fiscal years (N, N-1, N-2), extracts relevant accounts, performs calculations, and generates HTML/Excel outputs conforming to the official SYSCOHADA format. The architecture consists of 9 shared modules and 33 individual calculator scripts, with a main orchestrator coordinating execution and ensuring inter-note coherence validation.

## Tasks

- [x] 1. Set up project structure and core infrastructure
  - Create directory structure for modules, scripts, tests, and resources
  - Set up Python virtual environment with required dependencies (pandas, openpyxl, hypothesis, pytest, flask)
  - Create __init__.py files for proper package structure
  - Set up logging configuration (calcul_notes_annexes.log, calcul_notes_warnings.log, calcul_notes_errors.log)
  - _Requirements: 11.1, 11.2, 12.2_

- [x] 2. Implement Balance_Reader module
  - [x] 2.1 Create balance_reader.py with BalanceReader class
    - Implement __init__(fichier_balance: str) method
    - Implement charger_balances() method to load 3 balance sheets (N, N-1, N-2)
    - Implement detecter_onglets() method for automatic worksheet detection
    - Implement nettoyer_colonnes() method for column name normalization
    - Implement convertir_montants() method for numeric conversion with error handling
    - Define custom exceptions: BalanceNotFoundException, InvalidBalanceFormatException
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7_

  - [x] 2.2 Write property test for Balance_Reader
    - **Property 1: Balance Loading Completeness**
    - **Validates: Requirements 1.1, 1.2**

  - [x] 2.3 Write property test for column normalization
    - **Property 2: Column Name Normalization**
    - **Validates: Requirements 1.4**

  - [x] 2.4 Write property test for numeric conversion robustness
    - **Property 3: Numeric Conversion Robustness**
    - **Validates: Requirements 1.5, 1.6**


- [x] 3. Implement Account_Extractor module
  - [x] 3.1 Create account_extractor.py with AccountExtractor class
    - Implement __init__(balance: pd.DataFrame) method
    - Implement extraire_solde_compte(numero_compte: str) method returning 6 values dict
    - Implement extraire_comptes_multiples(racines: List[str]) method for summing multiple roots
    - Implement filtrer_par_racine(racine: str) method for filtering accounts
    - Handle missing accounts gracefully by returning zeros
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

  - [x] 3.2 Write property test for account filtering
    - **Property 4: Account Filtering by Root**
    - **Validates: Requirements 2.1, 2.5**

  - [x] 3.3 Write property test for account extraction completeness
    - **Property 5: Account Extraction Completeness**
    - **Validates: Requirements 2.2, 2.6**

  - [x] 3.4 Write property test for missing account handling
    - **Property 6: Missing Account Handling**
    - **Validates: Requirements 2.3, 8.1**

- [x] 4. Implement Movement_Calculator module
  - [x] 4.1 Create movement_calculator.py with MovementCalculator class
    - Implement calculer_solde_ouverture() method
    - Implement calculer_augmentations() method
    - Implement calculer_diminutions() method
    - Implement calculer_solde_cloture() method
    - Implement verifier_coherence() method with tolerance checking
    - Implement calculer_mouvements_amortissement() with sign inversion for depreciation accounts
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

  - [x] 4.2 Write property test for accounting equation coherence
    - **Property 7: Accounting Equation Coherence**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

  - [x] 4.3 Write property test for depreciation account sign inversion
    - **Property 8: Depreciation Account Sign Inversion**
    - **Validates: Requirements 3.7, 4.4, 4.5**

- [ ] 5. Implement VNC_Calculator module
  - [x] 5.1 Create vnc_calculator.py with VNCCalculator class
    - Implement calculer_vnc_ouverture() method
    - Implement calculer_vnc_cloture() method
    - Implement extraire_dotations() method for depreciation charges
    - Implement extraire_reprises() method for depreciation reversals
    - Implement valider_vnc() method to check VNC >= 0
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7_

  - [-] 5.2 Write property test for VNC calculation formula
    - **Property 9: VNC Calculation Formula**
    - **Validates: Requirements 4.1, 4.2, 4.6**

- [x] 6. Checkpoint - Ensure core calculation modules work correctly
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement HTML_Generator module
  - [x] 7.1 Create html_generator.py with HTMLGenerator class
    - Implement __init__(titre_note: str, numero_note: str) method
    - Implement generer_html(df: pd.DataFrame, colonnes_config: Dict) method
    - Implement generer_entetes() method for grouped headers
    - Implement generer_lignes() method with amount formatting
    - Implement formater_montant() method with thousand separators
    - Implement appliquer_style_css() method with SYSCOHADA styling
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_

  - [-] 7.2 Write property test for HTML generation conformity
    - **Property 11: HTML Generation Conformity**
    - **Validates: Requirements 6.2, 6.3, 6.4, 6.5, 6.6**

- [ ] 8. Implement Excel_Exporter module
  - [x] 8.1 Create excel_exporter.py with ExcelExporter class
    - Implement __init__(fichier_sortie: str) method
    - Implement exporter_note() method for single note export
    - Implement exporter_toutes_notes() method for batch export
    - Implement appliquer_formatage() method for borders, colors, numeric formats
    - Implement sauvegarder() method with timestamped filename
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [x] 8.2 Write property test for Excel export structure preservation
    - **Property 15: Excel Export Structure Preservation**
    - **Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**

- [ ] 9. Implement Mapping_Manager module
  - [x] 9.1 Create mapping_manager.py with MappingManager class
    - Implement __init__(fichier_json: str) method
    - Implement charger_correspondances() method with JSON validation
    - Implement obtenir_racines_compte() method for account root lookup
    - Implement valider_racines() method for numeric validation
    - Implement ajouter_correspondance() method for dynamic mapping updates
    - Define custom exception: InvalidJSONException
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7_

  - [x] 9.2 Write property test for mapping lookup consistency
    - **Property 12: Mapping Lookup Consistency**
    - **Validates: Requirements 7.2, 7.5, 7.7**

- [ ] 10. Implement Coherence_Validator module
  - [x] 10.1 Create coherence_validator.py with CoherenceValidator class
    - Implement __init__(notes: Dict[str, pd.DataFrame]) method
    - Implement valider_total_immobilisations() method
    - Implement valider_dotations_amortissements() method
    - Implement valider_continuite_temporelle() method
    - Implement calculer_taux_coherence() method
    - Implement generer_rapport_coherence() method for HTML report
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [x] 10.2 Write property test for inter-note coherence validation
    - **Property 16: Inter-Note Coherence Validation**
    - **Validates: Requirements 10.1, 10.2, 10.3**

  - [x] 10.3 Write property test for coherence rate calculation
    - **Property 17: Coherence Rate Calculation**
    - **Validates: Requirements 10.5, 10.6**

- [ ] 11. Implement Trace_Manager module
  - [x] 11.1 Create trace_manager.py with TraceManager class
    - Implement __init__(numero_note: str) method
    - Implement enregistrer_calcul() method for calculation tracing
    - Implement enregistrer_metadata() method for generation metadata
    - Implement sauvegarder_trace() method for JSON export
    - Implement exporter_csv() method for Excel analysis
    - Implement gerer_historique() method to keep last 10 traces
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7_

  - [x] 11.2 Write property test for calculation traceability
    - **Property 22: Calculation Traceability**
    - **Validates: Requirements 15.1, 15.2, 15.3, 15.4**

  - [x] 11.3 Write property test for trace history management
    - **Property 23: Trace History Management**
    - **Validates: Requirements 15.7**

  - [-] 11.4 Write property test for trace export format conversion
    - **Property 24: Trace Export Format Conversion**
    - **Validates: Requirements 15.6**

- [x] 12. Checkpoint - Ensure all shared modules are complete
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 13. Create calculator template and Note 3A implementation
  - [x] 13.1 Create calculateur_note_template.py as base template
    - Define CalculateurNote base class with common structure
    - Implement charger_balances() method using Balance_Reader
    - Implement calculer_ligne_note() method template
    - Implement generer_note() method template
    - Implement generer_html() method using HTML_Generator
    - Implement sauvegarder_html() method
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

  - [x] 13.2 Create calculer_note_3a.py for Immobilisations Incorporelles
    - Define mapping_comptes for accounts 21X (brut) and 281X/291X (amortissements)
    - Implement specific calculation logic for 4 lines (Frais R&D, Brevets, Logiciels, Autres)
    - Calculate 11 columns per line (brut ouverture/clôture, augmentations, diminutions, amort, dotations, reprises, VNC)
    - Generate HTML output with SYSCOHADA format
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 6.1, 6.2_

  - [x] 13.3 Write property test for script structure conformity
    - **Property 10: Script Structure Conformity**
    - **Validates: Requirements 5.2, 5.3, 5.4**

  - [x] 13.4 Write integration test for Note 3A complete calculation
    - Test complete workflow from balance loading to HTML generation
    - Verify all 11 columns calculated correctly
    - Verify coherence of accounting equations
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [ ] 14. Create calculators for Notes 3B-3E (Fixed Assets)
  - [x] 14.1 Create calculer_note_3b.py for Immobilisations Corporelles
    - Define mapping for accounts 22X (brut) and 282X/292X (amortissements)
    - Implement calculation for 9 lines (Terrains, Bâtiments, Installations, Matériel, etc.)
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 14.2 Create calculer_note_3c.py for Immobilisations Financières
    - Define mapping for accounts 26X and 27X
    - Implement calculation for financial investments
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 14.3 Create calculer_note_3d.py for Charges Immobilisées
    - Define mapping for accounts 20X
    - Implement calculation for deferred charges
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 14.4 Create calculer_note_3e.py for Écarts de Conversion Actif
    - Define mapping for accounts 47X
    - Implement calculation for foreign exchange differences
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 14.5 Write integration tests for Notes 3B-3E
    - Test each note's complete calculation workflow
    - Verify inter-note consistency for total immobilizations
    - _Requirements: 10.1, 10.2_

- [ ] 15. Create calculators for Notes 4-10 (Current Assets and Liabilities)
  - [x] 15.1 Create calculer_note_4.py for Stocks
    - Define mapping for accounts 3X
    - Implement calculation for inventory movements
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.2 Create calculer_note_5.py for Créances Clients
    - Define mapping for accounts 41X
    - Implement calculation for customer receivables
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.3 Create calculer_note_6.py for Autres Créances
    - Define mapping for accounts 42X, 43X, 44X, 45X
    - Implement calculation for other receivables
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.4 Create calculer_note_7.py for Trésorerie Actif
    - Define mapping for accounts 5X
    - Implement calculation for cash and cash equivalents
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.5 Create calculer_note_8.py for Capital
    - Define mapping for accounts 10X
    - Implement calculation for share capital movements
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.6 Create calculer_note_9.py for Réserves
    - Define mapping for accounts 11X
    - Implement calculation for reserves
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 15.7 Create calculer_note_10.py for Résultat
    - Define mapping for accounts 12X, 13X
    - Implement calculation for retained earnings
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 16. Checkpoint - Ensure asset and liability notes work correctly
  - Ensure all tests pass, ask the user if questions arise.

- [-] 17. Create calculators for Notes 11-20 (Provisions and Debts)
  - [x] 17.1 Create calculer_note_11.py for Provisions
    - Define mapping for accounts 19X
    - Implement calculation for provisions movements
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.2 Create calculer_note_12.py for Emprunts
    - Define mapping for accounts 16X
    - Implement calculation for loans and borrowings
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.3 Create calculer_note_13.py for Dettes Fournisseurs
    - Define mapping for accounts 40X
    - Implement calculation for supplier payables
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.4 Create calculer_note_14.py for Dettes Fiscales
    - Define mapping for accounts 44X
    - Implement calculation for tax liabilities
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.5 Create calculer_note_15.py for Dettes Sociales
    - Define mapping for accounts 42X, 43X
    - Implement calculation for social security liabilities
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.6 Create calculer_note_16.py for Autres Dettes
    - Define mapping for accounts 46X, 47X
    - Implement calculation for other liabilities
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.7 Create calculer_note_17.py for Trésorerie Passif
    - Define mapping for accounts 52X, 56X
    - Implement calculation for bank overdrafts
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.8 Create calculer_note_18.py for Charges Constatées d'Avance
    - Define mapping for accounts 476
    - Implement calculation for prepaid expenses
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.9 Create calculer_note_19.py for Produits Constatés d'Avance
    - Define mapping for accounts 477
    - Implement calculation for deferred income
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 17.10 Create calculer_note_20.py for Écarts de Conversion Passif
    - Define mapping for accounts 478
    - Implement calculation for foreign exchange differences (liabilities)
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 18. Create calculators for Notes 21-27 (Income Statement - Charges)
  - [x] 18.1 Create calculer_note_21.py for Achats de Marchandises
    - Define mapping for accounts 60X
    - Implement calculation for purchases of goods
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.2 Create calculer_note_22.py for Achats de Matières
    - Define mapping for accounts 601, 602
    - Implement calculation for raw materials purchases
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.3 Create calculer_note_23.py for Autres Achats
    - Define mapping for accounts 604, 605, 606, 607, 608
    - Implement calculation for other purchases
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.4 Create calculer_note_24.py for Services Extérieurs
    - Define mapping for accounts 61X, 62X
    - Implement calculation for external services
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.5 Create calculer_note_25.py for Charges de Personnel
    - Define mapping for accounts 66X
    - Implement calculation for personnel expenses
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.6 Create calculer_note_26.py for Dotations aux Amortissements
    - Define mapping for accounts 681X
    - Implement calculation for depreciation charges
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 18.7 Create calculer_note_27.py for Dotations aux Provisions
    - Define mapping for accounts 691X
    - Implement calculation for provision charges
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [ ] 19. Create calculators for Notes 28-33 (Income Statement - Produits)
  - [x] 19.1 Create calculer_note_28.py for Ventes de Marchandises
    - Define mapping for accounts 70X
    - Implement calculation for sales of goods
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 19.2 Create calculer_note_29.py for Ventes de Produits Finis
    - Define mapping for accounts 701, 702, 703
    - Implement calculation for sales of finished products
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 19.3 Create calculer_note_30.py for Production Immobilisée
    - Define mapping for accounts 72X
    - Implement calculation for capitalized production
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 19.4 Create calculer_note_31.py for Subventions d'Exploitation
    - Define mapping for accounts 71X
    - Implement calculation for operating subsidies
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 19.5 Create calculer_note_32.py for Reprises de Provisions
    - Define mapping for accounts 791X
    - Implement calculation for provision reversals
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 19.6 Create calculer_note_33.py for Produits Financiers
    - Define mapping for accounts 77X
    - Implement calculation for financial income
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

- [x] 20. Checkpoint - Ensure all 33 note calculators are complete
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 21. Implement main orchestrator
  - [x] 21.1 Create calcul_notes_annexes_main.py
    - Implement CalculNotesAnnexesMain class
    - Implement calculer_toutes_notes() method to execute all 33 calculators
    - Implement balance caching to load balances only once
    - Implement progress bar display during calculation
    - Implement parallel calculation for independent notes (optional optimization)
    - Generate summary report with calculation status for each note
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

  - [-] 21.2 Integrate Coherence_Validator into orchestrator
    - Call validator after all notes are calculated
    - Generate coherence report HTML
    - Emit alerts if coherence rate < 95%
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7_

  - [ ] 21.3 Integrate Trace_Manager into orchestrator
    - Generate trace files for all 33 notes
    - Manage trace history (keep last 10)
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 15.6, 15.7_

  - [ ]* 21.4 Write property test for performance constraint
    - **Property 18: Performance Constraint**
    - **Validates: Requirements 12.1, 12.2**

  - [ ]* 21.5 Write property test for calculation caching
    - **Property 19: Calculation Caching**
    - **Validates: Requirements 12.4**

  - [ ]* 21.6 Write integration test for all 33 notes calculation
    - Test complete workflow from balance loading to coherence validation
    - Verify performance < 30 seconds
    - Verify coherence rate >= 95%
    - _Requirements: 12.1, 10.5, 10.6_

- [ ] 22. Create Flask API endpoint for Claraverse integration
  - [ ] 22.1 Create api_notes_annexes.py with Flask endpoint
    - Implement /api/calculer_notes_annexes POST endpoint
    - Handle file upload (multipart/form-data)
    - Call orchestrator to calculate all 33 notes
    - Return JSON response with all notes data
    - Implement error handling with appropriate HTTP status codes (400, 404, 500, 503)
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

  - [ ] 22.2 Integrate API endpoint into main.py
    - Add route registration in Flask app
    - Configure CORS for frontend access
    - Add request validation and sanitization
    - _Requirements: 13.1, 13.2_

  - [ ]* 22.3 Write property test for API integration round-trip
    - **Property 20: API Integration Round-Trip**
    - **Validates: Requirements 13.2, 13.3, 13.4**

  - [ ]* 22.4 Write integration test for API endpoint
    - Test file upload and response format
    - Test error handling for invalid files
    - Test response time and performance
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

- [ ] 23. Create frontend integration components
  - [ ] 23.1 Create NotesAnnexesAccordionRenderer.tsx component
    - Implement accordion UI for displaying 33 notes
    - Implement clickable accordion items to expand/collapse notes
    - Render HTML content from API response
    - Add loading state and error handling
    - _Requirements: 13.4, 13.5_

  - [ ] 23.2 Add "Calculer Notes Annexes" button to EtatFinMenu
    - Add button in Etat fin interface
    - Implement file upload trigger
    - Call API endpoint on button click
    - Display results in accordion renderer
    - _Requirements: 13.1, 13.2, 13.3_

  - [ ] 23.3 Create NotesAnnexesAutoTrigger.js for automatic calculation
    - Implement auto-trigger when balance file is uploaded
    - Handle calculation progress display
    - Handle success/error notifications
    - _Requirements: 13.2, 13.3, 13.4_

- [ ] 24. Implement balance format flexibility
  - [ ] 24.1 Enhance Balance_Reader for format variations
    - Add support for multiple column name variations (spaces, separators)
    - Add support for comma and period as decimal separators
    - Add support for thousand separators (space, comma, period)
    - Implement automatic format detection
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6_

  - [ ]* 24.2 Write property test for balance format flexibility
    - **Property 21: Balance Format Flexibility**
    - **Validates: Requirements 14.1, 14.2, 14.3, 14.5, 14.6**

- [ ] 25. Checkpoint - Ensure integration and flexibility features work
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 26. Create comprehensive documentation
  - [ ] 26.1 Create README.md in Doc calcul notes annexes folder
    - Document architecture overview with diagrams
    - Document module responsibilities and interfaces
    - Document data flow and processing pipeline
    - Document file structure and organization
    - _Requirements: 11.1_

  - [ ] 26.2 Create GUIDE_UTILISATION.md
    - Document how to run individual note calculators
    - Document how to run all 33 notes via orchestrator
    - Document how to use API endpoint
    - Provide examples for each usage scenario
    - _Requirements: 11.3_

  - [ ] 26.3 Create TROUBLESHOOTING.md
    - Document common errors and solutions
    - Document balance file format requirements
    - Document performance optimization tips
    - Document debugging techniques
    - _Requirements: 11.6_

  - [ ] 26.4 Add comprehensive docstrings to all modules
    - Add class-level docstrings explaining purpose and usage
    - Add method-level docstrings with parameters, returns, and raises
    - Add inline comments for complex logic
    - _Requirements: 11.2_

- [ ] 27. Create test infrastructure and fixtures
  - [ ] 27.1 Create conftest.py with Hypothesis strategies
    - Implement st_balance() strategy for generating valid balances
    - Implement st_compte_racine() strategy for account roots
    - Implement st_montant() strategy for monetary amounts
    - Configure Hypothesis settings (max_examples=100, timeout=60s)
    - _Requirements: Testing Strategy_

  - [ ] 27.2 Create test fixtures in Tests/fixtures/
    - Create balance_demo_n_n1_n2.xlsx (valid complete balance)
    - Create balance_incomplete.xlsx (missing N-2 worksheet)
    - Create balance_invalid_format.xlsx (missing columns)
    - Create correspondances_test.json (test mapping file)
    - _Requirements: 11.7_

  - [ ] 27.3 Create test_all_notes.py integration test suite
    - Implement sequential execution of all 33 note calculators
    - Generate HTML summary report with status for each note
    - Display execution time and coherence metrics
    - _Requirements: 11.4, 11.5_

- [ ] 28. Implement error handling and logging
  - [ ] 28.1 Configure logging infrastructure
    - Set up three log files (main, warnings, errors)
    - Configure log rotation (daily, 30-day retention)
    - Configure log compression for old logs
    - Implement structured logging format with timestamps
    - _Requirements: 8.5, 8.6, 8.7, Error Handling_

  - [ ] 28.2 Implement custom exceptions
    - Define BalanceNotFoundException
    - Define InvalidBalanceFormatException
    - Define InvalidJSONException
    - Define FilePermissionException
    - Define EmptyBalanceException
    - Define InvalidAccountNumberException
    - _Requirements: Error Handling_

  - [ ] 28.3 Implement warning system
    - Implement IncoherentBalanceWarning
    - Implement NegativeVNCWarning
    - Implement AbnormalAccountBalanceWarning
    - Implement MissingAccountWarning
    - Implement LowCoherenceRateWarning
    - Log all warnings to calcul_notes_warnings.log
    - _Requirements: 3.6, 4.7, 8.5, 8.6, Error Handling_

  - [ ] 28.4 Implement graceful degradation
    - Handle missing accounts with zero values
    - Handle missing N-2 exercise gracefully
    - Continue processing with warnings for non-critical errors
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [ ]* 28.5 Write property test for graceful degradation
    - **Property 13: Graceful Degradation with Missing Data**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4**

  - [ ]* 28.6 Write property test for warning logging completeness
    - **Property 14: Warning Logging Completeness**
    - **Validates: Requirements 3.6, 4.7, 8.5, 8.6**

- [ ] 29. Optimize performance
  - [ ] 29.1 Implement balance caching in orchestrator
    - Load balances once and share across all calculators
    - Use dictionary-based account lookup for O(1) access
    - Implement result caching for repeated calculations
    - _Requirements: 12.2, 12.3, 12.4_

  - [ ] 29.2 Profile and optimize bottlenecks
    - Profile execution time for each module
    - Optimize pandas operations (vectorization)
    - Optimize HTML/Excel generation
    - Ensure total execution time < 30 seconds
    - _Requirements: 12.1_

  - [ ] 29.3 Implement optional parallel processing
    - Identify independent notes that can run in parallel
    - Implement parallel execution using multiprocessing
    - Add fallback to sequential processing if memory insufficient
    - _Requirements: 12.6, 12.7_

- [ ] 30. Final integration and end-to-end testing
  - [ ] 30.1 Test complete workflow with real balance file
    - Use P000 -BALANCE DEMO N_N-1_N-2.xlsx
    - Execute all 33 note calculators via orchestrator
    - Verify HTML files generated in Tests/ folder
    - Verify Excel export with all 33 notes
    - Verify coherence report generated
    - Verify trace files created
    - _Requirements: All_

  - [ ] 30.2 Test API integration with Claraverse frontend
    - Upload balance file via frontend interface
    - Verify API response with 33 notes
    - Verify accordion display in frontend
    - Verify error handling for invalid files
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 13.6_

  - [ ] 30.3 Performance validation
    - Measure execution time for complete calculation
    - Verify < 30 seconds constraint met
    - Verify memory usage acceptable
    - _Requirements: 12.1_

  - [ ] 30.4 Coherence validation
    - Verify inter-note coherence rate >= 95%
    - Verify total immobilizations match balance sheet
    - Verify depreciation charges match income statement
    - Verify temporal continuity (N-1 closing = N opening)
    - _Requirements: 10.1, 10.2, 10.3, 10.5, 10.6_

- [ ] 31. Final checkpoint - Complete system validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based tests and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties using Hypothesis
- Integration tests validate end-to-end workflows with real data
- The implementation follows the modular architecture defined in the design document
- All 33 note calculators follow the same template structure for consistency
- Performance optimization is critical to meet the < 30 seconds constraint
- Comprehensive error handling ensures robustness with incomplete or invalid data
