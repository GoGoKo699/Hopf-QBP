# Claim support and validation map

This page is for readers auditing whether the implementation supports the claims
made by *Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz*.
It distinguishes paper-level results, Appendix-B supporting statements, and
additional executable extensions.

The compiler hierarchy is load-bearing:

1. **Paper setting:** the direct-angle Hopf realization, in which each
   coordinate remains a directly programmed physical angle at its designated
   tree-split or leaf-phase location.
2. **Robustness beyond that setting:** an exact state- or frame-equivalent
   multiplexed recompilation that preserves the estimator identities and the
   asymptotic matched comparison while recombining elementary physical angles.

The second item is summarized in Appendix B and developed in detail here. It
does not redefine the ansatz or replace the direct-angle resource theorem.

## Evidence levels

| Support type | Meaning |
|---|---|
| **Exact-logical circuit check** | A Qibo circuit is executed with the NumPy statevector backend and compared with an independent NumPy reference. |
| **Algebraic reference check** | A finite-dimensional identity, decoder, convention, or resource formula is evaluated without Qibo. |
| **Checked factorization plus synthesis theorem** | An exact logical factorization is tested, while its asymptotic elementary-gate cost uses an established compiler result cited in the documentation. |
| **Analytic deduction exposed by code** | The finite premises of a statistical or asymptotic statement are checked, while the dimension-independent conclusion is mathematical rather than numerical. |

No finite numerical experiment proves an asymptotic concentration or
complexity claim. The documentation therefore separates tested ingredients from
analytic deductions.

## Audit summary

| Paper-level or supporting claim | Status and support | Main implementation | Main tests | Boundary |
|---|---|---|---|---|
| Native real and complex preparations reproduce the Hopf state | Paper-level exact state-column checks | `native_schedule.py`, `reference.py`, `circuits.py` | `test_native_schedule.py`, `test_operator_contracts.py` | State-column equality, not full-unitary equality. |
| The balanced real frame contains the state and normalized magnitude directions | Paper-level complete matrix and column checks | `reference.py`, `circuits.py` | `test_real_frame.py`, `test_four_qubit_example.py` | Finite dimensions through the tested range. |
| The global real circuit decodes the complete real coordinate gradient | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_real_global_estimator.py` | Exact phase-calibrated controlled `O`. |
| The global complex magnitude circuit decodes all magnitude derivatives | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_magnitude.py` | General implementation is the separated phase/frame construction. |
| The direct complex phase circuit decodes all leaf-phase derivatives | Paper-level exact signed one-hot check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_phase.py` | One uniform phase direction is physically null. |
| A checkpoint circuit returns every derivative at a selected depth | Paper-level exact depth-block check at every tested depth | `circuits.py`, `decoders.py`, `reference.py` | `test_checkpoints.py` | Each selected depth uses its own circuit stream. |
| Integrated complex checkpoint substitution is valid on the active interface | Paper-level projected matrix and decoded-mean checks | `reference.py`, `circuits.py`, `conventions.py` | `test_operator_contracts.py`, `test_four_qubit_example.py` | It need not preserve the full unitary or full output distribution. |
| Singular magnitude and zero-amplitude phase coordinates are handled without division | Paper-level exact singular-case checks | `reference.py`, `circuits.py`, `decoders.py` | `test_singular_cases.py`, `test_complex_phase.py` | The coordinate derivative vanishes when the differential vanishes. |
| Every single-depth global, checkpoint, and direct-phase record has norm `2` | Paper-level algebraic record checks | `decoders.py`, `reference.py` | `test_decoders.py`, `test_checkpoints.py`, `test_complex_phase.py` | Finite premise of the concentration argument. |
| Global coordinatewise execution scaling is `O((1 + log(n/delta))/epsilon^2)` | Paper-level analytic deduction from fixed-norm block records | Record definitions and norm tests | Norm and decoder tests above | Absolute coordinatewise error. |
| The concatenated magnitude record has norm `2*sqrt(n)` and fixed `l_2` accuracy costs `O(n/epsilon_2^2)` up to confidence | Appendix-B analytic result with executable support | `supporting_analysis.py`, `docs/STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` | Directional guarantees require a nonzero-gradient margin. |
| Relative/directional control and magnitude-block natural-gradient conditioning follow from the `l_2` bound and metric factors | Appendix-B conditional result with detailed supporting analysis | `supporting_analysis.py`, `docs/STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` checks the direction bound and metric premises | Regularization is an optimizer-layer choice. |
| The direct-angle assigned Hopf CNOT ledger matches the manuscript's coordinate-preserving compiler model | **Paper-level resource claim** | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py` | `test_resource_ledger.py` | Direct-angle finite counts, not globally optimal or routed counts. |
| The same logical forward and frame objects admit one `O(N)` multiplexed realization | **Appendix-B robustness statement with detailed factorization and tests** | `optimized_compiler.py`, `qbp_optimized_resource_ledger.py` | `test_optimized_compiler.py` | One reusable clean flag; elementary multiplexor angles generally recombine Hopf coordinates. |
| A reflection sum can be estimated by coefficient-one-norm term sampling | Supporting algebraic extension | `supporting_analysis.py` | `test_supporting_analysis.py` | Portable upper bound, not an optimal Hamiltonian measurement strategy. |
| Independent symmetric readout errors transform the records by explicit attenuation/bin-mixing channels | Supporting analytic readout model | `supporting_analysis.py` | `test_supporting_analysis.py` | Readout-only model; no gate noise, routing, or mitigation claim. |

