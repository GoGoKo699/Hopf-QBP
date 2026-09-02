# Gradient methods compared by task and access model

The methods below are not totally ordered. They return different objects, use
different objective interfaces, and prove guarantees in different norms or
optimizer models. A comparison based only on the number of circuit executions
would therefore be misleading.

## Common comparison axes

For every method, ask:

1. What is returned: one component, a complete materialized vector, a random
   direction, many expectation values, or an optimizer update?
2. What objective access is assumed: ordinary expectation evaluation,
   controlled reflection, coherent parameter registers, or shadow-compatible
   randomized measurements?
3. What structural property is used: generator spectrum, commutation,
   dynamical Lie algebra, locality, or an addressed differential frame?
4. What error norm and confidence are guaranteed?
5. Which resources are counted: executions, oracle calls, logical gates,
   ancillas, decoding, output, or optimizer iterations?

## Neutral comparison

| Method | Returned object | Access and structural premise | Reuse mechanism | Main comparison boundary |
|---|---|---|---|---|
| Parameter shift | One exact coordinate derivative; a complete vector by repetition | Ordinary shifted objective evaluations; the common two-eigenvalue rule uses two shifts per component | Usually coordinate-separated | Broad circuit applicability; complete-vector evaluations normally grow with the requested parameter count |
| Earlier indexed Hopf protocol | One selected raw Hopf derivative | Direct-angle Hopf state, tangent, and signed-branch preparations | Logarithmically many compiled access families, but the measured index selects one coordinate | The finite-shot complete-gradient cost was not shared |
| Hopf-QBP global | Complete raw Hopf-coordinate gradient | Calibrated controlled reflection and addressed Hopf differential frame | Every all-`X` outcome contributes to every magnitude coordinate; a second stream returns complex phases | Stronger objective access; output-sensitive in `M` |
| Hopf-QBP checkpoint | One selected depth block, or the complete vector through all depths | Same controlled reflection plus inverse suffix and active interface | One shared one-hot record within each selected depth | Reverse locality; a complete schedule uses one stream per depth |
| Structured-circuit backpropagation | Complete gradients and related differential quantities for eligible circuits | Commuting or otherwise structured parameterized circuits | Circuit-specific simultaneous measurement structure | Different ansatz class; efficiency follows its structural restrictions |
| Lie-algebraic gradient estimation | Complete gradient | Hadamard-test access, a polynomial-dimensional dynamical Lie algebra, and an observable-norm condition | Algebraic compression | Logarithmic shot dependence under its algebra and norm assumptions |
| Classical shadows | Many expectation values, not intrinsically a gradient | Randomized measurements and an observable-dependent shadow norm | One shadow predicts many target observables | A logarithm in the number of targets is meaningful only with the shadow-norm and measurement-ensemble factors |
| Quantum shadow gradient descent | Stochastic all-component optimizer update | Shadow-tomography adaptation and locality assumptions | One sample can update all components | Optimizer-level convergence task, not the same uniformly accurate materialized vector |
| Adaptive directional gradients | Unbiased stochastic gradient from random directional derivatives | Ordinary objective evaluations; no controlled-reflection requirement | Random directions interpolate between SPSA, coordinate descent, and full parameter shift | Parameter dependence moves into estimator variance and optimizer convergence |
| Generalized Hadamard-test methods | Selected derivatives and higher derivatives | Controlled generator or observable variants, depending on the construction | Circuit adaptation reduces some derivative-circuit costs | Not the same shared complete-vector output task |

## Hopf-QBP's specific regime

Hopf-QBP combines

```math
\text{addressed Hopf differential frame}
+
\text{controlled-reflection interference}
+
\text{fixed-norm correlated records}.
```

The global method requests a materialized raw coordinate-gradient vector and
proves simultaneous additive accuracy. Its defining feature is not merely a
Hadamard test or Walsh transform; it is that the Hopf frame gives every
magnitude direction a computational address, allowing one observed bit string
to contribute to every magnitude coordinate.

The checkpoint method asks a different architectural question: how far must the
reflected branch be reversed when only one tree depth is needed? It trades
cross-depth reuse for a shorter depth-specific reverse suffix.

## Access-model boundary

Hopf-QBP assumes a phase-calibrated controlled reflection. Parameter-shift and
directional methods generally use ordinary objective evaluations instead.
Classical-shadow methods use randomized measurement data and include a target-
observable-dependent statistical scale. These access models are not
interchangeable, so the repository does not claim universal dominance.

For a reflection-sum Hamiltonian

```math
H=\sum_\alpha c_\alpha O_\alpha,
\qquad
\Lambda=\sum_\alpha |c_\alpha|,
```

coefficient-one-norm term sampling gives an unbiased Hopf-QBP record with a
`Lambda**2` sufficient-shot penalty. See
[Observables and readout](OBSERVABLES_AND_READOUT.md).

## Output-norm boundary

The manuscript theorem controls the raw coordinate gradient. The same record
can be rescaled to normalized-frame or natural-gradient coordinates, but those
outputs have different norm and conditioning scales. See
[Statistical accuracy](STATISTICAL_ACCURACY.md) for the exact separation and
magnitude-block norm hierarchy.

## Primary references

- K. Mitarai et al., [Quantum circuit learning](https://arxiv.org/abs/1803.00745), *Physical Review A* **98**, 032309 (2018).
- M. Schuld et al., [Evaluating analytic gradients on quantum hardware](https://arxiv.org/abs/1811.11184), *Physical Review A* **99**, 032331 (2019).
- R. Lin and G. Li, [A Compass on the Quantum State Sphere](https://arxiv.org/abs/2607.14231) (2026).
- J. Bowles, D. Wierichs, and C.-Y. Park, [Backpropagation scaling in parameterised quantum circuits](https://arxiv.org/abs/2306.14962), *Quantum* **9**, 1873 (2025).
- M. Heidari, M. Mozakka, and W. Szpankowski, [Efficient gradient estimation with Lie algebraic symmetries](https://arxiv.org/abs/2404.05108) (2024, revised 2026).
- H.-Y. Huang, R. Kueng, and J. Preskill, [Predicting many properties of a quantum system from very few measurements](https://arxiv.org/abs/2002.08953), *Nature Physics* **16**, 1050 (2020).
- M. Heidari et al., [Quantum shadow gradient descent](https://arxiv.org/abs/2310.06935) (2023).
- B. Coyle et al., [Adaptive directional gradients for parameterised quantum circuits](https://arxiv.org/abs/2606.09734) (2026).
- D. Li et al., [Efficient quantum gradient and higher-order derivative estimation via generalized Hadamard test](https://arxiv.org/abs/2408.05406) (2024).
- K. Chinzei et al., [Expressibility and simultaneous gradient estimation](https://arxiv.org/abs/2406.18316), *npj Quantum Information* **11**, 79 (2025).
