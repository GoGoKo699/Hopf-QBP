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

This path has no Qibo dependency. It checks tree indexing, wire translation,
decoders, native real/complex schedules and state columns, interface projectors,
and assigned resource formulas.

```bash
python validate_qbp.py --analytic
```

## Circuit smoke test

This adds representative Qibo checks for:

- Qibo basis order and the ancilla-$Y$ sign convention;
- prepared-state-column equality without full-unitary equality;
- the complete addressed $R_C$ implementation of $W_{\mathbb C}$;
- the $B_{2,\mathbb C}$ checkpoint-interface identity;
- equality of checkpoint gradient means without an assertion of complete
  distribution equality;
- real global decoding;
- direct complex phase decoding; and
- the integrated complex depth-$2$ checkpoint.

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

## Assigned resource ledger

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable output:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format json
```

The general table reports native real/complex preparation, $U_{\mathrm{chk}}$,
and $W_{\mathbb R}$. When $n=4$ lies in the requested range, the text and JSON
outputs also report the Appendix-A objects
$W_{\mathbb C}$ and $B_{2,\mathbb C}$ and the $310/100/212$ record-circuit
totals. These are compiler-relative assigned CNOT charges. They exclude the
controlled observable, readout, and any separately assigned diagonal phase-layer
or workspace cost, and they are not Qibo-transpiler counts.

## Determinism and tolerances

- Parameter arrays and observables use fixed seeds in `qbp_validation/cases.py`.
- Circuit tests use exact statevectors and complete probability distributions.
- The principal circuit/reference tolerance is `3e-12`.
- No Monte Carlo sampling occurs in the validation suite or figure generation.
- Qibo-independent native state-column checks run through `n = 5`.
- General circuit checks use `n <= 4`.
- The integrated $W_{\mathbb C}$ and $B_{2,\mathbb C}$ compilers are checked only
  at the manuscript's explicit four-qubit instance.

Small residual differences across supported BLAS or NumPy builds may occur at
floating-point roundoff scale. Values exceeding the test tolerances cause a
failure.

## Interpretation of the three contracts

- Replacing one forward preparation by another with the same initialized state
  column leaves the complete later output distribution unchanged.
- Replacing the separated complex frame by the addressed $R_C$ compiler changes
  only a common phase and therefore leaves the global record distribution
  unchanged.
- Replacing the separated depth-$2$ complex checkpoint suffix by
  $B_{2,\mathbb C}$ preserves the checkpoint correlators and decoded gradient
  means. It need not preserve the complete output distribution.

## Clean generated outputs

The repository tracks only the two small PNG summaries used by `README.md`.
PDF/SVG variants and local logs belong in ignored directories such as
`generated_figures/` or `validation_logs/`.