## Scope relative to the first paper

The first Hopf paper supplies:

- the balanced real and complex coordinate charts;
- the inverse map;
- the diagonal pullback metric;
- normalized coordinate directions;
- exact preparation of an indexed tangent state;
- indexed signed-branch gradient estimation;
- the native preparation schedules; and
- the direct-angle coordinate-to-control interpretation.

The present project supplies:

- the computationally addressed differential frame;
- one shared magnitude record across coordinates and depths;
- Walsh decoding of the complete magnitude block;
- the direct complete phase record;
- complete-gradient concentration ingredients;
- checkpoint reverse suffixes and their interface contracts; and
- the compiler, statistical, observable, and readout companions listed above.

The distinctive step is not Hadamard interference or the Walsh transform in
isolation. It is their integration with the addressed Hopf frame so that one
physical outcome contributes to every magnitude coordinate.

## Direct-angle compiler scope

The primary circuits preserve

```math
\text{one Hopf coordinate}
\longleftrightarrow
\text{one designated tree-split or leaf-phase location}
\longleftrightarrow
\text{one directly programmed physical angle}.
```

For magnitude coordinates the angle belongs to an internal tree split. In the
complex chart, each leaf-phase coordinate is likewise a direct phase angle. The
native preparations, `U_chk`, `W_R`, and `B_d` are different unitary
completions or circuit organizations, but they retain this coordinate-faithful
structure. State- or frame-equivalent multiplexing can preserve the logical
output while changing the elementary physical parameters, so estimator
correctness and resource-model inheritance are reported separately.

## Claim 1: inherited conventions and forward states

For `N = 2**n`:

- the real magnitude block has length `N - 1`;
- the complex phase block has length `N`;
- the combined complex coordinate order is
  `(theta_1, ..., theta_{N-1}, theta_N, ..., theta_{2N-1})`; and
- native `HopfReal` and `HopfComplex` schedules prepare the same initialized
  state column as the recursive reference map.

Evidence:

- `native_schedule.py` independently reproduces the first-paper schedules;
- `reference.py` builds the recursive real and complex states;
- `test_native_schedule.py` compares native state columns through `n = 5`;
- `test_operator_contracts.py` checks that native, depth-completion, and frame
  circuits share the initialized state column while differing as full
  unitaries.

Only the initialized-state-column contract is used for forward preparation.
It does not imply full-unitary equality or preservation of the direct-angle
ledger.

## Claim 2: balanced differential frame

The addressed real frame `W_R` has column `0` equal to the prepared state and
column `lambda(j)` equal to the normalized complement direction for internal
node `j`. The raw derivative is that direction multiplied by
`sqrt(g[j,j])`, and the complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Evidence:

- `real_tree_data` constructs subtree states, complements, metric factors, and
  raw derivatives independently of circuit builders;
- `real_frame_matrix` and `complex_frame_matrix` construct complete reference
  frames;
- `add_real_frame` and `add_complex_frame_separated` build circuit versions;
- `test_real_frame.py` and `test_complex_frame.py` compare matrices, inverses,
  state columns, and singular completions.

For node `j`, the addressed gate uses the same physical angle `theta_j` as the
forward split. The general complex construction is the separated `D_ph W_R`;
the complete addressed `R_C` compiler is a four-qubit regression fixture.

## Claim 3: global real gradient

Logical sequence:

```text
forward real Hopf preparation
-> controlled O
-> W_R dagger
-> ancilla-X and system-X measurement
```

One outcome `(b, y)` contributes

```math
Z_j^{\mathbb R}
=
2\sqrt{g^{\mathbb R}_{j,j}}
(-1)^{b+\lambda(j)\cdot y}
```

