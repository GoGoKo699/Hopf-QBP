# Reproducibility checklist

The commands below assume they are run from the repository root. The validation
is deterministic and does not download datasets or create benchmark traces.

## Environment

Use Python 3.10, 3.11, 3.12, or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-optional.txt
```

The release target is Qibo 0.3.4 with its NumPy statevector backend. The circuit
module selects that backend explicitly.

## Minimal analytic check

This path has no Qibo dependency. It checks indexing, wire translation,
decoders, native real/complex schedules, recursive native state columns, and
the assigned resource formulas.

```bash
python validate_qbp.py --analytic
```

## Circuit smoke test

This adds representative Qibo checks for bit order, Y-basis sign, frame
columns, the global real estimator, the direct phase estimator, checkpoints,
and asymmetric completions.

```bash
python validate_qbp.py --smoke
```

## Complete validation

```bash
python validate_qbp.py
```

The complete suite discovers every `test_*.py` module under
`qbp_validation/tests/`. A successful run returns exit status zero. The unit
tests do not write figures, CSV files, logs, or statevector dumps.

Equivalent direct command:

```bash
python -m unittest discover \
  -s qbp_validation/tests \
  -p 'test_*.py' \
  -t . \
  -v
```

## Regenerate validation figures

Regenerate the two committed PNG files in the repository root:

```bash
python make_validation_figures.py
```

Write multiple formats to a generated directory:

```bash
python make_validation_figures.py \
  --outdir generated_figures \
  --formats png pdf svg
```

Expected stems:

```text
exact_logical_validation_residuals
circuit_decoded_gradient_parity
```

The figure script reruns the deterministic circuit/reference comparisons. It is
not a plotting-only wrapper around stored numerical data.

## Assigned resource ledger

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable output is available through:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format json
```

These values are compiler-relative assigned CNOT charges. They exclude the
controlled observable and any separately assigned phase-layer or workspace
cost, and they must not be interpreted as Qibo transpiler counts.

## Determinism and tolerances

- Parameter arrays and observables use fixed seeds in `qbp_validation/cases.py`.
- Circuit tests use exact statevectors and complete probability distributions.
- The principal circuit/reference tolerance is `3e-12`.
- No Monte Carlo sampling occurs in the validation suite or figure generation.
- The Qibo-independent native real and complex schedule checks run through
  `n = 5`; full circuit checks use `n <= 4`.

Small residual differences across supported BLAS or NumPy builds may occur at
floating-point roundoff scale. Values exceeding the test tolerances cause a
failure.

## Clean generated outputs

The repository intentionally tracks only the two small PNG summaries used by
`README.md`. PDF/SVG variants and local logs belong in ignored directories such
as `generated_figures/` or `validation_logs/`.
