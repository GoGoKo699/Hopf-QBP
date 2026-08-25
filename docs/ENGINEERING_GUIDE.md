# Engineering guide

This page specifies the implementable Hopf-QBP interface without reproducing
the paper's motivation, proofs, or four-qubit narrative example.

It is organized around the questions an engineer needs to answer:

1. What is the input contract?
2. Which circuit family returns the requested gradient block?
3. What exactly is measured?
4. How is the classical record decoded?
5. Which circuit substitutions are valid?
6. Which resource costs are included?
7. How can the reference implementation be adapted safely?

## 1. Input and output contract

### Inputs

- `n`: number of system qubits.
- `N = 2**n`: Hilbert-space dimension.
- Hopf coordinates:
  - real chart: `theta_mag` of length `N - 1`;
  - complex chart: `theta_mag` of length `N - 1` and `theta_ph` of length `N`.
- `O`: an `N x N` known Hermitian-unitary matrix or an equivalent exact logical
  implementation.
- exact controlled access to `O` with known branch phase.
- a requested output:
  - complete real gradient;
  - complete complex gradient;
  - all magnitude coordinates;
  - one selected magnitude depth; or
  - complex phase coordinates.

### Outputs

The output is a classical real vector in manuscript coordinate order:

- real: length `N - 1`;
- complex: length `2*N - 1`, obtained by concatenating magnitude and phase
  blocks.

The reference implementation works with complete probability distributions.
A shot-based implementation replaces exact probabilities by empirical counts
without changing the record definitions.

## 2. Coordinate, tree, and bit conventions

These conventions are load-bearing. A different bit order or rotation
normalization changes signs, marker labels, or prepared states.

### Coordinate order

```text
real:
(theta_1, ..., theta_{N-1})

complex:
(theta_1, ..., theta_{N-1}, theta_N, ..., theta_{2N-1})
```

In Python:

```text
theta_mag[j - 1] == theta_j             for 1 <= j < N
theta_ph[ell]    == theta_{N + ell}     for 0 <= ell < N
```

Use `split_theta` and `join_theta` in `qbp_validation/conventions.py` rather
than duplicating the indexing logic.

### Tree indexing

Internal nodes use breadth-first labels:

$$
j = 2^d + r,
\qquad
0\le d<n,
\qquad
0\le r<2^d.
$$

The computational-basis marker assigned to node `j` is implemented by
`marker_label(j, n)`:

$$
\lambda(j)
=
(2r+1)2^{n-d-1}.
$$

The leftmost basis label of the corresponding subtree is implemented by
`anchor_label(j, n)`:

$$
a(j)=r2^{n-d}.
$$

Use `frame_gate_specs(n)` and `depth_gate_specs(n, d)` to generate gate
locations. Do not recreate the tree map from a drawing.

### Basis order and Qibo wire order

Basis states are written

$$
|q_n\cdots q_1\rangle.
$$

Qibo system index `0` is the most-significant basis bit and corresponds to
manuscript wire `q_n`. Qibo index `n - 1` corresponds to `q_1`.

Use:

- `manuscript_wire_from_qibo_index`;
- `qibo_index_from_manuscript_wire`; and
- `bit_at`.

### Rotation convention

The Hopf papers use

$$
R_y(\theta)=e^{-i\theta Y}.
$$

Qibo's `RY(phi)` uses the half-angle convention, so the circuit builders send

```python
qibo.gates.RY(target, 2.0 * theta)
```

Missing this factor of two produces the wrong state and gradient.

### Open controls

Addressed two-level operations use both positive and negative controls.
`circuits.py` implements negative controls by conjugating the controlled gate
with `X` gates. An alternative backend must preserve the same control pattern.

## 3. Core data structures

### Recursive reference data

`real_tree_data(theta_mag)` returns:

- `state`: the real Hopf state;
- `subtree`: recursively prepared subtree states;
- `complements`: normalized magnitude directions;
- `sqrt_metric`: incoming amplitude weights;
- `metric = sqrt_metric**2`; and
- `derivatives`: raw coordinate derivatives.

This object is the easiest reference when adapting a decoder or validating a
new backend.

### Forward implementations

The repository exposes three forward completions:

