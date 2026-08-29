# Reproduce Everything

```bash
cd protein-hinge && python3 db/build_db.py && node site/verify_test.js
cd seedgraph && uv run python ../biocustody/scripts/run_atom_sot_semantic_003.py
cd antigence && python3 ../biocustody/scripts/run_antigence_b4_comparator.py
```

Do not retrain Antigence checkpoints.
