# Ancilla--depth robustness of the global Hopf frame

## Status

This page is a **research companion and theorem candidate**. It is not yet a
paper-level claim and does not modify the direct-angle resource theorem.

The exact Hopf identities below are implemented and tested in this repository.
The asymptotic depth deduction additionally invokes the exact circuit-synthesis
theorems of Sun, Tian, Yang, Yuan, and Zhang. The result concerns the **global
Hopf differential frame**. It does not establish compiler invariance of the
checkpoint protocol.

## 1. Question and conclusion

Let `n` be the number of system qubits and let

```math
N=2^n.
```

Sun et al. give exact state-preparation circuits of size `O(N)` whose depth
changes with the available clean ancillary workspace. The question is whether
the complete Hopf reverse frame can follow the same ancilla--depth profile, so
that global Hopf backpropagation remains asymptotically matched to scalar state
preparation after leaving the direct-angle compiler.

The candidate conclusion is:

> For a state compiler using `m` clean ancillary qubits, the real global Hopf
> frame has an exact clean implementation using at most `m+1` ancillary qubits, size
> `O(N)`, and the same asymptotic depth upper envelopes as the state-preparation
> constructions displayed in Figure 1 of Sun et al. The extra qubit is one
> reusable suffix flag. The separated complex frame inherits the same profile.

This is a structure-aware frame compiler. It does **not** follow by inverting an
arbitrary state-preparation circuit.

## 2. Required logical contract

The forward state-preparation circuit only needs the initialized-column
contract

```math
U_{\mathrm{prep}}|0^n\rangle=|\psi(\boldsymbol\theta)\rangle.
```

The global reverse circuit needs more. With clean workspace `w`, it must satisfy

```math
\widetilde W_{\mathbb R}
\bigl(|\varphi\rangle|0^w\rangle\bigr)
=
\bigl(W_{\mathbb R}|\varphi\rangle\bigr)|0^w\rangle
```

for every system input `|varphi>`. State-column equality alone is insufficient:
a state-equivalent unitary can act arbitrarily on the tangent subspace and mix
the marker amplitudes used by the decoder.

## 3. Addressed Hopf layers

Write the real frame as

```math
W_{\mathbb R}^{(n)}
=L_{n-1}^{(n)}\cdots L_1^{(n)}L_0^{(n)}.
```

At depth `d`, the layer contains `2**d` disjoint two-level rotations. For
`r=0,...,2**d-1`, define

```math
a_{d,r}=r2^{n-d},
\qquad
b_{d,r}=(2r+1)2^{n-d-1}.
```

Then

```math
L_d^{(n)}
=
\prod_{r=0}^{2^d-1}
G_{a_{d,r},b_{d,r}}
\bigl(\theta_{2^d+r}\bigr),
```

where `G_{a,b}(theta)` embeds the Hopf `R_y(theta)` block on computational
basis states `|a>` and `|b>`. The pairs at one depth are disjoint.

## 4. Exact conditioned-prefix identity

For a cut `0 <= t <= n`, let

```math
F_t^{(n)}
=L_{t-1}^{(n)}\cdots L_0^{(n)}
```

and let

```math
P_{n-t}=|0^{n-t}\rangle\!\langle0^{n-t}|.
```

The first `t` full-system layers obey the exact identity

```math
\boxed{
F_t^{(n)}
=
W_{\mathbb R}^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes\bigl(I-P_{n-t}\bigr).
}
```

Here `W_R^(t)` uses precisely the first `2**t-1` Hopf angles.

### Proof

For every `d<t`, the addressed condition in `L_d^(n)` requires all bits below
the depth-`d` target to be zero. Split those lower bits into:

1. the remaining bits inside the first `t` qubits; and
2. the external suffix of length `n-t`.

On the sector selected by `P_(n-t)`, the layer is exactly `L_d^(t)` on the
prefix. On the orthogonal suffix sector it is the identity. Therefore

