[Scientific text](README.md) · [Reviewer route](../review/README.md) · [Repository](../README.md)

<a id="S3"></a>

# III The balanced Hopf differential and forward interfaces

<a id="S3.SS1"></a>

## III A Repeating the local split across the tree

Applying the local split-and-complement rule at every internal node produces a full differential frame and one computational marker per node. Let $`n`$ be the number of qubits and $`N=2^{n}`$. For $`0\leq\ell<N`$, the basis labels are

<a id="S3.Ex19"></a>

```math
\ell=(q_{n}\cdots q_{1})_{2},\qquad\lvert b_{\ell}\rangle =\lvert q_{n}\cdots q_{1}\rangle .
```

A complete rooted binary tree has root $`1`$, children $`2j`$ and $`2j+1`$, internal nodes $`1\leq j<N`$, and leaves $`N+\ell`$. Internal nodes are indexed breadth first. The internal nodes at depth $`d`$ form

<a id="S3.Ex20"></a>

```math
\mathcal{L}_{d}:=\{2^{d},\ldots,2^{d+1}-1\},\qquad 0\leq d<n.
```

Writing $`j=2^{d}+r\in\mathcal{L}_{d}`$, attach to that node the computational marker

<a id="S3.Ex21"></a>

```math
\lambda(j):=(2r+1)2^{n-d-1}.
```

This is the leftmost leaf of the right child and will address the local complement created at node $`j`$.

To separate the coordinate blocks when needed, write

<a id="S3.E6"></a>

```math
\boldsymbol{\theta}_{\mathrm{mag}}:=(\theta_{1},\ldots,\theta_{N-1}),\qquad\boldsymbol{\theta}_{\mathrm{ph}}:=(\theta_{N},\ldots,\theta_{2N-1}).\tag{6}
```

The real chart uses $`\boldsymbol{\theta}=\boldsymbol{\theta}_{\mathrm{mag}}`$, while the complex chart uses $`\boldsymbol{\theta}=(\boldsymbol{\theta}_{\mathrm{mag}},\boldsymbol{\theta}_{\mathrm{ph}})`$.

The real magnitude angles have ranges

<a id="S3.EGx7"></a>

```math
\begin{aligned}\theta_{j} & \in[0,\pi/2], & 1\leq j<N/2,\end{aligned}
```

```math
\begin{aligned}\theta_{j} & \in[0,2\pi), & N/2\leq j<N.\end{aligned}
```

The final layer carries arbitrary real signs. The inherited rotation convention is

<a id="S3.E7"></a>

```math
R_{y}(\theta)=e^{-\mathrm{i}\theta Y}=\begin{pmatrix}\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta\end{pmatrix}.\tag{7}
```

The native real state-preparation circuit is denoted $`\mathrm{HopfReal}(\boldsymbol{\theta}_{\mathrm{mag}})`$.

<a id="S3.SS2"></a>

## III B Subtree states, complements, and weights

For $`0\leq\ell<N`$, set the leaf states to

<a id="S3.Ex24"></a>

```math
\lvert \sigma_{N+\ell}\rangle :=\lvert b_{\ell}\rangle .
```

Every internal node repeats the two-qubit split,

<a id="S3.Ex25"></a>

```math
\lvert \sigma_{j}\rangle =\cos\theta_{j}\lvert \sigma_{2j}\rangle +\sin\theta_{j}\lvert \sigma_{2j+1}\rangle ,
```

and the full real state is $`\lvert \psi^{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle :=\lvert \sigma_{1}\rangle`$. Within a construction at a fixed parameter point, the common argument $`\boldsymbol{\theta}_{\mathrm{mag}}`$ is suppressed.

The coefficient multiplying a subtree before its own split is the amplitude arriving at that node. Along the path from the root to an internal node, each left edge contributes a cosine and each right edge a sine. All such ancestor angles lie above the final sign-carrying layer and belong to $`[0,\pi/2]`$, so the incoming amplitude is nonnegative. Its square is denoted by $`g^{\mathbb{R}}_{j,j}`$. These quantities will also be the diagonal metric factors, and they obey

<a id="S3.EGx8"></a>

```math
\begin{aligned}g^{\mathbb{R}}_{1,1} & =1,\end{aligned}
```

```math
\begin{aligned}g^{\mathbb{R}}_{2j,2j} & =g^{\mathbb{R}}_{j,j}\cos^{2}\theta_{j},\end{aligned}
```

<a id="S3.E8"></a>

```math
\begin{aligned}g^{\mathbb{R}}_{2j+1,2j+1} & =g^{\mathbb{R}}_{j,j}\sin^{2}\theta_{j},\end{aligned}\tag{8}
```

for internal children. Thus $`\sqrt{g^{\mathbb{R}}_{j,j}(\boldsymbol{\theta}_{\mathrm{mag}})}`$ is the incoming amplitude at node $`j`$.

The normalized direction orthogonal to the split state at node $`j`$ is its local complement,

<a id="S3.E9"></a>

```math
\lvert e_{j}^{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle =-\sin\theta_{j}\lvert \sigma_{2j}\rangle +\cos\theta_{j}\lvert \sigma_{2j+1}\rangle .\tag{9}
```

The child-subtree states are orthonormal, so $`\lvert e_{j}^{\mathbb{R}}\rangle`$ is normalized and orthogonal to $`\lvert \sigma_{j}\rangle`$. Complements in disjoint subtrees have disjoint support. A descendant complement is also orthogonal to the descendant subtree state appearing in every ancestor combination. These support relations allow all local complements to coexist in one orthonormal basis.

