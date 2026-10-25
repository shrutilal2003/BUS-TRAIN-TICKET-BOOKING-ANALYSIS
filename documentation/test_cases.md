# Test Cases

| ID | Test | Expected result | Automated check |
|---|---|---|---|
| TC-01 | Generate the same seed twice | Identical rows and values | `test_generator_is_reproducible_and_includes_duplicate_examples` |
| TC-02 | Clean generated duplicate examples | Eight exact duplicates removed, 1,000 generated bookings retained | `test_cleaning_removes_only_exact_duplicate_rows` |
| TC-03 | Cancelled/pending status revenue | Neither contributes recognized revenue | `test_cancelled_and_pending_records_do_not_contribute_to_revenue` |
| TC-04 | Missing demographic/payment values | Cleaned selected columns contain no missing values | `test_missing_age_is_imputed_and_missing_fields_are_resolved` |
| TC-05 | Required input schema | Missing required columns produce a ValueError | Loader validation in `src/data_loader.py` |
| TC-06 | Missing input file | A FileNotFoundError identifies the requested path | Loader validation in `src/data_loader.py` |

Run the automated suite from the project root with `python -m unittest discover -s tests -v`. Expected/actual pass status in the report is populated after executing the suite; never infer a pass from this table alone.