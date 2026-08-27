# Claim support and validation map

This page is for readers auditing whether the repository supports the claims
made by *Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz*.
It also identifies which supporting results live only in the repository.

The compiler hierarchy is load-bearing:

1. **Paper setting:** the direct-angle Hopf realization, in which each
   coordinate remains the physical rotation angle associated with its tree
   node.
2. **Repository robustness question:** whether state- or frame-equivalent
   optimized recompilation preserves the estimator identities and asymptotic
   resource conclusion after leaving that direct-angle setting.

The second item supports community scrutiny but does not redefine the ansatz or
the resource theorem studied in the papers.

The repository supports statements at four evidence levels. They should not be
conflated.

| Support type | Meaning |
|---|---|
| **Exact-logical circuit check** | A Qibo circuit is executed with the NumPy statevector backend and compared with an independent NumPy reference. |
| **Algebraic reference check** | A finite-dimensional identity, decoder, convention, or resource formula is evaluated without Qibo. |
| **Checked factorization plus external synthesis theorem** | The repository verifies an exact logical factorization; its asymptotic elementary-gate cost uses an established compiler result cited in the documentation. |
| **Analytic deduction exposed by code** | The repository checks the finite premises of a statistical or asymptotic statement, while the dimension-independent conclusion is mathematical rather than numerical. |

No numerical experiment can prove an asymptotic concentration or complexity
claim. The repository therefore identifies the tested finite ingredients and
the separate analytic deduction.

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
| Global coordinatewise execution scaling is `O((1 + log(n/delta))/epsilon^2)` | Paper-level analytic deduction from fixed-norm block records | Record definitions and norm tests | Norm and decoder tests above | The concentration inequality is mathematical, not numerically proved. |
| The complete concatenated magnitude record has norm `2*sqrt(n)` | Repository supporting result | `supporting_analysis.py` | `test_supporting_analysis.py` | No optimizer claim. |
| Fixed complete-magnitude `l_2` accuracy costs `O(n/epsilon_2^2)` up to confidence | Repository analytic deduction | `supporting_analysis.py`, `docs/STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` checks formula inputs | Relative and directional accuracy remain conditional on nonzero gradient. |
| The direct-angle assigned Hopf CNOT ledger matches the manuscript's coordinate-preserving compiler model | **Paper-level resource claim** | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py` | `test_resource_ledger.py` | Direct-angle finite counts, not globally optimal or routed counts. |
| The same logical forward and frame objects admit one `O(N)` multiplexed realization | **Repository-only robustness result outside the defining compiler** | `optimized_compiler.py`, `qbp_optimized_resource_ledger.py` | `test_optimized_compiler.py` | One reusable clean flag; elementary multiplexor angles generally recombine Hopf coordinates. |
| A reflection sum can be estimated by coefficient-one-norm term sampling | Repository algebraic extension | `supporting_analysis.py` | `test_supporting_analysis.py` | Portable upper bound, not an optimal Hamiltonian measurement strategy. |
| Independent symmetric readout errors transform the records by explicit attenuation/bin-mixing channels | Repository analytic readout model | `supporting_analysis.py` | `test_supporting_analysis.py` | Readout-only model; no gate noise, routing, or mitigation claim. |

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

The present repository supplies:

- the computationally addressed differential frame;
- one shared magnitude record across coordinates and depths;
- Walsh decoding of the complete magnitude block;
- the direct complete phase record;
- complete-gradient concentration ingredients;
- checkpoint reverse suffixes and their interface contracts; and
- the compiler and statistical companion analyses listed above.

The distinctive step is not Hadamard interference or the Walsh transform in
isolation. It is their integration with the addressed Hopf frame so that one
physical outcome contributes to every magnitude coordinate.

## Direct-angle compiler scope

The primary circuits preserve

```math
\theta_j
\longleftrightarrow
\text{tree node }j
\longleftrightarrow
\text{one programmable physical rotation angle}.
```

The native preparations, `U_chk`, `W_R`, and `B_d` are different unitary
completions or circuit organizations, but they retain this coordinate-faithful
tree structure. A state-equivalent multiplexed compiler can preserve the
logical output while changing the elementary physical parameters. The
repository therefore separates estimator correctness from inheritance of the
paper's resource model.

## Claim 1: inherited conventions and forward states

### Operational statement

For `N = 2**n`:

- the real magnitude block has length `N - 1`;
- the complex phase block has length `N`;
- the combined complex coordinate order is
  `(theta_1, ..., theta_{N-1}, theta_N, ..., theta_{2N-1})`; and
- native `HopfReal` and `HopfComplex` schedules prepare the same initialized
  state column as the recursive reference map.

### Evidence

- `qbp_validation/native_schedule.py` independently reproduces the first
  paper's schedules without importing Qibo.
- `qbp_validation/reference.py` builds the recursive real and complex states.
- `test_native_schedule.py` compares native state columns through `n = 5`.
- `test_operator_contracts.py` checks that native, depth-completion, and frame
  circuits share the initialized state column while differing as full
  unitaries.

