[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S2"></a>

# II The two-qubit clue and the reverse task

<a id="S2.SS1"></a>

## II A One split, three directions

The two-qubit case contains the local split-and-complement pattern used throughout the paper. Take $`n=2`$ and $`N=4`$. The two depth-one subtree states are

<a id="S2.EGx2"></a>

```math
\begin{aligned}\lvert \sigma_{2}\rangle & =\cos\theta_{2}\lvert 00\rangle +\sin\theta_{2}\lvert 01\rangle ,\end{aligned}
```

```math
\begin{aligned}\lvert \sigma_{3}\rangle & =\cos\theta_{3}\lvert 10\rangle +\sin\theta_{3}\lvert 11\rangle ,\end{aligned}
```

and the root combines them as

<a id="S2.Ex5"></a>

```math
\lvert \psi^{\mathbb{R}}\rangle =\cos\theta_{1}\lvert \sigma_{2}\rangle +\sin\theta_{1}\lvert \sigma_{3}\rangle .
```

Differentiating one split replaces its local state direction by the orthogonal partner,

<a id="S2.EGx3"></a>

```math
\begin{aligned}\lvert e_{1}^{\mathbb{R}}\rangle & =-\sin\theta_{1}\lvert \sigma_{2}\rangle +\cos\theta_{1}\lvert \sigma_{3}\rangle ,\end{aligned}
```

```math
\begin{aligned}\lvert e_{2}^{\mathbb{R}}\rangle & =-\sin\theta_{2}\lvert 00\rangle +\cos\theta_{2}\lvert 01\rangle ,\end{aligned}
```

```math
\begin{aligned}\lvert e_{3}^{\mathbb{R}}\rangle & =-\sin\theta_{3}\lvert 10\rangle +\cos\theta_{3}\lvert 11\rangle .\end{aligned}
```

The derivatives are

<a id="S2.EGx4"></a>

```math
\begin{aligned}\partial_{\theta_{1}}\lvert \psi^{\mathbb{R}}\rangle & =\lvert e_{1}^{\mathbb{R}}\rangle ,\end{aligned}
```

```math
\begin{aligned}\partial_{\theta_{2}}\lvert \psi^{\mathbb{R}}\rangle & =\cos\theta_{1}\lvert e_{2}^{\mathbb{R}}\rangle ,\end{aligned}
```

```math
\begin{aligned}\partial_{\theta_{3}}\lvert \psi^{\mathbb{R}}\rangle & =\sin\theta_{1}\lvert e_{3}^{\mathbb{R}}\rangle .\end{aligned}
```

Every coordinate has one normalized direction, and a descendant derivative is weighted by the amplitude arriving at its node. The directions are mutually orthogonal: the two descendants occupy disjoint subtrees, and each local complement is orthogonal to the subtree state used by its ancestor. The balanced $`n`$-qubit construction repeats this split-and-complement rule at every internal node.

<a id="S2.SS2"></a>

## II B What a reusable reverse record must provide

For a normalized state family and a parameter-independent Hermitian observable, let

<a id="S2.E1"></a>

```math
{E_{O}(\boldsymbol{\theta})=\langle \psi(\boldsymbol{\theta})\rvert O\lvert \psi(\boldsymbol{\theta})\rangle}\tag{1}
```

be the scalar expectation objective. A real coordinate changes this objective through the transition moment

<a id="S2.E2"></a>

```math
{\partial_{\theta_{j}}E_{O}=2\mathrm{Re}\langle \partial_{\theta_{j}}\psi\rvert O\lvert \psi\rangle .}\tag{2}
```

Normalization gives $`\mathrm{Re}\langle \psi\vert \partial_{\theta_{j}}\psi\rangle =0`$. Any component of the state differential parallel to $`\lvert \psi\rangle`$ therefore contributes no change to the expectation; only the orthogonal component is needed.

A reusable reverse record needs four ingredients: orthogonal differential directions, their coordinate weights, a reversible map to computational columns, and a classical rule that reuses one outcome across a coordinate block. The Hopf tree supplies the weighted differential frame; controlled interference and classical decoding convert it into shared gradient records. Sections [III](balanced-differential.md#S3)–[VI](checkpoints.md#S6) construct the block estimators. Theorem [1](accuracy-resources.md#Thmtheorem1) gives their accuracy, work, and storage guarantees, and Appendix [B 1](proofs-and-compilation.md#A2.SS1) proves the common interference identities.

<a id="S2.SS3"></a>

## II C Objective access and output target

Fix a known Hopf state circuit, a parameter point, and a scalar expectation objective. The required output is the complete classical vector of raw Hopf-coordinate derivatives. The construction assumes that the objective is available coherently as a controlled reflection with known relative phase.

<a id="Thmassumption1"></a>

**Assumption 1 (Phase-calibrated controlled reflection).**

The observable is a known, parameter-independent Hermitian unitary,

<a id="S2.Ex12"></a>

```math
O=O^{\dagger},\qquad O^{2}=I,
```

and the exact controlled operation

<a id="S2.Ex13"></a>

```math
\mathrm{ctrl}(O)=\lvert 0\rangle \!\langle 0\rvert \otimes I+\lvert 1\rangle \!\langle 1\rvert \otimes O
```

is available with a known relative phase between its branches, called the controlled-branch phase.

A classical description of $`O`$, or uncontrolled access to it, does not supply this interface. If the controlled branch implements $`e^{\mathrm{i}\gamma}O`$, the $`X`$- and $`Y`$-readouts contain $`\mathrm{Re}(e^{\mathrm{i}\gamma}z)`$ and $`\mathrm{Im}(e^{\mathrm{i}\gamma}z)`$. A known $`\gamma`$ is removed by a phase correction or calibrated equatorial readout. An unknown one changes the fixed decoder but does not affect the uncontrolled channel $`O(\cdot)O^{\dagger}`$.

<a id="S2.SS3.p3.1"></a>

Ref. [[1](../references/paper-bibliography.md#bib.bib6)] obtained the same moments from separately prepared state, tangent, and signed-branch states. Calibrated controlled access instead creates the coherent branch relation used by the shared records. This is a Hadamard-test instance [[38](../references/paper-bibliography.md#bib.bib42)], with the calibration fixing the quadrature signs [[39](../references/paper-bibliography.md#bib.bib2)]. A detector bit $`b\in\{0,1\}`$ represents eigenvalue $`(-1)^{b}`$.

The complete Hopf chart has $`M`$ real-valued parameters and returns

<a id="S2.Ex14"></a>

```math
\nabla_{\boldsymbol{\theta}}E_{O}=\left(\partial_{\theta_{1}}E_{O},\ldots,\partial_{\theta_{M}}E_{O}\right)^{\mathsf{T}}\in\mathbb{R}^{M}.
```

Throughout, $`0<\varepsilon,\delta<1`$.

<a id="Thmdefinition1"></a>

**Definition 1 (Complete-gradient accuracy).**

An estimate $`\widehat{\nabla_{\boldsymbol{\theta}}E_{O}}\in\mathbb{R}^{M}`$ is $`(\varepsilon,\delta)`$ accurate if

<a id="S2.E3"></a>

```math
{\mathbb{P}\!\left[\left\|\widehat{\nabla_{\boldsymbol{\theta}}E_{O}}-\nabla_{\boldsymbol{\theta}}E_{O}\right\|_{\infty}\leq\varepsilon\right]\geq 1-\delta.}\tag{3}
```

The condition gives simultaneous absolute coordinatewise accuracy for the complete classical output. Each shared record has a coordinate block as its mean.

<a id="Thmdefinition2"></a>

**Definition 2 (State-coordinate quantum backpropagation).**

For a known differentiable state circuit $`\boldsymbol{\theta}\mapsto\lvert \psi(\boldsymbol{\theta})\rangle`$, a reverse protocol is called *state-coordinate quantum backpropagation* if controlled objective interference is followed by a known resolution of the state differential. The resolution may be a reverse unitary or the identity when the relevant differential directions are already localized in the measurement basis. The protocol returns a vector-valued record $`Z_{\mathcal{I}}`$ satisfying

<a id="S2.E4"></a>

```math
{\mathbb{E}Z_{\mathcal{I}}=\left(2\mathrm{Re}\langle \partial_{\theta_{j}}\psi\rvert O\lvert \psi\rangle \right)_{j\in\mathcal{I}}}\tag{4}
```

for a coordinate block $`\mathcal{I}`$. A complete protocol combines such shared blocks to produce the gradient in Definition [1](reverse-task.md#Thmdefinition1).

<a id="S2.SS3.p6.1"></a>

**Matched resource benchmark.** Following the complete-gradient versus function-evaluation comparison of Ref. [[3](../references/paper-bibliography.md#bib.bib1)], we use the logarithmic overhead scale realized in Ref. [[4](../references/paper-bibliography.md#bib.bib7)]. Under the direct-angle accounting of Sec. [VII C](accuracy-resources.md#S7.SS3), the benchmark permits $`\mathcal{O}(\log M)`$ overhead in assigned Hopf CNOT work and input/output-inclusive storage. The matched scalar uses the same forward preparation and controlled reflection but omits the reverse block; the gradient program materializes the complete vector. The gradient protocols resolve $`O\lvert \psi\rangle`$ globally in the addressed frame, locally at a checkpoint, or directly in the leaf basis.

Each execution starts from a fresh product input and ends with destructive product-basis measurement. State preparation, reverse blocks, controlled reflection, readout basis changes, and classical processing are exact. Only sampling fluctuations enter the accuracy bounds. The system and branch ancilla use $`n+1`$ qubits, besides compiler and controlled-reflection workspace. All displayed execution and Hopf-work bounds are per reflection.

**Reflection-sum objectives.** Let $`H=\sum_{\alpha=1}^{L}a_{\alpha}O_{\alpha}`$ have fixed real coefficients $`a_{\alpha}`$ and parameter-independent terms satisfying $`O_{\alpha}^{\dagger}=O_{\alpha}`$ and $`O_{\alpha}^{2}=I`$. Set $`\Lambda:=\sum_{\alpha}\vert a_{\alpha}\vert >0`$ and assume calibrated controlled access to each term. Sample $`\alpha`$ with $`p_{\alpha}=\vert a_{\alpha}\vert /\Lambda`$ and return $`\widetilde{Z}_{\mathcal{I}}:=\Lambda\mathrm{sgn}(a_{\alpha})Z_{\mathcal{I}}^{(\alpha)}`$ for a record $`Z_{\mathcal{I}}^{(\alpha)}`$ on block $`\mathcal{I}`$. With $`E_{H}:=\langle \psi\rvert H\lvert \psi\rangle`$,

<a id="S2.EGx5"></a>

```math
\begin{aligned}\mathbb{E}\widetilde{Z}_{\mathcal{I}} & =\sum_{\alpha}a_{\alpha}\mathbb{E}Z_{\mathcal{I}}^{(\alpha)}=\left(\partial_{\theta_{j}}E_{H}\right)_{j\in\mathcal{I}},\end{aligned}
```

```math
\begin{aligned}\|\widetilde{Z}_{\mathcal{I}}\|_{2} & \leq\Lambda B\quad\text{whenever}\quad\|Z_{\mathcal{I}}^{(\alpha)}\|_{2}\leq B.\end{aligned}
```

The sufficient execution bounds therefore acquire a factor of $`\Lambda^{2}`$. The matched scalar uses the same term distribution and expected controlled-term charge $`\sum_{\alpha}p_{\alpha}C(\mathrm{ctrl}(O_{\alpha}))`$.

<a id="S2.SS4"></a>

## II D Three circuit contracts

The constructions use three levels of circuit equality:

<a id="S2.EGx6"></a>

```math
\begin{aligned}U & =V, & \text{full-unitary equality},\end{aligned}
```

```math
\begin{aligned}U\lvert 0\rangle ^{\otimes n} & =V\lvert 0\rangle ^{\otimes n}, & \text{state-column equality},\end{aligned}
```

<a id="S2.E5"></a>

```math
{\begin{aligned}UP & =VP, & \text{active-interface equality}.\end{aligned}}\tag{5}
```

Here $`P`$ projects onto the interface subspace reached by the forward prefix. Full-unitary equality identifies the complete circuit action. State-column equality fixes the prepared state, which is sufficient when all subsequent operations are held fixed. Active-interface equality fixes exactly the columns reached at a checkpoint while leaving the unused completion free. The global-frame method uses designated columns of a complete frame; the checkpoint method uses the reached active interface.

This hierarchy separates forward correctness from compiler accounting. Any exact preparation with the same initialized state column may replace the forward circuit while the later controlled reflection, reverse block, and measurement remain fixed; the final record distribution is unchanged. The assigned-work statements below use the designated direct-angle Hopf schedules, which keep each chart coordinate directly tied to its physical control. A different state-equivalent compiler is evaluated with its own forward and reverse ledger. Appendix [A](four-qubit-example.md#A1) shows all three logical contracts in one finite circuit family.

The two-qubit construction fixes the local differential pattern, and the access model identifies the transition moments to be recovered. Applying the split-and-complement rule throughout the tree supplies the weighted orthonormal frame and depth interfaces used by both reverse methods.
