[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S5"></a>

# V Global-frame method for the complex Hopf chart

<a id="S5.SS1"></a>

## V A Complex chart and phase-dressed frame

Using the coordinate blocks in Eq. ([6](balanced-differential.md#S3.E6)), write $`\boldsymbol{\theta}=(\boldsymbol{\theta}_{\mathrm{mag}},\boldsymbol{\theta}_{\mathrm{ph}})`$. All magnitude angles now lie in $`[0,\pi/2]`$, and

<a id="S5.Ex44"></a>

```math
\theta_{N+\ell}\in[0,2\pi),\qquad 0\leq\ell<N.
```

Define the nonnegative magnitude state and diagonal phase unitary by

<a id="S5.EGx14"></a>

```math
\begin{aligned}\lvert \psi_{\mathrm{mag}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle & :=U_{\mathrm{chk}}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert 0\rangle ^{\otimes n},\end{aligned}
```

```math
\begin{aligned}D_{\mathrm{ph}}(\boldsymbol{\theta}_{\mathrm{ph}}) & :=\sum_{\ell=0}^{N-1}e^{\mathrm{i}\theta_{N+\ell}}\lvert b_{\ell}\rangle \!\langle b_{\ell}\rvert ,\end{aligned}
```

```math
\begin{aligned}\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle & :=D_{\mathrm{ph}}(\boldsymbol{\theta}_{\mathrm{ph}})\lvert \psi_{\mathrm{mag}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle .\end{aligned}
```

Write $`x_{\ell}(\boldsymbol{\theta}):=\langle b_{\ell}\vert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle`$. The native complex preparation satisfies

<a id="S5.EGx15"></a>

```math
\begin{aligned}\mathrm{HopfComplex}(\boldsymbol{\theta})\lvert 0\rangle ^{\otimes n} & =D_{\mathrm{ph}}(\boldsymbol{\theta}_{\mathrm{ph}})U_{\mathrm{chk}}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert 0\rangle ^{\otimes n}\end{aligned}
```

<a id="S5.E29"></a>

```math
{=\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle .}\tag{29}
```

For correctness substitutions, write $`U_{\mathrm{fwd}}^{\mathbb{C}}`$ for any exact complex preparation satisfying

<a id="S5.E30"></a>

```math
{U_{\mathrm{fwd}}^{\mathbb{C}}\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle .}\tag{30}
```

This is the complex instance of the state-column principle in Sec. [II D](reverse-task.md#S2.SS4). The designated assigned-work schedule is the direct-angle preparation $`D_{\mathrm{ph}}U_{\mathrm{chk}}`$; the native $`\mathrm{HopfComplex}`$ circuit is another direct-angle state-column completion. Appendix [A 2](four-qubit-example.md#A1.SS2) recalls the native gate-level realization, including the complex two-leaf completion.

Magnitude differentiation keeps the phase layer fixed. The resulting normalized direction is the phase-dressed real complement,

<a id="S5.Ex49"></a>

```math
\lvert e_{j}^{\mathbb{C}}(\boldsymbol{\theta})\rangle :=D_{\mathrm{ph}}(\boldsymbol{\theta}_{\mathrm{ph}})\lvert e_{j}^{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle .
```

The complex magnitude metric equals the real tree metric,

<a id="S5.E31"></a>

```math
{g^{\mathbb{C}}_{j,j}(\boldsymbol{\theta})=g^{\mathbb{R}}_{j,j}(\boldsymbol{\theta}_{\mathrm{mag}}),\qquad 1\leq j<N.}\tag{31}
```

Therefore,

<a id="S5.EGx16"></a>

```math
\begin{aligned}\partial_{\theta_{j}}\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle & =\sqrt{g^{\mathbb{C}}_{j,j}(\boldsymbol{\theta})}\lvert e_{j}^{\mathbb{C}}(\boldsymbol{\theta})\rangle ,\end{aligned}
```

<a id="S5.E32"></a>

```math
{\begin{aligned}\partial_{\theta_{j}}E_{O} & =2\sqrt{g^{\mathbb{C}}_{j,j}(\boldsymbol{\theta})}\mathrm{Re}\langle e_{j}^{\mathbb{C}}\rvert O\lvert \psi^{\mathbb{C}}\rangle ,\qquad 1\leq j<N.\end{aligned}}\tag{32}
```

The complete complex magnitude frame is

<a id="S5.EGx17"></a>

```math
\begin{aligned}W_{\mathbb{C}}(\boldsymbol{\theta}) & :=D_{\mathrm{ph}}(\boldsymbol{\theta}_{\mathrm{ph}})W_{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}}),\end{aligned}
```

```math
\begin{aligned}W_{\mathbb{C}}^{\dagger}(\boldsymbol{\theta}) & =W_{\mathbb{R}}^{\dagger}(\boldsymbol{\theta}_{\mathrm{mag}})D_{\mathrm{ph}}^{\dagger}(\boldsymbol{\theta}_{\mathrm{ph}}).\end{aligned}
```

Its columns satisfy

<a id="S5.Ex53"></a>

```math
W_{\mathbb{C}}(\boldsymbol{\theta})\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle ,\qquad W_{\mathbb{C}}(\boldsymbol{\theta})\lvert b_{\lambda(j)}\rangle =\lvert e_{j}^{\mathbb{C}}(\boldsymbol{\theta})\rangle .
```

Common parameter arguments may now be suppressed. The displayed definition gives the separated inverse frame. A compiler may absorb phase dressing into addressed gates; Appendix [A 6](four-qubit-example.md#A1.SS6) gives the four-qubit realization.

<a id="S5.SS1.p3.1"></a>

**Phase-metric convention.** For $`p_{\ell}:=\vert x_{\ell}\vert ^{2}`$ and $`\boldsymbol{p}=(p_{0},\ldots,p_{N-1})^{\mathsf{T}}`$, the complex chart uses the ambient round-sphere metric of Ref. [[1](../references/paper-bibliography.md#bib.bib6)],

<a id="S5.Ex54"></a>

```math
G_{\mathrm{ph}}^{\mathrm{sph}}=\mathrm{diag}(\boldsymbol{p}).
```

Quotienting global phase would instead give the unused projective comparison $`G_{\mathrm{ph}}^{\mathrm{FS}}=\mathrm{diag}(\boldsymbol{p})-\boldsymbol{p}\boldsymbol{p}^{\mathsf{T}}`$. Uniform phase is not metric-null in the adopted geometry, although expectation objectives are invariant along it.

The complete complex gradient uses two templates. The magnitude template reuses each joint all-$`X`$ outcome across the $`N-1`$ magnitude coordinates. The phase template places each ancilla-$`Y`$/system-$`Z`$ outcome in a signed one-hot histogram for the $`N`$ leaf phases. They share state preparation and $`\mathrm{ctrl}(O)`$ but run as separate circuit families with different reverse blocks and readouts.

<a id="S5.SS2"></a>

## V B Complex magnitude circuit and parity reuse

**One magnitude circuit template.** At a fixed parameter point, prepare $`\lvert +\rangle _{a}\lvert 0\rangle ^{\otimes n}`$ and apply

<a id="S5.Ex55"></a>

```math
U_{\mathrm{fwd}}^{\mathbb{C}}\longrightarrow\mathrm{ctrl}(O)\longrightarrow W_{\mathbb{C}}^{\dagger},
```

followed by $`X`$-basis measurement of every qubit. The accounting of assigned Hopf CNOT work for the designated separated implementation uses the block order

<a id="S5.Ex56"></a>

```math
U_{\mathrm{chk}}\longrightarrow D_{\mathrm{ph}}\longrightarrow\mathrm{ctrl}(O)\longrightarrow D_{\mathrm{ph}}^{\dagger}\longrightarrow W_{\mathbb{R}}^{\dagger}.
```

The state-column identity in Eq. ([29](global-complex.md#S5.E29)) also permits the native $`\mathrm{HopfComplex}`$ circuit as the forward block. Both forward choices belong to the same complex-magnitude measurement family and retain direct coordinate-to-angle control; the theorem’s finite constants refer to the separated schedule.

One execution returns the joint $`(n+1)`$-bit outcome $`(b_{m},\boldsymbol{y})`$ used by the real global-frame method. For every magnitude coordinate, define

<a id="S5.E33"></a>

```math
{Z_{j}^{\mathbb{C},\mathrm{mag}}(b_{m},\boldsymbol{y}):=2\sqrt{g^{\mathbb{C}}_{j,j}}(-1)^{b_{m}+\lambda(j)\cdot\boldsymbol{y}},\qquad 1\leq j<N.}\tag{33}
```

Let $`S_{\mathrm{mag}}^{\mathbb{C}}`$ be the number of independent magnitude executions. Their empirical average is

<a id="S5.E34"></a>

```math
{\widehat{\partial_{\theta_{j}}E_{O}}=\frac{1}{S_{\mathrm{mag}}^{\mathbb{C}}}\sum_{t=1}^{S_{\mathrm{mag}}^{\mathbb{C}}}Z_{j}^{\mathbb{C},\mathrm{mag}}(b_{m,t},\boldsymbol{y}_{t}).}\tag{34}
```

The same outcomes serve every $`j`$; only the marker and known metric factor change. Because $`g^{\mathbb{C}}_{j,j}=g^{\mathbb{R}}_{j,j}`$, the signed histogram and Walsh transform in Eqs. ([24](global-real.md#S4.E24))–([26](global-real.md#S4.E26)) apply without modification.

<a id="S5.SS3"></a>

## V C Direct phase circuit and signed leaf histogram

Each phase derivative is already supported on one computational-basis leaf and needs no inverse frame:

<a id="S5.E35"></a>

```math
{\partial_{\theta_{N+\ell}}\lvert \psi^{\mathbb{C}}(\boldsymbol{\theta})\rangle =\mathrm{i}x_{\ell}(\boldsymbol{\theta})\lvert b_{\ell}\rangle ,\qquad 0\leq\ell<N.}\tag{35}
```

Computational-basis readout is therefore the identity differential resolution in Definition [2](reverse-task.md#Thmdefinition2). The corresponding objective derivative is

<a id="S5.Ex57"></a>

```math
\partial_{\theta_{N+\ell}}E_{O}=2\mathrm{Im}\langle \psi^{\mathbb{C}}\rvert \Pi_{\ell}O\lvert \psi^{\mathbb{C}}\rangle ,\qquad\Pi_{\ell}:=\lvert b_{\ell}\rangle \!\langle b_{\ell}\rvert .
```

**One phase circuit template.** Prepare $`\lvert +\rangle _{a}\lvert 0\rangle ^{\otimes n}`$ with $`\mathrm{HopfComplex}`$, apply $`\mathrm{ctrl}(O)`$, then measure the ancilla in $`Y`$ and the system in $`Z`$. The state-column contract permits any exact $`U_{\mathrm{fwd}}^{\mathbb{C}}`$ satisfying Eq. ([30](global-complex.md#S5.E30)) for correctness; the assigned-work comparison retains the designated direct-angle schedule. One execution returns $`(b_{p},\widehat{\ell})`$, where $`b_{p}\in\{0,1\}`$ and $`\widehat{\ell}=(z_{n}\cdots z_{1})_{2}\in\{0,\ldots,N-1\}`$.

**Single-execution record and direct average.** For each leaf,

<a id="S5.E36"></a>

```math
{Z_{N+\ell}^{\mathbb{C},\mathrm{ph}}(b_{p},\widehat{\ell}):=2(-1)^{b_{p}}\mathbf{1}\!\left\{\widehat{\ell}=\ell\right\}.}\tag{36}
```

Here and below, $`\mathbf{e}_{r}`$ denotes a classical standard basis vector; it is distinct from the normalized quantum tangent kets $`\lvert e_{j}^{\mathbb{R}}\rangle`$ and $`\lvert e_{j}^{\mathbb{C}}\rangle`$. Equivalently, with $`\mathbf{e}_{\widehat{\ell}}`$ the standard basis vector of $`\mathbb{R}^{N}`$, the complete phase record is

<a id="S5.E37"></a>

```math
{Z^{\mathbb{C},\mathrm{ph}}(b_{p},\widehat{\ell})=2(-1)^{b_{p}}\mathbf{e}_{\widehat{\ell}},\qquad\|Z^{\mathbb{C},\mathrm{ph}}\|_{2}=2.}\tag{37}
```

Let $`S_{\mathrm{ph}}^{\mathbb{C}}`$ be the number of independent phase outcomes. Their empirical average is

<a id="S5.EGx18"></a>

```math
\begin{aligned}\widehat{\partial_{\theta_{N+\ell}}E_{O}} & =\frac{2}{S_{\mathrm{ph}}^{\mathbb{C}}}\sum_{t=1}^{S_{\mathrm{ph}}^{\mathbb{C}}}(-1)^{b_{p,t}}\mathbf{1}\!\left\{\widehat{\ell}_{t}=\ell\right\}\end{aligned}
```

```math
=\frac{2}{S_{\mathrm{ph}}^{\mathbb{C}}}\left(C_{0,\ell}^{\mathrm{ph}}-C_{1,\ell}^{\mathrm{ph}}\right),
```

where $`C_{b,\ell}^{\mathrm{ph}}:=\#\{t:(b_{p,t},\widehat{\ell}_{t})=(b,\ell)\}`$. Each outcome updates one leaf bin, and the complete signed histogram returns all $`N`$ phase derivatives. Its classical decoding uses $`\mathcal{O}(S_{\mathrm{ph}}^{\mathbb{C}}+N)`$ operations and $`\mathcal{O}(N)`$ slots.

<a id="S5.SS3.p4.1"></a>

The record naturally retains all $`N`$ phase coordinates in the order of Ref. [[1](../references/paper-bibliography.md#bib.bib6)]. A uniform leaf-phase shift leaves the expectation objective unchanged, so the exact phase-gradient block is zero-sum. At a zero-probability leaf, the corresponding phase differential and exact derivative vanish; the direct estimator remains defined without division by the leaf amplitude.

Protocol [1](global-complex.md#S5.SS3.p6.pic1) summarizes the single-execution estimators. Each magnitude outcome serves all depths, and the phase stream completes the complex gradient.

<a id="S5.SS3.p6.pic1"></a>

<a id="S5.SS3.p6.pic1.p1.1"></a>

## Protocol 1. Global-frame method: one execution serves all depths

**ONE MAGNITUDE EXECUTION**

Prepare the real or complex Hopf state, apply $`\mathrm{ctrl}(O)`$, and apply the chart-specific inverse frame $`W_{\mathbb{R}}^{\dagger}`$ or $`W_{\mathbb{C}}^{\dagger}`$. Measure the ancilla and system in $`X`$, obtaining $`(b_{m},\boldsymbol{y})`$.

**WHAT THAT EXECUTION MEANS**

For every internal node $`j`$, the same outcome enters the real or complex record in Eq. ([22](global-real.md#S4.E22)) or Eq. ([33](global-complex.md#S5.E33)). Its ancilla and Walsh signs, together with the known metric factor, form one simultaneous sample of the complete magnitude-gradient block.

**AFTER MANY EXECUTIONS**

The signed histogram of $`\boldsymbol{y}`$ contains all required parity moments. One fast Walsh–Hadamard transform evaluates them together; metric rescaling then returns the complete magnitude block.

**COMPLEX PHASES**

For the complex chart, a second family of executions measures the ancilla in $`Y`$ and the system in $`Z`$. Each outcome names one leaf and contributes a signed one-hot sample to the phase-gradient block.

**RETURN**

The real chart returns the magnitude block. The complex chart concatenates the magnitude and phase blocks.

<a id="S5.SS4"></a>

## V D Complex guarantee and cost at a glance

**Guarantee.** The magnitude and phase records satisfy

<a id="S5.EGx19"></a>

<a id="S5.E38"></a>

```math
{\begin{aligned}\mathbb{E}Z_{j}^{\mathbb{C},\mathrm{mag}} & =\partial_{\theta_{j}}E_{O}, & \vert Z_{j}^{\mathbb{C},\mathrm{mag}}\vert & \leq 2\sqrt{g^{\mathbb{C}}_{j,j}}\leq 2,\end{aligned}}\tag{38}
```

<a id="S5.E39"></a>

```math
{\begin{aligned}\mathbb{E}Z_{N+\ell}^{\mathbb{C},\mathrm{ph}} & =\partial_{\theta_{N+\ell}}E_{O}.\end{aligned}}\tag{39}
```

Every complex magnitude depth has the norm-two property in Eq. ([28](global-real.md#S4.E28)), and every phase record has norm two by Eq. ([37](global-complex.md#S5.E37)). With the allocations $`S_{\mathrm{mag}}^{\mathbb{C}}`$ and $`S_{\mathrm{ph}}^{\mathbb{C}}`$ in Eq. ([50](accuracy-resources.md#S7.E50)), the all-$`X`$ magnitude and separate $`Y/Z`$ phase templates recover the complete complex coordinate vector. Appendix [B 6](proofs-and-compilation.md#A2.SS6) proves phase dressing, magnitude parity, the phase-quadrature sign, the one-hot identity, and the compiler global-phase identity. The two records supply the complex case of Theorem [1](accuracy-resources.md#Thmtheorem1)(A).

**Cost at a glance.** For the complete complex Hopf chart, $`M=2N-1`$, and the gradient uses separate magnitude and phase templates. Their total global execution count is $`S_{\mathrm{glob}}^{\mathbb{C}}:=S_{\mathrm{mag}}^{\mathbb{C}}+S_{\mathrm{ph}}^{\mathbb{C}}`$. Assigned Hopf CNOT work sums the selected forward and reverse block charges over these executions; the controlled reflection is reported as the matched application component. Both streams accumulate in length-$`N`$ histograms. Classical decoding costs $`\mathcal{O}(S_{\mathrm{glob}}^{\mathbb{C}}+N\log N)`$, auxiliary storage is $`\mathcal{O}(N)`$, and the output has $`2N-1`$ entries. At fixed accuracy and confidence, $`S_{\mathrm{glob}}^{\mathbb{C}}=\mathcal{O}(\log\log M)`$.

The global-frame method now returns the complete real or complex Hopf gradient, with one magnitude stream shared across every depth. Checkpointing uses the same differential structure at a different resolution: it replaces the complete inverse frame by a layer-local reverse suffix when only selected depths are needed.
