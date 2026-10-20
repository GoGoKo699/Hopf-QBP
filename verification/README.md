# Verification and reproduction

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
documentation integrity. See the [validation map](../review/README.md) for
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

The table reproduces the paper's coordinate-preserving no-clean-ancilla
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
- Integrated `W_C` and `B_{2,C}` compilers are checked at the paper's
  explicit four-qubit instance.

Small residual differences across supported BLAS or NumPy builds may occur at
floating-point roundoff scale. Values exceeding the test tolerances fail.

## Continuous integration

`.github/workflows/validation.yml` runs:

1. the Qibo-free analytic suite; and
2. the complete Qibo exact-logical suite.

A green workflow checks the finite circuit contracts, compiler-factorization
identities, and numerical premises documented in the [reviewer route](../review/README.md).
The concentration and asymptotic statements are established by the linked proofs.

## Clean generated outputs

The two validation PNG summaries are distinct from the original paper figures
embedded in the scientific account. Generated PDF/SVG variants and local logs
belong in ignored directories such as
`generated_figures/` or `validation_logs/`.

## Expected finite values and figure checks

For `n = 4`, the direct-angle ledger and `test_resource_ledger.py` agree exactly
on the following assigned CNOT values:

| Object | Assigned CNOT count |
|---|---:|
| Native real or complex forward preparation | 100 |
| Depth-ordered preparation | 140 |
| Real or integrated complex addressed frame | 210 |
| Real or integrated complex depth-2 suffix | 112 |
| Native forward plus global inverse frame | 310 |
| Direct complex phase record, excluding the controlled observable and readout | 100 |
| Native forward plus depth-2 checkpoint suffix | 212 |

The native-forward checkpoint totals for depths `0, 1, 2, 3` are
`240, 236, 212, 100`. These integer values check the paper's assigned cost
functional. The controlled objective and separately charged workspace or phase
resources retain the accounting stated in the [resource proof](../science/proofs-and-compilation.md#A2.SS9).

The paper's Figures 1–9 are explicit construction diagrams in the
[four-qubit companion](../science/four-qubit-example.md), with original assets
and complete captions. Tables I–III specify the node registry, checkpoint
settings, and finite cost ledger. Use `test_four_qubit_example.py`,
`test_operator_contracts.py`, and `test_resource_ledger.py` to compare those
constructions with executable fixtures. The two figures generated by
`make_validation_figures.py` summarize independent finite checks; they are
separate from the paper's numbered circuit diagrams.

The [complete paper map](../review/PAPER_MAP.md) gives the exact Markdown
location of every equation, statement, protocol, figure, table, and appendix
subsection. Circuit-versus-reference residuals should remain below each test's
declared tolerance (principally `3e-12` with zero relative tolerance); the
resource integers must match exactly. The full suite reports `OK` and exit
status zero only when every discovered test passes.
