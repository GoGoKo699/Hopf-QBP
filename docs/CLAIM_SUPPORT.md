# Claim support and validation map

This page is for readers auditing whether the implementation supports the claims
made by *Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz*.
It distinguishes paper-level results, Appendix-B supporting statements, and
additional executable extensions.

The compiler hierarchy is load-bearing:

1. **Paper setting:** the direct-angle Hopf realization, in which each
   coordinate remains a directly programmed physical angle at its designated
   tree-split or leaf-phase location.
2. **Ideal-model compiler invariance:** one exact state- or frame-equivalent
   multiplexed recompilation that preserves the estimator and asymptotic matched
   comparison while recombining elementary angles.

The second item is summarized in Appendix B and developed in detail in
[Optimized compilation](OPTIMIZED_COMPILATION.md). It does not redefine the
ansatz, preserve the elementary Hopf angles, or establish noise robustness.

## Evidence levels

| Support type | Meaning |
|---|---|
| **Exact-logical circuit check** | A Qibo circuit is executed with the NumPy statevector backend and compared with an independent NumPy reference. |
| **Algebraic reference check** | A finite-dimensional identity, decoder, convention, or resource formula is evaluated without Qibo. |
| **Checked factorization plus synthesis theorem** | An exact logical factorization is tested, while its asymptotic elementary-gate cost uses an established synthesis result. |
| **Analytic deduction exposed by code** | The finite premises of a statistical or asymptotic statement are checked, while the dimension-independent conclusion is mathematical rather than numerical. |

No finite numerical experiment proves an asymptotic concentration or
complexity claim. The documentation therefore separates tested ingredients from
analytic deductions.

## Audit summary

