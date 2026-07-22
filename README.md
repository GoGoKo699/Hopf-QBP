# Hopf-QBP Exact-Logical Validation

Deterministic exact-logical validation for the constructions in
*The Compass in Reverse: Quantum Backpropagation with the Hopf Ansatz*.

This repository checks:

- the global addressed-frame estimator for real and complex magnitude coordinates;
- the direct complex-phase estimator;
- checkpointed Hopf adjoints at every tree depth;
- singular-coordinate behavior;
- representative ordered polyspherical frames;
- the explicit four-qubit construction; and
- the manuscript's compiler-relative CNOT ledger.

The analytic reference formulas and decoders do not import Qibo or call the
circuit builders. Shared indexing, basis-ordering, tree, and resource-accounting
conventions are centralized in
[`qbp_validation/conventions.py`](qbp_validation/conventions.py). Circuit tests
build and execute actual `qibo.models.Circuit` objects with Qibo's NumPy
statevector backend. Exact output distributions are summed directly; no Monte
Carlo shots are used.

## Papers in the series

- **Accompanying manuscript:** *The Compass in Reverse: Quantum Backpropagation with the Hopf Ansatz*
- **First paper:** [Hopf ansatz, arXiv:2607.14231](https://arxiv.org/abs/2607.14231)
- **First-paper code:** [GoGoKo699/Hopf-ansatz](https://github.com/GoGoKo699/Hopf-ansatz)

The two code repositories are complementary and have no runtime dependency on
one another. `Hopf-ansatz` contains the optimization-chart utilities, stress
tests, and safeguards accompanying the first paper. `Hopf-QBP` contains the
exact-logical validation of the global-frame, direct-phase, and checkpointed
reverse constructions in the second manuscript.

## Scope

This repository validates finite-dimensional algebraic and exact-logical circuit
identities. It does **not** benchmark:

- optimizer performance;
- finite-shot convergence;
- execution time or memory;
- device routing;
- approximate synthesis;
- hardware noise; or
- physical-device performance.

Assigned CNOT charges are computed from the manuscript's stated compiler model.
They are not inferred from Qibo-transpiled circuits. The controlled observable,
and any separately assigned phase-layer, workspace, or synthesis cost, are
excluded wherever the corresponding manuscript ledger excludes them.

## Repository structure

| File or directory | Role |
|---|---|
| [`validate_qbp.py`](validate_qbp.py) | Runs the analytic checks, a representative smoke suite, or the complete circuit suite. |
| [`make_validation_figures.py`](make_validation_figures.py) | Recomputes the deterministic validation figures from circuit and analytic data. |
| [`qbp_resource_ledger.py`](qbp_resource_ledger.py) | Prints the native, checkpoint-preparation, addressed-frame, and checkpoint CNOT charges. |
| [`qbp_validation/conventions.py`](qbp_validation/conventions.py) | Basis ordering, tree indexing, marker labels, wire translation, ordered-tree topology, and ledger formulas. |
| [`qbp_validation/native_schedule.py`](qbp_validation/native_schedule.py) | Reproduces the first paper's native `HopfReal` and `HopfComplex` schedules and assigned charges without importing Qibo. |
| [`qbp_validation/reference.py`](qbp_validation/reference.py) | Independent recursive states, local complements, path factors, derivatives, and exact gradients. |
| [`qbp_validation/circuits.py`](qbp_validation/circuits.py) | Qibo builders for native preparations, `U_chk`, `W_R`, phase layers, global estimators, checkpoints, and ordered-tree frames. |
| [`qbp_validation/decoders.py`](qbp_validation/decoders.py) | Walsh, signed-histogram, phase one-hot, checkpoint, and ordered-tree decoders. |
| [`qbp_validation/cases.py`](qbp_validation/cases.py) | Deterministic interior, singular, observable, and ordered-tree test cases. |
| [`qbp_validation/tests/`](qbp_validation/tests/) | Convention, circuit, decoder, singular-case, four-qubit, ordered-tree, native-schedule, asymmetric-completion, and resource tests. |
| [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) | Clean-environment commands, suite descriptions, figure regeneration, and deterministic-output notes. |

## Installation

Use Python 3.10, 3.11, 3.12, or 3.13.

Create an isolated environment and install the analytic dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install the pinned circuit dependency for Qibo checks:

```bash
python -m pip install -r requirements-optional.txt
```

The analytic suite requires only `requirements.txt`. The smoke suite, complete
circuit suite, and validation-figure regeneration require both dependency files.

## Quick start

Run the Qibo-free convention, decoder, native-schedule, and resource checks:

```bash
python validate_qbp.py --analytic
```

Run the analytic checks plus a representative Qibo circuit subset:

```bash
python validate_qbp.py --smoke
```

Run the complete validation suite:

```bash
python validate_qbp.py
```

Regenerate the committed validation figures:

```bash
python make_validation_figures.py
```

Print the assigned logical CNOT ledger:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
```

Machine-readable ledger output is also available:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format csv
python qbp_resource_ledger.py --nmin 2 --nmax 10 --format json
```

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for the complete clean-environment
sequence and optional figure formats.

## Notation and circuit conventions

For `n` system qubits, let $N = 2^n$. Python arrays use zero-based indexing,
while manuscript parameters use one-based indexing.

- `theta_mag[j - 1]` stores $\theta_j$, for $1 \le j \le N-1$. Thus
  `theta_mag` represents
  $\boldsymbol{\theta}_{\mathrm{mag}} = (\theta_1,\ldots,\theta_{N-1})$.
- `theta_ph[ell]` stores $\theta_{N+\ell}$, for $0 \le \ell < N$. Thus
  `theta_ph` represents
  $\boldsymbol{\theta}_{\mathrm{ph}} = (\theta_N,\ldots,\theta_{2N-1})$.
- `join_theta` and `split_theta` convert between these two blocks and the first
  paper's complete complex Hopf coordinate vector.
- Basis states are written $\lvert q_n \cdots q_1\rangle$. Qibo system index
  `0` is the most-significant basis bit and corresponds to manuscript wire
  $q_n$; Qibo index `n - 1` corresponds to $q_1$.
- The papers use $R_y(\theta) = e^{-i\theta Y}$. Qibo therefore receives
  `RY(2 * theta)`.
- `HopfReal`, $U_{\mathrm{chk}}$, and $W_{\mathbb{R}}$ prepare the same state
  from $\lvert 0\rangle$, but they are distinct full-unitary completions.
- The complex global-magnitude circuit uses the literal asymmetric sequence

$$
U_{\mathrm{chk}}
\;\longrightarrow\;
D_{\mathrm{ph}}
\;\longrightarrow\;
\operatorname{ctrl}(O)
\;\longrightarrow\;
D_{\mathrm{ph}}^{\dagger}
\;\longrightarrow\;
W_{\mathbb{R}}^{\dagger}.
$$

In the resource notation, $C_{\mathrm{chk}} = C(U_{\mathrm{chk}})$ denotes the
checkpoint-preparation charge. A depth-dependent quantity
$C_{\mathrm{chk},d}$ denotes the complete depth-$d$ checkpoint-record charge
under the manuscript's stated exclusions.

## What counts as circuit-level validation

A circuit check satisfies both conditions:

1. the tested state or measurement distribution is produced by an actual
   `qibo.models.Circuit` executed with the NumPy statevector backend; and
2. the expected state, frame column, coordinate derivative, or gradient is
   computed by [`qbp_validation/reference.py`](qbp_validation/reference.py),
   which imports no Qibo code and calls no circuit builder.

The test suite does not inject expected statevectors into Qibo. Controlled
`RY(2 * theta)` gates are built with explicit open controls. Exact diagonal
phase layers and controlled reflections are represented by logical `Unitary`
gates, matching the manuscript's access model.

The ordered polyspherical checks use exact finite-dimensional two-level
rotations. They validate the frame algebra and parity decoder for representative
ordered trees; they do not claim a general hardware-efficient synthesis for an
arbitrary tree.

## Validation matrix

| Test group | Statement checked |
|---|---|
| [`test_conventions.py`](qbp_validation/tests/test_conventions.py) | Big-endian labels, marker bijection, manuscript/Qibo wire translation, complete complex-vector splitting, and observable assumptions. |
| [`test_native_schedule.py`](qbp_validation/tests/test_native_schedule.py) | The first paper's native real and complex schedules, the four-qubit table, recursive state columns, and native assigned charges. |
| [`test_circuit_conventions.py`](qbp_validation/tests/test_circuit_conventions.py) | Qibo bit significance and the manuscript's $S^{\dagger}$-then-$H$ ancilla-$Y$ sign convention. |
| [`test_real_frame.py`](qbp_validation/tests/test_real_frame.py) | $W_{\mathbb{R}}\lvert 0\rangle = \lvert \psi\rangle$ and $W_{\mathbb{R}}\lvert \lambda(j)\rangle = \lvert e_j\rangle$, including singular completions. |
| [`test_asymmetric_completions.py`](qbp_validation/tests/test_asymmetric_completions.py) | Native, checkpoint, and addressed completions share the prepared-state column but differ as full unitaries; the asymmetric complex decoder remains exact. |
| [`test_real_global_estimator.py`](qbp_validation/tests/test_real_global_estimator.py) | One all-$X$ distribution returns the complete real magnitude gradient, with direct and FWHT decoders agreeing. |
| [`test_complex_magnitude.py`](qbp_validation/tests/test_complex_magnitude.py) | Phase-dressed frame columns and the global complex-magnitude estimator for $n = 1,2,3,4$. |
| [`test_complex_phase.py`](qbp_validation/tests/test_complex_phase.py) | The ancilla-$Y$/system-label signed one-hot phase estimator, common-phase cancellation, and zero-amplitude leaves. |
| [`test_checkpoints.py`](qbp_validation/tests/test_checkpoints.py) | Real and complex magnitude checkpoints at every depth and fixed-norm checkpoint records. |
| [`test_singular_cases.py`](qbp_validation/tests/test_singular_cases.py) | Zero path factors give zero derivatives without breaking the addressed frame or checkpoint circuits. |
| [`test_polyspherical.py`](qbp_validation/tests/test_polyspherical.py) | Ordered-tree frame columns, diagonal derivative Gram matrix, anchor translation, and parity readout for balanced and unbalanced examples. |
| [`test_decoders.py`](qbp_validation/tests/test_decoders.py) | FWHT correctness, signed histograms, checkpoint suffix marginalization, and one-hot records. |
| [`test_four_qubit_example.py`](qbp_validation/tests/test_four_qubit_example.py) | All four-qubit marker labels, the explicit node-5 formulas, every checkpoint depth, and the `100/140/210` completion comparison. |
| [`test_resource_ledger.py`](qbp_validation/tests/test_resource_ledger.py) | Controlled-rotation, native, depth-layer, addressed-frame, and checkpoint assigned charges. |

## Validation figures

<p align="center">
  <img src="exact_logical_validation_residuals.png" width="760" alt="Maximum exact-logical Qibo-to-reference residuals">
</p>

Each point is the largest absolute discrepancy in one deterministic validation
family. The dashed line is the principal unit-test tolerance
$3 \times 10^{-12}$. Residuals at floating-point roundoff scale should be read as
finite-size identity checks, not as performance data.

<p align="center">
  <img src="circuit_decoded_gradient_parity.png" width="560" alt="Circuit-decoded gradients compared with independent analytic derivatives">
</p>

Each plotted point is a gradient component obtained by exact summation of a
complete circuit output distribution. A deterministic subset is displayed for
legibility; the annotated maximum residual is computed over all checked
components.

The figure-generation script reruns the circuit/reference comparisons. It is
not a plotting-only wrapper around stored numerical data.

## Coverage and interpretation

Balanced Hopf checks use $n = 1,2,3,4$ and include:

- generic interior coordinates;
- real final-layer sign changes;
- upstream angles equal to $0$ and $\pi/2$;
- zero-amplitude complex leaves;
- Pauli reflections;
- diagonal reflections; and
- fixed-seed Householder reflections.

Qibo-independent native real and complex schedule checks run through $n = 5$.
The ordered polyspherical tests use two full binary trees on eight encoded
leaves, including an unbalanced tree with a nonzero root anchor.

These tests validate finite-size instances of the exact algebraic premises in
the manuscript. They do not numerically prove concentration inequalities or
asymptotic resource statements. Decoder complexity is not timed, workspace is
not measured, and the ordered-tree resource extension remains conditional on
the efficient-frame assumptions stated in the manuscript.

## Citation

When using this repository, cite both:

1. *The Compass in Reverse: Quantum Backpropagation with the Hopf Ansatz*; and
2. the first Hopf-ansatz paper, [arXiv:2607.14231](https://arxiv.org/abs/2607.14231).
