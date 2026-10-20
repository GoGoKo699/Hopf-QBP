# Educational anchor and bridge

The single educational anchor is **Michael A. Nielsen and Isaac L. Chuang,
*Quantum Computation and Quantum Information*, 10th Anniversary Edition,
Cambridge University Press, ISBN 9781107002173**. The
[publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf)
fix the section numbering used here. The companion
[Hopf-ansatz learning route](https://github.com/GoGoKo699/Hopf-ansatz/blob/main/learning/ANCHOR.md)
uses the same edition and conventions.

This route starts from linear algebra, elementary calculus, and basic
probability. It develops the Hopf background locally, so reading the companion
repository is useful but is not a prerequisite. The [30 milestones](MILESTONES.md)
lead to the complete scientific account of
[*Compass in the Mirror: Quantum Backpropagation with the Hopf
Ansatz*](https://arxiv.org/abs/2610.14177). The textbook anchors the foundations;
the project pages supply the differential frame, readout constructions,
concentration argument and resource analysis.

## Selected textbook route

| Nielsen–Chuang sections | Foundation | Connection developed here |
|---|---|---|
| §§2.1.1–2.1.7; §§2.2.1–2.2.2 | Bases, inner products, Hermitian operators, tensor products and unitary evolution | State derivatives become columns of a unitary frame. |
| §§2.2.3, 2.2.5, 2.2.7–2.2.8 | Measurement, phase and composite systems | Controlled-branch interference retains signs and complex quadratures. |
| §§4.2–4.5 | Rotations, controlled operations, measurement and synthesis | Separate forward preparations, complete inverse frames and checkpoint interfaces. |
| §6.1 | Reflections and their geometric action | Interpret the Hermitian-unitary objective and its controlled implementation. |
| §3.2.1; Appendix 1 | Resources and basic probability | Distinguish a record, an execution, a full output, and a confidence allocation. |
| §§9.2.1–9.2.2 | Trace distance and fidelity | Compare physical states without confusing state fidelity with a branch-phase or operator contract. |

The selected sections are enough to begin the local bridge. Hopf geometry,
Walsh decoding, vector concentration and compiler contracts are supplied below
and in the paper's proofs; they are not attributed to the textbook.

## Notation and output

Let $n$ be the number of qubits and $N=2^n$. Basis labels are
$\lvert q_n\cdots q_1\rangle$, with the leftmost bit most significant.
A breadth-first binary-tree node is $j=2^d+r$, where $d$ is its depth and
$0\le r<2^d$. The real chart has $M=N-1$ magnitude angles. The complex
chart adds $N$ leaf phases and has $M=2N-1$ real-valued coordinates.

The objective is

```math
E_O(\theta)=\langle\psi(\theta)\mid O\mid\psi(\theta)\rangle,
\qquad O=O^\dagger,\qquad O^2=I.
```

Its output is the classical raw-coordinate vector
$q=\nabla_\theta E_O$. The principal accuracy target is

```math
\Pr\{\lVert\widehat q-q\rVert_\infty\le\varepsilon\}\ge1-\delta.
```

Thus every coordinate has additive error at most $\varepsilon$ in the same
successful run of the procedure. This target differs from Euclidean,
relative, directional or metric-rescaled error. A complete output still has
$M$ classical entries.

## 1. Reconstruct the local Hopf geometry

For orthonormal branch states $u,v$, put
$s=\cos\theta\,u+\sin\theta\,v$ and
$e=-\sin\theta\,u+\cos\theta\,v$. Then $s,e$ are orthonormal.
Recursively applying this split to orthogonal leaf groups gives a normalized
state. For two qubits,

```math
\psi(a,b,c)=
\begin{pmatrix}
\cos a\cos b\\ \cos a\sin b\\
\sin a\cos c\\ \sin a\sin c
\end{pmatrix},
\qquad
 g=\mathrm{diag}(1,\cos^2a,\sin^2a).
```

Here $g_{jj}=\lVert\partial_j\psi\rVert^2$ is the subtree probability
entering split $j$. On the canonical chart,

```math
\partial_j\psi=w_j e_j,\qquad w_j=\sqrt{g_{jj}}.
```

The normalized magnitude complements $e_j$ are mutually orthogonal and
orthogonal to $\psi$. Each depth partitions all leaves, so
$\sum_{j\text{ at depth }d}g_{jj}=1$. These two structural facts drive
the frame construction and the statistical argument respectively.

When $w_j=0$, the raw differential vanishes. A recursively defined complement
can still be used as a frame column, but it is not obtained by dividing the
zero differential by zero. The estimator keeps the multiplier $w_j$.

**Connect to the paper:** [two-qubit clue](../science/reverse-task.md#S2.SS1),
[balanced differential](../science/balanced-differential.md#S3.SS2), and
[subtree-frame proof](../science/proofs-and-compilation.md#A2.SS2).

## 2. A forward state column does not determine a reverse circuit

Suppose $U\lvert0\rangle=V\lvert0\rangle=\psi$. This is enough to
replace one initialized forward preparation by the other. It does not imply
that their actions on any other input agree.

A one-qubit example is $U=I$ and $V=Z$: both prepare $\lvert0\rangle$,
but their inverses act differently on $\lvert+\rangle$. After an objective
operation, the system can occupy directions outside the initialized state
column, so a reverse replacement needs a stronger statement.

| Contract | What is fixed | Role |
|---|---|---|
| $U\lvert0^n\rangle=V\lvert0^n\rangle$ | Initialized state column | Substitute a forward preparation. |
| $U=V$ | Every input vector | Substitute a complete inverse frame. |
| $UP_d=VP_d$ | Action on a specified interface subspace | Justify the corresponding checkpoint construction. |

The checkpoint proof uses its active-interface identity and the associated
correlator argument; it need not establish equality of the complete outcome
distribution. Separately, a direct-angle compiler keeps each Hopf coordinate
as its designated physical angle. Logical equality alone does not preserve
that property or its cost ledger.

**Connect to the paper:** [three contracts](../science/reverse-task.md#S2.SS4),
[forward substitution](../science/proofs-and-compilation.md#A2.SS3), and
[checkpoint substitution](../science/proofs-and-compilation.md#A2.SS7).

## 3. Controlled reflection turns a derivative into interference

The required objective interface is the phase-calibrated gate

```math
\mathrm{ctrl}(O)
=\lvert0\rangle\langle0\rvert\otimes I
+\lvert1\rangle\langle1\rvert\otimes O.
```

Preparing an ancilla in $\lvert+\rangle$ produces
$(\lvert0\rangle\psi+\lvert1\rangle O\psi)/\sqrt2$.
The off-diagonal ancilla coherences retain the transition moments needed by

```math
q_j=2w_j\mathrm{Re}\langle e_j\mid O\mid\psi\rangle.
```

Replacing the controlled branch by $e^{i\gamma}O$ rotates the measured
quadrature. A known $\gamma$ can be compensated. Uncontrolled access to $O$
or a classical description does not by itself supply this interface.

For $O=Z\otimes I$ in the two-qubit example, $E_O=\cos2a$ and
$q=(-2\sin2a,0,0)$. This is a useful local reference for every decoder:
the observable sees only the weight of the two top-level subtrees.

**Connect to the paper:** [objective assumption](../science/reverse-task.md#Thmassumption1)
and [controlled-interference identities](../science/proofs-and-compilation.md#A2.SS1).

## 4. The frame makes every magnitude direction readable

Assign the state to column zero and node $j=2^d+r$ to the marker

```math
\lambda(j)=(2r+1)2^{n-d-1}.
```

The addressed real frame satisfies
$W_{\mathbb R}\lvert0\rangle=\psi$ and
$W_{\mathbb R}\lvert\lambda(j)\rangle=e_j$.
After its inverse, the interference state is

```math
\frac{\lvert0\rangle\lvert0^n\rangle
+\lvert1\rangle\lvert v\rangle}{\sqrt2},
\qquad v=W_{\mathbb R}^\dagger O\psi.
```

Measuring every qubit in the $X$ basis gives an ancilla bit $b$ and system
bits $y$. The product of the ancilla eigenvalue and the system eigenvalues
selected by marker $\lambda$ is $(-1)^{b+\lambda\cdot y}$, where the dot
product is modulo two. Its expectation is $\mathrm{Re}v_\lambda$.
Consequently, the same outcome gives

```math
Z_j(b,y)=2w_j(-1)^{b+\lambda(j)\cdot y}
```

for every magnitude coordinate, with $\mathbb E Z_j=q_j$.

For $n=2$, the three markers are $10,01,11$. At $a=\pi/4$, one outcome
$b=0,y=10$ gives $Z=(-2,\sqrt2,-\sqrt2)$. The two depth-one components
have opposite signs in this observation. Repeated outcomes average them to
the corresponding derivatives. Records from the same shot are correlated;
the analysis uses independent fresh executions, not independent coordinates.

**Connect to the paper:** [frame construction](../science/global-real.md#S4.SS1),
[inverse readout](../science/global-real.md#S4.SS2), and
[record and decoder](../science/global-real.md#S4.SS3).

## 5. Walsh decoding reuses a classical histogram

For $S$ outcomes, form the signed histogram

```math
h(y)=\frac1S\sum_{s=1}^{S}(-1)^{b_s}\mathbf1\{y_s=y\}.
```

Its unnormalized Walsh transform is

```math
\widehat h(\lambda)=\sum_y(-1)^{\lambda\cdot y}h(y).
```

The estimate is $\widehat q_j=2w_j\widehat h(\lambda(j))$.
This is exactly the sample mean of the record above, evaluated in a batch.
Building the histogram costs $O(S)$, the fast transform costs $O(N\log N)$,
and writing and rescaling the output costs $O(N)$. Storage is $O(N)$.
The transform avoids separately updating all $M$ coordinates for every shot;
it does not compress the final vector to fewer than $M$ entries.

**Connect to the paper:** [global decoder](../science/global-real.md#S4.SS3)
and [Walsh proof](../science/proofs-and-compilation.md#A2.SS5).

## 6. Complex phases have a separate direct record

Write $D_{\mathrm{ph}}=\mathrm{diag}(e^{i\phi_\ell})$.
The complex magnitude frame is $W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}$,
so removing phases and applying the real inverse frame preserves the magnitude
parity rule.

For phase coordinate $\phi_\ell$, however,

```math
\partial_{\phi_\ell}\psi=i\psi_\ell\lvert\ell\rangle,
\qquad
q_{\phi_\ell}=2\mathrm{Im}\bigl[\psi_\ell^*(O\psi)_\ell\bigr].
```

Measure the interference ancilla in $Y$ and the system in the computational
basis. If the outcome is $(b,\ell)$, return $2(-1)^b e_\ell$, where
$e_\ell$ now denotes a standard classical unit vector, not a tangent state.
Its mean is the full phase-gradient block. This circuit stream needs no
inverse magnitude frame. A zero-amplitude leaf has zero expected phase
derivative, although individual signed records in that bin need not vanish.

The chart retains the common phase. With $p_\ell=|\psi_\ell|^2$, its
round-sphere phase metric is $\mathrm{diag}(p)$. A common phase
change gives tangent $i\psi$ with norm one. Quotienting by global phase
instead gives the Fubini–Study block
$\mathrm{diag}(p)-pp^{\mathsf T}$, which annihilates the all-ones
vector. Hopf-QBP uses the former convention. Expectation invariance gives
$\sum_\ell q_{\phi_\ell}=0$ without changing that metric convention.

**Connect to the paper:** [complex magnitude](../science/global-complex.md#S5.SS2),
[direct phases](../science/global-complex.md#S5.SS3), and
[complex identities](../science/proofs-and-compilation.md#A2.SS6).

## 7. A checkpoint exposes one layer

Let $U_d$ implement the split layer at depth $d$, so the depth-ordered
preparation is $U_{\mathrm{chk}}=U_{n-1}\cdots U_0$.
For selected depth $d$, define the lower suffix
$B_d=U_{n-1}\cdots U_{d+1}$. Reversing this suffix after objective access
exposes the selected split and its prefix address.

The real checkpoint measures the ancilla and split target in $Y$, and the
prefix in the computational basis. An outcome $(b_c,b_t,r)$ produces

```math
Z_d^{\mathrm{chk}}=-2(-1)^{b_c+b_t}e_r.
```

Its mean is the raw gradient block at that depth. Each requested depth needs
its own stream. At the final real depth, the lower suffix is empty. The
complex construction additionally handles the phase layer through its stated
active-interface contract.

A global record is useful when the whole vector is wanted; checkpointing
offers shorter reverse suffixes for selected layers. Their comparison must
count both repetitions and the compiled circuit used per repetition.

**Connect to the paper:** [checkpoint construction](../science/checkpoints.md#S6.SS2),
[complex interface](../science/checkpoints.md#S6.SS3), and
[protocol choice](../science/accuracy-resources.md#S7.SS4).

## 8. Fixed norm explains the complete-coordinate shot bound

For a global record restricted to depth $d$,

```math
\lVert Z_d\rVert_2^2
=4\sum_{j\text{ at depth }d}g_{jj}=4.
```

The checkpoint and phase records are signed one-hot vectors of norm two as
well. Their width can grow while their total Euclidean norm stays fixed.
A vector concentration argument therefore controls one block independently of
its number of coordinates. For independent executions, one sufficient count
for block Euclidean error at most $\varepsilon$ and failure probability
$\eta$ is

```math
S_*(\eta)=
\left\lceil
\frac{4\bigl(1+\sqrt{2\log(1/\eta)}\bigr)^2}{\varepsilon^2}
\right\rceil.
```

A block Euclidean bound also bounds every coordinate in that block.
For real global readout, the same $`S_*(\delta/n)`$ shots serve every depth;
a union bound combines only the $n$ depth failures. For complex global
readout, use $`S_*(\delta/(2n))`$ magnitude shots and
$`S_*(\delta/2)`$ phase shots. The complete checkpoint schedule instead
executes the magnitude stream separately at every depth.

This yields sufficient scaling

```math
S_{\mathrm{glob}}=O\!\left(\frac{1+\log(n/\delta)}{\varepsilon^2}\right),
\qquad
S_{\mathrm{chk}}=O\!\left(\frac{n[1+\log(n/\delta)]}{\varepsilon^2}\right).
```

At fixed accuracy and confidence, $n=\Theta(\log M)$ converts these to
$O(\log\log M)$ and $O(\log M\log\log M)$. The confidence argument
concerns repeated executions, not free output writing or unknown objective
implementation costs.

**Connect to the paper:** [fixed-norm accuracy](../science/accuracy-resources.md#S7.SS2)
and [concentration proof and allocations](../science/proofs-and-compilation.md#A2.SS8).

## 9. Error norms and costs complete the interpretation

Concatenating all $n$ magnitude blocks gives a single-record norm
$2\sqrt n$. Hence the complete-vector Euclidean guarantee has a different
statistical scale from the coordinatewise guarantee. Relative or directional
accuracy additionally depends on a nonzero gradient signal.

Metric rescaling changes the target again. If $\widehat q_j$ has absolute
error at most $\varepsilon$, then $\widehat q_j/w_j$ can have error
$\varepsilon/w_j$, and $\widehat q_j/g_{jj}$ can have error
$\varepsilon/g_{jj}$. Small coordinate weights help the ordinary raw record
but can make these rescaled outputs ill-conditioned. No division is needed
by the raw-coordinate decoder.

The resource comparison keeps controlled-objective calls, assigned Hopf CNOT
work, classical decoding, and storage separate. The matched scalar evaluation
uses the same objective access and designated forward preparation. The
multiplexed compiler is an exact alternative with its own clean-flag contract
and physical-angle interpretation. Its ledger must be paired with a forward
comparator compiled in the same setting.

**Connect to the paper:** [assigned resources and theorem](../science/accuracy-resources.md#S7.SS3),
[accuracy refinements](../science/proofs-and-compilation.md#A2.SS8),
[gate ledger](../science/proofs-and-compilation.md#A2.SS9), and
[exact multiplexed compilation](../science/proofs-and-compilation.md#A2.SS10).

## 10. Assemble and check the complete mechanism

The tree gives weighted orthogonal magnitude directions. The addressed frame
turns their objective responses into computational labels. Interference and
all-$`X`$ parity measurements then make one record informative about every
magnitude coordinate. A direct signed leaf record supplies phases, while
checkpoint suffixes supply selected layers. Fixed record norms establish the
accuracy bounds; matched ledgers state the computational cost.

Read the [four-qubit companion](../science/four-qubit-example.md#A1) to see
the same contracts at gate level. Follow the
[theorem proof](../science/proofs-and-compilation.md#A2.SS11) for the
all-size argument and [reproducibility instructions](../verification/README.md)
for independent circuit/reference comparisons. Finite checks support the
implemented identities and conventions; the written proofs establish the
general statistical and asymptotic claims.