1. native `HopfReal` or `HopfComplex` schedules;
2. depth completion `U_chk`; and
3. addressed frame preparation.

They can share the initialized state column without being equal as full
unitaries. Forward substitution is valid when only the prepared state column
enters the later circuit.

The designated resource accounting uses:

```text
real forward:    U_chk
complex forward: D_ph U_chk
```

Native forward circuits are also validated and may be used when their compiler
is preferred.

### Depth-layer compiler

For depth `d` and prefix `r`, define the internal node

$$
j=2^d+r.
$$

`add_depth_layer` applies `R_y(theta_j)` to Qibo system index `d`, controlled by
the first `d` system qubits matching the binary prefix `r`. Lower suffix qubits
are not controls. The `2**d` control patterns are disjoint, so gates within one
depth layer commute on the computational-basis sectors they address.

The complete depth preparation is

$$
U_{\mathrm{chk}}
=
U_{n-1}\cdots U_1U_0.
$$

The circuit builder appends layers in increasing `d`, which produces this
state-update order.

### Addressed real frame

For node `j = 2**d + r`, the anchor and marker labels are

$$
a(j)=r2^{n-d},
\qquad
\lambda(j)=(2r+1)2^{n-d-1}.
$$

They differ only on Qibo system index `d`. `add_real_frame` therefore applies
one addressed `R_y(theta_j)` on that target, controlled by all other system
qubits matching the anchor label. The gates are appended in increasing depth
and node order.

This completion satisfies:

- column `0` is the prepared state; and
- column `lambda(j)` is the normalized complement direction for node `j`.

The inverse frame reverses the gate order and negates every angle.

### Phase layer and complex frame

The leaf-phase layer is

$$
D_{\mathrm{ph}}
=
\operatorname{diag}
\left(e^{i\theta_N},\ldots,e^{i\theta_{2N-1}}\right).
$$

The portable complex magnitude frame is

$$
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
$$

`add_phase_layer` represents `D_ph` as one exact logical `Unitary`. This is an
access-model choice, not a claim that a generic hardware implementation has
zero cost.

### Reverse suffixes

For selected depth `d`, define

$$
B_d=U_{n-1}\cdots U_{d+1}.
$$

`add_inverse_depth_suffix` appends the inverse layers from `n - 1` down to
`d + 1`. The real checkpoint reverse block is `B_d dagger`. The general
separated complex checkpoint first applies `D_ph dagger` and then
`B_d dagger` after the controlled observable.

### Complex one-qubit gate

The native complex schedule and the explicit integrated fixtures use

$$
R_C(\theta_a,\theta_b,\theta_c)
=
\begin{pmatrix}
 e^{i\theta_b}\cos\theta_a & -e^{-i\theta_c}\sin\theta_a\\
 e^{i\theta_c}\sin\theta_a & e^{-i\theta_b}\cos\theta_a
\end{pmatrix}.
$$

The general engineering path does not require reconstructing the explicit
four-qubit phase compiler: use the separated `D_ph` and `W_R` blocks unless an
integrated compiler has been independently proved under the appropriate
contract.

## 4. Objective-access contract

The repository assumes

$$
O=O^\dagger,
\qquad
O^2=I,
$$

and exact access to

$$
\operatorname{ctrl}(O)
=
|0\rangle\!\langle0|\otimes I
+
|1\rangle\!\langle1|\otimes O.
$$

### Controlled-branch phase

If the implemented controlled branch is `exp(i*gamma) O`, then the measured
`X` and `Y` quadratures are rotated by `gamma`. A known phase can be corrected
with an ancilla phase gate or calibrated equatorial measurement. An unknown
phase invalidates the direct decoder.

### Observable validation

`is_hermitian_unitary` in `reference.py` checks the matrix contract used by the
tests. Production code should perform an equivalent compile-time or
construction-time check.

### Measurement-basis convention

The reference circuits implement a `Y`-basis measurement by applying
`S dagger` and then `H` before computational-basis readout. In state-update
order the net rotation is `H S dagger`. The decoder signs in the phase and
checkpoint records assume this convention.

### What is not supported automatically

The repository does not convert a generic Hermitian observable into a
controlled reflection. A sum of terms, block encoding, LCU construction, or
application-specific binary test requires a separate controlled-access layer.

