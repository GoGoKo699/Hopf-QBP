# Statistical accuracy, output geometry, and conditioning

The manuscript's primary finite-shot target is simultaneous absolute accuracy
of the **raw Hopf-coordinate gradient**. Appendix B also gives the complete
magnitude-vector `l_2` bound, conditional relative and directional guarantees,
and magnitude-block natural-gradient conditioning. This page makes the output
objects, metric conventions, separation examples, and executable test map
explicit.

## 1. Raw coordinatewise target

For each magnitude depth, one global outcome produces a vector record of exact
Euclidean norm `2`. A checkpoint record and a direct complex phase record are
also norm-`2` signed one-hot vectors.

For a norm-`R` random vector, the sufficient fixed-norm count is

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

This is an absolute raw-coordinate `l_infinity` statement. It is not a claim of
relative error, state-space tangent accuracy, natural-gradient accuracy, or
optimizer convergence.

## 2. Complete raw magnitude-vector `l_2` accuracy

Concatenate the `n` magnitude-depth records obtained from one global outcome:

```math
Z_{\mathrm{mag}}
=
Z_0\oplus Z_1\oplus\cdots\oplus Z_{n-1}.
```

Every depth block has norm `2`, so

```math
\|Z_{\mathrm{mag}}\|_2
=
2\sqrt n.
```

Applying the same vector concentration argument directly gives

```math
S_{2,\mathrm{mag}}
=
\left\lceil
\frac{4n
\left(1+\sqrt{2\log(1/\delta)}\right)^2}
{\varepsilon_2^2}
\right\rceil.
```

Hence fixed complete-vector Euclidean accuracy requires

```math
O\left(
\frac{n\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right)
=
O\left(
\frac{\log M\{1+\log(1/\delta)\}}{\varepsilon_2^2}
\right)
```

independent executions. At fixed shot count the accumulated raw-vector noise
grows as `sqrt(n) = sqrt(log M)`, not as `sqrt(M)`.

For the complex chart, the direct phase record is a separate norm-`2` stream.
A fixed allocation of total Euclidean error and failure probability between the
magnitude and phase blocks preserves the `O(n)` scaling.

## 3. Relative and directional guarantees are conditional

Let

```math
\widehat v=v+e,
\qquad
\|e\|_2\leq\xi,
\qquad
\|v\|_2=\mathcal G.
```

When `0 <= xi < gradient_norm`,

```math
v^\mathsf{T}\widehat v
\geq
\mathcal G(\mathcal G-\xi)>0,
```

so `-v_hat` is a descent direction. The normalized-direction error obeys

```math
\left\|
\frac{\widehat v}{\|\widehat v\|_2}
-
\frac{v}{\mathcal G}
\right\|_2
\leq
\frac{2\xi}{\mathcal G}.
```

Choosing `xi = rho*G` gives relative `l_2` error at most `rho`, direction error
at most `2*rho`, and the sufficient magnitude-stream count

```math
S_{\mathrm{rel}}
=
O\left(
\frac{n\{1+\log(1/\delta)\}}
{\rho^2\mathcal G^2}
\right).
```

A fixed magnitude/phase allocation gives the same `n` dependence for the
complete complex gradient. No uniform relative or directional guarantee can
hold at a stationary point.

Shared readout removes the coordinate-count penalty at fixed absolute accuracy;
it does not remove signal-to-noise conditioning when the complete gradient norm
is small. If `G` is exponentially small, the displayed relative-error count is
correspondingly large.

## 4. Raw coordinate accuracy does not imply frame accuracy

For an active magnitude coordinate `k`,

```math
\partial_{\theta_k}|\psi\rangle
=
\sqrt{g_{k,k}}\,|e_k\rangle.
```

Define

```math
q_k
=
\partial_{\theta_k}E_O,
\qquad
c_k
=
\frac{q_k}{\sqrt{g_{k,k}}},
\qquad
\nu_k
=
\frac{q_k}{g_{k,k}}.
```

These are respectively the raw coordinate derivative, normalized-frame
coefficient, and inverse-metric coordinate.

Choose `0 < g[k,k] < (epsilon/2)**2` and define the Householder reflection

```math
O_k
=
I-
\bigl(|\psi\rangle-|e_k\rangle\bigr)
\bigl(\langle\psi|-\langle e_k|\bigr).
```

Because `|psi>` and `|e_k>` are orthonormal,

```math
O_k^\dagger=O_k,
\qquad
O_k^2=I,
\qquad
O_k|\psi\rangle=|e_k\rangle.
```

Therefore

```math
q_k
=
2\sqrt{g_{k,k}}
<
\varepsilon,
\qquad
c_k=2,
```

and all other normalized-frame coefficients vanish. The zero estimate is thus
`epsilon`-accurate in raw coordinate `l_infinity` error while its
normalized-frame error is `2`.

This is an exact separation of output tasks, not a defect in the raw-coordinate
theorem. Converting raw-coordinate guarantees into normalized-frame or natural
coordinates requires metric conditioning. The reflection is an existence
construction; no efficient application-specific compiler for it is claimed.

## 5. Magnitude-block norm hierarchy

Let

