# Optimized compilation companion

This page complements the manuscript's explicit assigned CNOT ledger. The
assigned ledger decomposes each addressed multi-controlled rotation separately;
it is useful because it gives concrete finite counts under one declared
no-clean-ancilla model. It is not an optimal-synthesis claim.

The same Hopf-QBP circuit objects also admit an exact `O(N)` compiler, where
`N = 2**n`, by grouping each depth into a uniformly controlled rotation. This
page states the factorization, its clean-ancilla contract, the resource bound,
and the checks implemented in this repository.

## 1. Two resource views

| View | Purpose | What is counted |
|---|---|---|
| Assigned ledger | Reproduce the finite counts printed in the manuscript | Independently decomposed multi-controlled rotations under the declared formulas |
| Optimized companion | Compare against standard `O(N)` state-preparation synthesis | Uniformly controlled-rotation cores, with suffix-predicate work exposed separately |

Neither table is a routed hardware estimate. Both exclude the controlled
observable, readout, device connectivity, and approximate synthesis unless a
quantity is explicitly added.

Run the two ledgers with:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10
```

## 2. Forward preparation is depthwise multiplexed

For depth `d`, let the first `d` system qubits be the prefix register, let the
next qubit be the target, and leave the lower suffix untouched. The checkpoint
preparation layer is

```math
U_d
=
\sum_{r=0}^{2^d-1}
|r\rangle\!\langle r|
\otimes R_y(\theta_{2^d+r})
\otimes I_{2^{n-d-1}}.
```

This is a uniformly controlled `R_y` with `d` controls. In the standard
Gray-code construction, a nontrivial `k`-control uniformly controlled rotation
uses `2**k` CNOTs and `2**k` local rotations. The uncontrolled layer uses no
CNOT.

Therefore

```math
C_{\mathrm{ucr}}(U_{\mathrm{chk}})
\leq
\sum_{d=1}^{n-1}2^d
=
N-2.
```

For the inverse suffix below a selected depth `d`,

```math
C_{\mathrm{ucr}}(B_d^\dagger)
\leq
\sum_{k=d+1}^{n-1}2^k
=
N-2^{d+1}.
```

These are upper bounds for the multiplexor cores. Adjacent-layer cancellations
may reduce particular compiled circuits further; no such cancellation is used
here.

## 3. Addressed-frame layer with one clean flag

At depth `d`, the addressed real frame applies angle
`theta[2**d + r]` only when:

1. the upper prefix equals `r`; and
2. every lower suffix bit is zero.

Introduce one clean flag `f` and compute

```math
f
\mathrel{\oplus}= 
[\text{lower suffix}=0].
```

Then apply one uniformly controlled `R_y` to the depth-`d` target:

- prefix `r`, flag `1`: angle `theta[2**d + r]`;
- prefix `r`, flag `0`: angle `0`.

Finally uncompute the flag. The exact contract is

```math
\widetilde W_{\mathbb R}
\bigl(|\varphi\rangle\otimes|0\rangle_f\bigr)
=
\bigl(W_{\mathbb R}|\varphi\rangle\bigr)
\otimes|0\rangle_f
```

for every system input `|varphi>`. Equality on an arbitrary initial flag state
is neither needed nor claimed.

For `d < n-1`, the multiplexor has `d+1` controls: the `d` prefix bits plus the
flag. At the final depth there is no lower suffix and no flag is required. For
`n >= 2`, the CNOT count of the uniformly controlled-rotation cores is therefore

```math
\begin{aligned}
C_{\mathrm{ucr-core}}(W_{\mathbb R})
&\leq
\sum_{d=0}^{n-2}2^{d+1}+2^{n-1} \\
&=
3\,2^{n-1}-2
=
\frac{3}{2}N-2.
\end{aligned}
```

The suffix predicate is computed and uncomputed once at each nonfinal depth.
Its control widths are

```text
n-1, n-1, n-2, n-2, ..., 1, 1.
```

A standard exact ancilla-free multi-controlled-X decomposition is quadratic in
its control width. Consequently the total predicate contribution is
`O(n**3)`. The overall frame cost is

```math
C(W_{\mathbb R})
=
O(N+n^3)
=
O(N),
```

because `N = 2**n`. The same flag is reused at every depth and is returned to
`|0>` before the next layer.

The repository reports the multiplexor CNOT count and the predicate widths
separately rather than hiding a compiler-dependent finite constant inside one
number.

## 4. Complex frame

The portable complex magnitude frame is

```math
W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}.
```

An arbitrary `n`-qubit diagonal unitary has an exact `O(2**n)` synthesis, so

```math
C(D_{\mathrm{ph}})=O(N),
\qquad
C(W_{\mathbb C})=O(N).
```

The same conclusion applies to the separated complex forward preparation
`D_ph U_chk`. The explicit four-qubit integrated `R_C` fixtures remain useful
finite regression tests, but they are not required for the general asymptotic
compiler.

## 5. Matched scalar comparison

A scalar Hopf objective execution and a global-gradient-record execution share:

- the same system size;
- the same forward state;
- the same controlled observable; and
- the same observable-access phase convention.

Using the optimized constructions above,

```math
C_{\mathrm{scalar}}=O(N),
\qquad
C_{\mathrm{global\ record}}=O(N).
```

Thus the circuit-work ratio per independent execution is `O(1)`. The global
method's complete-gradient execution overhead remains its statistical factor,
not an extra logarithmic compiler factor.

This comparison is output-sensitive. The complete chart has
`M = N - 1` real coordinates or `M = 2N - 1` complex coordinates, so
`M = Theta(2**n)`. The result is not an exponential compression of an
exponentially long classical output vector.

## 6. Executable support

The Qibo-free reference implementation is in:

```text
qbp_validation/optimized_compiler.py
qbp_validation/tests/test_optimized_compiler.py
qbp_optimized_resource_ledger.py
```

The tests check:

- every addressed depth through `n = 5`;
- the complete addressed frame through `n = 4`;
- equality on the clean-flag input subspace;
- zero flag leakage;
- the multiplexor-core counts;
- inverse-suffix counts; and
- the full predicate-width ledger.

Run:

```bash
python validate_qbp.py --analytic
```

The matrix checks validate the exact flag factorization. The asymptotic CNOT
claim additionally uses the established Gray-code synthesis of uniformly
controlled rotations and standard multi-controlled-X constructions.

## 7. Primary references

- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  [Transformation of quantum states using uniformly controlled rotations](https://arxiv.org/abs/quant-ph/0407010),
  *Quantum Information and Computation* **5**, 467–473 (2005).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  [Quantum circuits with uniformly controlled one-qubit gates](https://arxiv.org/abs/quant-ph/0410066),
  *Physical Review A* **71**, 052330 (2005).
- V. V. Shende, S. S. Bullock, and I. L. Markov,
  [Synthesis of quantum-logic circuits](https://arxiv.org/abs/quant-ph/0406176),
  *IEEE Transactions on Computer-Aided Design* **25**, 1000–1010 (2006).
- A. Barenco et al.,
  [Elementary gates for quantum computation](https://arxiv.org/abs/quant-ph/9503016),
  *Physical Review A* **52**, 3457–3467 (1995).
- S. S. Bullock and I. L. Markov,
  [Smaller circuits for arbitrary n-qubit diagonal computations](https://arxiv.org/abs/quant-ph/0303039),
  *Quantum Information and Computation* **4**, 27–47 (2004).
