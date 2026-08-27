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
   coordinate remains a directly programmed physical angle at its designated
   tree-split or leaf-phase location.
2. **Multiplexed robustness companion:** a repository-only state-equivalent
   recompilation used to test whether the estimator identities and `O(N)`
   asymptotic comparison survive after leaving the direct-angle setting.

Passing the second set of checks does not redefine the ansatz or imply that its
elementary multiplexor angles remain the original Hopf coordinates.

## Minimal analytic check

This path has no Qibo dependency. It checks:

- tree indexing and wire translation;
- decoders and fixed-norm records;
- native real/complex schedules and state columns;
- interface projectors;
- the direct-angle assigned resource formulas;
- the clean-flag multiplexed robustness factorization and core counts;
- complete-vector and directional formulas;
- common-phase projection;
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

The table reproduces the manuscript's concrete coordinate-preserving
no-clean-ancilla assigned charges. Magnitude coordinates remain the physical
angles of their designated tree splits, and complex leaf phases remain directly
programmed phase angles. The table excludes the controlled observable, readout,
and any separately assigned diagonal phase-layer or workspace cost. It is not a
global optimality or Qibo-transpiler claim.

## Multiplexed robustness companion

```bash
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable output:

```bash
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10 --format json
```

The numeric CNOT columns are exact upper bounds for the uniformly controlled
`R_y` cores in one state-equivalent recompilation. The all-zero suffix
predicates are reported separately through their number and control widths
because their finite elementary-gate count depends on the chosen
multi-controlled-X decomposition. The exact clean-flag factorization is covered
by `test_optimized_compiler.py`.

This companion verifies estimator and asymptotic robustness outside the
direct-angle compiler. It generally does not preserve one Hopf coordinate as
one elementary physical multiplexor angle.

## Determinism and tolerances

- Parameter arrays and observables use fixed seeds in `qbp_validation/cases.py`.
- Circuit tests use exact statevectors and complete probability distributions.
- The principal circuit/reference tolerance is `3e-12`.
- No Monte Carlo sampling occurs in the central validation suite or figure generation.
- Qibo-independent native state-column checks run through `n = 5`.
- General Qibo circuit checks use `n <= 4`.
- Optimized clean-flag depth checks run through `n = 5`.
- The complete optimized flagged frame is checked through `n = 4`.
- The integrated `W_C` and `B_{2,C}` compilers are checked only at the
  manuscript's explicit four-qubit instance.

Small residual differences across supported BLAS or NumPy builds may occur at
floating-point roundoff scale. Values exceeding the test tolerances cause a
failure.

## Interpretation of the contracts

- Replacing one forward preparation by another with the same initialized state
  column leaves the complete later output distribution unchanged.
- Replacing the separated complex frame by the addressed `R_C` compiler changes
  only a common phase and leaves the global record distribution unchanged.
- Replacing the separated depth-`2` complex checkpoint suffix by `B_{2,C}`
  preserves checkpoint correlators and decoded gradient means. It need not
  preserve the complete output distribution.
- Replacing the direct addressed frame by the optimized flagged factorization
  is valid when the reusable flag enters and leaves in `|0>`. No equality is
  claimed on an arbitrary initial flag state.
- None of these logical equalities alone implies preservation of the
  direct-angle coordinate-to-control contract. Compiler scope and estimator
  correctness must be reported separately.

## Continuous integration

`.github/workflows/validation.yml` runs:

1. the Qibo-free analytic suite; and
2. the complete Qibo exact-logical suite on the pinned optional dependency.

A green workflow therefore checks both the repository-only robustness analysis
and the pre-existing direct-angle circuit contracts.

## Clean generated outputs

The repository tracks only the two small PNG summaries used by `README.md`.
PDF/SVG variants and local logs belong in ignored directories such as
`generated_figures/` or `validation_logs/`.
