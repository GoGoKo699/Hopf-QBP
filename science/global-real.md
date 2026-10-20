[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S4"></a>

# IV Global-frame method for the real Hopf chart

<a id="S4.SS1"></a>

## IV A Construction of the addressed frame

The addressed frame is a reversible circuit whose zero column is the prepared state and whose designated nonzero columns are the normalized magnitude directions. It places each local complement in the computational column marked by $`\lambda(j)`$. For $`j=2^{d}+r\in\mathcal{L}_{d}`$, define the leftmost leaf of its subtree by

<a id="S4.Ex31"></a>

```math
\ell_{0}(j):=r2^{n-d}.
```

Let $`G_{j}`$ be the two-level rotation

<a id="S4.EGx10"></a>

<a id="S4.E16"></a>

```math
\begin{aligned}G_{j}\lvert b_{\ell_{0}(j)}\rangle & =\cos\theta_{j}\lvert b_{\ell_{0}(j)}\rangle +\sin\theta_{j}\lvert b_{\lambda(j)}\rangle ,\end{aligned}\tag{16}
```

<a id="S4.E17"></a>

```math
\begin{aligned}G_{j}\lvert b_{\lambda(j)}\rangle & =-\sin\theta_{j}\lvert b_{\ell_{0}(j)}\rangle +\cos\theta_{j}\lvert b_{\lambda(j)}\rangle ,\end{aligned}\tag{17}
```

and let it act as the identity elsewhere. Gates at one depth act on disjoint basis pairs. Applying parent layers before descendant layers gives

<a id="S4.Ex32"></a>

```math
V_{d}:=\prod_{r=0}^{2^{d}-1}G_{2^{d}+r},\qquad W_{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}}):=V_{n-1}\cdots V_{1}V_{0}.
```

Read columnwise, the product has the following action. At node $`j`$, the gate $`G_{j}`$ creates the state and complement coefficient patterns on the two child anchors. Descendant gates then expand those anchors into the complete child-subtree states. The marker map assigns each resulting complement a distinct nonzero computational label.

**Construction guarantee.** The map $`j\mapsto\lambda(j)`$ is a bijection from the $`N-1`$ internal nodes to the nonzero computational labels, and

<a id="S4.E18"></a>

```math
W_{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{R}}\rangle ,\qquad W_{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert b_{\lambda(j)}\rangle =\lvert e_{j}^{\mathbb{R}}\rangle .\tag{18}
```

Every normalized magnitude direction therefore has a reversible computational address. Appendix [B 4](proofs-and-compilation.md#A2.SS4) proves the marker bijection and column induction. Appendix [A 5](four-qubit-example.md#A1.SS5) lists the $`n=4`$ addressed gates.

<a id="S4.SS2"></a>

## IV B Why the inverse frame is readable

With the differential columns computationally addressed, controlled interference turns their transition amplitudes into jointly measurable parity moments. Whenever $`W\lvert 0\rangle ^{\otimes n}=\lvert \psi\rangle`$, applying the inverse frame after the controlled reflection gives

<a id="S4.E19"></a>

```math
\lvert \Omega_{W}\rangle =\frac{\lvert 0\rangle _{a}\lvert 0\rangle ^{\otimes n}+\lvert 1\rangle _{a}W^{\dagger}O\lvert \psi\rangle }{\sqrt{2}}.\tag{19}
```

For a basis label $`k=(k_{n}\cdots k_{1})_{2}`$, define

<a id="S4.Ex33"></a>

```math
X(k):=\bigotimes_{q=1}^{n}X_{q}^{k_{q}},\qquad k\cdot\boldsymbol{y}:=\sum_{q=1}^{n}k_{q}y_{q}\pmod{2}.
```

An all-$`X`$ outcome $`(b,\boldsymbol{y})`$ then has parity expectation

<a id="S4.E20"></a>

```math
\mathbb{E}\!\left[(-1)^{b+k\cdot\boldsymbol{y}}\right]=\operatorname{Re}\langle b_{k}\rvert W^{\dagger}O\lvert \psi\rangle .\tag{20}
```

Thus one measured bit string supplies a $`\{\pm 1\}`$ sample for every addressed frame column. Repeated outcomes estimate all corresponding transition moments. Setting $`W=W_{\mathbb{R}}`$ and $`k=\lambda(j)`$ recovers Eq. ([13](balanced-differential.md#S3.E13)). Appendix [B 1](proofs-and-compilation.md#A2.SS1) proves the generic identity, and Appendix [B 5](proofs-and-compilation.md#A2.SS5) proves its Hopf-frame specialization.

**What controlled interference contributes.** Write

<a id="S4.Ex34"></a>

```math
W^{\dagger}O\lvert \psi\rangle =\sum_{\ell=0}^{N-1}v_{\ell}\lvert b_{\ell}\rangle .
```

Equation ([20](global-real.md#S4.E20)) reads $`\operatorname{Re}v_{k}`$ linearly from the coherent two-branch state. For comparison, let $`p_{\mathrm{unc}}(\boldsymbol{y})`$ be the all-$`X`$ probability obtained by applying $`O`$, then $`W^{\dagger}`$, and measuring only the system. Its Walsh coefficient is

<a id="S4.Ex35"></a>

```math
\sum_{\boldsymbol{y}}(-1)^{k\cdot\boldsymbol{y}}p_{\mathrm{unc}}(\boldsymbol{y})=\sum_{\ell=0}^{N-1}v_{\ell}v_{\ell\oplus k}^{*},
```

where $`\ell\oplus k`$ is bitwise addition modulo two. System probabilities therefore encode amplitude autocorrelations. The coherent branch ancilla supplies the relative phase that turns the same parity analysis into the linear moment required by the gradient.

<a id="S4.SS3"></a>

## IV C Circuit template, outcomes, and decoder

**One circuit template.** At a fixed parameter point, the native-forward real implementation prepares $`\lvert +\rangle _{a}\lvert 0\rangle ^{\otimes n}`$ and applies

<a id="S4.E21"></a>

```math
\mathrm{HopfReal}(\boldsymbol{\theta}_{\mathrm{mag}})\longrightarrow\operatorname{ctrl}(O)\longrightarrow W_{\mathbb{R}}^{\dagger}(\boldsymbol{\theta}_{\mathrm{mag}}),\tag{21}
```

followed by $`X`$-basis measurement of the ancilla and all $`n`$ system qubits. This gate sequence and readout define the circuit template. One fresh execution returns the joint $`(n+1)`$-bit outcome

<a id="S4.Ex36"></a>

```math
(b_{m},\boldsymbol{y}),\qquad b_{m}\in\{0,1\},\qquad\boldsymbol{y}=(y_{1},\ldots,y_{n})\in\{0,1\}^{n}.
```

The state-column contract in Sec. [II D](reverse-task.md#S2.SS4) permits any exact $`U_{\mathrm{fwd}}^{\mathbb{R}}`$ satisfying Eq. ([15](balanced-differential.md#S3.E15)) to serve as the forward block for correctness. The native circuit displays the template; the assigned-work comparison uses the designated direct-angle forward of Sec. [VII C](accuracy-resources.md#S7.SS3).

**Single-execution record and direct average.** For every internal node, the same joint outcome defines

<a id="S4.E22"></a>

```math
Z_{j}^{\mathbb{R}}(b_{m},\boldsymbol{y}):=2\sqrt{g^{\mathbb{R}}_{j,j}}(-1)^{b_{m}+\lambda(j)\cdot\boldsymbol{y}}.\tag{22}
```

Given $`S`$ independent outcomes $`\{(b_{m,t},\boldsymbol{y}_{t})\}_{t=1}^{S}`$, the empirical coordinate gradient is

<a id="S4.EGx11"></a>

```math
\begin{aligned}\widehat{\partial_{\theta_{j}}E_{O}} & =\frac{1}{S}\sum_{t=1}^{S}Z_{j}^{\mathbb{R}}(b_{m,t},\boldsymbol{y}_{t})\end{aligned}
```

<a id="S4.E23"></a>

```math
=\frac{2\sqrt{g^{\mathbb{R}}_{j,j}}}{S}\sum_{t=1}^{S}(-1)^{b_{m,t}+\lambda(j)\cdot\boldsymbol{y}_{t}}.\tag{23}
```

The same $`S`$ outcomes enter Eq. ([23](global-real.md#S4.E23)) for every $`j`$; only the predetermined marker $`\lambda(j)`$ and known metric factor change. Records from one execution are correlated, but distinct executions are independent.

For $`n=2`$, $`\lambda(1)=(10)_{2}`$, $`\lambda(2)=(01)_{2}`$, and $`\lambda(3)=(11)_{2}`$; one outcome $`(b_{m},y_{1},y_{2})`$ supplies

<a id="S4.EGx12"></a>

```math
\begin{aligned}Z_{1}^{\mathbb{R}} & =2(-1)^{b_{m}+y_{2}},\end{aligned}
```

```math
\begin{aligned}Z_{2}^{\mathbb{R}} & =2\cos\theta_{1}(-1)^{b_{m}+y_{1}},\end{aligned}
```

```math
\begin{aligned}Z_{3}^{\mathbb{R}} & =2\sin\theta_{1}(-1)^{b_{m}+y_{1}+y_{2}}.\end{aligned}
```

The same $`S`$ recorded outcomes enter all three averages.

**Signed histogram and Walsh decoder.** The classical decoder first accumulates the joint counts

<a id="S4.E24"></a>

```math
C_{b,\boldsymbol{y}}:=\sum_{t=1}^{S}\mathbf{1}\!\left\{b_{m,t}=b,\ \boldsymbol{y}_{t}=\boldsymbol{y}\right\}\tag{24}
```

The counts obey $`\sum_{\boldsymbol{y}}(C_{0,\boldsymbol{y}}+C_{1,\boldsymbol{y}})=S`$. Define their signed histogram by

<a id="S4.Ex41"></a>

```math
h(\boldsymbol{y}):=C_{0,\boldsymbol{y}}-C_{1,\boldsymbol{y}}=\sum_{t:\boldsymbol{y}_{t}=\boldsymbol{y}}(-1)^{b_{m,t}}.
```

<a id="S4.SS3.p4.3"></a>

A fast Walsh–Hadamard transform [[40](../references/paper-bibliography.md#bib.bib5)] then evaluates all parity moments together:

<a id="S4.E25"></a>

```math
\widehat{m}_{k}=\frac{1}{S}\sum_{\boldsymbol{y}}h(\boldsymbol{y})(-1)^{k\cdot\boldsymbol{y}}.\tag{25}
```

The $`k=0`$ entry is the marginal ancilla imbalance and estimates only $`E_{O}`$. The other system-resolved parity entries retain the frame components needed for the complete gradient. After a tree pass computes the metric factors,

<a id="S4.E26"></a>

```math
\widehat{\partial_{\theta_{j}}E_{O}}=2\sqrt{g^{\mathbb{R}}_{j,j}}\widehat{m}_{\lambda(j)}.\tag{26}
```

The transform is the batched implementation of the direct averages in Eq. ([23](global-real.md#S4.E23)); it requires no additional quantum execution. The complete classical decoder uses $`\mathcal{O}(S+N\log N)`$ additions and subtractions and stores $`\mathcal{O}(N)`$ auxiliary histogram values.

<a id="S4.SS4"></a>

## IV D Global real guarantee and cost at a glance

**Guarantee.** For every internal node,

<a id="S4.E27"></a>

```math
\mathbb{E}Z_{j}^{\mathbb{R}}=\partial_{\theta_{j}}E_{O},\qquad\vert Z_{j}^{\mathbb{R}}\vert \leq 2\sqrt{g^{\mathbb{R}}_{j,j}}\leq 2.\tag{27}
```

When $`g^{\mathbb{R}}_{j,j}=0`$, the record is identically zero. At depth $`d`$, collect the magnitude coordinates as

<a id="S4.EGx13"></a>

```math
\begin{aligned}Z_{d}^{\mathrm{fr}} & :=\left(Z_{2^{d}+r}^{\mathbb{R}}\right)_{r=0}^{2^{d}-1},\end{aligned}
```

```math
\begin{aligned}\mu_{d}^{\mathrm{mag}} & :=\left(\partial_{\theta_{2^{d}+r}}E_{O}\right)_{r=0}^{2^{d}-1}.\end{aligned}
```

Every outcome satisfies

<a id="S4.E28"></a>

```math
\mathbb{E}Z_{d}^{\mathrm{fr}}=\mu_{d}^{\mathrm{mag}},\qquad\|Z_{d}^{\mathrm{fr}}\|_{2}=2.\tag{28}
```

Let $`S_{\mathrm{mag}}^{\mathbb{R}}`$ be the number of independent records in the real magnitude stream. The global-frame method repeats one template, and the same records serve every depth. The fixed-norm concentration result in Sec. [VII B](accuracy-resources.md#S7.SS2) gives the sufficient allocation in Eq. ([50](accuracy-resources.md#S7.E50)); one common count covers all coordinates and depths. Appendix [B 5](proofs-and-compilation.md#A2.SS5) proves the parity sign, unbiasedness, zero-weight behavior, depth normalization, and Walsh decoder. These identities supply the real case of Theorem [1](accuracy-resources.md#Thmtheorem1)(A).

<a id="S4.SS4.p2.1"></a>

**Cost at a glance.** For the complete real chart, $`M=N-1`$. At one parameter point, the template in Eq. ([21](global-real.md#S4.E21)) is executed $`S_{\mathrm{mag}}^{\mathbb{R}}`$ times. Each execution returns one joint $`(n+1)`$-bit outcome contributing to all $`N-1`$ coordinates. Outcomes stream into the $`N`$ signed-histogram bins, avoiding storage of the full raw record list. For the native and designated Hopf preparations, the forward block and addressed inverse frame each require $`\mathcal{O}(nN)`$ assigned Hopf CNOT work per execution [[1](../references/paper-bibliography.md#bib.bib6)]. The application-dependent controlled reflection and readout are reported separately. Classical decoding costs $`\mathcal{O}(S_{\mathrm{mag}}^{\mathbb{R}}+N\log N)`$ operations, uses $`\mathcal{O}(N)`$ auxiliary storage, and returns $`N-1`$ entries. The live quantum register contains the system, branch ancilla, and any compiler workspace. Sec. [VII C](accuracy-resources.md#S7.SS3) compares this assigned Hopf CNOT work with the matched scalar program used in the theorem.

The real construction establishes the shared magnitude mechanism: one global-frame template is repeated, and every outcome is reused across all tree depths. The complex chart preserves this mechanism after phase dressing and adds a separate leaf-local record to complete the phase-coordinate block.
