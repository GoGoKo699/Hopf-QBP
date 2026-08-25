# Claim support and validation map

This page is for reviewers and readers auditing whether the repository actually
supports the claims made by *Compass in the Mirror: Quantum Backpropagation
with the Hopf Ansatz*.

The repository supports claims at three different levels. They should not be
conflated.

| Support type | Meaning |
|---|---|
| **Exact-logical circuit check** | A Qibo circuit is executed with the NumPy statevector backend and compared with an independent NumPy reference. |
| **Algebraic reference check** | A finite-dimensional identity, decoder, convention, or resource formula is evaluated without Qibo. |
| **Analytic deduction exposed by code** | The repository checks the premises of a statistical or asymptotic statement, while the dimension-independent deduction is mathematical rather than numerical. |

No numerical experiment can prove an asymptotic concentration or complexity
claim. The repository therefore identifies which finite ingredients are tested
and which conclusion is analytic.

## Audit summary

| Paper-level claim | Repository support | Main implementation | Main tests | Boundary |
|---|---|---|---|---|
| Native real and complex preparations reproduce the Hopf state | Exact state-column checks | `native_schedule.py`, `reference.py`, `circuits.py` | `test_native_schedule.py`, `test_operator_contracts.py` | State-column equality, not full-unitary equality. |
| The balanced real frame contains the state and normalized magnitude directions | Complete matrix and column checks | `reference.py`, `circuits.py` | `test_real_frame.py`, `test_four_qubit_example.py` | Finite dimensions through the tested range. |
| The global real circuit decodes the complete real coordinate gradient | Exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_real_global_estimator.py` | Exact-logical access to controlled `O`. |
| The global complex magnitude circuit decodes all magnitude derivatives | Exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_magnitude.py` | General implementation is the separated phase/frame construction. |
| The direct complex phase circuit decodes all leaf-phase derivatives | Exact signed one-hot check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_phase.py` | One uniform phase direction is automatically null. |
| A checkpoint circuit returns every derivative at a selected depth | Exact depth-block check at every tested depth | `circuits.py`, `decoders.py`, `reference.py` | `test_checkpoints.py` | Each selected depth uses its own circuit stream. |
| Integrated complex checkpoint substitution is valid on the active interface | Projected matrix and decoded-mean checks | `reference.py`, `circuits.py`, `conventions.py` | `test_operator_contracts.py`, `test_four_qubit_example.py` | It need not preserve the full unitary or full output distribution. |
| Singular magnitude and zero-amplitude phase coordinates are handled without division | Exact singular-case checks | `reference.py`, `circuits.py`, `decoders.py` | `test_singular_cases.py`, `test_complex_phase.py` | The coordinate derivative correctly vanishes when the differential vanishes. |
| Every global-depth, checkpoint, and direct-phase record has norm `2` | Algebraic record checks | `decoders.py`, `reference.py` | `test_decoders.py`, `test_checkpoints.py`, `test_complex_phase.py` | This is the finite premise used by the concentration argument. |
| The assigned Hopf CNOT ledger matches the stated compiler model | Formula and finite-ledger checks | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py` | `test_resource_ledger.py` | Assigned model, not transpiler or hardware counts. |
| Global execution scaling is `O((1 + log(n/delta))/epsilon^2)` | Analytic deduction from fixed-norm block records | Record definitions and norm tests | Norm and decoder tests above | The concentration inequality is mathematical, not numerically proved. |
| Complete checkpoint execution scaling gains a factor `n` | Analytic accounting over depth-specific streams | Circuit family organization | `test_checkpoints.py` verifies separate depth templates | The complete schedule runs one stream per depth. |

## Claim 1: inherited Hopf conventions and forward states

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
  paper's native schedules without importing Qibo.
- `qbp_validation/reference.py` builds the recursive real and complex states.
- `test_native_schedule.py` compares native state columns through `n = 5`.
- `test_operator_contracts.py` checks that native, depth-completion, and frame
  circuits share the initialized state column while differing as full
  unitaries.

### What is not claimed

The different forward completions are not interchangeable in arbitrary
unitary contexts. Only the initialized-state-column contract is used for
forward preparation.

## Claim 2: balanced differential frame

### Operational statement

The addressed real frame `W_R` has:

- column `0` equal to the prepared real Hopf state; and
- column `lambda(j)` equal to the normalized complement direction associated
  with internal node `j`.

The raw coordinate derivative equals the normalized direction multiplied by
its known incoming metric factor `sqrt(g[j,j])`.

The complex magnitude frame is