| Paper-level or supporting claim | Status and support | Main implementation | Main tests | Boundary |
|---|---|---|---|---|
| Native real and complex preparations reproduce the Hopf state | Paper-level exact state-column checks | `native_schedule.py`, `reference.py`, `circuits.py` | `test_native_schedule.py`, `test_operator_contracts.py` | State-column equality, not full-unitary equality. |
| The balanced real frame contains the state and normalized magnitude directions | Paper-level complete matrix and column checks | `reference.py`, `circuits.py` | `test_real_frame.py`, `test_four_qubit_example.py` | Finite dimensions through the tested range. |
| The global real circuit decodes the complete raw coordinate gradient | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_real_global_estimator.py` | Exact phase-calibrated controlled reflection. |
| The global complex magnitude circuit decodes all magnitude derivatives | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_magnitude.py` | General implementation uses separated phase/frame blocks. |
| The direct complex phase circuit decodes all leaf-phase derivatives | Paper-level exact signed one-hot check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_phase.py` | Expectation objectives are invariant under a uniform leaf-phase shift. |
| A checkpoint circuit returns every derivative at a selected depth | Paper-level exact depth-block check | `circuits.py`, `decoders.py`, `reference.py` | `test_checkpoints.py` | Each selected depth uses its own circuit stream. |
| Integrated complex checkpoint substitution is valid on the active interface | Paper-level projected-matrix and decoded-mean checks | `reference.py`, `circuits.py`, `conventions.py` | `test_operator_contracts.py`, `test_four_qubit_example.py` | It need not preserve the full unitary or complete distribution. |
| Singular magnitude and zero-amplitude phase coordinates are handled without division | Paper-level exact singular checks | `reference.py`, `circuits.py`, `decoders.py` | `test_singular_cases.py`, `test_complex_phase.py` | Zero-weight magnitude records vanish. Zero-amplitude phase derivatives vanish, but individual phase records need not. |
| Every single-depth global, checkpoint, and direct-phase record has norm `2` | Paper-level algebraic record checks | `decoders.py`, `reference.py` | `test_decoders.py`, `test_checkpoints.py`, `test_complex_phase.py` | Finite premise of the concentration argument. |
| Global coordinatewise execution scaling is `O((1 + log(n/delta))/epsilon^2)` | Paper-level analytic deduction | Record definitions and norm tests | Norm and decoder tests above | Absolute raw-coordinate error. |
| The concatenated magnitude record has norm `2*sqrt(n)` and fixed `l_2` accuracy costs `O(n/epsilon_2^2)` up to confidence | Appendix-B analytic result with executable support | `supporting_analysis.py`, `STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` | Raw magnitude vector; the complex phase stream is separate. |
| Relative/directional control and magnitude-block natural-gradient conditioning follow from the `l_2` bound and metric factors | Appendix-B conditional result | `supporting_analysis.py`, `STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` | Requires a nonzero-gradient margin; damping is an optimizer choice. |
| Raw-coordinate accuracy does not imply normalized-frame accuracy without metric conditioning | Main-text interpretation with Appendix-B proof and exact executable support | `swap_reflection`, `STATISTICAL_ACCURACY.md` | `test_coordinate_frame_separation_with_hopf_split` | Real-chart existence result; no efficient compiler for the witness reflection is claimed. |
| The ambient-sphere phase metric is the adopted convention; the projective block is an unused comparison | Main-text convention with Appendix-B derivation and executable support | `ambient_phase_metric`, `projective_phase_metric` | `test_phase_metric_conventions_and_support_rank` | The projective quotient remains low-profile and is not used by the theorem. |
| The magnitude output objects obey the stated sufficient norm hierarchy | Supporting analytic result | norm-bound helpers, `STATISTICAL_ACCURACY.md` | `test_magnitude_norm_hierarchy` | Upper bounds for the displayed rescaling decoder, not converses. |
| The direct-angle assigned CNOT ledger matches the manuscript's compiler model | **Paper-level resource claim** | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py` | `test_resource_ledger.py` | Finite assigned counts, not global optimality or routing. |
| One exact multiplexed realization preserves the estimator and the `O(N)` matched forward/frame scaling | **Appendix-B exact compiler result with detailed executable support** | `optimized_compiler.py`, `qbp_optimized_resource_ledger.py` | `test_optimized_compiler.py` | One reusable clean flag; elementary angles generally recombine Hopf coordinates. |
| A reflection sum admits unbiased coefficient-one-norm term sampling with a `Lambda**2` sufficient-shot factor | Main-text extension with executable support | `supporting_analysis.py`, `OBSERVABLES_AND_READOUT.md` | `test_supporting_analysis.py` | Portable upper bound, not an optimal Hamiltonian strategy. |
| Independent symmetric readout errors transform records by attenuation and bin mixing | Supporting analytic readout model | `supporting_analysis.py`, `OBSERVABLES_AND_READOUT.md` | `test_supporting_analysis.py` | Readout-only; no coherent gate-noise or mitigation claim. |

## Scope relative to the first paper

The first Hopf paper supplies the balanced real and complex charts, inverse map,
diagonal pullback metric, normalized coordinate directions, indexed tangent and
signed-branch estimators, native schedules, and the direct-angle
coordinate-to-control interpretation.

The present project supplies the computationally addressed differential frame,
one magnitude record shared across coordinates and depths, Walsh decoding, the
direct complete phase record, complete-gradient concentration, checkpoint
suffixes and active-interface contracts, and the supporting compiler,
statistical, observable, readout, and method-positioning analyses listed above.

## Claim 1: inherited conventions and forward states

For `N = 2**n`:

- the real magnitude block has length `N - 1`;
- the complex phase block has length `N`;
- the combined complex order is `(theta_1, ..., theta_{N-1}, theta_N, ..., theta_{2N-1})`;
- native `HopfReal` and `HopfComplex` schedules reproduce the recursive state.

Evidence: `native_schedule.py`, `reference.py`, `test_native_schedule.py`, and
`test_operator_contracts.py`. The initialized-state-column contract does not
imply full-unitary equality or preservation of the direct-angle ledger.

## Claim 2: balanced differential frame

The addressed real frame has

```math
W_{\mathbb R}|0\rangle=|\psi^{\mathbb R}\rangle,
\qquad
W_{\mathbb R}|b_{\lambda(j)}\rangle=|e_j^{\mathbb R}\rangle,
```

and

