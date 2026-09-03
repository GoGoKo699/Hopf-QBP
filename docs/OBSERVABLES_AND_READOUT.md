# Reflection-sum objectives and analytic readout sensitivity

The paper's validated core uses one known Hermitian-unitary objective, exact
phase-calibrated controlled access, and exact-logical circuit execution. This
page expands the main-text reflection-sum formula and records an independent
symmetric-readout model. It is not a hardware benchmark.

## 1. Core controlled-reflection contract

The objective is

```math
E_O(\boldsymbol\theta)
=
\langle\psi(\boldsymbol\theta)|O|\psi(\boldsymbol\theta)\rangle,
\qquad
O^\dagger=O,
\qquad
O^2=I.
```

The controlled branch must have a known relative phase. If the implemented
branch is `exp(i gamma) O`, the measured interference components are rotated by
`gamma`. A known phase can be compensated; an unknown phase invalidates the
fixed decoder. A classical description of `O`, or uncontrolled access to it,
does not itself supply this coherent interface.

## 2. Reflection-sum objectives

Let

```math
H
=
\sum_{\alpha=1}^{L}a_\alpha O_\alpha,
\qquad
O_\alpha^\dagger=O_\alpha,
\qquad
O_\alpha^2=I,
\qquad
\Lambda=\sum_\alpha|a_\alpha|>0.
```

Suppose every term has the calibrated controlled access above. Sample term
`alpha` with

```math
p_\alpha
=
\frac{|a_\alpha|}{\Lambda}.
```

If `Z^(alpha)` is any unbiased Hopf-QBP record for `O_alpha`, return

```math
\widetilde Z
=
\Lambda\,\mathrm{sgn}(a_\alpha)Z^{(\alpha)}.
```

Then

```math
\begin{aligned}
\mathbb E[\widetilde Z]
&=
\sum_\alpha
\frac{|a_\alpha|}{\Lambda}
\Lambda\,\mathrm{sgn}(a_\alpha)
\mathbb E[Z^{(\alpha)}]\\
&=
\sum_\alpha a_\alpha\nabla E_{O_\alpha}
=
\nabla\langle H\rangle.
\end{aligned}
```

A base norm bound `B` becomes `Lambda*B`, so the corresponding sufficient
execution count gains a factor `Lambda**2`. For a norm-`2` depth or phase
record the sampled norm is at most `2*Lambda`; for the concatenated magnitude
record it is at most `2*Lambda*sqrt(n)`.

The expected controlled-term charge of one sampled record is

```math
\sum_\alpha p_\alpha C(\mathrm{ctrl}(O_\alpha)).
```

A matched scalar comparator uses the same term distribution and expected
controlled-term charge. This is a portable upper bound, not a claim that term
sampling is optimal for every Hamiltonian. Commuting groups, shadow methods,
coefficient-aware allocation, or application-specific block encodings require
their own access and normalization models.

## 3. Global parity under independent readout flips

For internal node `j`, the global magnitude sign is

```math
(-1)^{b+\lambda(j)\cdot y}.
```

Let the interference-ancilla bit flip independently with probability `p_c` and
system bit `k` with probability `p_k`. Conditional on the ideal outcome, the
mean sign is attenuated by

```math
\kappa_j
=
(1-2p_c)
\prod_{k:\lambda(j)_k=1}(1-2p_k).
```

Only marker-supported system bits enter this product. For a uniform error rate
`p` and node `j=2**d+r`,

```math
\kappa_j
=
(1-2p)^{1+\mathrm{wt}(\lambda(j))}
=
(1-2p)^{2+\mathrm{wt}(r)}.
```

Thus the largest sign-parity weight at depth `d` is `d+2`, including the
interference ancilla.

## 4. Checkpoint and direct-phase records

The checkpoint sign is `(-1)^(b_c+b_t)`. Independent branch and target errors
attenuate it by

```math
(1-2p_c)(1-2p_t).
```

Prefix errors do not add to the sign parity; they mix the one-hot address bins
through

```math
T
=
\bigotimes_{k=1}^{d}
\begin{pmatrix}
1-p_k & p_k\\
p_k & 1-p_k
\end{pmatrix}.
```

For the direct complex phase record, the branch error attenuates the sign by
`1-2p_c`, while system `Z`-readout errors mix leaf bins through the analogous
independent-bit-flip channel.

If calibrated transfer factors are nonsingular, one may invert or regularize
these classical channels. Such correction amplifies variance and is not part of
the exact-logical theorem.

## 5. Boundary of this analysis

The formulas above establish unbiased reflection-sum sampling and exact mean
transformations under independent symmetric readout flips. They do not model:

- coherent state-preparation, frame, or controlled-reflection errors;
- two-qubit depolarizing noise;
- correlated readout;
- device routing and SWAP insertion;
- approximate synthesis;
- mitigation; or
- optimizer behavior.

A hardware comparison must fix the topology, transpiler, controlled-objective
compiler, noise channel, mitigation method, parameter ensemble, shot
allocation, and requested output norm.

## 6. Executable support

The formulas are implemented and tested in:

```text
qbp_validation/supporting_analysis.py
qbp_validation/tests/test_supporting_analysis.py
```

The tests verify coefficient-one-norm probabilities, unbiased scaled records,
the `Lambda` norm factor, marker-supported parity attenuation, checkpoint and
phase attenuation, and stochasticity of the bin-mixing channel.

Run:

```bash
python validate_qbp.py --analytic
```