### Boundary

The forward completions are not interchangeable in arbitrary unitary contexts.
Only the initialized-state-column contract is used for forward preparation.
State-column equality also does not imply preservation of the direct-angle
coordinate-to-control map or its assigned ledger.

## Claim 2: balanced differential frame

The addressed real frame `W_R` has:

- column `0` equal to the prepared real Hopf state; and
- column `lambda(j)` equal to the normalized complement direction associated
  with internal node `j`.

The raw coordinate derivative is the normalized direction multiplied by its
known incoming metric factor `sqrt(g[j,j])`. The complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

### Evidence

- `real_tree_data` in `reference.py` constructs subtree states, complements,
  metric factors, and raw derivatives independently of circuit builders.
- `real_frame_matrix` and `complex_frame_matrix` construct complete reference
  frames.
- `add_real_frame` and `add_complex_frame_separated` in `circuits.py` build the
  circuit versions.
- `test_real_frame.py` and `test_complex_frame.py` compare matrices, inverses,
  state columns, and singular completions.

### Direct-angle interpretation

For node `j`, the addressed gate uses the same physical angle `theta_j` as the
forward split at that tree node. The forward circuit prepares the split state;
the addressed frame places that state and its local complement in paired
computational columns. This shared angle is part of the geometric compiler
contract.

### Boundary

The complete addressed complex `R_C` compiler is an explicit four-qubit
fixture. The portable general construction is separated `D_ph W_R`.

## Claim 3: global real gradient

The logical sequence is:

```text
forward real Hopf preparation
-> controlled O
-> W_R dagger
-> ancilla-X and system-X measurement
```

One outcome `(b, y)` contributes to every internal node:

```math
Z_j^{\mathbb R}
=
2\sqrt{g^{\mathbb R}_{j,j}}
(-1)^{b+\lambda(j)\cdot y}.
```

The exact-distribution decoder:

1. accumulates `h[y] = count(0,y) - count(1,y)`;
2. applies the unnormalized fast Walsh-Hadamard transform;
3. reads the entries indexed by `lambda(j)`; and
4. multiplies by `2*sqrt_metric[j-1]/S`.

### Evidence

- Circuit: `real_global_measurement_circuit`.
- Decoder: `decode_balanced_magnitude_gradient`.
- Independent gradient: `real_gradient`.
- Test: `test_real_global_estimator.py`.

## Claim 4: global complex gradient

The complex gradient uses two circuit families.

### Magnitude family

```text
U_chk -> D_ph -> controlled O -> D_ph dagger -> W_R dagger
-> all-X measurement
```

It uses the same parity decoder and real metric factors as the real chart.

### Phase family

```text
complex Hopf preparation -> controlled O
-> ancilla-Y and system-Z measurement
```

One outcome `(b, ell)` contributes

```math
Z_{N+\ell}^{\mathbb C,\mathrm{ph}}
=
2(-1)^b\mathbf 1[\widehat\ell=\ell].
```

### Evidence

- Magnitude circuit and test: `complex_magnitude_separated_circuit`,
  `test_complex_magnitude.py`.
- Phase circuit, decoder, and test: `complex_phase_measurement_circuit`,
  `decode_phase_gradient`, `test_complex_phase.py`.

The phase tests include zero-amplitude leaves and the exact null uniform-phase
direction.

## Claim 5: checkpointed depth gradients

For selected depth `d`:

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

### Evidence

- Real circuit: `real_checkpoint_measurement_circuit`.
- Complex separated circuit: `complex_checkpoint_separated_circuit`.
- Decoder: `decode_checkpoint_gradient`.
- Tests: `test_checkpoints.py` and `test_singular_cases.py`.

Changing `d` changes the reverse suffix, readout target, and circuit template.
One checkpoint stream is not reused across different depths.

## Claim 6: logical substitution contracts versus compiler preservation

The repository distinguishes:

```math
U=V,
```

```math
U|0\rangle^{\otimes n}=V|0\rangle^{\otimes n},
```

and

```math
UP_d=VP_d.
```

`test_operator_contracts.py` includes negative checks showing that weaker
contracts do not imply full-unitary equality. For the four-qubit integrated
complex checkpoint, separated and integrated circuits may have different
complete distributions while returning the same decoded gradient mean.

The optimized frame adds a clean-flag contract:

```math
\widetilde W_{\mathbb R}
(|\varphi\rangle|0\rangle_f)
=
(W_{\mathbb R}|\varphi\rangle)|0\rangle_f.
```

`test_optimized_compiler.py` checks the system block and zero flag leakage.

These are correctness contracts. None alone implies that the replacement keeps
one Hopf coordinate as one elementary physical gate angle. Direct-angle
compiler preservation is therefore reported separately from state, unitary,
active-interface, or clean-flag equivalence.

## Claim 7: singular coordinates and gauge

The estimators do not divide by a metric factor or leaf amplitude. Therefore:

