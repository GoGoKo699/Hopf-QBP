[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S6"></a>

# VI Checkpoint method: layer-local reverse gradients

<a id="S6.SS1"></a>

## VI A From a complete frame to one active depth

The checkpoint method returns the reflected response to one selected tree layer. The forward prefix creates the state at depth $`d`$; after the controlled reflection, the inverse suffix returns the reflected branch to that layer. The measured prefix then identifies the active coordinate. This is the checkpointed adjoint mechanism.

For depth $`d`$, factor the depth completion as

<a id="S6.EGx20"></a>

```math
\begin{aligned}A_{d} & :=U_{d}\cdots U_{1}U_{0},\end{aligned}
```

```math
\begin{aligned}B_{d} & :=U_{n-1}\cdots U_{d+1},\qquad U_{\mathrm{chk}}=B_{d}A_{d},\end{aligned}
```

and define the checkpoint state

<a id="S6.Ex62"></a>

```math
\lvert \alpha_{d}\rangle :=A_{d}\lvert 0\rangle ^{\otimes n}.
```

The real reflected branch after suffix reversal is

<a id="S6.Ex63"></a>

```math
\lvert \beta_{d}^{\mathbb{R}}\rangle :=B_{d}^{\dagger}O\lvert \psi^{\mathbb{R}}\rangle .
```

For $`j=2^{d}+r`$, differentiation at the selected depth gives

<a id="S6.E40"></a>

```math
\partial_{\theta_{j}}E_{O}=2\operatorname{Im}\langle \beta_{d}^{\mathbb{R}}\rvert Q_{d,r}\lvert \alpha_{d}\rangle .\tag{40}
```

Thus $`B_{d}^{\dagger}`$ is the required real reverse block.

<a id="S6.SS2"></a>

## VI B Real checkpoint template and decoder

**One depth-specific circuit template.** For a selected depth $`d`$, prepare $`\lvert +\rangle _{a}\lvert 0\rangle ^{\otimes n}`$ and apply

<a id="S6.Ex64"></a>

```math
\mathrm{HopfReal}(\boldsymbol{\theta}_{\mathrm{mag}})\longrightarrow\operatorname{ctrl}(O)\longrightarrow B_{d}^{\dagger}(\boldsymbol{\theta}_{\mathrm{mag}}).
```

The state-column contract permits any exact $`U_{\mathrm{fwd}}^{\mathbb{R}}`$ satisfying Eq. ([15](balanced-differential.md#S3.E15)) for correctness. The assigned-work comparison fixes $`U_{\mathrm{chk}}`$ as the designated direct-angle forward for this checkpoint program and its matched scalar baseline. After suffix reversal, the two branches are

<a id="S6.E41"></a>

```math
\lvert \Omega_{d}^{\mathbb{R}}\rangle =\frac{\lvert 0\rangle _{a}\lvert \alpha_{d}\rangle +\lvert 1\rangle _{a}\lvert \beta_{d}^{\mathbb{R}}\rangle }{\sqrt{2}}.\tag{41}
```

The $`Y`$-quadrature identity in Appendix [B 1](proofs-and-compilation.md#A2.SS1) converts their interference into the transported derivative in Eq. ([40](checkpoints.md#S6.E40)).

**One joint outcome.** Measure the branch ancilla in $`Y`$, the $`d`$ prefix qubits in $`Z`$, and the target $`q_{n-d}`$ in $`Y`$. The record uses the ancilla, prefix, and target; the lower suffix need not be measured. One execution returns $`(b_{c},b_{t},\widehat{r})`$, where $`\widehat{r}=(z_{n}\cdots z_{n-d+1})_{2}\in\{0,\ldots,2^{d}-1\}`$, with $`\widehat{r}=0`$ at depth zero.

**Single-execution record and direct average.** The outcome defines

<a id="S6.E42"></a>

```math
Z_{d}^{\mathrm{chk}}(b_{c},b_{t},\widehat{r}):=-2(-1)^{b_{c}+b_{t}}\mathbf{e}_{\widehat{r}}\in\mathbb{R}^{2^{d}},\tag{42}
```

where $`\mathbf{e}_{\widehat{r}}`$ is the standard basis vector indexed by the measured prefix. Let $`S_{d}`$ be the number of records collected at depth $`d`$. Their average gives $`\widehat{\mu}_{d}^{\mathrm{mag}}=S_{d}^{-1}\sum_{s=1}^{S_{d}}Z_{d,s}^{\mathrm{chk}}`$. Componentwise,

<a id="S6.E43"></a>

```math
\widehat{\partial_{\theta_{2^{d}+r}}E_{O}}=-\frac{2}{S_{d}}\sum_{s=1}^{S_{d}}(-1)^{b_{c,s}+b_{t,s}}\mathbf{1}\!\left\{\widehat{r}_{s}=r\right\}.\tag{43}
```

Each outcome updates one of the $`2^{d}`$ prefix bins. The same stream therefore recovers every coordinate at depth $`d`$. Changing the depth changes the suffix, readout target, and associated circuit template.

<a id="S6.SS3"></a>

## VI C Complex active-interface extension

Before the suffix is applied, the reached interface consists of states whose lower $`n-d-1`$ qubits remain in $`\lvert 0\rangle`$. Its projector is

<a id="S6.Ex65"></a>

```math
P_{d}:=I_{q_{n}\cdots q_{n-d}}\otimes(\lvert 0\rangle \!\langle 0\rvert )^{\otimes(n-d-1)}.
```

Both $`\lvert \alpha_{d}\rangle`$ and $`Q_{d,r}\lvert \alpha_{d}\rangle`$ lie in this subspace. A complex-compatible suffix therefore needs to agree with the separated phase-dressed suffix only on these reached columns:

<a id="S6.Ex66"></a>

```math
B_{d,\mathbb{C}}P_{d}=D_{\mathrm{ph}}B_{d}P_{d}.
```

This active-interface identity fixes exactly the action used by the checkpoint record. The unused unitary completion remains free. The separated choice $`B_{d,\mathbb{C}}=D_{\mathrm{ph}}B_{d}`$ satisfies the same relation on the full space. Define the transported complex response by

<a id="S6.Ex67"></a>

```math
\lvert \beta_{d}^{\mathbb{C}}\rangle :=B_{d,\mathbb{C}}^{\dagger}O\lvert \psi^{\mathbb{C}}\rangle .
```

**One complex depth-$`d`$ template.** An integrated realization applies $`\mathrm{HopfComplex}`$, $`\operatorname{ctrl}(O)`$, and $`B_{d,\mathbb{C}}^{\dagger}`$, followed by the real checkpoint’s $`Y/Z/Y`$ measurement and signed one-hot record. The separated realization is

<a id="S6.E44"></a>

```math
U_{\mathrm{chk}}\longrightarrow D_{\mathrm{ph}}\longrightarrow\operatorname{ctrl}(O)\longrightarrow D_{\mathrm{ph}}^{\dagger}\longrightarrow B_{d}^{\dagger}.\tag{44}
```

The interface identity preserves the measured correlators and the average in Eq. ([43](checkpoints.md#S6.E43)); integrated and separated completions may act differently on the unused columns. At the final depth, $`B_{n-1}=I`$ and $`P_{n-1}=I`$. The real reverse block is the identity, and the complex reverse block is $`D_{\mathrm{ph}}^{\dagger}`$. These templates supply the complex magnitude block. The direct phase template of Sec. [V](global-complex.md#S5) supplies the complementary phase-coordinate block.

Protocol [2](checkpoints.md#S6.SS3.p4.pic1) gives the layer-local estimator one execution at a time. Different depths use separate streams because each has its own reverse suffix and measured target.

<a id="S6.SS3.p4.pic1"></a>

<a id="S6.SS3.p4.pic1.p1.1"></a>

## Protocol 2. Checkpoint method: one execution serves one depth

**CHOOSE A DEPTH**

Fix $`d`$. The checkpointed adjoint reverses the reflected branch only through the suffix below that layer.

**ONE CHECKPOINT EXECUTION**

Prepare the Hopf state, apply $`\operatorname{ctrl}(O)`$, and apply the chart-specific reverse block $`B_{d}^{\dagger}`$ or $`B_{d,\mathbb{C}}^{\dagger}`$. Measure the ancilla and the depth-$`d`$ target in $`Y`$ and the active prefix in $`Z`$, obtaining $`(b_{c},b_{t},\widehat{r})`$.

**WHAT THAT EXECUTION MEANS**

The prefix $`\widehat{r}`$ selects one coordinate at depth $`d`$, while the two $`Y`$ outcomes supply its sign. The signed one-hot contribution $`-2(-1)^{b_{c}+b_{t}}\mathbf{e}_{\widehat{r}}`$ samples the complete depth-$`d`$ gradient block.

**AFTER MANY EXECUTIONS**

Average the records to recover all $`2^{d}`$ derivatives at that depth. Requested depths use separate streams because their reverse suffixes and targets differ.

**COMPLEX COMPLETION**

For a complete complex gradient, append the direct phase stream from the global-frame construction.

<a id="S6.SS4"></a>

## VI D Checkpoint guarantee and cost at a glance

**Guarantee.** For either magnitude construction, with $`\mu_{d}^{\mathrm{mag}}`$ interpreted in its corresponding chart,

<a id="S6.E45"></a>

```math
\mathbb{E}Z_{d}^{\mathrm{chk}}=\mu_{d}^{\mathrm{mag}},\tag{45}
```

and every record satisfies

<a id="S6.E46"></a>

```math
\|Z_{d}^{\mathrm{chk}}\|_{2}=2.\tag{46}
```

The checkpoint and global records therefore have the same statistical scale at a fixed depth. For one selected depth, the common count in Eq. ([49](accuracy-resources.md#S7.E49)) with failure probability $`\eta=\delta`$ suffices. Equation ([50](accuracy-resources.md#S7.E50)) gives the complete-coordinate allocations. A complete real gradient uses one stream for each of the $`n`$ magnitude depths; a complete complex gradient adds the direct phase stream. Appendix [B 7](proofs-and-compilation.md#A2.SS7) proves the transported derivative, $`Y`$-quadrature sign, one-hot readout, interface substitution, and within-depth commutation. Appendix [A 8](four-qubit-example.md#A1.SS8) gives the real and complex four-qubit depth-$`2`$ circuits. One selected depth is a block reverse pass; the complete all-depth schedule supplies Theorem [1](accuracy-resources.md#Thmtheorem1)(B).

**Cost at a glance.** A selected depth uses one template, $`S_{d}`$ repetitions, and a signed $`2^{d}`$-bin histogram. For $`q`$ selected depths, the checkpoint method sums the repeated charges of $`q`$ templates. A complete real schedule streams all histograms in $`\mathcal{O}(\sum_{d=0}^{n-1}S_{d}+N)`$ classical operations and uses $`\mathcal{O}(N)`$ auxiliary storage, producing $`N-1`$ entries because $`\sum_{d}2^{d}=N-1`$. At fixed accuracy and confidence, the complete real schedule uses $`\mathcal{O}(\log M\log\log M)`$ executions with $`M=N-1`$; adding the direct complex-phase histogram gives the same order with $`M=2N-1`$.
