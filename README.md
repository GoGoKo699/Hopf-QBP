# Hopf-QBP: implementation reference and exact-logical validation

Reference circuits, decoders, compiler analyses, statistical extensions, and
deterministic tests for *Compass in the Mirror: Quantum Backpropagation with
the Hopf Ansatz*.

## What problem does Hopf-QBP solve?

Hopf-QBP addresses the finite-shot cost of returning the complete
**raw Hopf-coordinate gradient**. Under calibrated controlled-reflection access,
every global magnitude outcome contributes to every magnitude coordinate; a
separate leaf record supplies the complex phase derivatives.

The accuracy target is simultaneous absolute raw-coordinate `l_infinity` error
at most `epsilon`, with probability at least `1 - delta`. For a complete chart
with `M = N - 1` real coordinates or `M = 2*N - 1` complex coordinates, where
`N = 2**n`, the resource layers are distinct:

| Quantity | Global Hopf-QBP scaling |
|---|---|
| Returned object | Materialized `M`-entry raw coordinate-gradient vector |
| Independent executions | `O((1 + log(n/delta))/epsilon^2)` |
| Fixed-accuracy execution count | `O(log log M)` |
| Controlled-reflection calls | One per independent execution |
| Direct-angle Hopf work per magnitude execution | `O(M log M)` |
| Direct-angle total Hopf work at fixed accuracy/confidence | `O(M log M log log M)` |
| One optimized state-equivalent recompilation | `O(M)` Hopf work per execution |
| Optimized total Hopf work at fixed accuracy/confidence | `O(M log log M)` |
| Walsh decoding | `O(M log M)` |
| Materialized output | `M` classical entries |

Thus `O(log log M)` counts independent circuit executions, not end-to-end
runtime or output size. The result is output-sensitive because `M = Theta(2**n)`.
Reflection-sum objectives introduce their coefficient-one-norm scale; see
[Observables and readout](docs/OBSERVABLES_AND_READOUT.md).

## Choose a route