for every internal node. The decoder forms the signed system histogram, applies
an unnormalized fast Walsh-Hadamard transform, reads the marker entries, and
multiplies by the metric factors.

Evidence: `real_global_measurement_circuit`,
`decode_balanced_magnitude_gradient`, `real_gradient`, and
`test_real_global_estimator.py`.

## Claim 4: global complex gradient

The complex magnitude family uses

```text
U_chk -> D_ph -> controlled O -> D_ph dagger -> W_R dagger
-> all-X measurement
```

with the same marker and metric decoder as the real chart. The phase family uses

```text
complex Hopf preparation -> controlled O
-> ancilla-Y and system-Z measurement
```

and one outcome contributes

```math
Z_{N+\ell}^{\mathbb C,\mathrm{ph}}
=
2(-1)^b\mathbf 1[\widehat\ell=\ell].
```

Evidence: `complex_magnitude_separated_circuit`,
`complex_phase_measurement_circuit`, `decode_phase_gradient`,
`test_complex_magnitude.py`, and `test_complex_phase.py`. The phase tests include
zero-amplitude leaves and the null uniform-phase direction.

## Claim 5: checkpointed depth gradients

At selected depth `d`:

```text
forward Hopf preparation
-> controlled O
-> inverse suffix below depth d
-> ancilla-Y, target-Y, active-prefix-Z measurement
```

The record is

```math
Z_d^{\mathrm{chk}}
=
-2(-1)^{b_c+b_t}e_{\widehat r}.
```

Evidence: `real_checkpoint_measurement_circuit`,
`complex_checkpoint_separated_circuit`, `decode_checkpoint_gradient`,
`test_checkpoints.py`, and `test_singular_cases.py`. Each depth has its own
circuit stream.

## Claim 6: substitution contracts

The implementation distinguishes

```math
U=V,
```

```math
U|0\rangle^{\otimes n}=V|0\rangle^{\otimes n},
```

```math
UP_d=VP_d,
```

and the clean-flag contract

```math
\widetilde W_{\mathbb R}
(|\varphi\rangle|0\rangle_f)
=
(W_{\mathbb R}|\varphi\rangle)|0\rangle_f.
```

`test_operator_contracts.py` includes negative checks showing that weaker
contracts do not imply full-unitary equality. The integrated complex checkpoint
can change the complete distribution while preserving decoded gradient means.
`test_optimized_compiler.py` checks the clean-flag system block and zero flag
leakage. None of these logical contracts alone preserves one coordinate as one
elementary physical angle.

## Claim 7: singular coordinates and gauge

The estimators do not divide by a metric factor or leaf amplitude:

- zero incoming metric factor -> zero magnitude derivative and record;
- zero leaf amplitude -> zero phase derivative;
- unused completion columns do not alter the requested differential interface.

`test_singular_cases.py` uses exact upstream angles `0` and `pi/2`. The exact
phase gradient is zero-sum because expectation objectives are invariant under a
uniform leaf-phase shift. `project_common_phase_gradient` optionally removes
finite-shot common-phase noise, and `test_supporting_analysis.py` checks that
this projection is nonexpansive in Euclidean error.

## Claim 8: coordinatewise, Euclidean, directional, and metric-conditioned accuracy

Each magnitude-depth, checkpoint, and direct-phase record has norm `2`. The
fixed-norm concentration bound gives

```math
S_*(\eta)
=
\left\lceil
\frac{4\left(1+\sqrt{2\log(1/\eta)}\right)^2}
{\varepsilon^2}
\right\rceil.
```

Allocating failure over `n` magnitude depths yields

```math
S_{\mathrm{global}}
=
O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right),
```

and the complete checkpoint schedule gains one factor `n`. Concatenating the
`n` global magnitude blocks gives norm `2*sqrt(n)` and

```math
S_{2,\mathrm{mag}}
=
O\left(
\frac{n\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right).
```

For `g_hat = g + e`, `||e||_2 <= eta < ||g||_2 = G` implies

```math
g^T g_{\mathrm{hat}} > 0,
\qquad
\left\|
\frac{g_{\mathrm{hat}}}{\|g_{\mathrm{hat}}\|_2}
-
\frac{g}{G}
\right\|_2
\leq
\frac{2\eta}{G}.
```

Thus relative and directional guarantees require a nonzero-gradient margin.
For a magnitude coordinate, ordinary-record variance scales as `4*g[j,j]`, an
unregularized inverse-metric record as `4/g[j,j]`, and a regularized inverse as

```math
\frac{4g_{j,j}}{(g_{j,j}+\lambda)^2}
\leq
\frac{1}{\lambda}.
```

