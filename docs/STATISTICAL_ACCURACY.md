# Statistical accuracy beyond coordinatewise error

The manuscript's primary finite-shot target is simultaneous absolute
coordinatewise accuracy. Appendix B now gives the complete-vector Euclidean
bound, the conditional relative and directional consequences, and the
magnitude-block natural-gradient conditioning statement. This page retains the
full derivation, gauge interpretation, optimizer boundary, and executable test
map without changing the core estimator.

## 1. Coordinatewise target

For each magnitude depth, one global outcome produces a vector record of exact
Euclidean norm `2`. A checkpoint record and a direct complex phase record are
also norm-`2` signed one-hot vectors.

For a norm-`R` random vector, the concentration bound used by the manuscript
gives the sufficient count

```math
S(R,\varepsilon,\eta)
=
\left\lceil
\frac{R^2
\left(1+\sqrt{2\log(1/\eta)}\right)^2}
{\varepsilon^2}
\right\rceil.
```

Allocating failure probability over the `n` magnitude depths gives

```math
S_{\infty,\mathrm{global}}
=
O\left(
\frac{1+\log(n/\delta)}{\varepsilon_\infty^2}
\right).
```

This is an absolute `l_infinity` statement. It is not silently interpreted as
relative error or optimizer convergence.

## 2. Complete magnitude-vector `l_2` accuracy

Concatenate the `n` magnitude-depth records obtained from one global outcome:

```math
Z_{\mathrm{mag}}
=
Z_0\oplus Z_1\oplus\cdots\oplus Z_{n-1}.
```

Every depth block has norm `2`, so every concatenated record has deterministic
norm

```math
\|Z_{\mathrm{mag}}\|_2
=
2\sqrt n.
```

Applying the same vector concentration argument directly, without a union bound
over coordinates or depths, yields

```math
S_{2,\mathrm{mag}}
=
\left\lceil
\frac{4n
\left(1+\sqrt{2\log(1/\delta)}\right)^2}
{\varepsilon_2^2}
\right\rceil.
```

Therefore fixed complete-vector Euclidean accuracy requires

```math
O\left(
\frac{n\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right)
=
O\left(
\frac{\log M\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right)
```

independent executions. At fixed shot count the accumulated complete-vector
noise grows as `sqrt(n) = sqrt(log M)`, not as `sqrt(M)`.

For the complex chart, the direct phase record is produced by a separate
norm-`2` stream. Allocating the total Euclidean error and failure probability
between the magnitude and phase blocks adds only an `O(1)` phase-stream term;
the complete complex scaling remains `O(n)` at fixed `l_2` accuracy.

## 3. Relative and directional guarantees are conditional

Let

```math
\widehat g=g+e,
\qquad
\|e\|_2\leq\eta,
\qquad
\|g\|_2=G.
```

When `0 <= eta < G`,

```math
g^\mathsf{T}\widehat g
\geq
G(G-\eta)>0,
```

so `-g_hat` is guaranteed to be a descent direction. The normalized-direction
error obeys

```math
\left\|
\frac{\widehat g}{\|\widehat g\|_2}
-
\frac{g}{\|g\|_2}
\right\|_2
\leq
\frac{2\eta}{G}.
```

Choosing `eta = rho*G` gives relative `l_2` error at most `rho`, normalized
direction error at most `2*rho`, and the sufficient global magnitude count

```math
S_{\mathrm{rel}}
=
O\left(
\frac{n\{1+\log(1/\delta)\}}
{\rho^2G^2}
\right).
```

A fixed allocation between magnitude and phase streams gives the same `n`
dependence for the complete complex gradient. No uniform relative or
directional guarantee can hold at a stationary point. For example, when the
observable is the identity, the exact gradient is zero and a relative direction
is undefined.

## 4. Small metric factors and natural-gradient conditioning

For a magnitude coordinate `j`, the ordinary coordinate-gradient record has
the form

```math
Z_j
=
2\sqrt{g_{j,j}}\,\sigma_j,
\qquad
\sigma_j\in\{-1,+1\}.
```

Hence

```math
\mathbb E[Z_j^2]
=
4g_{j,j}.
```

Small metric factors do not create a division instability in the ordinary
coordinate estimator; they reduce its absolute record scale. At
`g[j,j] = 0`, the coordinate differential, exact derivative, and record all
vanish.

An unregularized natural-gradient component divides by the metric, so its
rescaled record has second moment

```math
\mathbb E\left[\left(\frac{Z_j}{g_{j,j}}\right)^2\right]
=
\frac{4}{g_{j,j}},
```

which is ill-conditioned near a chart boundary. A regularized inverse gives

```math
\mathbb E\left[
\left(\frac{Z_j}{g_{j,j}+\lambda}\right)^2
\right]
=
\frac{4g_{j,j}}{(g_{j,j}+\lambda)^2}
\leq
\frac{1}{\lambda}.
```

Thresholding or freezing small-weight coordinates provides an alternative.
These choices belong to the optimizer layer; they are not required for the
correctness of the ordinary gradient record.

## 5. Common-phase gauge projection

The complex chart retains all `N` leaf phases and therefore parametrizes the
unit sphere rather than quotienting by global phase. Expectation-value
objectives are invariant under a uniform phase shift, so the exact phase block
satisfies

```math
\mathbf 1^\mathsf{T}g_{\mathrm{ph}}=0.
```

A finite-shot estimate can be projected onto the physical zero-sum subspace:

```math
\widehat g_{\mathrm{ph}}^{\perp}
=
\widehat g_{\mathrm{ph}}
-
\frac{\mathbf 1^\mathsf{T}\widehat g_{\mathrm{ph}}}{N}\mathbf 1.
```

This projection is unbiased and cannot increase Euclidean error because the
true phase gradient already lies in the projected subspace. It is an optional
classical postprocessing step, not a change to the quantum circuit.

## 6. Executable support

The supporting formulas are implemented and tested in:

```text
qbp_validation/supporting_analysis.py
qbp_validation/tests/test_supporting_analysis.py
```

The tests check the exact complete-record norm, sufficient shot-count formula,
conditional direction bound, readout formulas, reflection-sum unbiasedness, and
nonexpansive common-phase projection.

Run:

```bash
python validate_qbp.py --analytic
```

## 7. Deliberate boundary

These statements characterize estimation error. They do not claim:

- convergence of a particular optimizer;
- a uniform relative guarantee near stationary points;
- stability of an unregularized natural-gradient inverse at singular chart
  coordinates; or
- hardware noise resilience.