## 5. Global real gradient

### Circuit builder

```python
real_global_measurement_circuit(theta_mag, observable)
```

Logical sequence:

```text
ancilla H
-> real Hopf forward preparation
-> controlled O
-> W_R dagger
-> X measurement on ancilla and all system qubits
```

`real_global_native_forward_circuit` replaces the frame forward with the native
`HopfReal` schedule while keeping the same reverse decoder.

### Outcome

One execution returns:

```text
(b_m, y)
```

where `b_m` is the ancilla bit and `y` is the `n`-bit system outcome.

### Coordinate record

For every internal node `j`:

$$
Z_j^{\mathbb R}(b_m,y)
=
2\sqrt{g_{j,j}^{\mathbb R}}
(-1)^{b_m+\lambda(j)\cdot y}.
$$

One physical outcome is reused for all `N - 1` magnitude coordinates.
Coordinate records from one execution are correlated; independent executions
remain independent.

### Exact-distribution decoder

```python
decode_balanced_magnitude_gradient(
    probabilities,
    sqrt_metric,
    n,
    use_fwht=True,
)
```

The decoder:

1. reshapes the probability vector into ancilla and system blocks;
2. forms `h[y] = p(0,y) - p(1,y)`;
3. applies `fwht(h)`;
4. reads `moment[marker_label(j,n)]`; and
5. multiplies by `2*sqrt_metric[j-1]`.

For empirical counts, first divide the signed histogram by the number of
executions or apply the equivalent normalization after the transform.

### Classical cost

For `S` outcomes:

- histogram accumulation: `O(S)`;
- Walsh transform: `O(N log N)`;
- metric rescaling and output: `O(N)`;
- auxiliary histogram storage: `O(N)`.

## 6. Global complex gradient

The complex gradient is the concatenation of two separately executed circuit
families.

### 6.1 Magnitude block

General builder:

```python
complex_magnitude_separated_circuit(theta_mag, theta_ph, observable)
```

Designated logical sequence:

```text
U_chk
-> D_ph
-> controlled O
-> D_ph dagger
-> W_R dagger
-> all-X measurement
```

The complex magnitude record uses the same marker map and metric factors as the
real chart:

$$
Z_j^{\mathbb C,\mathrm{mag}}
=
2\sqrt{g_{j,j}^{\mathbb C}}
(-1)^{b_m+\lambda(j)\cdot y},
$$

with

$$
g_{j,j}^{\mathbb C}=g_{j,j}^{\mathbb R}.
$$

Use the same `decode_balanced_magnitude_gradient` function.

### 6.2 Phase block

Builder:

```python
complex_phase_measurement_circuit(theta_mag, theta_ph, observable)
```

Native-forward variant:

```python
complex_phase_native_forward_circuit(theta_mag, theta_ph, observable)
```

Logical sequence:

```text
complex Hopf forward preparation
-> controlled O
-> ancilla-Y measurement
-> system-Z measurement
```

One outcome `(b_p, ell)` contributes the signed one-hot vector

$$
Z^{\mathbb C,\mathrm{ph}}
=
2(-1)^{b_p}e_{\ell}.
$$

Decoder:

```python
decode_phase_gradient(probabilities)
```

For empirical data, maintain two leaf histograms and return

```text
2 * (counts_ancilla_0 - counts_ancilla_1) / S
```

### Uniform phase direction

The sum of all phase derivatives is zero. This is a physical global-phase
redundancy, not a decoder defect.

## 7. Checkpointed magnitude gradients

Use a checkpoint when only one depth or a small set of depths is needed.

### Real builder

```python
real_checkpoint_measurement_circuit(theta_mag, observable, depth)
```

Native-forward variant:

```python
real_checkpoint_native_forward_circuit(theta_mag, observable, depth)
```

### Complex builder

```python
complex_checkpoint_separated_circuit(
    theta_mag,
    theta_ph,
    observable,
    depth,
)
```

### Logical sequence

```text
Hopf forward preparation
-> controlled O
-> chart-specific inverse suffix below depth d
-> ancilla-Y measurement
-> depth target-Y measurement
-> active-prefix-Z measurement
```

The lower suffix need not be measured.

### Outcome and record

One execution returns:

```text
(b_c, b_t, r)
```