The detailed derivations and executable formulas are in
`docs/STATISTICAL_ACCURACY.md` and `supporting_analysis.py`.

## Claim 9: direct-angle ledger and optimized recompilation robustness

### Direct-angle assigned ledger

The paper-level ledger is implemented by:

- `controlled_ry_cnot_charge`;
- `controlled_rc_cnot_charge`;
- `depth_layer_cnot_charge`;
- `depth_preparation_cnot_charge`;
- `frame_cnot_charge`; and
- `inverse_suffix_cnot_charge`.

`test_resource_ledger.py` checks controlled-gate values, depth layers,
forward/frame/suffix totals, and the finite four-qubit record totals. These are
direct-angle assigned counts, not global optimality or routed-hardware claims.

### Multiplexed robustness companion

Each forward depth is a uniformly controlled `R_y`, so its core count sums to
`N-2`. Each addressed-frame depth is factored into:

1. compute the all-zero lower-suffix predicate into one clean flag;
2. apply a prefix-and-flag uniformly controlled `R_y`;
3. uncompute the flag.

The frame multiplexor-core count is `3*N/2 - 2` for `n >= 2`. Predicate work is
polynomial in `n`, so both the complete forward and addressed frame are `O(N)`
under this exact state-equivalent recompilation. The separated diagonal phase
layer is also `O(N)`.

Evidence:

- exact matrices and resource functions: `optimized_compiler.py`;
- tests: `test_optimized_compiler.py`;
- command-line table: `qbp_optimized_resource_ledger.py`;
- derivation and synthesis references: `docs/OPTIMIZED_COMPILATION.md`.

The result uses one reusable clean flag. It establishes asymptotic robustness
for this compiler without redefining the direct-angle Hopf setting, preserving
elementary coordinate angles, or claiming routed/noisy-device costs.

## Claim 10: reflection sums and readout transfer

For

```math
H=\sum_\alpha c_\alpha O_\alpha,
\qquad
\Lambda=\sum_\alpha|c_\alpha|,
```

sampling term `alpha` with probability `|c_alpha|/Lambda` and scaling its QBP
record by `Lambda*sign(c_alpha)` is unbiased. Its record norm gains a factor
`Lambda`, and sufficient shot counts gain `Lambda**2`.

Under independent symmetric readout flips, global parity coefficients are
attenuated only by the interference ancilla and marker-supported system bits.
Checkpoint and phase address errors mix one-hot bins through an independent
bit-flip channel.

Evidence: `supporting_analysis.py`, `test_supporting_analysis.py`, and
`docs/OBSERVABLES_AND_READOUT.md`. These are portable analytic extensions, not
a full general-Hamiltonian measurement comparison or hardware-noise benchmark.

## Validation matrix

| Test | Main responsibility |
|---|---|
| `test_conventions.py` | Tree indexing, basis order, parameter splitting, marker map, projectors, and observable conditions. |
| `test_native_schedule.py` | Native real and complex schedules and state columns. |
| `test_circuit_conventions.py` | Qibo bit significance and ancilla-`Y` sign convention. |
| `test_operator_contracts.py` | Full-unitary, state-column, and active-interface distinctions. |
| `test_real_frame.py` | Complete real frame and inverse. |
| `test_complex_frame.py` | Separated complex frame and four-qubit integrated compiler. |
| `test_real_global_estimator.py` | Complete real global gradient and Walsh decoder. |
| `test_complex_magnitude.py` | Complex magnitude gradient. |
| `test_complex_phase.py` | Direct phase gradient and zero-amplitude leaves. |
| `test_checkpoints.py` | Real and complex selected-depth gradients. |
| `test_singular_cases.py` | Exact singular-coordinate behavior. |
| `test_decoders.py` | Walsh, signed histograms, marginalization, and fixed-norm records. |
| `test_four_qubit_example.py` | Explicit compiler fixture labels and interfaces. |
| `test_resource_ledger.py` | Direct-angle assigned gate and record-circuit charges. |
| `test_optimized_compiler.py` | Clean-flag robustness factorization and multiplexor ledger. |
| `test_supporting_analysis.py` | `l_2`, direction, gauge, reflection-sum, and readout identities. |

## Deliberate nonclaims

The project does not provide evidence for optimizer quality, hardware
advantage, coherent-noise resilience, routing efficiency, approximate
synthesis, or arbitrary observables outside the stated reflection-access
models. The optimized robustness result applies to one exact recompilation; it
does not prove compiler-independent finite constants or preserve one coordinate
as one elementary physical angle.
