[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S7"></a>

# VII Backpropagation accuracy, resources, and protocol choice

<a id="S7.SS1"></a>

## VII A Reverse pullback and shared records

The controlled reflection creates one objective response on state space. The inverse Hopf frame resolves that response along normalized magnitude directions, and the metric factors convert those frame components into coordinate derivatives. Writing $`W_{\mathbb{R}}:=W_{\mathbb{R}}`$ and using the complex frame $`W_{\mathbb{C}}`$ from Sec. [V](global-complex.md#S5), the component form of this pullback is, for $`\mathbb{K}\in\{\mathbb{R},\mathbb{C}\}`$ and $`1\leq j\lt N`$,

<a id="S7.E47"></a>

```math
{\partial_{\theta_{j}}E_{O}=2\sqrt{g^{\mathbb{K}}_{j,j}}\mathrm{Re}\langle b_{\lambda(j)}\rvert W_{\mathbb{K}}^{\dagger}O\lvert \psi^{\mathbb{K}}\rangle .}\tag{47}
```

Controlled interference makes all addressed components in Eq. ([47](accuracy-resources.md#S7.E47)) jointly readable. The checkpoint identity in Eq. ([40](checkpoints.md#S6.E40)), together with the complex active-interface construction of Sec. [VI C](checkpoints.md#S6.SS3), implements the same coordinate pullback after transport to one selected depth. Complex phase directions are already localized in the computational basis, so their differential resolution is the identity. The global, checkpoint, and direct phase records therefore meet the operational record condition in Definition [2](reverse-task.md#Thmdefinition2).

The global method reuses outcomes across all $`n`$ magnitude-depth records. Checkpointing instead uses a separate stream for each requested layer. In the complex chart, both constructions add a direct phase stream.

<a id="S7.SS2"></a>

## VII B Fixed-norm records and complete-chart accuracy

The width of a tree depth does not set its statistical scale. Every global magnitude-depth vector has norm two by Eq. ([28](global-real.md#S4.E28)), and one global outcome supplies all of these depth records. Checkpoint and direct phase records are also norm-two signed one-hot vectors by Eqs. ([46](checkpoints.md#S6.E46)) and ([37](global-complex.md#S5.E37)). The same concentration statement therefore controls every block, regardless of its number of coordinates.

**Fixed-norm concentration.** Let $`Z_{1},\ldots,Z_{S}\in\mathbb{R}^{p}`$ be independent, identically distributed vectors with $`\|Z_{t}\|_{2}\leq B`$ almost surely. Set $`\mu:=\mathbb{E}Z_{t}`$ and $`\widehat{\mu}:=S^{-1}\sum_{t}Z_{t}`$. For every $`\eta\in(0,1)`$,

<a id="S7.E48"></a>

```math
{\mathbb{P}\!\left[\|\widehat{\mu}-\mu\|_{\infty}\gt \frac{B\{1+\sqrt{2\log(1/\eta)}\}}{\sqrt{S}}\right]\leq\eta.}\tag{48}
```

For the norm-two Hopf records, define the common sufficient count

<a id="S7.E49"></a>

```math
{S_{\star}(\eta):=\left\lceil\frac{4\{1+\sqrt{2\log(1/\eta)}\}^{2}}{\varepsilon^{2}}\right\rceil.}\tag{49}
```

Applying Eq. ([48](accuracy-resources.md#S7.E48)) to each complete depth vector and combining the depth-level failure events gives a simultaneous coordinate guarantee. This union bound does not require the depth records decoded from one outcome to be independent. Allocating the total failure probability across the required blocks gives

<a id="S7.EGx21"></a>

```math
\begin{aligned}S_{\mathrm{mag}}^{\mathbb{R}} & :=S_{\star}(\delta/n), & S_{\mathrm{mag}}^{\mathbb{C}} & :=S_{\star}(\delta/(2n)),\end{aligned}
```

```math
\begin{aligned}S_{\mathrm{ph}}^{\mathbb{C}} & :=S_{\star}(\delta/2), & S_{\mathrm{glob}}^{\mathbb{C}} & :=S_{\mathrm{mag}}^{\mathbb{C}}+S_{\mathrm{ph}}^{\mathbb{C}},\end{aligned}
```

```math
\begin{aligned}S_{\mathrm{glob}}^{\mathbb{R}} & :=S_{\mathrm{mag}}^{\mathbb{R}}, & S_{\mathrm{chk}}^{\mathbb{R}} & :=nS_{\mathrm{mag}}^{\mathbb{R}},\end{aligned}
```

<a id="S7.E50"></a>

```math
{\begin{aligned}S_{\mathrm{chk}}^{\mathbb{C}} & :=nS_{\mathrm{mag}}^{\mathbb{C}}+S_{\mathrm{ph}}^{\mathbb{C}}.\end{aligned}}\tag{50}
```

Consequently, for either chart $`\mathbb{K}\in\{\mathbb{R},\mathbb{C}\}`$,

<a id="S7.EGx22"></a>

```math
\begin{aligned}S_{\mathrm{glob}}^{\mathbb{K}} & =\mathcal{O}\!\left(\frac{1+\log(n/\delta)}{\varepsilon^{2}}\right),\end{aligned}
```

<a id="S7.E51"></a>

```math
{\begin{aligned}S_{\mathrm{chk}}^{\mathbb{K}} & =\mathcal{O}\!\left(\frac{n\{1+\log(n/\delta)\}}{\varepsilon^{2}}\right).\end{aligned}}\tag{51}
```

At fixed absolute coordinate accuracy and confidence, these become $`\mathcal{O}(\log\log M)`$ and $`\mathcal{O}(\log M\log\log M)`$, respectively. These are sufficient counts for the displayed allocations, not lower bounds on the number of executions. Per-execution work and the $`M`$-entry classical output are accounted for below. Appendix [B 8](proofs-and-compilation.md#A2.SS8) proves the concentration bound, derives both orders explicitly, and records the corresponding complete-vector $`\ell_{2}`$ guarantee.

<a id="S7.SS3"></a>

## VII C Assigned Hopf CNOT work

<a id="S7.SS3.p1.1"></a>

The resource comparison uses the direct-angle Hopf realization inherited from Ref. [[1](../references/paper-bibliography.md#bib.bib6)]. Each magnitude coordinate remains the physical rotation angle of its designated tree split, and each complex leaf phase remains a directly programmed phase angle. Keeping this coordinate-to-control map explicit makes the chart, inverse, metric, tangent frame, and counted physical controls part of one transparent geometry. The same cost functional is used for scalar and gradient programs. Assigned Hopf CNOT work is the assigned CNOT charge of Hopf-specific circuit blocks. For such a block $`U`$, let $`C_{\mathrm{H}}(U)`$ denote its assigned CNOT count. For a program $`\mathcal{P}`$, let $`\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathcal{P};\varepsilon,\delta)`$ denote the total charge of its Hopf forward and reverse blocks over all executions required for $`(\varepsilon,\delta)`$ accuracy.

The controlled reflection, its compiler workspace, final basis changes, measurement, and classical processing are reported as separate application and classical resources. Each matched scalar or gradient execution contains one call to the same $`\mathrm{ctrl}(O)`$. Adding the same nonnegative application-dependent controlled-reflection charge to every scalar and gradient execution preserves the overhead orders below up to a constant factor. The logarithmic matched-resource benchmark is therefore evaluated using assigned Hopf CNOT work and the matched storage comparison below. The explicit controlled two-level Hopf-gate charges assume all-to-all connectivity, zero clean work ancillas, exact one-qubit primitives, and the decompositions stated in Appendix [B 9](proofs-and-compilation.md#A2.SS9).

For the designated schedules used in the theorem, set

<a id="S7.EGx23"></a>

```math
\begin{aligned}U_{\mathrm{fwd}}^{\mathbb{R}} & :=U_{\mathrm{chk}}, & U_{\mathrm{fwd}}^{\mathbb{C}} & :=D_{\mathrm{ph}}U_{\mathrm{chk}},\end{aligned}
```

```math
\begin{aligned}c_{\mathrm{fwd}}^{\mathbb{K}} & :=C_{\mathrm{H}}(U_{\mathrm{fwd}}^{\mathbb{K}}).\end{aligned}
```

<a id="S7.SS3.p3.2"></a>

The matched scalar circuit uses this same forward preparation and the same $`\mathrm{ctrl}(O)`$ access. It omits the Hopf reverse block and measures the branch ancilla in $`X`$ to estimate $`E_{O}`$. Hoeffding’s inequality [[41](../references/paper-bibliography.md#bib.bib4)] gives

<a id="S7.E52"></a>

```math
{S_{F}(\varepsilon,\delta)=\left\lceil\frac{2}{\varepsilon^{2}}\log\frac{2}{\delta}\right\rceil,}\tag{52}
```

and the corresponding assigned Hopf CNOT work is

<a id="S7.E53"></a>

```math
{\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{scalar})=S_{F}\,c_{\mathrm{fwd}}^{\mathbb{K}}.}\tag{53}
```

The arguments $`(\varepsilon,\delta)`$ are suppressed in the remaining work formulas.

Let

<a id="S7.EGx24"></a>

```math
\begin{aligned}c_{\mathrm{fr}}^{\mathbb{R}} & :=C_{\mathrm{H}}(W_{\mathbb{R}}^{\dagger}), & c_{\mathrm{fr}}^{\mathbb{C}} & :=C_{\mathrm{H}}(W_{\mathbb{C}}^{\dagger}),\end{aligned}
```

```math
\begin{aligned}c_{d}^{\mathbb{R}} & :=C_{\mathrm{H}}(B_{d}^{\dagger}), & c_{d}^{\mathbb{C}} & :=C_{\mathrm{H}}(B_{d,\mathbb{C}}^{\dagger}).\end{aligned}
```

The repeated Hopf-block charges of the displayed schedules are

<a id="S7.EGx25"></a>

```math
\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{R}}(\mathrm{global}) & =S_{\mathrm{mag}}^{\mathbb{R}}\left(c_{\mathrm{fwd}}^{\mathbb{R}}+c_{\mathrm{fr}}^{\mathbb{R}}\right),\end{aligned}
```

```math
\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{C}}(\mathrm{global}) & =S_{\mathrm{mag}}^{\mathbb{C}}\left(c_{\mathrm{fwd}}^{\mathbb{C}}+c_{\mathrm{fr}}^{\mathbb{C}}\right)+S_{\mathrm{ph}}^{\mathbb{C}}c_{\mathrm{fwd}}^{\mathbb{C}},\end{aligned}
```

```math
\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{R}}(\mathrm{checkpoint}) & =\sum_{d=0}^{n-1}S_{\mathrm{mag}}^{\mathbb{R}}\left(c_{\mathrm{fwd}}^{\mathbb{R}}+c_{d}^{\mathbb{R}}\right),\end{aligned}
```

<a id="S7.E54"></a>

```math
{\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{C}}(\mathrm{checkpoint}) & =\sum_{d=0}^{n-1}S_{\mathrm{mag}}^{\mathbb{C}}\left(c_{\mathrm{fwd}}^{\mathbb{C}}+c_{d}^{\mathbb{C}}\right)+S_{\mathrm{ph}}^{\mathbb{C}}c_{\mathrm{fwd}}^{\mathbb{C}}.\end{aligned}}\tag{54}
```

The complex magnitude and phase families therefore retain their separate execution counts and Hopf charges.

For the designated schedules,

<a id="S7.E55"></a>

```math
{c_{\mathrm{fr}}^{\mathbb{K}}\leq 2c_{\mathrm{fwd}}^{\mathbb{K}},\qquad c_{d}^{\mathbb{K}}\leq c_{\mathrm{fwd}}^{\mathbb{K}}\quad(0\leq d\lt n).}\tag{55}
```

The real frame bound follows because the final depth of $`U_{\mathrm{chk}}`$ already contains half as many gates with the same largest control count as $`W_{\mathbb{R}}`$. Every inverse suffix is a subset of the depth layers of $`U_{\mathrm{chk}}`$. Adding the same diagonal phase layer to the designated complex forward and reverse blocks preserves the factors in Eq. ([55](accuracy-resources.md#S7.E55)). The exact sums appear in Appendix [B 9](proofs-and-compilation.md#A2.SS9).

**Matched storage.** The designated scalar and gradient circuits use the same system register, branch ancilla, forward-compiler workspace, and controlled-reflection workspace. Their blocks execute sequentially, so phase-layer and controlled-reflection workspaces are reused. Under the adopted Hopf-gate ledger, the addressed controlled two-level gates use zero clean work ancillas. A reverse schedule adds streamed histograms and a complete gradient using $`\mathcal{O}(M)`$ classical slots; the scalar input already contains the $`M`$ chart parameters. Total input/output-inclusive storage therefore grows by at most a constant factor relative to the matched scalar program.

The record identities, norm-two concentration bound, and matched compiler comparison give the complete-gradient guarantee. One global magnitude stream serves all depths, whereas checkpoints use one stream per depth. A direct phase stream completes the complex chart.

<a id="Thmtheorem1"></a>

**Theorem 1 (Quantum backpropagation and checkpointed reverse gradients with the Hopf ansatz).**

Let $`\mathbb{K}\in\{\mathbb{R},\mathbb{C}\}`$, and let $`M=N-1`$ for $`\mathbb{K}=\mathbb{R}`$ and $`M=2N-1`$ for $`\mathbb{K}=\mathbb{C}`$. Under Assumption [1](reverse-task.md#Thmassumption1), the correctness and execution statements below hold for $`n\geq 1`$. The assigned Hopf CNOT work and storage statements use the designated direct-angle separated schedules and assume $`n\geq 2`$ to ensure a nonzero matched forward charge.

**(A) Global-frame method.** The global magnitude pullback in Eq. ([47](accuracy-resources.md#S7.E47)), together with the direct phase family for $`\mathbb{K}=\mathbb{C}`$, implements the reverse state-coordinate task of Definition [2](reverse-task.md#Thmdefinition2). With the allocations in Eq. ([50](accuracy-resources.md#S7.E50)), it produces an $`(\varepsilon,\delta)`$-accurate complete raw Hopf-coordinate gradient using

<a id="S7.Ex79"></a>

```math
S_{\mathrm{glob}}^{\mathbb{K}}=\mathcal{O}\!\left(\frac{1+\log(n/\delta)}{\varepsilon^{2}}\right)
```

independent executions. Under Eq. ([55](accuracy-resources.md#S7.E55)), the assigned Hopf CNOT work ratio relative to the matched scalar program satisfies

<a id="S7.E56"></a>

```math
{\frac{\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{global})}{\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{scalar})}=\mathcal{O}\!\left(\frac{1+\log(n/\delta)}{\log(2/\delta)}\right).}\tag{56}
```

**(B) Checkpoint method.** At each depth, the checkpointed adjoint implements the transported pullback in Eq. ([40](checkpoints.md#S6.E40)), with the complex active-interface extension of Sec. [VI C](checkpoints.md#S6.SS3). A selected checkpoint therefore implements the reverse state-coordinate task of Definition [2](reverse-task.md#Thmdefinition2) for its depth block. With the allocations in Eq. ([50](accuracy-resources.md#S7.E50)), the complete all-depth schedule, together with the direct phase family for $`\mathbb{K}=\mathbb{C}`$, produces the same $`(\varepsilon,\delta)`$-accurate complete raw Hopf-coordinate gradient using

<a id="S7.Ex80"></a>

```math
S_{\mathrm{chk}}^{\mathbb{K}}=\mathcal{O}\!\left(\frac{n\{1+\log(n/\delta)\}}{\varepsilon^{2}}\right)
```

independent executions. Under Eq. ([55](accuracy-resources.md#S7.E55)),

<a id="S7.E57"></a>

```math
{\frac{\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{checkpoint})}{\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{scalar})}=\mathcal{O}\!\left(\frac{n\{1+\log(n/\delta)\}}{\log(2/\delta)}\right).}\tag{57}
```

Under the designated direct-angle forward-charge condition $`c_{\mathrm{fwd}}^{\mathbb{K}}=\mathcal{O}(M\log M)`$, the same cost functional gives, at fixed accuracy and confidence,

<a id="S7.EGx26"></a>

```math
\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{scalar}) & =\mathcal{O}(M\log M),\end{aligned}
```

```math
\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{global}) & =\mathcal{O}(M\log M\log\log M),\end{aligned}
```

<a id="S7.E58"></a>

```math
{\begin{aligned}\mathsf{W}_{\mathrm{H}}^{\mathbb{K}}(\mathrm{checkpoint}) & =\mathcal{O}(M\log^{2}M\log\log M).\end{aligned}}\tag{58}
```

<a id="Thmtheorem1.p4.2"></a>

For the designated schedules, the matched-storage argument above gives $`\mathcal{O}(1)`$ total input/output-inclusive storage overhead. The additional classical histogram and output storage is $`\mathcal{O}(M)`$. Since $`M=2^{n}-1`$ in the real case and $`M=2^{n+1}-1`$ in the complex case, the preceding bounds have the stated dependence on $`M`$. Relative to the matched scalar program, the global-frame method has $`\mathcal{O}(\log\log M)`$ overhead in assigned Hopf CNOT work and therefore meets the logarithmic matched-resource benchmark. The displayed complete-checkpoint overhead is $`\mathcal{O}(\log M\log\log M)`$. Within the same resource specialization it remains polylogarithmic in the broader sense of Ref. [[3](../references/paper-bibliography.md#bib.bib1)], but the present bound does not meet the stricter logarithmic benchmark.

**Coordinate and geometric outputs.** The theorem controls raw Hopf-coordinate derivatives in the norm of Definition [1](reverse-task.md#Thmdefinition1). For an active real magnitude coordinate, define the normalized-frame and inverse-metric outputs by

<a id="S7.Ex83"></a>

```math
\chi_{j}:=\frac{\partial_{\theta_{j}}E_{O}}{\sqrt{g^{\mathbb{R}}_{j,j}}},\qquad\nu_{j}:=\frac{\partial_{\theta_{j}}E_{O}}{g^{\mathbb{R}}_{j,j}}.
```

At a parameter point with $`0\lt g^{\mathbb{R}}_{k,k}\lt (\varepsilon/2)^{2}`$, choose a Hermitian unitary that swaps $`\lvert \psi^{\mathbb{R}}\rangle`$ with $`\lvert e_{k}^{\mathbb{R}}\rangle`$ and hold it fixed during differentiation. Then $`\partial_{\theta_{k}}E_{O}=2\sqrt{g^{\mathbb{R}}_{k,k}}\lt \varepsilon`$ but $`\chi_{k}=2`$. Thus raw coordinate and normalized-frame accuracy are distinct near small metric weights; Appendix [B 8](proofs-and-compilation.md#A2.SS8) gives the witness and conditioning bounds.

The theorem uses the direct-angle ledger, in which each Hopf coordinate remains one directly programmed physical angle. Appendix [B 10](proofs-and-compilation.md#A2.SS10) separately gives an exact multiplexed realization that recombines those angles while preserving the estimator and $`\mathcal{O}(N)`$ matched forward/frame scaling. This alternative has its own compiler ledger; it does not replace the theorem’s accounting. Finite and proof details appear in Appendices [A 9](four-qubit-example.md#A1.SS9), [B 9](proofs-and-compilation.md#A2.SS9), and [B 11](proofs-and-compilation.md#A2.SS11).

**Classical processing.** These operation counts use a word-RAM whose words can store one $`n`$-bit outcome label, so reading or incrementing one histogram address costs $`\mathcal{O}(1)`$. Global decoding streams an $`N`$-bin signed histogram and applies one Walsh–Hadamard transform, requiring $`\mathcal{O}(S_{\mathrm{glob}}^{\mathbb{K}}+N\log N)`$ operations. Checkpoint and direct phase records use signed histograms, requiring $`\mathcal{O}(S_{\mathrm{chk}}^{\mathbb{K}}+N)`$ operations for a complete schedule. A complete gradient contains $`M`$ entries, so linear output work is intrinsic to the requested output.

<a id="S7.SS4"></a>

## VII D Choosing the reverse protocol

At a fixed depth, $`Z_{d}^{\mathrm{fr}}`$ and $`Z_{d}^{\mathrm{chk}}`$ are unbiased for $`\mu_{d}^{\mathrm{mag}}`$ and both have norm two. They differ in how many depths one template and record stream serves.

The global frame is the natural choice when many or all depths are requested and its inverse is available. Every all-$`X`$ outcome contributes to every depth; one signed histogram and Walsh transform decode the magnitude block. The complex chart adds the direct phase stream.

Checkpoints are useful when one or a few depths are active and their suffixes or interfaces are easier to compile. Each depth has its own reverse block, readout target, and $`2^{d}`$-bin histogram, whose average recovers the complete depth block. The final real depth needs no reverse suffix.

For $`q`$ requested depths $`d_{1},\ldots,d_{q}`$, checkpoints use $`q`$ templates. They are favorable when their repeated compiled records cost less than the full-frame records or when a layer-local update is the intended output. Appendix [A 9](four-qubit-example.md#A1.SS9) gives the finite four-qubit comparison. Both methods resolve the same normalized differential: globally in the addressed frame or locally at an active interface.
