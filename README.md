# Hopf-QBP Exact-Logical Validation

This repository contains deterministic exact-logical circuit validation for
*The Compass in Reverse: Quantum Backpropagation with the Hopf Ansatz*.
It checks the global addressed-frame estimator, the direct complex-phase
estimator, the checkpointed Hopf adjoint, singular-coordinate behavior,
representative polyspherical frames, the four-qubit construction, and the
assigned compiler ledger.

The analytic references and decoders are independent NumPy implementations.
Circuit tests build and execute `qibo.models.Circuit` objects with Qibo's NumPy
statevector backend. Exact output distributions are summed directly; no Monte
Carlo shots are used.

The repository does **not** benchmark optimization, finite-shot convergence,
execution time, memory, routing, approximate synthesis, device noise, or
hardware performance. Assigned CNOT charges are checked from the manuscript's
compiler-relative formulas and are not inferred from Qibo-transpiled circuits.

## Relation to the first Hopf paper

The inherited chart, tree, gate, and circuit notation follows the first paper:

- paper: [Hopf ansatz, arXiv:2607.14231](https://arxiv.org/abs/2607.14231)
- code: [GoGoKo699/Hopf-ansatz](https://github.com/GoGoKo699/Hopf-ansatz)

The two repositories are complementary and have no runtime dependency on one
another. `Hopf-ansatz` contains the optimization-chart utilities, stress tests,
and safeguards accompanying the first paper. `Hopf-QBP` contains the
exact-logical validation of the global-frame, direct-phase, and checkpointed
reverse constructions in the second manuscript.

## Repository contents

| File or directory | Role |
|---|---|
| `validate_qbp.py` | Runs the Qibo-free analytic checks, a smoke suite, or the complete circuit suite. |
| `make_validation_figures.py` | Recomputes the two deterministic repository figures from circuit and analytic data. |
| `qbp_resource_ledger.py` | Prints the native, checkpoint-preparation, addressed-frame, and checkpoint CNOT charges used by the manuscript ledger. |
| `qbp_validation/conventions.py` | Basis ordering, tree indexing, marker labels, manuscript/Qibo wire translation, polyspherical topology, and ledger formulas. |
| `qbp_validation/native_schedule.py` | Reproduces the first paper's native `HopfReal` and `HopfComplex` schedules and charges without importing Qibo. |
| `qbp_validation/reference.py` | Independent recursive states, local complements, metric factors, derivatives, and exact gradients. |
| `qbp_validation/circuits.py` | Qibo builders for the native circuits, `U_chk`, `W_R`, phase layers, global estimators, checkpoints, and polyspherical frames. |
| `qbp_validation/decoders.py` | Walsh, signed-histogram, phase one-hot, and checkpoint decoders. |
| `qbp_validation/cases.py` | Deterministic interior, singular, observable, and ordered-tree cases. |
| `qbp_validation/tests/` | Convention, circuit, decoder, singular-case, four-qubit, polyspherical, native-schedule, asymmetric-completion, and resource tests. |
| `REPRODUCIBILITY.md` | Clean-environment commands, smoke tests, full validation, and figure regeneration. |

## Notation and circuit conventions

The public code follows the notation shared by the two papers.

- `theta_mag` stores \(\boldsymbol\theta_{\mathrm{mag}}=(\theta_1,\ldots,\theta_{N-1})\).
- `theta_ph` stores \(\boldsymbol\theta_{\mathrm{ph}}=(\theta_N,\ldots,\theta_{2N-1})\), with leaf \(\ell\) carrying phase \(\theta_{N+\ell}\).
- `join_theta` and `split_theta` convert between the two blocks and the first paper's single complex coordinate vector.
- Basis states are written \(\lvert q_n\cdots q_1\rangle\). Qibo system index `0` is the most-significant bit and corresponds to manuscript wire \(q_n\).
- The papers use \(R_y(\theta)=e^{-i\theta Y}\); Qibo therefore receives `RY(2 * theta)`.
- `HopfReal`, `U_chk`, and `W_R` share the prepared-state column but are distinct full-unitary completions. The complex global-magnitude test executes the literal asymmetric sequence
  \[
  U_{\mathrm{chk}}\to D_{\mathrm{ph}}\to \operatorname{ctrl}(O)
  \to D_{\mathrm{ph}}^\dagger\to W_{\mathbb R}^\dagger.
  \]

## Requirements

Use Python 3.10, 3.11, 3.12, or 3.13.

Install the NumPy and plotting dependencies:

```bash
python -m pip install -r requirements.txt
```

Install the pinned circuit dependency for Qibo checks:

```bash
python -m pip install -r requirements-optional.txt
```

The Qibo-free analytic checks require only `requirements.txt`. The full suite
and figure regeneration require both files.

## Quick start

Run the independent convention, decoder, native-schedule, and ledger checks:

```bash
python validate_qbp.py --analytic
```

Run a representative circuit subset:

```bash
python validate_qbp.py --smoke
```

Run the complete validation suite:

```bash
python validate_qbp.py
```

Regenerate the committed PNG summaries:

```bash
python make_validation_figures.py
```

Print the assigned logical CNOT ledger:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
```

See `REPRODUCIBILITY.md` for a clean-environment sequence and optional output
formats.

## What counts as circuit-level validation

A circuit check satisfies both conditions:

1. the tested state or measurement distribution is produced by an actual
   `qibo.models.Circuit` executed with the NumPy statevector backend;
2. the expected state, frame column, or coordinate derivative is computed by
   `qbp_validation/reference.py`, which imports no Qibo code.

The suite does not inject expected statevectors into Qibo. It builds controlled
`RY(2 * theta)` gates with explicit open controls. The exact diagonal phase
layer and controlled reflection are represented by logical `Unitary` gates,
matching the manuscript access model. The polyspherical checks use exact
finite-dimensional two-level rotations and therefore validate the frame
algebra, not an arbitrary-tree synthesis claim.

## Validation matrix

| Test group | Statement checked |
|---|---|
| `test_conventions.py` | Big-endian labels, marker bijection, wire translation, full complex-vector splitting, and observable assumptions. |
| `test_native_schedule.py` | The first paper's native real/complex schedules, four-qubit table, recursive state columns, and native charges. |
| `test_circuit_conventions.py` | Qibo bit significance and the manuscript's `S^dagger`-then-`H` Y-basis sign. |
| `test_real_frame.py` | `W_R |0> = |psi>` and `W_R |lambda(j)> = |e_j>`, including singular completions. |
| `test_asymmetric_completions.py` | Native, checkpoint, and addressed completions share the state column but differ as full unitaries; the asymmetric complex decoder remains exact. |
| `test_real_global_estimator.py` | One all-X distribution returns the complete real magnitude gradient, with direct and FWHT decoders agreeing. |
| `test_complex_magnitude.py` | Phase-dressed frame columns and the global complex-magnitude estimator. |
| `test_complex_phase.py` | Ancilla-Y/system-Z signed one-hot phase estimator and common-phase cancellation. |
| `test_checkpoints.py` | Real and complex magnitude checkpoints at every depth and fixed-norm records. |
| `test_singular_cases.py` | Zero metric factors give zero derivatives without breaking the frame or checkpoints. |
| `test_polyspherical.py` | Ordered-tree frame columns, diagonal metric, translation, and parity readout for balanced and unbalanced examples. |
| `test_decoders.py` | FWHT, signed histograms, checkpoint suffix marginalization, and one-hot records. |
| `test_four_qubit_example.py` | All four-qubit markers, node-5 formulas, all checkpoint depths, and the `100/140/210` completion comparison. |
| `test_resource_ledger.py` | Controlled-rotation, native, depth, addressed-frame, and checkpoint assigned charges. |

## Validation figures

<p align="center">
  <img src="exact_logical_validation_residuals.png" width="760" alt="Exact-logical Qibo validation residuals">
</p>

Each point is the largest absolute discrepancy in one deterministic validation
family. The dashed line is the unit-test tolerance \(3\times10^{-12}\).
Residuals at roundoff scale should be read as finite-size identity checks, not
as performance data.

<p align="center">
  <img src="circuit_decoded_gradient_parity.png" width="560" alt="Circuit-decoded gradients versus independent analytic derivatives">
</p>

Each plotted point is a component obtained by exact summation of a complete
circuit output distribution. A deterministic subset is displayed for
legibility, while the annotated maximum residual is computed over all checked
components.

## Coverage and interpretation

Balanced Hopf checks use `n = 1, 2, 3, 4` and include generic interior
coordinates, real final-layer sign changes, upstream `0` and `pi/2` angles,
zero-amplitude complex leaves, Pauli reflections, diagonal reflections, and
fixed-seed Householder reflections. Native schedule state columns are also
checked without Qibo through `n = 5`.

The polyspherical checks use two ordered full binary trees on eight encoded
leaves, including an unbalanced tree with a nonzero root anchor.

These tests validate finite-size instances of the exact algebraic premises in
the manuscript. They do not numerically prove concentration inequalities or
asymptotic resource statements. In particular, decoder complexity is not timed,
workspace is not measured, and the polyspherical resource extension remains
conditional on the efficient-frame assumptions stated in the manuscript.

## Citation

When using this repository, cite the first Hopf-ansatz paper and the
accompanying Hopf-QBP manuscript.