```math
L_d^{(n)}
=
L_d^{(t)}\otimes P_{n-t}
+
I_{2^t}\otimes\bigl(I-P_{n-t}\bigr).
```

The two suffix projectors are orthogonal and invariant under every factor, so
multiplying the layers gives the boxed identity.

The repository checks this equality for every cut through `n=8` with independent
random angle assignments.

## 5. Unary realization of the prefix frame

Let `E_t` encode a `t`-qubit computational basis state into the
single-excitation code of `2**t` unary modes:

```math
E_t|r\rangle=|e_r\rangle.
```

Replace every computational two-level rotation in `W_R^(t)` by the same Givens
rotation on unary modes `a_(d,r)` and `b_(d,r)`. Denote the resulting unary
network by `G_t`. Then

```math
E_t^\dagger G_tE_t=W_{\mathbb R}^{(t)},
```

and

```math
\bigl(I-E_tE_t^\dagger\bigr)G_tE_t=0.
```

The second identity states that the network does not leak from the unary code.
At each tree depth the mode pairs are disjoint, so all Givens rotations at that
depth can be applied in parallel. A number-preserving two-mode Givens rotation
is a fixed two-qubit unitary, and adding one copied predicate control gives a
fixed three-qubit unitary. Both have constant-size, constant-depth exact
decompositions over arbitrary one-qubit gates and CNOTs. The unary Hopf network
therefore has `t` logical Givens layers and `O(2**t)` size, and its controlled
version has the same asymptotic depth and size once the controls are fanned out.

Dense exact tests verify the code action, zero leakage, layer disjointness, and
unitarity through `t=3`. The ambient unary Hilbert space has dimension
`2**(2**t)`, so larger dense tests are deliberately blocked.

## 6. Clean unary-prefix compiler

Sun et al. Lemma 28 supplies an exact unary-to-binary transformation on
`2**t` register qubits. It has depth `O(t)`, size `O(2**t)`, and uses
`2**(t+1)` clean ancillary qubits. Its inverse maps

```math
|r\rangle|0^{2^t-t}\rangle
\longmapsto
|e_r\rangle.
```

The conditioned prefix in Section 4 can therefore be implemented as follows.

1. Apply the inverse unary-to-binary transform to encode the binary prefix into
   the unary code.
2. If `t<n`, compute the predicate `[external suffix = 0]` into one clean wire.
3. Fan out that predicate coherently to enough clean controls for the widest
   unary layer.
4. Apply the `t` controlled, parallel Givens layers.
5. Undo the fanout and predicate.
6. Apply the unary-to-binary transform.

The widest unary layer contains `2**(t-1)` rotations. A CNOT tree produces that
many coherent controls in depth `O(t)` and size `O(2**t)`. The controls are not
measured, are never modified by the controlled Givens gates, and are uncomputed
exactly.

The clean ancillary requirement is bounded by

```math
(2^t-t)+2^{t+1}=3\,2^t-t.
```

The first term supplies the unary register wires not already occupied by the
`t` system qubits. The second is the transform workspace. After the encoding
transform, that workspace is clean and is reused for the suffix flag and its
fanout. Thus the prefix compiler has depth `O(n+t)=O(n)` and size `O(2**t)`.

The repository uses the conservative Sun-style choice

```math
t=
\min\left\{
 n,
 \max\left(0,\left\lfloor\log_2(m/3)\right\rfloor\right)
\right\}.
```

It guarantees `3*2**t-t <= m` without relying on the small `-t` saving.

## 7. Remaining addressed layers

For every remaining nonfinal depth `d>=t`, compute the lower-suffix-zero
predicate into one reusable flag, apply one uniformly controlled `R_y`, and
uncompute the flag. The uniformly controlled gate has:

- `d` prefix controls;
- one suffix flag control; and
- one target.

Its total width is therefore `d+2`. At the final depth there is no lower suffix,
so the ordinary width is `n` and no flag predicate is required.