```math
\partial_{\theta_j}|\psi\rangle
=
\sqrt{g_{j,j}}|e_j\rangle.
```

The complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Evidence: `real_tree_data`, `real_frame_matrix`, `complex_frame_matrix`,
`test_real_frame.py`, and `test_complex_frame.py`.

## Claim 3: global real gradient

Logical sequence:

```text
forward real Hopf preparation
-> controlled reflection
-> W_R dagger
-> ancilla-X and system-X measurement
```

One outcome contributes

```math
Z_j^{\mathbb R}
=
2\sqrt{g^{\mathbb R}_{j,j}}
(-1)^{b+\lambda(j)\cdot y}
```

for every internal node. A signed histogram and one Walsh-Hadamard transform
recover all marker parities. Evidence: `real_global_measurement_circuit`,
`decode_balanced_magnitude_gradient`, `real_gradient`, and
`test_real_global_estimator.py`.

## Claim 4: global complex gradient

The complex magnitude family uses the separated order

```text
U_chk -> D_ph -> controlled reflection -> D_ph dagger -> W_R dagger
```

and the direct phase family uses ancilla-`Y` and system-`Z` readout. One phase
outcome contributes

```math
Z_{N+\ell}^{\mathbb C,\mathrm{ph}}
=
2(-1)^b\mathbf 1[\widehat\ell=\ell].
```

Evidence: `test_complex_magnitude.py` and `test_complex_phase.py`, including
zero-amplitude leaves and uniform-phase objective invariance.

## Claim 5: checkpointed depth gradients

At depth `d`:

```text
forward Hopf preparation
-> controlled reflection
-> inverse suffix below d
-> ancilla-Y, target-Y, active-prefix-Z measurement
```

The record is

```math
Z_d^{\mathrm{chk}}
=
-2(-1)^{b_c+b_t}e_{\widehat r}.
```

Evidence: `real_checkpoint_measurement_circuit`,
`complex_checkpoint_separated_circuit`, `decode_checkpoint_gradient`, and
`test_checkpoints.py`.

## Claim 6: substitution contracts

The implementation distinguishes full-unitary, initialized-state-column,
active-interface, and clean-flag equality. `test_operator_contracts.py` includes
negative checks showing that weaker contracts do not imply full-unitary
equality. `test_optimized_compiler.py` checks the clean-flag system block and
zero flag leakage. None of these logical contracts alone preserves one Hopf
coordinate as one elementary physical angle.

## Claim 7: singular coordinates and phase invariance

The estimators do not divide by a metric factor or leaf amplitude:

- zero incoming metric factor gives a zero magnitude derivative and record;
- zero leaf amplitude gives a zero phase derivative;
- unused completion columns do not alter the active differential interface.

Expectation objectives are invariant under a uniform leaf-phase shift, so the
exact phase-gradient block is zero-sum. `project_common_phase_gradient`
optionally removes finite-shot common-phase noise without increasing Euclidean
error. This objective-invariance statement is distinct from the optional
projective Fubini--Study metric convention.

## Claim 8: output norms and geometric conditioning

The manuscript theorem controls the raw Hopf-coordinate gradient. The same
magnitude record can be rescaled into normalized-frame or natural coordinates,
but its scale changes:

```math
q_j=\partial_{\theta_j}E_O,
\qquad
\chi_j=\frac{q_j}{\sqrt{g_{j,j}}},
\qquad
\nu_j=\frac{q_j}{g_{j,j}}.
```

The exact swap-reflection example shows that `|partial_{theta_k} E| < epsilon` can coexist with
`chi_k = 2` when `g[k,k]` is small. Therefore raw-coordinate accuracy does not
imply normalized-frame accuracy without metric conditioning.

The complete raw magnitude record has norm `2*sqrt(n)`, whereas the complete
active frame record has norm `2*sqrt(M_+)`. An unregularized natural-coordinate
record is bounded by `2/sqrt(g_min)`, and a damped record by `1/sqrt(tau)`.
See [Statistical accuracy](STATISTICAL_ACCURACY.md) for the full hierarchy and
its boundaries.

## Claim 9: complex phase metric convention

