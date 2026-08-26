# Observable extensions and analytic readout sensitivity

The validated core contract uses one known Hermitian unitary `O`, exact
phase-calibrated controlled access to `O`, and exact-logical circuit execution.
This page gives two portable extensions that do not alter that contract:
reflection-sum term sampling and an analytic independent-readout-error model.
It is not a hardware benchmark.

## 1. Core controlled-reflection contract

The objective is

```math
E_O(\theta)
=
\langle\psi(\theta)|O|\psi(\theta)\rangle,
```

with

```math
O^\dagger=O,
\qquad
O^2=I.
```

The controlled branch must have a known relative phase. If the implemented
branch is `exp(i gamma) O`, the measured interference quadrature is rotated by
`gamma`. A known phase can be compensated; an unknown phase invalidates the
direct decoder.

The repository does not claim to compile an arbitrary nonunitary observable,
block encoding, or application-specific binary test into this interface.

## 2. Reflection-sum Hamiltonians

Suppose

```math
H
=
\sum_{\alpha=1}^{L}c_\alpha O_\alpha,
\qquad
O_\alpha^\dagger=O_\alpha,
\qquad
O_\alpha^2=I,
```

with real coefficients. Define

```math
\Lambda
=
\sum_{\alpha=1}^{L}|c_\alpha|.
```

For `Lambda > 0`, sample term `alpha` with

```math
p_\alpha
=
\frac{|c_\alpha|}{\Lambda}.
```

If `Z^(alpha)` is any unbiased Hopf-QBP record for `O_alpha`, output

```math
\widetilde Z
=
\Lambda\,\mathrm{sgn}(c_\alpha)Z^{(\alpha)}.
```

Then

```math
\mathbb E[\widetilde Z]
=
\sum_\alpha c_\alpha\mathbb E[Z^{(\alpha)}]
=
\nabla\langle H\rangle.
```

A norm-`2` depth or phase record becomes a norm-at-most-`2 Lambda` sampled
record. The sufficient execution count therefore gains a factor
`Lambda**2`. For the complete concatenated magnitude record, the norm bound is
`2 Lambda sqrt(n)`.

The expected controlled-operation cost of one term-sampled record is

```math
\sum_\alpha p_\alpha C(\mathrm{ctrl}(O_\alpha)).
```

A matched scalar comparator can use the same term sampling and controlled-term
cost. This is a portable upper bound, not a claim that independent term
sampling is optimal for every Hamiltonian. Commuting-group measurements,
classical shadows, coefficient-aware shot allocation, or application-specific
block encodings may provide better scalar and gradient interfaces and must be
compared under their own access assumptions.

## 3. Global parity under independent readout flips

For internal node `j`, the global magnitude sign is

```math
(-1)^{b+\lambda(j)\cdot y}.
```

Let the interference-ancilla bit flip independently with probability `p_c` and
system bit `k` flip with probability `p_k`. Conditional on the ideal outcome,
the observed sign is attenuated by

```math
\kappa_j
=
(1-2p_c)
\prod_{k:\lambda(j)_k=1}(1-2p_k).
```

Only marker-supported system bits enter this product. The record is not
necessarily a parity of the entire measured string.

For uniform error probability `p`, with node `j = 2**d + r`,

```math
\kappa_j
=
(1-2p)^{1+\mathrm{wt}(\lambda(j))}
=
(1-2p)^{2+\mathrm{wt}(r)}.
```

The largest sign-parity weight at depth `d` is therefore `d+2`, including the
interference ancilla.

## 4. Checkpoint and direct-phase records

The checkpoint sign is

```math
(-1)^{b_c+b_t}.
```

Independent ancilla and target readout errors attenuate it by

```math
(1-2p_c)(1-2p_t).
```

Errors in the measured prefix do not add to this sign parity; instead they mix
the one-hot address bins through the classical independent-bit-flip channel.
For bit error probabilities `p_1, ..., p_d`, the bin channel is

```math
T
=
\bigotimes_{k=1}^{d}
\begin{pmatrix}
1-p_k & p_k\\
p_k & 1-p_k
\end{pmatrix}.
```

The direct complex phase record behaves similarly:

- the ancilla error attenuates the sign by `1-2p_c`;
- system `Z`-readout errors mix the leaf bins through the corresponding
  independent-bit-flip channel.

If the error rates are calibrated and the transfer factors are nonsingular,
one may invert or regularize these classical channels. Such correction
amplifies variance and is not included in the exact-logical theorem.

## 5. What this analysis does and does not establish

It establishes the exact mean transformation under independent symmetric
readout flips. It does not model:

- coherent gate errors;
- two-qubit depolarizing noise;
- correlated readout;
- device connectivity and SWAP insertion;
- controlled-observable synthesis noise;
- error mitigation; or
- optimizer behavior.

A meaningful comparison of global, checkpoint, separate-tangent, and
parameter-shift methods under those effects must fix a device topology,
transpiler, observable compiler, noise channel, mitigation method, parameter
ensemble, shot allocation, and optimizer. Those choices define a separate
hardware study rather than a validation requirement for the present
exact-logical interface.

## 6. Executable support

The reflection-sum and readout transfer formulas are implemented in:

```text
qbp_validation/supporting_analysis.py
qbp_validation/tests/test_supporting_analysis.py
```

The tests verify:

- unbiased one-norm term sampling;
- the `Lambda` record-norm factor;
- marker-supported global attenuation;
- checkpoint and direct-phase sign attenuation; and
- stochasticity of the independent bin-mixing channel.

Run:

```bash
python validate_qbp.py --analytic
```