and contributes

$$
Z_d^{\mathrm{chk}}
=
-2(-1)^{b_c+b_t}e_r
\in\mathbb R^{2^d}.
$$

Decoder:

```python
decode_checkpoint_gradient(probabilities, n, depth)
```

For empirical data, keep one signed histogram of length `2**depth`.

### Coordinate placement

The returned block corresponds to nodes

```text
start = 2**depth - 1
stop  = 2**(depth + 1) - 1
```

in zero-based Python slicing of the magnitude-gradient vector.

### Final depth

At `depth = n - 1`, the real inverse suffix is the identity. The complex
separated circuit still removes `D_ph` before the target readout.

### Multiple depths

Each requested depth needs a distinct circuit template because its inverse
suffix and target wire differ. For depths `d_1, ..., d_q`, execute `q` streams
and place each decoded block in its breadth-first slice.

## 8. Substitution contracts

This is the most important implementation distinction in the repository.

### Full-unitary equality

$$
U=V.
$$

Use this when the complete action on every input state matters.

### Initialized-state-column equality

$$
U|0\rangle^{\otimes n}
=
V|0\rangle^{\otimes n}.
$$

This is sufficient for replacing a forward preparation that is always applied
to the initialized system register. It is not sufficient for replacing a
reverse block.

### Active-interface equality

$$
UP_d=VP_d.
$$

This is sufficient when the state entering the block is guaranteed to lie in
the checkpoint interface selected by `P_d`.

`checkpoint_interface_projector(n, depth)` constructs the reference projector.

### Integrated four-qubit fixtures

The repository includes:

- an addressed four-qubit `R_C` compiler for `W_C`; and
- a four-qubit depth-2 complex suffix `B_2_C`.

They exist to test compiler identities:

- the frame is equal to `W_C` up to one common phase; and
- the suffix matches `D_ph B_2` on the active interface.

The integrated checkpoint may change unused columns and the complete output
distribution while preserving the required gradient correlators. Do not use
these helpers as evidence for a general all-`n` integrated compiler.

## 9. Singular coordinates

The reference implementation never divides by `sqrt_metric` or by a leaf
amplitude.

### Zero magnitude metric

If an upstream path weight is zero, then:

```text
sqrt_metric[j - 1] == 0
```

and the corresponding global magnitude record is identically zero. The raw
coordinate derivative also vanishes.

### Zero complex leaf amplitude

A phase derivative is proportional to the amplitude on that leaf. If the leaf
amplitude is zero, the decoded phase derivative is zero.

### Engineering rule

Do not normalize a raw derivative by a vanishing metric factor in the gradient
pipeline. Normalized frame directions are compiler objects; coordinate
derivatives retain the metric multiplier.

## 10. Fixed-norm records and shot allocation

Every magnitude depth record, checkpoint record, and direct phase record has
Euclidean norm at most `2`. This gives one dimension-independent statistical
scale per block.

A sufficient count for one block with failure probability `eta` is

$$
S_*(\eta)
=
\left\lceil
\frac{4\left(1+\sqrt{2\log(1/\eta)}\right)^2}{\varepsilon^2}
\right\rceil.
$$

For complete-coordinate absolute error:

```text
real global magnitude:       S_*(delta / n)
complex global magnitude:    S_*(delta / (2*n))
complex direct phase:        S_*(delta / 2)
real complete checkpoint:    n * S_*(delta / n)
complex complete checkpoint: n * S_*(delta / (2*n)) + S_*(delta / 2)
```

These are sufficient allocations, not adaptive stopping rules. They target
coordinatewise absolute `l_infinity` accuracy.

## 11. Choosing global versus checkpoint

| Question | Global frame | Checkpoint |
|---|---|---|
| How many depths per circuit family? | All magnitude depths | One selected depth |
| Reverse block | Complete inverse frame | Suffix below selected depth |
| Measurement | All qubits in `X` | Ancilla and target in `Y`, prefix in `Z` |
| Decoder | Signed `N`-bin histogram + FWHT | Signed `2**d`-bin histogram |
| Quantum stream reuse | Across all depths | Within one depth only |
| Best use | Complete or many-depth gradients | Layer-local or sparse-depth updates |
| Final real depth | Still uses inverse frame | No reverse suffix |