```math
I_+
=
\{j:g_{j,j}>0\},
\qquad
M_+=|I_+|,
\qquad
g_{\min}=\min_{j\in I_+}g_{j,j}.
```

The following are sufficient bounds for direct rescalings of the displayed
global magnitude record. They are not lower bounds or optimality statements.

| Requested magnitude output | Single-record scale | Sufficient execution scaling |
|---|---:|---:|
| Raw coordinate `l_infinity` | depth-vector norm `2` | `O(epsilon^-2 log(n/delta))` |
| Raw complete `l_2` | `2*sqrt(n)` | `O(n epsilon^-2 [1+log(1/delta)])` |
| Frame coefficient `l_infinity` | each active component bounded by `2` | `O(epsilon^-2 log(M_+/delta))` |
| Complete frame-vector `l_2` | `2*sqrt(M_+)` | `O(M_+ epsilon^-2 [1+log(1/delta)])` |
| Natural coordinate `l_infinity` | at most `2/sqrt(g_min)` | `O(g_min^-1 epsilon^-2 log(M_+/delta))` |
| Damped natural coordinate `l_infinity` | at most `1/sqrt(tau)` | `O(tau^-1 epsilon^-2 log(M_+/delta))` |

The frame coefficients divide the raw record by `sqrt(g[j,j])`; natural
coordinates divide it by `g[j,j]`. The table is restricted to the complete real
gradient or the complex magnitude block. The complex phase block has its own
support and metric structure.

## 6. Small metric factors and natural-gradient conditioning

For a global magnitude coordinate, every ordinary record satisfies

```math
Z_j^2
=
4g_{j,j}.
```

Small metric factors do not create a division instability in the ordinary
coordinate estimator; they reduce its absolute scale. At `g[j,j] = 0`, the
coordinate differential, exact derivative, and ordinary record vanish.

An unregularized inverse-metric record has second moment

```math
\mathbb E\left[\left(\frac{Z_j}{g_{j,j}}\right)^2\right]
=
\frac{4}{g_{j,j}},
```

which is ill-conditioned near a chart boundary. A damped inverse with
regularization `tau > 0` gives

```math
\mathbb E\left[
\left(\frac{Z_j}{g_{j,j}+\tau}\right)^2
\right]
=
\frac{4g_{j,j}}{(g_{j,j}+\tau)^2}
\leq
\frac{1}{\tau}.
```

Thresholding or freezing small-weight coordinates is another possible
optimizer-layer convention. These choices do not alter the correctness of the
ordinary Hopf-QBP record.

## 7. Complex phase metric convention

Write the leaf probabilities as

```math
p_\ell=|x_\ell|^2,
\qquad
\sum_\ell p_\ell=1.
```

The complex Hopf chart follows the ambient round-sphere convention of the first
paper. Its phase block is

```math
G_{\mathrm{ph}}^{\mathrm{sphere}}
=
\mathrm{diag}(p).
```

Under this convention the uniform phase direction represents `i|psi>` and has
ambient squared norm `1`; it is not metric-null.

If one instead quotients by global phase and uses the projective
Fubini--Study metric, the phase block becomes

```math
G_{\mathrm{ph}}^{\mathrm{FS}}
=
\mathrm{diag}(p)-pp^\mathsf{T}.
```

It satisfies

```math
G_{\mathrm{ph}}^{\mathrm{FS}}\mathbf 1=0.
```

If `s` leaves have positive probability, the projective block has rank `s-1`;
zero-probability leaves add further null coordinate directions. This projective
quotient is a valid alternative geometry, but it is not the metric convention
used by Hopf-QBP.

## 8. Uniform-phase objective invariance

Expectation objectives are invariant under a uniform leaf-phase shift, so the
exact phase-gradient block satisfies

```math
\mathbf 1^\mathsf{T}q_{\mathrm{ph}}=0.
```

A finite-shot estimate can be projected onto that zero-sum subspace:

```math
\widehat q_{\mathrm{ph}}^{\perp}
=
\widehat q_{\mathrm{ph}}
-
\frac{\mathbf 1^\mathsf{T}\widehat q_{\mathrm{ph}}}{N}\mathbf 1.
```

This projection is unbiased and cannot increase Euclidean error because the
true objective gradient is already zero-sum. It is optional classical
postprocessing, not a switch to the projective natural gradient.

## 9. Executable support

The supporting formulas are implemented and tested in:

```text
qbp_validation/supporting_analysis.py
qbp_validation/tests/test_supporting_analysis.py
```

The tests check:

- complete-record norms and sufficient shot counts;
- conditional descent and normalized-direction bounds;
- the exact Hopf swap-reflection separation;
- frame and natural-coordinate norm scales;
- ordinary and damped inverse-metric second moments;
- ambient and projective phase metrics, support rank, and the common-phase null vector;
- reflection-sum unbiasedness;
- readout transfer formulas; and
- nonexpansive zero-sum projection.

Run:

```bash
python validate_qbp.py --analytic
```

## 10. Deliberate boundary

These statements characterize estimation error and output geometry. They do not
claim optimizer convergence, a uniform relative guarantee near stationarity,
stability of an unregularized inverse at singular coordinates, optimality of
the displayed norm hierarchy, or hardware-noise resilience.
