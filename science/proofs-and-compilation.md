[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="A2"></a>

# Appendix B Technical foundations, proofs, and compiler derivations

This appendix develops the proofs from the common interference identities to the complete-gradient theorem.

<a id="A2.SS1"></a>

## B 1 Controlled-interference identities

Let $`W\lvert 0\rangle ^{\otimes n}=\lvert \psi\rangle`$ and let an admissible forward circuit prepare the same state. Starting from $`\lvert +\rangle _{a}\lvert 0\rangle ^{\otimes n}`$, the forward block, $`\mathrm{ctrl}(O)`$, and $`W^{\dagger}`$ produce Eq. ([19](global-real.md#S4.E19)). Since $`X(k)\lvert 0\rangle ^{\otimes n}=\lvert b_{k}\rangle`$,

<a id="A2.Ex113"></a>

```math
\langle \Omega_{W}\rvert X_{a}\otimes X(k)\lvert \Omega_{W}\rangle =\frac{1}{2}\left(\langle 0\rvert X(k)W^{\dagger}O\lvert \psi\rangle +\langle \psi\rvert OWX(k)\lvert 0\rangle \right)=\mathrm{Re}\langle b_{k}\rvert W^{\dagger}O\lvert \psi\rangle .
```

The measured eigenvalue of $`X_{a}\otimes X(k)`$ is $`(-1)^{b+k\cdot\boldsymbol{y}}`$, proving Eq. ([20](global-real.md#S4.E20)).

For normalized branches $`\lvert \alpha\rangle ,\lvert \beta\rangle`$ and a Hermitian system operator $`A`$, set $`\lvert \Omega\rangle =(\lvert 0\rangle \lvert \alpha\rangle +\lvert 1\rangle \lvert \beta\rangle )/\sqrt{2}`$. Using $`\langle 0\rvert Y\lvert 1\rangle =-\mathrm{i}`$ and $`\langle 1\rvert Y\lvert 0\rangle =\mathrm{i}`$ gives

<a id="A2.E66"></a>

```math
{\langle \Omega\rvert Y_{a}\otimes A\lvert \Omega\rangle =\mathrm{Im}\langle \alpha\rvert A\lvert \beta\rangle =-\mathrm{Im}\langle \beta\rvert A\lvert \alpha\rangle .}\tag{B1}
```

The direct phase record uses the first form and the checkpoint record the second.

<a id="A2.SS2"></a>

## B 2 Balanced Hopf differential frame

For a tree node $`j`$, let $`\mathcal{H}_{j}`$ be the span of its descendant basis leaves and let $`\mathcal{I}(j)`$ be the internal nodes in that subtree.

<a id="Thmlemma1"></a>

**Lemma 1 (Subtree frame).**

The set $`\mathcal{B}_{j}:=\{\lvert \sigma_{j}\rangle \}\cup\{\lvert e_{k}^{\mathbb{R}}\rangle :k\in\mathcal{I}(j)\}`$ is an orthonormal basis of $`\mathcal{H}_{j}`$.

<a id="A2.SS2.2"></a>

**Proof.**

At a leaf, $`\mathcal{B}_{j}=\{\lvert b_{\ell}\rangle \}`$. Assume the statement for both children of an internal node $`j`$. Their leaf spaces are orthogonal. In the direct sum of the two child bases, replace the pair $`\lvert \sigma_{2j}\rangle ,\lvert \sigma_{2j+1}\rangle`$ by

<a id="A2.Ex114"></a>

```math
\begin{pmatrix}\lvert \sigma_{j}\rangle \\[2.0pt]
\lvert e_{j}^{\mathbb{R}}\rangle \end{pmatrix}=\begin{pmatrix}\cos\theta_{j}&\sin\theta_{j}\\
-\sin\theta_{j}&\cos\theta_{j}\end{pmatrix}\begin{pmatrix}\lvert \sigma_{2j}\rangle \\[2.0pt]
\lvert \sigma_{2j+1}\rangle \end{pmatrix}.
```

This orthogonal change of basis leaves every strict-descendant complement unchanged, completing the induction. ∎

At the root, Lemma [1](proofs-and-compilation.md#Thmlemma1) gives Eq. ([10](balanced-differential.md#S3.E10)). For an internal node $`j`$, expansion along the unique root-to-$`j`$ path gives

<a id="A2.E67"></a>

```math
{\lvert \psi^{\mathbb{R}}\rangle =\lvert \psi_{\neg j}\rangle +\sqrt{g^{\mathbb{R}}_{j,j}}\lvert \sigma_{j}\rangle ,\qquad\lvert \psi_{\neg j}\rangle \in\mathcal{H}_{j}^{\perp}.}\tag{B2}
```

The first term and incoming coefficient are independent of $`\theta_{j}`$. The coefficient is the nonnegative product of ancestor sine and cosine factors; its square obeys Eq. ([8](balanced-differential.md#S3.E8)). Since $`\partial_{\theta_{j}}\lvert \sigma_{j}\rangle =\lvert e_{j}^{\mathbb{R}}\rangle`$, Eq. ([11](balanced-differential.md#S3.E11)) follows. Orthonormality gives Eq. ([12](balanced-differential.md#S3.E12)). For $`g^{\mathbb{R}}_{j,j}=0`$, the coordinate derivative vanishes by Eq. ([B2](proofs-and-compilation.md#A2.E67)); Eq. ([9](balanced-differential.md#S3.E9)) still defines a normalized completion column.

For a Hermitian observable,

<a id="A2.Ex115"></a>

```math
\partial_{\theta_{j}}E_{O}=\langle \partial_{\theta_{j}}\psi\rvert O\lvert \psi\rangle +\langle \psi\rvert O\lvert \partial_{\theta_{j}}\psi\rangle =2\sqrt{g^{\mathbb{R}}_{j,j}}\mathrm{Re}\langle e_{j}^{\mathbb{R}}\rvert O\lvert \psi^{\mathbb{R}}\rangle ,
```

which is Eq. ([13](balanced-differential.md#S3.E13)).

<a id="A2.SS3"></a>

## B 3 Depth completion and forward-state substitution

Define real path coefficients recursively by

<a id="A2.E68"></a>

```math
{a_{0,0}=1,\qquad a_{d+1,2r}=a_{d,r}\cos\theta_{2^{d}+r},\qquad a_{d+1,2r+1}=a_{d,r}\sin\theta_{2^{d}+r}.}\tag{B3}
```

After the first $`d+1`$ depth layers,

<a id="A2.E69"></a>

```math
{U_{d}\cdots U_{0}\lvert 0\rangle ^{\otimes n}=\sum_{r=0}^{2^{d+1}-1}a_{d+1,r}\lvert r\rangle _{q_{n}\cdots q_{n-d}}\lvert 0\rangle _{q_{n-d-1}\cdots q_{1}}.}\tag{B4}
```

For $`d=0`$, this is the rotation in Eq. ([7](balanced-differential.md#S3.E7)) on $`q_{n}`$. Assume the statement through depth $`d-1`$. In the component with prefix $`r`$, exactly one projector in $`U_{d}`$ is active, and it rotates the fresh target $`q_{n-d}`$ from $`\lvert 0\rangle`$ to $`\cos\theta_{2^{d}+r}\lvert 0\rangle +\sin\theta_{2^{d}+r}\lvert 1\rangle`$. This gives the two recursions in Eq. ([B3](proofs-and-compilation.md#A2.E68)), so Eq. ([B4](proofs-and-compilation.md#A2.E69)) follows by induction.

At $`d=n-1`$, the coefficients are the real Hopf leaf amplitudes. Hence $`U_{\mathrm{chk}}\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{R}}\rangle`$, proving Eq. ([14](balanced-differential.md#S3.E14)); applying $`D_{\mathrm{ph}}`$ gives $`D_{\mathrm{ph}}U_{\mathrm{chk}}\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{C}}\rangle`$, which, together with the native complex state column, proves Eq. ([29](global-complex.md#S5.E29)).

For forward substitution, let $`U\lvert 0\rangle ^{\otimes n}=V\lvert 0\rangle ^{\otimes n}=\lvert \psi\rangle`$. Either forward block gives the same complete joint state, so identical subsequent unitaries and measurements give the same final state and output distribution. This establishes state-column substitution for the real-global, complex-global, direct-phase, and checkpoint records.

The forward and reverse circuits may therefore use different unitary completions of the same prepared state. This is a correctness statement: the assigned-work comparison additionally fixes the direct-angle forward and reverse schedules of Sec. [VII C](accuracy-resources.md#S7.SS3). A state-equivalent recompilation with different elementary physical angles requires its own ledger.

<a id="A2.SS4"></a>

## B 4 Addressed real-frame columns

Every nonzero integer $`k\lt N`$ has a unique factorization $`k=(2r+1)2^{t}`$ with $`t\geq 0`$. Setting $`d=n-t-1`$ gives $`0\leq r\lt 2^{d}`$ and $`k=(2r+1)2^{n-d-1}=\lambda(2^{d}+r)`$, so the marker map is a bijection.

Let $`W_{j}`$ be the product of addressed rotations in the subtree rooted at $`j`$, with $`G_{j}`$ applied before its strict descendants. The child products act on orthogonal leaf spaces, and $`W_{j}=(W_{2j}\oplus W_{2j+1})G_{j}`$. At a leaf, the anchor column is already the leaf state. Assuming the child anchor columns map to the child subtree states, Eqs. ([16](global-real.md#S4.E16)) and ([17](global-real.md#S4.E17)) give

<a id="A2.EGx31"></a>

```math
\begin{aligned}W_{j}\lvert b_{\ell_{0}(j)}\rangle & =\cos\theta_{j}\lvert \sigma_{2j}\rangle +\sin\theta_{j}\lvert \sigma_{2j+1}\rangle =\lvert \sigma_{j}\rangle ,\end{aligned}
```

```math
\begin{aligned}W_{j}\lvert b_{\lambda(j)}\rangle & =-\sin\theta_{j}\lvert \sigma_{2j}\rangle +\cos\theta_{j}\lvert \sigma_{2j+1}\rangle =\lvert e_{j}^{\mathbb{R}}\rangle .\end{aligned}
```

The same induction preserves all strict-descendant marker columns. At the root, $`\ell_{0}(1)=0`$, proving Eq. ([18](global-real.md#S4.E18)).

<a id="A2.SS5"></a>

## B 5 Global real readout and Walsh decoding

For any admissible real forward preparation, the state-column contract gives $`W_{\mathbb{R}}^{\dagger}U_{\mathrm{fwd}}^{\mathbb{R}}\lvert 0\rangle =\lvert 0\rangle`$ and $`W_{\mathbb{R}}^{\dagger}OU_{\mathrm{fwd}}^{\mathbb{R}}\lvert 0\rangle =W_{\mathbb{R}}^{\dagger}OW_{\mathbb{R}}\lvert 0\rangle`$. Hence

<a id="A2.EGx32"></a>

```math
\begin{aligned}\lvert \Omega_{\mathbb{R}}\rangle & =\frac{\lvert 0\rangle _{a}\lvert 0\rangle ^{\otimes n}+\lvert 1\rangle _{a}W_{\mathbb{R}}^{\dagger}OW_{\mathbb{R}}\lvert 0\rangle ^{\otimes n}}{\sqrt{2}},\end{aligned}
```

```math
\begin{aligned}\mathbb{E}\!\left[(-1)^{b_{m}+\lambda(j)\cdot\boldsymbol{y}}\right] & =\mathrm{Re}\langle e_{j}^{\mathbb{R}}\rvert O\lvert \psi^{\mathbb{R}}\rangle ,\end{aligned}
```

where the second line uses Eq. ([20](global-real.md#S4.E20)) at $`k=\lambda(j)`$ and Eq. ([18](global-real.md#S4.E18)). Multiplication by $`2\sqrt{g^{\mathbb{R}}_{j,j}}`$ proves Eqs. ([22](global-real.md#S4.E22)) and ([27](global-real.md#S4.E27)). Averaging independent copies gives Eq. ([23](global-real.md#S4.E23)); the same argument after phase dressing gives Eq. ([34](global-complex.md#S5.E34)). A zero metric factor makes the record zero for every outcome.

The metric mass is conserved across each tree depth, since the root weight is one and every parent splits by $`\cos^{2}\theta_{j}+\sin^{2}\theta_{j}=1`$. Therefore

<a id="A2.EGx33"></a>

```math
\begin{aligned}\sum_{r=0}^{2^{d}-1}g^{\mathbb{R}}_{2^{d}+r,2^{d}+r} & =1,\end{aligned}
```

```math
\begin{aligned}\|Z_{d}^{\mathrm{fr}}\|_{2}^{2} & =4\sum_{r=0}^{2^{d}-1}g^{\mathbb{R}}_{2^{d}+r,2^{d}+r}=4,\end{aligned}
```

which is Eq. ([28](global-real.md#S4.E28)).

Finally,

<a id="A2.Ex122"></a>

```math
\frac{1}{S}\sum_{t=1}^{S}(-1)^{b_{m,t}+k\cdot\boldsymbol{y}_{t}}=\frac{1}{S}\sum_{\boldsymbol{y}}\left[\sum_{t:\boldsymbol{y}_{t}=\boldsymbol{y}}(-1)^{b_{m,t}}\right](-1)^{k\cdot\boldsymbol{y}}=\frac{1}{S}\sum_{\boldsymbol{y}}h(\boldsymbol{y})(-1)^{k\cdot\boldsymbol{y}}.
```

<a id="A2.SS5.p3.2"></a>

This is Eq. ([25](global-real.md#S4.E25)). The fast Walsh–Hadamard transform uses $`\mathcal{O}(N\log N)`$ additions and subtractions [[40](../references/paper-bibliography.md#bib.bib5)]; one tree pass computes all metric factors in $`\mathcal{O}(N)`$ further operations.

<a id="A2.SS6"></a>

## B 6 Complex magnitude and direct phase identities

Since $`D_{\mathrm{ph}}`$ is independent of every magnitude angle and is unitary,

<a id="A2.EGx34"></a>

```math
\begin{aligned}\partial_{\theta_{j}}\lvert \psi^{\mathbb{C}}\rangle & =D_{\mathrm{ph}}\partial_{\theta_{j}}\lvert \psi_{\mathrm{mag}}\rangle =\sqrt{g^{\mathbb{C}}_{j,j}}\lvert e_{j}^{\mathbb{C}}\rangle ,\end{aligned}
```

```math
\begin{aligned}W_{\mathbb{C}}\lvert 0\rangle & =\lvert \psi^{\mathbb{C}}\rangle , & W_{\mathbb{C}}\lvert b_{\lambda(j)}\rangle & =\lvert e_{j}^{\mathbb{C}}\rangle .\end{aligned}
```

The first line proves Eq. ([32](global-complex.md#S5.E32)); the second uses $`W_{\mathbb{C}}=D_{\mathrm{ph}}W_{\mathbb{R}}`$ and the real frame columns. For any admissible complex forward preparation,

<a id="A2.EGx35"></a>

```math
\begin{aligned}W_{\mathbb{C}}^{\dagger}U_{\mathrm{fwd}}^{\mathbb{C}}\lvert 0\rangle & =\lvert 0\rangle ,\end{aligned}
```

```math
\begin{aligned}W_{\mathbb{C}}^{\dagger}OU_{\mathrm{fwd}}^{\mathbb{C}}\lvert 0\rangle & =W_{\mathbb{C}}^{\dagger}O\lvert \psi^{\mathbb{C}}\rangle ,\end{aligned}
```

```math
\begin{aligned}\mathbb{E}(-1)^{b_{m}+\lambda(j)\cdot\boldsymbol{y}} & =\mathrm{Re}\langle e_{j}^{\mathbb{C}}\rvert O\lvert \psi^{\mathbb{C}}\rangle .\end{aligned}
```

Thus Eqs. ([33](global-complex.md#S5.E33)) and ([38](global-complex.md#S5.E38)) follow. Phase dressing preserves the metric factors, so each depth record has norm two.

For a phase coordinate, direct differentiation and the controlled-interference identity give

<a id="A2.EGx36"></a>

```math
\begin{aligned}\partial_{\theta_{N+\ell}}\lvert \psi^{\mathbb{C}}\rangle & =\mathrm{i}\Pi_{\ell}\lvert \psi^{\mathbb{C}}\rangle =\mathrm{i}x_{\ell}\lvert b_{\ell}\rangle ,\end{aligned}
```

```math
\begin{aligned}\partial_{\theta_{N+\ell}}E_{O} & =2\mathrm{Im}\langle \psi^{\mathbb{C}}\rvert \Pi_{\ell}O\lvert \psi^{\mathbb{C}}\rangle ,\end{aligned}
```

```math
\begin{aligned}\lvert \Omega_{\mathrm{ph}}\rangle & =\frac{\lvert 0\rangle _{a}\lvert \psi^{\mathbb{C}}\rangle +\lvert 1\rangle _{a}O\lvert \psi^{\mathbb{C}}\rangle }{\sqrt{2}},\end{aligned}
```

```math
\begin{aligned}\langle \Omega_{\mathrm{ph}}\rvert Y_{a}\otimes\Pi_{\ell}\lvert \Omega_{\mathrm{ph}}\rangle & =\mathrm{Im}\langle \psi^{\mathbb{C}}\rvert \Pi_{\ell}O\lvert \psi^{\mathbb{C}}\rangle .\end{aligned}
```

The first line is Eq. ([35](global-complex.md#S5.E35)); the last follows from Eq. ([B1](proofs-and-compilation.md#A2.E66)) with $`A=\Pi_{\ell}`$. The measured eigenvalue is $`(-1)^{b_{p}}\mathbf{1}\!\left\{\widehat{\ell}=\ell\right\}`$, so multiplication by two proves Eqs. ([36](global-complex.md#S5.E36))– ([37](global-complex.md#S5.E37)).

The phase tangents also satisfy $`\mathrm{Re}\langle\partial_{\theta_{N+\ell}}\psi^{\mathbb{C}}\vert \partial_{\theta_{N+m}}\psi^{\mathbb{C}}\rangle=p_{\ell}\delta_{\ell m}`$, with $`p_{\ell}:=\vert x_{\ell}\vert ^{2}`$. Hence $`G_{\mathrm{ph}}^{\mathrm{sph}}=\mathrm{diag}(\boldsymbol{p})`$; subtracting the state-parallel part gives the unused projective block $`G_{\mathrm{ph}}^{\mathrm{FS}}=\mathrm{diag}(\boldsymbol{p})-\boldsymbol{p}\boldsymbol{p}^{\mathsf{T}}`$.

For the integrated four-qubit $`R_{\mathbb{C}}`$ compiler in Appendix [A 6 a](four-qubit-example.md#A1.SS6.SSS1), let $`D_{\widehat{\phi}}:=\sum_{\ell=0}^{15}e^{\mathrm{i}\widehat{\phi}_{\ell}}\lvert b_{\ell}\rangle \!\langle b_{\ell}\rvert`$. Suppose the two child-anchor columns have already expanded to

<a id="A2.EGx37"></a>

```math
\begin{aligned}\lvert \widetilde{\sigma}_{2j}\rangle & =e^{-\mathrm{i}\Phi_{2j}}D_{\widehat{\phi}}\lvert \sigma_{2j}\rangle ,\end{aligned}
```

```math
\begin{aligned}\lvert \widetilde{\sigma}_{2j+1}\rangle & =e^{-\mathrm{i}\Phi_{2j+1}}D_{\widehat{\phi}}\lvert \sigma_{2j+1}\rangle .\end{aligned}
```

At a leaf, $`\lvert b_{\ell}\rangle =e^{-\mathrm{i}\Phi_{16+\ell}}D_{\widehat{\phi}}\lvert b_{\ell}\rangle`$, so the induction begins. The first and second columns of the addressed gate in Eq. ([A4](four-qubit-example.md#A1.E62)) produce, respectively,

<a id="A2.EGx38"></a>

```math
\begin{aligned}e^{-\mathrm{i}\Phi_{2j+1}}\cos\theta_{j}\lvert \widetilde{\sigma}_{2j}\rangle +e^{-\mathrm{i}\Phi_{2j}}\sin\theta_{j}\lvert \widetilde{\sigma}_{2j+1}\rangle & =e^{-\mathrm{i}\Phi_{j}}D_{\widehat{\phi}}\lvert \sigma_{j}\rangle ,\end{aligned}
```

```math
\begin{aligned}-e^{\mathrm{i}\Phi_{2j}}\sin\theta_{j}\lvert \widetilde{\sigma}_{2j}\rangle +e^{\mathrm{i}\Phi_{2j+1}}\cos\theta_{j}\lvert \widetilde{\sigma}_{2j+1}\rangle & =D_{\widehat{\phi}}\lvert e_{j}^{\mathbb{R}}\rangle .\end{aligned}
```

At the root, $`\Phi_{1}=0`$. The state column and all fifteen marker columns are therefore those of $`D_{\widehat{\phi}}W_{\mathbb{R}}`$. These are all sixteen columns, so

<a id="A2.Ex136"></a>

```math
\widetilde{W}_{\mathbb{C}}^{(R_{\mathbb{C}})}=D_{\widehat{\phi}}W_{\mathbb{R}}=e^{-\mathrm{i}\bar{\phi}}D_{\mathrm{ph}}W_{\mathbb{R}}=e^{-\mathrm{i}\bar{\phi}}W_{\mathbb{C}},
```

proving Eq. ([A5](four-qubit-example.md#A1.E63)). The common phase on the complete decoded state leaves measurement probabilities unchanged.

<a id="A2.SS7"></a>

## B 7 Checkpoint transport and active-interface substitution

The generators within one depth commute because their prefix projectors are orthogonal. For $`j=2^{d}+r`$, using $`U_{\mathrm{chk}}=B_{d}A_{d}`$ gives

<a id="A2.EGx39"></a>

```math
\begin{aligned}\partial_{\theta_{j}}U_{d} & =-\mathrm{i}Q_{d,r}U_{d},\end{aligned}
```

```math
\begin{aligned}\partial_{\theta_{j}}\lvert \psi^{\mathbb{R}}\rangle & =-\mathrm{i}B_{d}Q_{d,r}\lvert \alpha_{d}\rangle ,\end{aligned}
```

```math
\begin{aligned}\partial_{\theta_{j}}E_{O} & =2\mathrm{Im}\langle \beta_{d}^{\mathbb{R}}\rvert Q_{d,r}\lvert \alpha_{d}\rangle ,\qquad\lvert \beta_{d}^{\mathbb{R}}\rangle :=B_{d}^{\dagger}O\lvert \psi^{\mathbb{R}}\rangle .\end{aligned}
```

The last line is Eq. ([40](checkpoints.md#S6.E40)). For the state in Eq. ([41](checkpoints.md#S6.E41)), Eq. ([B1](proofs-and-compilation.md#A2.E66)) gives

<a id="A2.EGx40"></a>

```math
\begin{aligned}\langle \Omega_{d}^{\mathbb{R}}\rvert Y_{a}\otimes Q_{d,r}\lvert \Omega_{d}^{\mathbb{R}}\rangle & =-\mathrm{Im}\langle \beta_{d}^{\mathbb{R}}\rvert Q_{d,r}\lvert \alpha_{d}\rangle ,\end{aligned}
```

```math
\begin{aligned}\mathbb{E}\!\left[(-1)^{b_{c}+b_{t}}\mathbf{1}\!\left\{\widehat{r}=r\right\}\right] & =\langle \Omega_{d}^{\mathbb{R}}\rvert Y_{a}\otimes Q_{d,r}\lvert \Omega_{d}^{\mathbb{R}}\rangle .\end{aligned}
```

Measuring the prefix in $`Z`$ realizes $`\lvert r\rangle \!\langle r\rvert`$, measuring the target in $`Y`$ realizes the Pauli $`Y`$, and the lower suffix may be discarded because $`Q_{d,r}`$ acts there as the identity. Multiplication by $`-2`$ proves Eqs. ([42](checkpoints.md#S6.E42)) and ([45](checkpoints.md#S6.E45)). Exactly one prefix is observed, so Eq. ([46](checkpoints.md#S6.E46)) follows.

Equation ([B4](proofs-and-compilation.md#A2.E69)) shows that $`\lvert \alpha_{d}\rangle`$ has a zero lower suffix. Since $`Q_{d,r}`$ acts there as the identity, both $`\lvert \alpha_{d}\rangle`$ and $`Q_{d,r}\lvert \alpha_{d}\rangle`$ are fixed by the active-interface projector $`P_{d}`$. For the complex state, differentiation and the interface contract give

<a id="A2.EGx41"></a>

<a id="A2.E70"></a>

```math
{\begin{aligned}\partial_{\theta_{j}}\lvert \psi^{\mathbb{C}}\rangle & =-\mathrm{i}D_{\mathrm{ph}}B_{d}Q_{d,r}\lvert \alpha_{d}\rangle =-\mathrm{i}B_{d,\mathbb{C}}Q_{d,r}\lvert \alpha_{d}\rangle ,\end{aligned}}\tag{B5}
```

```math
\begin{aligned}\lvert \psi^{\mathbb{C}}\rangle & =D_{\mathrm{ph}}B_{d}\lvert \alpha_{d}\rangle =B_{d,\mathbb{C}}\lvert \alpha_{d}\rangle .\end{aligned}
```

Thus the reference branch decodes to $`\lvert \alpha_{d}\rangle`$. With $`\lvert \beta_{d}^{\mathbb{C}}\rangle =B_{d,\mathbb{C}}^{\dagger}O\lvert \psi^{\mathbb{C}}\rangle`$, the same derivation applies, and its correlators depend only on $`B_{d,\mathbb{C}}P_{d}`$. The separated choice $`B_{d,\mathbb{C}}=D_{\mathrm{ph}}B_{d}`$ gives Eq. ([44](checkpoints.md#S6.E44)). The explicit four-qubit first-column calculation in Appendix [A 8 a](four-qubit-example.md#A1.SS8.SSS1) proves Eq. ([A6](four-qubit-example.md#A1.E64)); substituting it into Eq. ([B5](proofs-and-compilation.md#A2.E70)) gives Eq. ([A7](four-qubit-example.md#A1.E65)). Generators within one depth commute, while different depths retain their physical circuit order.

<a id="A2.SS8"></a>

## B 8 Fixed-norm concentration and complete-chart allocations

Let $`\widehat{\mu}=S^{-1}\sum_{t}Z_{t}`$ and $`\mu=\mathbb{E}Z_{t}`$. Using $`\|v\|_{\infty}\leq\|v\|_{2}`$, Jensen’s inequality, and independence gives

<a id="A2.EGx42"></a>

```math
\begin{aligned}\mathbb{E}\|Z_{1}-\mu\|_{2}^{2} & =\mathbb{E}\|Z_{1}\|_{2}^{2}-\|\mu\|_{2}^{2}\leq B^{2},\end{aligned}
```

```math
\begin{aligned}\mathbb{E}\|\widehat{\mu}-\mu\|_{\infty} & \leq\sqrt{\mathbb{E}\|\widehat{\mu}-\mu\|_{2}^{2}}\leq\frac{B}{\sqrt{S}}.\end{aligned}
```

<a id="A2.SS8.p1.2"></a>

Replacing one sample changes $`\|\widehat{\mu}-\mu\|_{\infty}`$ by at most $`2B/S`$. McDiarmid’s inequality [[45](../references/paper-bibliography.md#bib.bib8)] therefore gives

<a id="A2.Ex145"></a>

```math
\mathbb{P}\!\left[\|\widehat{\mu}-\mu\|_{\infty}-\mathbb{E}\|\widehat{\mu}-\mu\|_{\infty}\gt u\right]\leq\exp\!\left(-\frac{Su^{2}}{2B^{2}}\right).
```

Setting $`u=B\sqrt{2\log(1/\eta)/S}`$ proves Eq. ([48](accuracy-resources.md#S7.E48)).

Every magnitude-depth, checkpoint, and direct phase record has norm two, so $`S_{\star}(\eta)`$ controls the $`\ell_{\infty}`$ error of the entire record vector. At depth $`d`$ the vector has $`2^{d}`$ coordinates, but its norm remains two; therefore the block width does not enter the count and no coordinate-wise union bound is needed.

There are $`n`$ magnitude depths. Assigning failure probability $`\delta/n`$ to each real depth, or $`\delta/(2n)`$ to each complex magnitude depth while reserving $`\delta/2`$ for the direct phase family, gives

<a id="A2.Ex146"></a>

```math
S_{\star}(\delta/n),\ S_{\star}(\delta/(2n))=\mathcal{O}\!\left(\frac{1+\log(n/\delta)}{\varepsilon^{2}}\right),\qquad S_{\star}(\delta/2)=\mathcal{O}\!\left(\frac{1+\log(1/\delta)}{\varepsilon^{2}}\right).
```

At fixed $`\varepsilon`$ and $`\delta`$, one magnitude stream costs $`\mathcal{O}(\log n)`$ executions and the phase stream costs $`\mathcal{O}(1)`$. One global outcome supplies all $`n`$ magnitude-depth records; a complete checkpoint schedule uses $`n`$ depth-specific streams. Thus

<a id="A2.EGx43"></a>

```math
\begin{aligned}S_{\mathrm{glob}}^{\mathbb{K}} & =\mathcal{O}(\log n),\end{aligned}
```

```math
\begin{aligned}S_{\mathrm{chk}}^{\mathbb{K}} & =\mathcal{O}(n\log n),\end{aligned}
```

with the $`\mathcal{O}(1)`$ phase term included only in the complex chart. The union bound does not require the depth records decoded from one global outcome to be independent. These counts reproduce Eqs. ([50](accuracy-resources.md#S7.E50)) and ([51](accuracy-resources.md#S7.E51)).

**Complete-vector Euclidean accuracy.** Concatenate the $`n`$ magnitude-depth records from one global outcome as $`Z_{\mathrm{mag}}:=Z_{0}^{\mathrm{fr}}\oplus\cdots\oplus Z_{n-1}^{\mathrm{fr}}`$, and set $`\mu_{\mathrm{mag}}:=\mathbb{E}Z_{\mathrm{mag}}`$ and $`\widehat{\mu}_{\mathrm{mag}}:=S^{-1}\sum_{t=1}^{S}Z_{\mathrm{mag},t}`$. Since every block has norm two, $`\|Z_{\mathrm{mag}}\|_{2}=2\sqrt{n}`$. Applying the same bounded-difference argument directly to the Euclidean norm gives

<a id="A2.E71"></a>

```math
{\mathbb{P}\!\left[\left\|\widehat{\mu}_{\mathrm{mag}}-\mu_{\mathrm{mag}}\right\|_{2}\gt \frac{2\sqrt{n}\{1+\sqrt{2\log(1/\delta)}\}}{\sqrt{S}}\right]\leq\delta.}\tag{B6}
```

A sufficient allocation for fixed complete-magnitude $`\ell_{2}`$ accuracy $`\varepsilon_{2}`$ is

<a id="A2.Ex149"></a>

```math
S=\mathcal{O}\!\left(\frac{n\{1+\log(1/\delta)\}}{\varepsilon_{2}^{2}}\right)=\mathcal{O}\!\left(\frac{\log M\{1+\log(1/\delta)\}}{\varepsilon_{2}^{2}}\right).
```

For the complex chart, the separate norm-two phase stream adds only a constant-order term under any fixed split of Euclidean error and confidence.

**Relative, directional, and metric-conditioned accuracy.** Let $`\widehat{\boldsymbol{v}}=\boldsymbol{v}+\boldsymbol{e}`$, where $`\boldsymbol{v}`$ is the complete real gradient or complex magnitude block, $`\mathcal{G}:=\|\boldsymbol{v}\|_{2}`$, and $`\|\boldsymbol{e}\|_{2}\leq\xi\lt \mathcal{G}`$. Then

<a id="A2.Ex150"></a>

```math
\boldsymbol{v}^{\mathsf{T}}\widehat{\boldsymbol{v}}\geq\mathcal{G}(\mathcal{G}-\xi)\gt 0,\qquad\left\|\frac{\widehat{\boldsymbol{v}}}{\|\widehat{\boldsymbol{v}}\|_{2}}-\frac{\boldsymbol{v}}{\mathcal{G}}\right\|_{2}\leq\frac{2\xi}{\mathcal{G}}.
```

Thus $`-\widehat{\boldsymbol{v}}`$ is a strict descent direction. Setting $`\xi=\rho\mathcal{G}`$, $`0\lt \rho\lt 1`$, in Eq. ([B6](proofs-and-compilation.md#A2.E71)) gives, for either stated block,

<a id="A2.Ex151"></a>

```math
S_{\mathrm{rel}}=\left\lceil\frac{4n\{1+\sqrt{2\log(1/\delta)}\}^{2}}{\rho^{2}\mathcal{G}^{2}}\right\rceil.
```

A fixed magnitude/phase allocation preserves the $`n`$ dependence for the full complex gradient. No uniform relative guarantee holds when the reference norm vanishes, $`\mathcal{G}=0`$.

For the theorem-adjacent separation, fix a parameter point and an active real coordinate $`k`$. Construct $`O_{k}`$ at that point and hold it fixed during differentiation:

<a id="A2.Ex152"></a>

```math
O_{k}=I-(\lvert \psi^{\mathbb{R}}\rangle -\lvert e_{k}^{\mathbb{R}}\rangle )(\langle \psi^{\mathbb{R}}\rvert -\langle e_{k}^{\mathbb{R}}\rvert ).
```

Orthonormality gives $`O_{k}^{\dagger}=O_{k}`$, $`O_{k}^{2}=I`$, and $`O_{k}\lvert \psi^{\mathbb{R}}\rangle =\lvert e_{k}^{\mathbb{R}}\rangle`$, so $`\partial_{\theta_{j}}E_{O_{k}}=2\sqrt{g^{\mathbb{R}}_{k,k}}\delta_{jk}`$ and $`\chi_{k}=2`$. If $`0\lt g^{\mathbb{R}}_{k,k}\lt (\varepsilon/2)^{2}`$, the zero vector has raw $`\ell_{\infty}`$ error below $`\varepsilon`$ but frame error two.

For a global magnitude record with $`g^{\mathbb{K}}_{j,j}\gt 0`$, $`Z_{j}\in\{\pm 2\sqrt{g^{\mathbb{K}}_{j,j}}\}`$, $`\mathbb{E}Z_{j}=\partial_{\theta_{j}}E_{O}`$, and $`Z_{j}^{2}=4g^{\mathbb{K}}_{j,j}`$. Unitarity gives $`\vert \partial_{\theta_{j}}E_{O}\vert \leq 2\sqrt{g^{\mathbb{K}}_{j,j}}`$, while, for $`\tau\gt 0`$,

<a id="A2.Ex153"></a>

```math
\mathbb{E}\!\left[\left(\frac{Z_{j}}{g^{\mathbb{K}}_{j,j}}\right)^{2}\right]=\frac{4}{g^{\mathbb{K}}_{j,j}},\qquad\mathbb{E}\!\left[\left(\frac{Z_{j}}{g^{\mathbb{K}}_{j,j}+\tau}\right)^{2}\right]=\frac{4g^{\mathbb{K}}_{j,j}}{(g^{\mathbb{K}}_{j,j}+\tau)^{2}}\leq\frac{1}{\tau}.
```

Small metric weights therefore suppress ordinary noise but condition an unregularized natural gradient. Damping or freezing them is an optimizer choice; the ordinary record vanishes when $`g^{\mathbb{K}}_{j,j}=0`$.

Since $`n=\log_{2}(M+1)`$ in the real chart and $`n=\log_{2}(M+1)-1`$ in the complex chart, fixed absolute coordinate accuracy and confidence give $`S_{\mathrm{glob}}^{\mathbb{K}}=\mathcal{O}(\log\log M)`$ and $`S_{\mathrm{chk}}^{\mathbb{K}}=\mathcal{O}(\log M\log\log M)`$; per-execution Hopf work and the materialized $`M`$-entry output remain separate.

<a id="A2.SS9"></a>

## B 9 Assigned Hopf CNOT ledger and finite charges

Use the direct-angle count $`C_{\mathrm{H}}`$ of Sec. [VII C](accuracy-resources.md#S7.SS3); controlled-reflection, measurement, and classical costs remain separate. The controlled-rotation charge is

<a id="A2.Ex154"></a>

```math
c_{R_{y}}(m)=\begin{cases}0,&m=0,\\
2^{m+1}-2,&1\leq m\leq 4,\\
16(m+1)-40,&m\geq 5,\end{cases}
```

<a id="A2.SS9.p1.2"></a>

where the last line uses Ref. [[46](../references/paper-bibliography.md#bib.bib3)] and open controls use exact $`X`$ conjugations. Set

<a id="A2.EGx44"></a>

```math
\begin{aligned}C_{U} & :=C_{\mathrm{H}}(U_{\mathrm{chk}})=\sum_{d=0}^{n-1}2^{d}c_{R_{y}}(d),\end{aligned}
```

```math
\begin{aligned}C_{W} & :=C_{\mathrm{H}}(W_{\mathbb{R}})=(N-1)c_{R_{y}}(n-1),\end{aligned}
```

```math
\begin{aligned}C_{B_{d}} & :=C_{\mathrm{H}}(B_{d}^{\dagger})=\sum_{h=d+1}^{n-1}2^{h}c_{R_{y}}(h).\end{aligned}
```

The final depth contributes $`(N/2)c_{R_{y}}(n-1)`$ and every suffix is contained in $`U_{\mathrm{chk}}`$, so

<a id="A2.E72"></a>

```math
{C_{W}\leq 2\left(1-\frac{1}{N}\right)C_{U}\leq 2C_{U},\qquad C_{B_{d}}\leq C_{U},}\tag{B7}
```

with $`C_{U},C_{W}=\mathcal{O}(nN)`$ for $`n\geq 2`$. In the real chart set $`(c_{\mathrm{fwd}},c_{\mathrm{fr}},c_{d})=(C_{U},C_{W},C_{B_{d}})`$; in the separated complex chart add the common phase charge $`C_{D}:=C_{\mathrm{H}}(D_{\mathrm{ph}})`$ to all three. Equation ([B7](proofs-and-compilation.md#A2.E72)) then gives

<a id="A2.Ex158"></a>

```math
c_{\mathrm{fr}}^{\mathbb{K}}\leq 2c_{\mathrm{fwd}}^{\mathbb{K}},\qquad c_{d}^{\mathbb{K}}\leq c_{\mathrm{fwd}}^{\mathbb{K}},
```

which proves Eq. ([55](accuracy-resources.md#S7.E55)). Native-forward and integrated alternatives use the same functional but need not obey these finite constants; Appendix [A 9](four-qubit-example.md#A1.SS9) gives their explicit four-qubit charges.

<a id="A2.SS10"></a>

## B 10 Exact multiplexed recompilation

<a id="A2.SS10.p1.1"></a>

The direct-angle ledger keeps coordinates and physical controls in one geometry. One exact multiplexed realization preserves the estimator while recombining those angles and therefore has its own ledger. Each forward depth $`U_{d}=\sum_{r=0}^{2^{d}-1}\lvert r\rangle\langle r\rvert \otimes R_{y}(\theta_{2^{d}+r})\otimes I_{2^{n-d-1}}`$ is uniformly controlled. Fix the unpruned Gray-code templates, with $`2^{d}`$ core CNOTs for $`d\geq 1`$ and none at the root [[47](../references/paper-bibliography.md#bib.bib47)]. Their forward charge is

<a id="A2.Ex159"></a>

```math
C_{\mathrm{ucr}}(U_{\mathrm{chk}})=\sum_{d=1}^{n-1}2^{d}=N-2.
```

For an addressed depth $`d\lt n-1`$, write a basis label as prefix $`r`$, target bit $`q`$, and lower suffix $`z`$. A reusable clean flag computes $`F_{d}\lvert r,q,z\rangle \lvert 0\rangle _{f}=\lvert r,q,z\rangle \lvert [z=0]\rangle _{f}`$. Let $`V_{d,f}`$ apply the prefix-selected $`R_{y}(\theta_{2^{d}+r})`$ to the target when the flag is one and act as the identity when it is zero. This leaves the suffix unchanged, so $`F_{d}^{\dagger}V_{d,f}F_{d}`$ implements the addressed layer $`V_{d}`$ on a clean flag and returns the flag to zero. The final depth needs no flag. Composing the layers gives the full-frame contract

<a id="A2.E73"></a>

```math
{\widetilde{W}_{\mathbb{R}}(\lvert \varphi\rangle \lvert 0\rangle _{f})=(W_{\mathbb{R}}\lvert \varphi\rangle )\lvert 0\rangle _{f}\qquad\text{for every }\lvert \varphi\rangle .}\tag{B8}
```

The nonfinal multiplexors have $`d+1`$ controls, hence

<a id="A2.Ex160"></a>

```math
C_{\mathrm{ucr-core}}(W_{\mathbb{R}})\leq\sum_{d=0}^{n-2}2^{d+1}+2^{n-1}=\frac{3}{2}N-2.
```

<a id="A2.SS10.p2.3"></a>

Quadratic exact multi-controlled-$`X`$ synthesis contributes $`2\sum_{m=1}^{n-1}\mathcal{O}(m^{2})=\mathcal{O}(n^{3})`$ for computing and uncomputing the suffix predicates [[48](../references/paper-bibliography.md#bib.bib48)]. Thus $`C(W_{\mathbb{R}})=\mathcal{O}(N+n^{3})=\mathcal{O}(N)`$; exact diagonal synthesis also gives $`C(D_{\mathrm{ph}})=\mathcal{O}(N)`$ [[49](../references/paper-bibliography.md#bib.bib49)].

For these fixed templates and $`n\geq 2`$, a real scalar execution uses $`N-2`$ forward-core CNOTs and a global-record execution adds at most $`\frac{3}{2}N-2+\mathcal{O}(n^{3})`$ for the inverse frame. The matched per-execution ratio is bounded by

<a id="A2.Ex161"></a>

```math
1+\frac{\frac{3}{2}N-2+\mathcal{O}(n^{3})}{N-2}=\mathcal{O}(1).
```

Adding the same nonnegative controlled-reflection charge preserves this bound. In the separated complex construction, the same $`\mathcal{O}(N)`$ phase-layer charge is added to both the forward and reverse blocks, again giving a constant-order ratio. The global method therefore retains its $`\mathcal{O}(\log\log M)`$ statistical overhead under this one exact recompilation. The theorem continues to use the direct-angle ledger; no compiler-independent finite ratio is asserted.

<a id="A2.SS11"></a>

## B 11 Proof of the complete-gradient Hopf quantum-backpropagation theorem

<a id="A2.SS11.2"></a>

**Proof of Theorem [1](accuracy-resources.md#Thmtheorem1).**

Equations ([27](global-real.md#S4.E27)), ([38](global-complex.md#S5.E38)), and ([39](global-complex.md#S5.E39)) give unbiased global records for all real and complex coordinates, while Eq. ([45](checkpoints.md#S6.E45)) gives the complete block at each selected depth. Their norm-two bounds and the allocations in Eq. ([50](accuracy-resources.md#S7.E50)) yield the target $`(\varepsilon,\delta)`$ accuracy. Global outcomes are reused across all magnitude depths, whereas checkpoints use one stream per depth, giving Eq. ([51](accuracy-resources.md#S7.E51)).

The matched scalar and gradient programs share the direct-angle forward compiler and exact block formulas in Eqs. ([53](accuracy-resources.md#S7.E53)) and ([54](accuracy-resources.md#S7.E54)). Substituting Eq. ([55](accuracy-resources.md#S7.E55)) gives Eqs. ([56](accuracy-resources.md#S7.E56)) and ([57](accuracy-resources.md#S7.E57)); with $`c_{\mathrm{fwd}}^{\mathbb{K}}=\mathcal{O}(M\log M)`$, this gives Eq. ([58](accuracy-resources.md#S7.E58)).

Shared live workspace, ancilla-free sequential reverse blocks, and $`\mathcal{O}(M)`$ classical output give constant storage overhead. Using $`n=\log_{2}(M+1)`$ in the real chart and $`n=\log_{2}(M+1)-1`$ in the complex chart gives the stated $`\mathcal{O}(\log\log M)`$ global and $`\mathcal{O}(\log M\log\log M)`$ checkpoint classifications. ∎