For requested depths `d_1, ..., d_q`, compare the compiled repeated cost of the
`q` suffix circuits with one complete frame circuit. The statistical scale is
the same at a fixed depth; the difference is circuit organization.

## 12. Assigned resource ledger

The repository uses a declared compiler-relative Hopf CNOT model.

### Controlled `R_y`

For `q` controls:

```text
q = 0:       0
1 <= q <= 4: 2**(q + 1) - 2
q >= 5:      16*(q + 1) - 40
```

Implemented by `controlled_ry_cnot_charge(q)`.

### Controlled `R_C`

For `q` controls:

```text
q = 0:       0
1 <= q <= 4: 2**(q + 1) - 2
q >= 5:      20*(q + 1) - 38, when q + 1 is odd
             20*(q + 1) - 42, when q + 1 is even
```

Implemented by `controlled_rc_cnot_charge(q)`.

### Derived charges

```text
frame W_R:
((2**n) - 1) * controlled_ry_cnot_charge(n - 1)

depth layer U_d:
(2**d) * controlled_ry_cnot_charge(d)

U_chk:
sum(depth_layer_cnot_charge(d) for d in range(n))

inverse suffix B_d dagger:
sum(depth_layer_cnot_charge(k) for k in range(d + 1, n))
```

Use `qbp_resource_ledger.py` rather than copying these formulas into downstream
analysis.

### Included and excluded costs

Included:

- generated Hopf controlled-gate charges for the selected forward and reverse
  blocks.

Excluded unless separately supplied:

- controlled `O`;
- readout;
- device routing;
- approximate synthesis;
- application workspace;
- generic diagonal phase-layer synthesis; and
- backend transpilation effects.

The output is an assigned logical ledger, not a physical gate estimate.

## 13. Minimal exact-logical usage

The following examples use complete statevector distributions. They are small
reference calls, not sampling or performance benchmarks.

### Complete real gradient

```python
from qbp_validation.cases import observables, regular_theta_mag
from qbp_validation.circuits import probabilities, real_global_measurement_circuit
from qbp_validation.decoders import decode_balanced_magnitude_gradient
from qbp_validation.reference import real_tree_data

n = 3
theta_mag = regular_theta_mag(n)
observable = observables(n)[0]

probs = probabilities(
    real_global_measurement_circuit(theta_mag, observable)
)

gradient = decode_balanced_magnitude_gradient(
    probs,
    real_tree_data(theta_mag).sqrt_metric,
    n,
)
print(gradient)  # length 2**n - 1
```

### Complete complex gradient

```python
import numpy as np

from qbp_validation.cases import complex_theta_mag, observables, theta_ph
from qbp_validation.circuits import (
    complex_magnitude_separated_circuit,
    complex_phase_measurement_circuit,
    probabilities,
)
from qbp_validation.decoders import (
    decode_balanced_magnitude_gradient,
    decode_phase_gradient,
)
from qbp_validation.reference import real_tree_data

n = 3
theta_mag = complex_theta_mag(n)
phase = theta_ph(n)
observable = observables(n)[0]

magnitude_probs = probabilities(
    complex_magnitude_separated_circuit(theta_mag, phase, observable)
)
phase_probs = probabilities(
    complex_phase_measurement_circuit(theta_mag, phase, observable)
)

magnitude_gradient = decode_balanced_magnitude_gradient(
    magnitude_probs,
    real_tree_data(theta_mag).sqrt_metric,
    n,
)
phase_gradient = decode_phase_gradient(phase_probs)
full_gradient = np.concatenate((magnitude_gradient, phase_gradient))

print(full_gradient)  # length 2**(n + 1) - 1
```

### One checkpoint depth

```python
from qbp_validation.cases import observables, regular_theta_mag
from qbp_validation.circuits import (
    probabilities,
    real_checkpoint_measurement_circuit,
)
from qbp_validation.decoders import decode_checkpoint_gradient

n = 4
depth = 2
theta_mag = regular_theta_mag(n)
observable = observables(n)[0]

probs = probabilities(
    real_checkpoint_measurement_circuit(theta_mag, observable, depth)
)
depth_gradient = decode_checkpoint_gradient(probs, n, depth)

start = 2**depth - 1
stop = 2**(depth + 1) - 1
print(depth_gradient)  # corresponds to full_gradient[start:stop]
```