Sun et al. Lemma 12 implements a `k`-qubit uniformly controlled gate with `m`
clean ancillary qubits in depth

```math
O\left(k+\frac{2^k}{k+m}\right)
```

and size `O(2**k)`. Their Lemma 41 gives an exact linear-depth
multi-controlled-X construction without additional workspace. Consequently the
tail contributes

```math
O\left(
 n(n-t+1)
 +
 \sum_{d=t}^{n-1}
 \frac{2^{d+O(1)}}{d+m+O(1)}
\right)
```

depth. The geometric-tail estimate

```math
\sum_{k=1}^{n}\frac{2^k}{k+m}
=O\left(\frac{2^n}{n+m}\right)
```

gives

```math
D_{\mathrm{tail}}
=O\left(
 n(n-t+1)+\frac{N}{n+m}
\right).
```

The summed uniformly controlled gate sizes are geometric, and the predicate
work is polynomial in `n`, so the tail size is `O(N)`.

## 8. Candidate real-frame theorem

> **Candidate theorem (clean ancilla--depth robustness of the real global
> frame).** Let `m>=0`, and choose `t` as in Section 6. In the exact all-to-all
> circuit model with arbitrary one-qubit gates and CNOTs, the addressed real
> Hopf frame has a clean implementation using at most `m+1` ancillary qubits, size
> `O(N)`, and depth
>
> ```math
> \boxed{
> D_{\mathrm{frame}}(n,m)
> =
> O\left(
> n(n-t+1)+\frac{N}{n+m}
> \right).
> }
> ```
>
> The possible additional qubit is the reusable flag used by the remaining
> addressed layers. It is returned to `|0>` after every layer. Some endpoint
> cases do not need it, but the theorem uses the uniform upper bound `m+1`.

The result is an upper-bound construction. It does not claim a new lower bound
or an exact finite-depth constant.
Reversing the clean circuit implements `W_R^dagger` with the same depth, size,
and workspace, which is the operation used by the global gradient protocol.

## 9. Reduction to the three Figure 1 regimes

The theorem candidate reproduces the state-preparation upper envelopes in
Figure 1 of Sun et al.

### Smaller ancillary workspace

When

```math
m=O\left(\frac{N}{n\log n}\right),
```

the sequential term is dominated by `N/(n+m)`. Hence

```math
D_{\mathrm{frame}}(n,m)
=O\left(\frac{N}{n+m}\right).
```

### Intermediate ancillary workspace

When

```math
m=\omega\left(\frac{N}{n\log n}\right)
\quad\text{and}\quad
m=o(N),
```

we have `n-t=O(log n)`, so

```math
D_{\mathrm{frame}}(n,m)=O(n\log n).
```

This retains the same logarithmic upper--lower gap as the cited state-preparation
result. No attempt is made here to close that gap.

### Linear ancillary workspace

When

```math
m=\Omega(N),
```

we have `n-t=O(1)`, and therefore

```math
D_{\mathrm{frame}}(n,m)=O(n).
```

Thus the global frame matches all three asymptotic **upper** profiles, with one
additional reusable clean qubit.

## 10. Separated complex frame

The portable complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

Sun et al. Lemmas 10 and 11 give exact `O(N)`-size diagonal synthesis with depth
`O(N/n)` without workspace and `O(log m+N/m)` in the relevant ancillary range.
Using no more workspace than needed, this diagonal layer does not exceed the
corresponding Figure 1 state-preparation upper envelope. Therefore the separated
complex frame has the same three asymptotic profiles.

The direct complex phase-gradient family does not use an inverse differential
frame and is unaffected by this compiler question.

## 11. Record-wise classical decoder

The existing exact-distribution decoder forms a signed histogram and applies a
fast Walsh--Hadamard transform. Its arithmetic cost is

```math
O(S+Nn)
```

for `S` measured outcomes.

For the optimized `O(N)` compiler regime, a second decoder is useful. One
outcome `(b,y)` contributes the complete Walsh character vector

