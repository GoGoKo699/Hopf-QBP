# Reproducibility

Run these commands from the repository root. Validation is deterministic.

## Environment

Use Python 3.10, 3.11, 3.12, or 3.13.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r requirements-optional.txt
```

The circuit tests use Qibo 0.3.4 with its NumPy statevector backend. The circuit
module selects that backend explicitly.

## Minimal analytic check

This Qibo-free suite checks conventions, decoders, native schedules, resource
formulas, optimized factorization, statistical and readout identities, and
documentation integrity. See the [validation map](docs/CLAIM_SUPPORT.md) for
individual claims and tests.

```bash
python validate_qbp.py --analytic
```

## Circuit smoke test

This adds representative Qibo checks for:

- Qibo basis order and the ancilla-`Y` sign convention;
- prepared-state-column equality without full-unitary equality;
- the complete addressed `R_C` implementation of `W_C`;
- the `B_{2,C}` checkpoint-interface identity;
- equality of checkpoint gradient means without complete-distribution equality;
- real global decoding;
- direct complex phase decoding; and
- the integrated complex depth-`2` checkpoint.

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

Regenerate the two committed PNG files:

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

The script reruns circuit/reference comparisons. It is not a plotting-only
wrapper around stored numerical data.

## Direct-angle assigned resource ledger

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable output:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format json
```

The table reproduces the manuscript's coordinate-preserving no-clean-ancilla
assigned charges. It excludes the controlled observable, readout, and any
separately assigned phase-layer or workspace cost. It is not a global
optimality or transpiler claim.

## Multiplexed exact-compilation companion

```bash
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable output:

```bash
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10 --format json
```

The numeric CNOT columns are upper bounds for uniformly controlled `R_y` cores.
The all-zero suffix predicates are reported through their number and control
widths because the finite elementary-gate constant depends on the chosen
multi-controlled-X decomposition. `test_optimized_compiler.py` checks the exact
clean-flag factorization.

## Determinism and tolerances

- Parameter arrays and observables use fixed seeds in `qbp_validation/cases.py`.
- Circuit tests use exact statevectors and complete probability distributions.
- The principal circuit/reference tolerance is `3e-12`.
- No Monte Carlo sampling occurs in the central suite or figure generation.
- Qibo-independent native state-column checks run through `n = 5`.
- General Qibo circuit checks use `n <= 4`.
- Clean-flag depth checks run through `n = 5`.
- The complete flagged frame is checked through `n = 4`.
- Integrated `W_C` and `B_{2,C}` compilers are checked at the manuscript's
  explicit four-qubit instance.

Small residual differences across supported BLAS or NumPy builds may occur at
floating-point roundoff scale. Values exceeding the test tolerances fail.

## Continuous integration

`.github/workflows/validation.yml` runs:

1. the Qibo-free analytic suite; and
2. the complete Qibo exact-logical suite.

A green workflow checks the manuscript-level circuit contracts, Appendix-B
compiler analysis, and the output-geometry supporting results.

## Clean generated outputs

The repository tracks only the two PNG summaries used by `README.md`. PDF/SVG
variants and local logs belong in ignored directories such as
`generated_figures/` or `validation_logs/`.