## 14. Reference implementation map

### Circuit construction

`qbp_validation/circuits.py`

- `_controlled_ry_with_pattern`
- `_controlled_unitary_with_pattern`
- `add_real_frame`
- `add_depth_layer`
- `add_depth_preparation`
- `add_inverse_depth_suffix`
- `add_native_real_preparation`
- `add_native_complex_preparation`
- `add_phase_layer`
- `add_complex_frame_separated`
- `add_controlled_observable`
- global, phase, and checkpoint circuit builders

### Independent formulas

`qbp_validation/reference.py`

- recursive states and derivatives;
- real and complex frames;
- exact coordinate gradients;
- depth prefix and suffix matrices;
- interface projectors and compiler fixtures.

### Classical decoding

`qbp_validation/decoders.py`

- `fwht`
- `signed_system_histogram`
- `decode_balanced_magnitude_gradient`
- `decode_phase_gradient`
- `decode_checkpoint_gradient`
- single-shot record constructors

### Conventions and ledger

`qbp_validation/conventions.py`

- parameter splitting;
- tree and marker maps;
- basis and wire translation;
- active-interface projectors;
- compiler-relative charge formulas.

## 15. Adapting the reference safely

### Replace the simulator backend

Preserve:

- basis significance;
- rotation normalization;
- negative-control semantics;
- controlled-branch phase;
- measurement-basis convention; and
- probability or count ordering.

Add a backend conformance test before running the gradient suite. The existing
`test_circuit_conventions.py` shows the minimum bit-order and ancilla-`Y` checks.

### Replace the forward compiler

A forward replacement is valid if it prepares exactly the same state from the
initialized input. Test state-column equality, not merely state fidelity on a
small collection of parameter points.

### Replace a reverse compiler

State-column equality is not enough. Establish either:

- complete frame/unitary equality; or
- the exact active-interface identity used by the checkpoint circuit.

Then compare decoded gradient means. Complete distribution equality is not
required unless the substitution claims it.

### Add shot sampling

The record formulas already define unbiased estimators. A sampling layer should:

1. preserve the complete joint measurement outcome;
2. accumulate signed histograms without discarding system labels;
3. use independent fresh preparations across executions; and
4. report confidence allocation separately for magnitude depths and complex
   phases.

### Add a new controlled observable

The observable layer must document:

- proof or construction of Hermitian unitarity;
- controlled implementation;
- branch-phase calibration;
- logical or physical resource cost; and
- any workspace that is absent from the Hopf-only ledger.

## 16. Common failure modes

| Failure | Consequence |
|---|---|
| Using `RY(theta)` instead of `RY(2*theta)` in Qibo | Wrong prepared state and all downstream gradients. |
| Reversing Qibo bit significance | Wrong marker parities and checkpoint prefixes. |
| Ignoring negative controls | Addressed rotations act on extra basis pairs. |
| Unknown controlled-branch phase | `X`/`Y` quadratures are rotated; signs are invalid. |
| Treating state-column equality as full-unitary equality | Invalid reverse substitution. |
| Treating active-interface equality as full-unitary equality | Incorrect claims about complete output distributions. |
| Dividing by zero metric factors | Artificial singularity not present in the coordinate derivative. |
| Mixing magnitude and phase streams | Incompatible reverse blocks and measurement bases. |
| Calling ledger values transpiler counts | Misstates the resource model. |
| Generalizing the four-qubit integrated fixture to arbitrary `n` | Unsupported compiler claim. |

## 17. Validation workflow for an engineering change

A modification should pass the following sequence:

1. `python validate_qbp.py --analytic`
2. `python validate_qbp.py --smoke`
3. `python validate_qbp.py`
4. `python make_validation_figures.py`
5. `python qbp_resource_ledger.py --nmin 2 --nmax 10`

For a new backend or compiler, add tests at the contract level it claims:
full-unitary, state-column, or active-interface. Also add at least one decoded
mean comparison against `reference.py` and one singular-coordinate case.

The repository's purpose is to keep these contracts inspectable. New features
should not weaken that separation by deriving both the circuit and its expected
answer from the same implementation path.