```math
W_C = D_{\mathrm{ph}} W_R.
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

### Boundary

The complete addressed complex `R_C` compiler in this repository is an
explicit four-qubit fixture. The portable general implementation is the
separated `D_ph W_R` construction.

## Claim 3: global real gradient

### Circuit

The general logical sequence is:

```text
forward real Hopf preparation
-> controlled O
-> W_R dagger
-> ancilla-X and system-X measurement
```

One outcome `(b, y)` contributes to every internal node:

```math
Z_j^{\mathbb{R}}
=
2\sqrt{g^{\mathbb{R}}_{j,j}}
(-1)^{b+\lambda(j)\cdot y}.
```

### Decoder

1. Accumulate the signed system histogram
   `h[y] = count(0, y) - count(1, y)`.
2. Apply the unnormalized fast Walsh-Hadamard transform.
3. Read the entries indexed by `lambda(j)`.
4. Multiply by `2 * sqrt_metric[j - 1] / S`.

### Evidence

- Circuit: `real_global_measurement_circuit`.
- Decoder: `decode_balanced_magnitude_gradient`.
- Independent gradient: `real_gradient`.
- Test: `test_real_global_estimator.py`.

The tests compare complete decoded gradients with independent analytic
coordinates for multiple deterministic Hermitian-unitary observables.

## Claim 4: global complex gradient

The complex gradient has two independent circuit families.

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
Z_{N+\ell}^{\mathbb{C},\mathrm{ph}}
=
2(-1)^b\mathbf{1}[\widehat{\ell}=\ell].
```

### Evidence

- Magnitude circuit: `complex_magnitude_separated_circuit`.
- Magnitude test: `test_complex_magnitude.py`.
- Phase circuit: `complex_phase_measurement_circuit`.
- Phase decoder: `decode_phase_gradient`.
- Phase test: `test_complex_phase.py`.

The phase tests also check zero-amplitude leaves and the automatically null
uniform-phase direction.

## Claim 5: checkpointed depth gradients

### Circuit

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
-2(-1)^{b_c+b_t}e_{\widehat{r}}.
```

### Evidence

- Real circuit: `real_checkpoint_measurement_circuit`.
- Complex separated circuit: `complex_checkpoint_separated_circuit`.
- Decoder: `decode_checkpoint_gradient`.
- Tests: `test_checkpoints.py` and `test_singular_cases.py`.

The complete test suite checks every depth for `n <= 4` and compares each
returned block with the corresponding slice of an independent full gradient.

### Boundary

Changing `d` changes the inverse suffix, readout target, and circuit template.
The checkpoint method does not reuse one quantum stream across different
depths.

## Claim 6: substitution contracts

The repository explicitly distinguishes:

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

`test_operator_contracts.py` includes negative checks showing that the weaker
contracts do not imply full-unitary equality.

For the four-qubit complex checkpoint fixture, the integrated and separated
circuits can have different complete output distributions while returning the
same decoded gradient mean. This is intentional and directly tested.

## Claim 7: singular coordinates

The estimators do not divide by a metric factor or by a leaf amplitude.
Therefore:

- a zero incoming metric factor produces a zero magnitude-coordinate record;
- a zero leaf amplitude produces a zero phase derivative; and
- arbitrary completion behavior outside the active differential interface does
  not alter the requested gradient.

`test_singular_cases.py` uses exact upstream angles `0` and `pi/2` and verifies
real, complex, global, and checkpoint outputs.

## Claim 8: fixed-norm concentration ingredients

For each magnitude depth, the global record vector has Euclidean norm `2`.
Checkpoint and direct phase records are signed one-hot vectors with norm `2`.
The repository checks these record properties and their means.

A standard vector concentration bound then yields the sufficient count

```math
S_*(\eta)
=
\left\lceil
\frac{4\left(1+\sqrt{2\log(1/\eta)}\right)^2}{\varepsilon^2}
\right\rceil.
```

Allocating failure probability over `n` magnitude depths, plus the complex
phase family where applicable, gives:

```math
S_{\mathrm{global}}
=
O\!\left(\frac{1+\log(n/\delta)}{\varepsilon^2}\right),
```

and

```math
S_{\mathrm{checkpoint}}
=
O\!\left(\frac{n\{1+\log(n/\delta)\}}{\varepsilon^2}\right).
```

The numerical suite verifies the record identities and unbiased means. It does
not purport to numerically prove the concentration theorem.

## Claim 9: assigned Hopf CNOT ledger

The ledger uses declared charges for controlled one-qubit rotations and sums
them over generated Hopf schedules. The implementation is in:

- `controlled_ry_cnot_charge`;
- `controlled_rc_cnot_charge`;
- `depth_layer_cnot_charge`;
- `depth_preparation_cnot_charge`;
- `frame_cnot_charge`;
- `inverse_suffix_cnot_charge`; and
- the native schedule charge functions.

`test_resource_ledger.py` checks controlled-gate values, depth layers,
forward/frame/suffix totals, and the finite four-qubit record totals.

The ledger excludes the controlled observable, readout, device routing,
approximate synthesis, and separately assigned diagonal phase-layer cost where
stated. It is a compiler-relative comparison, not a hardware estimate.

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
| `test_resource_ledger.py` | Assigned gate and record-circuit charges. |

## Deliberate nonclaims

The repository does not provide evidence for optimizer quality, hardware
advantage, noise resilience, routing efficiency, approximate synthesis,
finite-shot wall-clock performance, or general observables outside the stated
controlled-reflection model.

The absence of those studies is a scope decision, not missing support for the
paper's stated exact-logical claims.
