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

## Compiler hierarchy used by the checks

The validation distinguishes two roles:

1. **Direct-angle Hopf compiler:** the defining paper setting, in which each
   coordinate remains a directly programmed physical angle at its tree-split or
   leaf-phase location.
2. **Multiplexed exact-compilation companion:** an Appendix-B state-equivalent
   construction used to test whether the estimator and `O(N)` matched
   comparison survive after leaving the direct-angle setting.

The second item is exact ideal-model invariance, not a noise-robustness claim.
It generally does not preserve the original elementary Hopf angles.

## Minimal analytic check

This path has no Qibo dependency. It checks:

- tree indexing and wire translation;
- decoders and fixed-norm records;
- native real/complex schedules and state columns;
- interface projectors;
- direct-angle assigned resource formulas;
- clean-flag multiplexed factorization and core counts;
- complete-vector, relative/directional, and natural-gradient-conditioning formulas;
- exact raw-coordinate versus normalized-frame separation;
- magnitude frame/natural-coordinate norm scales;
- ambient and projective phase metrics, support rank, and common-phase null vector;
- zero-sum projection from uniform-phase objective invariance;
- reflection-sum term sampling; and
- analytic readout transfer functions.

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

## Output-geometry checks

The analytic suite contains an explicit two-qubit Hopf separation witness. It
constructs a small incoming metric weight, a normalized Hopf direction, and the
Householder reflection swapping the state with that direction. The test verifies
that the raw coordinate gradient is below a chosen tolerance while the
normalized-frame coefficient remains exactly `2`.

The same test module checks:

- complete active-frame record norm `2*sqrt(M_+)`;
- natural-coordinate bound `2/sqrt(g_min)`;
- damped bound `1/sqrt(tau)`;
- ambient phase block `diag(p)`;
- projective block `diag(p)-p p^T`;
- positive semidefiniteness, support rank, and the common-phase null vector.

See [Statistical accuracy](docs/STATISTICAL_ACCURACY.md) for interpretation.

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

## Interpretation of the contracts

- A forward replacement with the same initialized state column preserves the
  later output distribution.
- The addressed `R_C` frame differs from the separated complex frame only by a
  common phase in the validated four-qubit fixture.
- The integrated complex checkpoint preserves active-interface correlators and
  decoded means, not necessarily the complete distribution.
- The flagged frame factorization is valid when the reusable flag enters and
  leaves in `|0>`.
- None of these equalities alone preserves the direct-angle
  coordinate-to-control contract.

## Continuous integration

`.github/workflows/validation.yml` runs:

1. the Qibo-free analytic suite; and
2. the complete Qibo exact-logical suite.

A green workflow checks the manuscript-level circuit contracts, Appendix-B
compiler analysis, and the output-geometry supporting results.

## Method-comparison boundary

[Method comparison](docs/METHOD_COMPARISON.md) is a documentation comparison,
not an executable benchmark. It organizes methods by returned object, access
model, structure, reuse, and error/resource statement. The repository does not
claim that methods with different interfaces are directly ordered.

## Clean generated outputs

The repository tracks only the two PNG summaries used by `README.md`. PDF/SVG
variants and local logs belong in ignored directories such as
`generated_figures/` or `validation_logs/`.