| Goal | Start here |
|---|---|
| Audit a paper-level claim | [Claim support and validation map](docs/CLAIM_SUPPORT.md) |
| Understand the output objects, norm hierarchy, and metric boundary | [Statistical accuracy](docs/STATISTICAL_ACCURACY.md) |
| Compare gradient methods under their actual tasks and access models | [Method comparison](docs/METHOD_COMPARISON.md) |
| Understand or implement the defining direct-angle Hopf compiler | [Engineering guide](docs/ENGINEERING_GUIDE.md) |
| Study exact ideal-model invariance under optimized recompilation | [Optimized compilation companion](docs/OPTIMIZED_COMPILATION.md) |
| Extend to reflection sums or inspect readout sensitivity | [Observables and readout](docs/OBSERVABLES_AND_READOUT.md) |
| Reproduce the deterministic validation | [Reproducibility checklist](REPRODUCIBILITY.md) |
| Read the first paper and its implementation | [Hopf-ansatz repository](https://github.com/GoGoKo699/Hopf-ansatz) |

## Direct-angle Hopf compiler contract

The defining circuit realization preserves

```math
\text{one Hopf coordinate}
\longleftrightarrow
\text{one designated tree-split or leaf-phase location}
\longleftrightarrow
\text{one directly programmed physical angle}.
```

For magnitude coordinates this is the `R_y` angle attached to an internal tree
node. In the complex chart, each leaf-phase coordinate is retained as a directly
programmed phase angle. The native preparations, depth-ordered completion
`U_chk`, addressed frame `W_R`, and checkpoint suffixes retain this direct-angle
structure. The manuscript's finite resource ledger belongs to this
coordinate-preserving setting.

The [optimized compilation](docs/OPTIMIZED_COMPILATION.md) companion preserves
the state, frame action, and decoded estimator while generally recombining the
elementary angles. It establishes exact ideal-model invariance under one
multiplexed recompilation. “Quantum backpropagation” here refers to gradients
of the Hopf state coordinates under these matched resource models.

## Supported access model

The core objective is

```math
E_O(\boldsymbol{\theta})
=
\langle\psi(\boldsymbol{\theta})|O|\psi(\boldsymbol{\theta})\rangle.
```

The validated gradient protocols assume:

- `O` is a known Hermitian unitary, so `O = O†` and `O² = I`;
- exact controlled access to `O` is available; and
- the relative phase between the controlled branches is known or calibrated.

An unknown controlled-branch phase rotates the measured interference components
and invalidates the fixed decoder. A real-coefficient reflection sum can be
handled by coefficient-one-norm term sampling, with the resulting `Lambda**2`
sampling factor documented in
[Observables and readout](docs/OBSERVABLES_AND_READOUT.md).

## Three output records

### Global magnitude record

For internal node `j`, one all-`X` outcome `(b, y)` contributes

```math
Z_j
=
2\sqrt{g_{j,j}}\,(-1)^{b+\lambda(j)\cdot y}.
```

The same physical outcome contributes to every magnitude coordinate. A signed
system histogram followed by one fast Walsh-Hadamard transform evaluates all
required parities together.

### Direct complex phase record

One ancilla-`Y` and system-`Z` outcome `(b, ell)` contributes

```math
Z^{\mathrm{ph}}
=
2(-1)^b e_{\ell}.
```

It updates one leaf bin and directly estimates the complete phase-gradient
block.

### Checkpoint record

At selected depth `d`, one outcome `(b_c, b_t, r)` contributes

```math
Z_d^{\mathrm{chk}}
=
-2(-1)^{b_c+b_t}e_r.
```

It updates one prefix bin and estimates every magnitude derivative at that
depth.

The exact sign, bit order, and gate-angle conventions are specified in the
[engineering guide](docs/ENGINEERING_GUIDE.md).

## Quick start

Use Python 3.10–3.13. From an activated virtual environment:

```bash
python -m pip install -r requirements.txt -r requirements-optional.txt
python validate_qbp.py
```

Use `python validate_qbp.py --analytic` for Qibo-free checks or `--smoke` for
representative circuit contracts. [Reproducibility](REPRODUCIBILITY.md) contains
environment setup, ledger and figure commands, output formats, and tolerances.

## Validation coverage

General circuit checks cover `n = 1, 2, 3, 4`. Qibo-independent native
state-column checks extend through `n = 5`. The clean-flag depth factorization
is checked through `n = 5`, and the complete flagged frame through `n = 4`.
Deterministic cases include interior coordinates, final-layer signs, exact
singular angles, zero-amplitude leaves, Pauli and diagonal reflections, and
fixed-seed Householder reflections.

The central circuit suite compares Qibo statevectors and complete output
probability distributions with independent NumPy references.

<p align="center">
  <img src="exact_logical_validation_residuals.png" width="760" alt="Maximum exact-logical Qibo-to-reference residuals">
</p>

<p align="center">
  <img src="circuit_decoded_gradient_parity.png" width="560" alt="Circuit-decoded gradients compared with independent analytic derivatives">
</p>

These plots summarize finite-dimensional identity checks. Concentration and
asymptotic complexity statements combine these checked premises with
mathematical concentration and synthesis results; the
[claim support map](docs/CLAIM_SUPPORT.md) distinguishes the evidence for each
result.

The returned object is the raw coordinate gradient. Conversion to
normalized-frame or natural-gradient error requires the metric conditions in
[Statistical accuracy](docs/STATISTICAL_ACCURACY.md).

## Papers in the series

- **Second paper:** *Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz*.
- **First paper:** [A Compass on the Quantum State Sphere: The Hopf Ansatz for Arbitrary Pure-State Optimization](https://arxiv.org/abs/2607.14231).
- **First-paper code:** [GoGoKo699/Hopf-ansatz](https://github.com/GoGoKo699/Hopf-ansatz).

The repositories have no runtime dependency on one another.

## Citation

When using this repository, cite both the Hopf-QBP manuscript and the first
Hopf-ansatz paper. Machine-readable software metadata is provided in
`CITATION.cff`.

## License

This software is released under the [MIT License](LICENSE).