- a zero incoming metric factor produces a zero magnitude-coordinate record;
- a zero leaf amplitude produces a zero phase derivative; and
- arbitrary completion behavior outside the active differential interface does
  not alter the requested gradient.

`test_singular_cases.py` uses exact upstream angles `0` and `pi/2` and verifies
real, complex, global, and checkpoint outputs.

Expectation objectives are invariant under a uniform complex leaf-phase shift.
The exact phase gradient is zero-sum. `project_common_phase_gradient` optionally
projects a finite-shot estimate onto this physical subspace, and
`test_supporting_analysis.py` checks that the projection is nonexpansive in
Euclidean error.

## Claim 8: coordinatewise and complete-vector concentration ingredients

Each magnitude depth record has norm `2`. Checkpoint and direct phase records
are norm-`2` signed one-hot vectors. A standard fixed-norm vector concentration
bound gives

```math
S_*(\eta)
=
\left\lceil
\frac{4\left(1+\sqrt{2\log(1/\eta)}\right)^2}
{\varepsilon^2}
\right\rceil.
```

Allocating failure over `n` magnitude depths, plus the complex phase family
where applicable, gives

```math
S_{\mathrm{global}}
=
O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right),
```

and the complete checkpoint schedule gains an additional factor `n` because it
uses one independent stream per depth.

Concatenating the `n` global magnitude blocks gives record norm `2*sqrt(n)` and
therefore

```math
S_{2,\mathrm{mag}}
=
O\left(
\frac{n\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right).
```

See `docs/STATISTICAL_ACCURACY.md` for the directional, metric, and gauge
interpretation.

## Claim 9: direct-angle paper ledger and repository-only compiler robustness

### Direct-angle assigned ledger: paper-level resource claim

The manuscript ledger is implemented by:

- `controlled_ry_cnot_charge`;
- `controlled_rc_cnot_charge`;
- `depth_layer_cnot_charge`;
- `depth_preparation_cnot_charge`;
- `frame_cnot_charge`; and
- `inverse_suffix_cnot_charge`.

`test_resource_ledger.py` checks controlled-gate values, depth layers,
forward/frame/suffix totals, and the finite four-qubit record totals.

This ledger retains each Hopf coordinate as the physical angle of its designated
tree rotation. It is the compiler model used to state the manuscript's finite
resource comparison. It is not a claim of optimal synthesis over all exact
circuits implementing the same state or unitary.

### Multiplexed robustness companion: repository-only result

Each forward depth is logically a uniformly controlled `R_y`, so its core count
sums to `N-2`. Each addressed-frame depth is factored into:

1. compute the all-zero lower-suffix predicate into one clean flag;
2. apply a prefix-and-flag uniformly controlled `R_y`; and
3. uncompute the flag.

The frame multiplexor-core count is `3*N/2 - 2` for `n >= 2`. The predicate
control widths are exposed separately and give polynomial work in `n` under
standard exact multi-controlled-X synthesis. Thus the complete forward and
addressed frame are both `O(N)` under this state-equivalent recompilation.

Evidence:

- exact matrices and resource functions: `optimized_compiler.py`;
- tests: `test_optimized_compiler.py`;
- command-line table: `qbp_optimized_resource_ledger.py`;
- derivation and primary references: `docs/OPTIMIZED_COMPILATION.md`.

The optimized conclusion uses one reusable clean flag. Its elementary physical
angles generally need not equal the Hopf coordinates individually. It therefore
tests asymptotic robustness outside the defining compiler rather than replacing
the paper's resource model. It is not a routed, noise-aware, or
approximate-synthesis count.

## Claim 10: reflection sums and readout transfer

For

```math
H=\sum_\alpha c_\alpha O_\alpha,
\qquad
\Lambda=\sum_\alpha|c_\alpha|,
```

sampling term `alpha` with probability `|c_alpha|/Lambda` and scaling its QBP
record by `Lambda*sign(c_alpha)` is unbiased. Its fixed-norm bound gains a
factor `Lambda`, and sufficient shot counts gain `Lambda**2`.

Under independent symmetric readout flips, global parity coefficients are
attenuated only by the interference ancilla and marker-supported system bits.
Checkpoint and phase address errors instead mix one-hot bins through an
independent-bit-flip channel.

Evidence:

- formulas: `supporting_analysis.py`;
- tests: `test_supporting_analysis.py`;
- interpretation and boundaries: `docs/OBSERVABLES_AND_READOUT.md`.

These are portable analytic extensions, not a full general-Hamiltonian
measurement comparison or hardware-noise benchmark.

## Validation matrix by test file

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

The repository does not provide evidence for optimizer quality, hardware
advantage, coherent-noise resilience, routing efficiency, approximate
synthesis, or arbitrary observables outside the stated reflection-access
models.

The optimized robustness analysis does not redefine the Hopf ansatz, prove that
every state-equivalent compiler has the same cost, or preserve one coordinate
as one elementary physical angle. The absence of a multi-model hardware
benchmark is a scope decision, not missing support for the exact-logical claims
above.