For leaf probabilities `p`, Hopf-QBP follows the ambient-sphere phase block

```math
G_{\mathrm{ph}}^{\mathrm{sph}}=\mathrm{diag}(p).
```

The optional projective convention is

```math
G_{\mathrm{ph}}^{\mathrm{FS}}
=
\mathrm{diag}(p)-pp^\mathsf{T},
```

with the uniform phase in its null space and rank `s-1` on support size `s`.
The projective quotient is not used by the manuscript theorem.

## Claim 10: compiler ledgers

The direct-angle ledger is implemented by the controlled-gate, depth-layer,
forward, frame, and suffix charge functions and checked by
`test_resource_ledger.py`.

The multiplexed companion groups each forward depth into a uniformly controlled
`R_y` and factors each addressed-frame depth through one clean suffix flag. Its
multiplexor-core counts are `N - 2` and `3*N/2 - 2`; predicate work is polynomial
in `n`, so both objects are `O(N)`. The result is exact in the ideal circuit
model and does not establish routed or noisy-device performance.

## Claim 11: reflection sums and readout transfer

For

```math
H=\sum_\alpha a_\alpha O_\alpha,
\qquad
\Lambda=\sum_\alpha|a_\alpha|,
```

sampling term `alpha` with probability `|a_alpha|/Lambda` and scaling its QBP
record by `Lambda*sign(a_alpha)` is unbiased. Record norms gain a factor
`Lambda`, and sufficient shot counts gain `Lambda**2`.

Under independent symmetric readout flips, global parities are attenuated by
the branch bit and marker-supported system bits. Checkpoint and phase address
errors mix one-hot bins through an independent bit-flip channel. See
[Observables and readout](OBSERVABLES_AND_READOUT.md).

## Method positioning

[Method comparison](METHOD_COMPARISON.md) compares Hopf-QBP with parameter
shift, the earlier indexed Hopf protocol, structured-circuit methods,
Lie-algebraic estimators, classical shadows, shadow-gradient methods,
directional estimators, and generalized Hadamard tests. The comparison is
organized by returned object, access model, structural premise, reuse
mechanism, and error/resource statement; it does not claim universal dominance.

## Validation matrix

| Test | Main responsibility |
|---|---|
| `test_conventions.py` | Tree indexing, basis order, parameter splitting, markers, and interfaces. |
| `test_native_schedule.py` | Native real and complex schedules and state columns. |
| `test_circuit_conventions.py` | Qibo bit significance and ancilla-`Y` sign. |
| `test_operator_contracts.py` | Full-unitary, state-column, and active-interface distinctions. |
| `test_real_frame.py` | Complete real frame and inverse. |
| `test_complex_frame.py` | Separated complex frame and four-qubit integrated compiler. |
| `test_real_global_estimator.py` | Complete real global gradient and Walsh decoder. |
| `test_complex_magnitude.py` | Complex magnitude gradient. |
| `test_complex_phase.py` | Direct phase gradient and zero-amplitude leaves. |
| `test_checkpoints.py` | Real and complex selected-depth gradients. |
| `test_singular_cases.py` | Exact singular-coordinate behavior. |
| `test_decoders.py` | Walsh, signed histograms, marginalization, and fixed-norm records. |
| `test_four_qubit_example.py` | Explicit compiler fixtures and interfaces. |
| `test_resource_ledger.py` | Direct-angle assigned charges. |
| `test_optimized_compiler.py` | Clean-flag factorization and multiplexor ledger. |
| `test_supporting_analysis.py` | `l_2`, direction, separation, phase metrics, norm hierarchy, reflection sums, and readout. |
| `test_documentation.py` | UTF-8 integrity, control characters, local link targets, fence balance, and claim-map structure. |

## Deliberate nonclaims

The project does not provide evidence for optimizer quality, hardware
advantage, coherent-noise resilience, routing efficiency, approximate
synthesis, or arbitrary observables outside the stated reflection-access
models. The norm hierarchy contains sufficient upper bounds for the displayed
decoder, not a matching lower bound or universal complexity boundary.