The next result identifies the moving frame used by the reverse construction. It is the orthonormal basis whose first column is the state and whose remaining columns are the normalized coordinate directions, with completion columns at zero-weight coordinates.

**Balanced Hopf differential guarantee.** The set

<a id="S3.E10"></a>

```math
\left\{\lvert \psi^{\mathbb{R}}\rangle ,\lvert e_{1}^{\mathbb{R}}\rangle ,\ldots,\lvert e_{N-1}^{\mathbb{R}}\rangle \right\}\tag{10}
```

is an orthonormal basis. The incoming amplitude at node $`j`$ is also the coefficient of its coordinate derivative:

<a id="S3.E11"></a>

```math
\partial_{\theta_{j}}\lvert \psi^{\mathbb{R}}(\boldsymbol{\theta}_{\mathrm{mag}})\rangle =\sqrt{g^{\mathbb{R}}_{j,j}(\boldsymbol{\theta}_{\mathrm{mag}})}\lvert e_{j}^{\mathbb{R}}\rangle .\tag{11}
```

Consequently,

<a id="S3.E12"></a>

```math
\operatorname{Re}\langle \partial_{\theta_{i}}\psi^{\mathbb{R}}\vert \partial_{\theta_{j}}\psi^{\mathbb{R}}\rangle =\delta_{ij}g^{\mathbb{R}}_{j,j},\tag{12}
```

so the squared incoming amplitudes are precisely the diagonal metric coefficients.

<a id="S3.SS2.p6.1"></a>

For $`g^{\mathbb{R}}_{j,j}>0`$, $`\lvert e_{j}^{\mathbb{R}}\rangle`$ is the normalized coordinate tangent of Ref. [[1](../references/paper-bibliography.md#bib.bib6)]. When $`g^{\mathbb{R}}_{j,j}=0`$, the coordinate derivative vanishes and Eq. ([9](balanced-differential.md#S3.E9)) supplies the normalized completion column. For the objective in Eq. ([1](reverse-task.md#S2.E1)),

<a id="S3.E13"></a>

```math
\partial_{\theta_{j}}E_{O}=2\sqrt{g^{\mathbb{R}}_{j,j}(\boldsymbol{\theta}_{\mathrm{mag}})}\operatorname{Re}\langle e_{j}^{\mathbb{R}}\rvert O\lvert \psi^{\mathbb{R}}\rangle .\tag{13}
```

Appendix [B 2](proofs-and-compilation.md#A2.SS2) proves the orthonormality, derivative, metric, and zero-weight statements. Appendix [A 3](four-qubit-example.md#A1.SS3) gives the four-qubit metric factors together with representative tangent-state formulas.

Each coordinate differential is a known weight times one moving-frame column. The reverse construction must make those columns accessible without preparing them separately. A depth-ordered forward completion first fixes the layer interfaces and the matched scalar baseline. The addressed frame then assigns a computational label to every normalized magnitude direction.

<a id="S3.SS3"></a>

## III C Depth-ordered completion and the state-column contract

A depth-ordered forward completion serves two later roles: it defines the designated scalar baseline and exposes the layer interfaces used by the checkpoint method. For $`j=2^{d}+r\in\mathcal{L}_{d}`$, define

<a id="S3.EGx9"></a>

```math
\begin{aligned}Q_{d,r} & :=\lvert r\rangle \!\langle r\rvert _{q_{n}\cdots q_{n-d+1}}\otimes Y_{q_{n-d}}\otimes I,\end{aligned}
```

```math
\begin{aligned}U_{d} & :=\prod_{r=0}^{2^{d}-1}\exp\!\left(-\mathrm{i}\theta_{2^{d}+r}Q_{d,r}\right),\end{aligned}
```

```math
\begin{aligned}U_{\mathrm{chk}}(\boldsymbol{\theta}_{\mathrm{mag}}) & :=U_{n-1}\cdots U_{1}U_{0}.\end{aligned}
```

The prefix projector is absent at $`d=0`$. Within one depth, the generators commute because their prefix projectors are orthogonal.

The depth completion and the native real circuit prepare the same initialized state:

<a id="S3.E14"></a>

```math
\mathrm{HopfReal}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert 0\rangle ^{\otimes n}=U_{\mathrm{chk}}(\boldsymbol{\theta}_{\mathrm{mag}})\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{R}}\rangle .\tag{14}
```

For correctness substitutions, write $`U_{\mathrm{fwd}}^{\mathbb{R}}`$ for any exact real preparation satisfying

<a id="S3.E15"></a>

```math
U_{\mathrm{fwd}}^{\mathbb{R}}\lvert 0\rangle ^{\otimes n}=\lvert \psi^{\mathbb{R}}\rangle .\tag{15}
```

This is the real instance of the state-column principle in Sec. [II D](reverse-task.md#S2.SS4). Native preparation may therefore be used in the record circuits, while $`U_{\mathrm{chk}}`$ supplies the checkpoint factorization and is the designated forward in the assigned Hopf CNOT ledger for the separated schedule. Both are direct-angle Hopf realizations: every $`\theta_{j}`$ remains the physical angle of its designated tree split. A further state-equivalent replacement preserves the record distributions but is assessed with its own compiler ledger. Appendix [B 3](proofs-and-compilation.md#A2.SS3) proves the common state column and the invariance of later measurements under its replacement; Appendix [A 4](four-qubit-example.md#A1.SS4) displays the corresponding four-qubit depth circuit.

The remaining ingredient for the global method is a computationally addressed frame. Its inverse makes one reflected record readable across every magnitude depth.