```math
(-1)^b
\bigl((-1)^{k\cdot y}\bigr)_{k=0}^{N-1}.
```

All `N` entries can be generated recursively in `O(N)` arithmetic. Averaging
`S` outcomes therefore costs

```math
O(SN)
```

and uses `O(N)` storage. One may choose the smaller of the two decoders:

```math
O\bigl(S+N\min(S,n)\bigr).
```

At fixed absolute coordinate accuracy and confidence, global Hopf QBP uses
`S=O(log n)=O(log log M)` executions. The record-wise decoder then has
output-sensitive cost `O(N log n)`, so it does not introduce an additional
factor of `n` relative to an `O(N)` compiled scalar program.

The implementation is tested against the empirical histogram-plus-FWHT decoder
for every `n=1,...,6` in the deterministic analytic suite.

## 12. Interpretation

The result supports the following conceptual statement:

> The balanced Hopf chart supplies the coherent differential frame, metric
> weights, marker structure, and shared gradient record. A compiler inherits
> global Hopf backpropagation scaling when it realizes that frame cleanly at
> cost comparable to forward state preparation.

This goes beyond the designated direct-angle realization. It is not a claim
that every state-equivalent compiler works automatically.

The chart-level and compiler-level ingredients are distinct:

| Ingredient | Origin |
|---|---|
| Orthogonal weighted tangent frame | Hopf chart |
| Depthwise norm-two gradient records | Hopf chart and global measurement |
| Marker/Walsh decoder | Hopf chart and chosen computational addressing |
| Clean realization of the complete frame | Structure-aware compiler |
| Ancilla--depth upper profile | Compiler synthesis theorems |
| Controlled-objective access | QBP access model |

## 13. Deliberate boundaries

This companion does not establish:

- validity of the inverse of an arbitrary state-preparation compiler;
- preservation of one Hopf coordinate as one elementary physical angle;
- the same result for checkpoint interfaces after arbitrary resynthesis;
- a strict zero-extra-ancilla frame compiler at the `m=0` endpoint;
- approximate Clifford+T error propagation;
- routed-device depth, noise robustness, or hardware constants;
- generic arbitrary-unitary synthesis of the frame; or
- new optimality lower bounds.

Using a generic arbitrary-unitary compiler for `W_R` would generally cost
`O(N**2)` size and would not support the matched conclusion.

## 14. Executable support

Exact structural checks and term ledgers are in:

```text
qbp_validation/ancilla_depth_compiler.py
qbp_validation/tests/test_ancilla_depth_compiler.py
qbp_ancilla_depth_ledger.py
```

The record-wise decoder is in:

```text
qbp_validation/decoders.py
qbp_validation/tests/test_decoders.py
```

Run:

```bash
python validate_qbp.py --analytic
python qbp_ancilla_depth_ledger.py --n 10
python qbp_ancilla_depth_ledger.py --n 12 --ancillas 0,24,256,4096
```

The ledger reports exact structural quantities and unit-coefficient proxies for
the asymptotic depth terms. It is not an exact finite gate-depth estimator.

## 15. Primary references

- X. Sun, G. Tian, S. Yang, P. Yuan, and S. Zhang,
  [Asymptotically Optimal Circuit Depth for Quantum State Preparation and
  General Unitary Synthesis](https://doi.org/10.1109/TCAD.2023.3244885),
  *IEEE Transactions on Computer-Aided Design of Integrated Circuits and
  Systems* **42**, 3301--3314 (2023); [arXiv:2108.06150](https://arxiv.org/abs/2108.06150).
- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  [Transformation of quantum states using uniformly controlled
  rotations](https://arxiv.org/abs/quant-ph/0407010),
  *Quantum Information and Computation* **5**, 467--473 (2005).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  [Quantum circuits with uniformly controlled one-qubit
  gates](https://arxiv.org/abs/quant-ph/0410066),
  *Physical Review A* **71**, 052330 (2005).
