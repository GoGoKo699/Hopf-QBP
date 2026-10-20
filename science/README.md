# Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz

Ruge Lin  ([ORCID](https://orcid.org/0000-0002-9297-7622))

Corresponding author: [gogoko699@gmail.com](mailto:gogoko699@gmail.com)

Affiliation: Thrust of Artificial Intelligence, Information Hub, The Hong Kong University of Science and Technology (Guangzhou), Guangzhou 511453, China

Ranyiliu Chen  ([ORCID](https://orcid.org/0000-0001-6060-6192))

Affiliation: Quantum Science Center of Guangdong-Hong Kong-Macao Greater Bay Area, Shenzhen 518045, China

<a id="abstract1"></a>

## Abstract

A variational quantum state may have many control angles, and its complete gradient contains one derivative for each. The task is to turn access to selected derivatives into a shared finite-shot record for the complete vector. The Hopf ansatz supplies the setting: it constructs any normalized pure state from nested two-way magnitude splits and, for complex states, leaf phases, with one directly programmed angle per split or phase. Earlier Hopf constructions prepare the state, recover coordinates from known amplitudes, and provide indexed derivative access. With a phase-calibrated controlled reflection, the inverse Hopf frame maps each normalized magnitude direction to a computational label, so every all-$`X`$ outcome contributes to every magnitude derivative. A separate signed leaf record supplies the complex phase block. A checkpoint variant reverses only the suffix below a selected depth and returns that layer’s gradient block. For a complete chart with $`M`$ real-valued parameters, sufficient execution counts are $`\mathcal{O}(\log\log M)`$ for the global method and $`\mathcal{O}(\log M\log\log M)`$ for the complete checkpoint schedule at fixed additive coordinate accuracy and confidence. The global saving is record reuse, not a reduction of the $`M`$-entry output. Under the designated direct-angle schedules, the global method’s assigned Hopf CNOT work and input/output-inclusive storage have at most logarithmic overhead relative to a matched scalar evaluation. The same Hopf geometry thus carries a state forward and the objective’s complete coordinate response backward.

## Read the paper

This is the complete Markdown text of [arXiv:2610.14177](https://arxiv.org/abs/2610.14177), [version 1](https://arxiv.org/abs/2610.14177v1). Numbering follows the paper PDF.

[Reviewer route](../review/README.md) · [Learning route](../learning/MILESTONES.md) · [Repository](../README.md)

| Paper part | Read |
| --- | --- |
| I Introduction | [motivation.md](motivation.md#S1) |
| II The two-qubit clue and the reverse task | [reverse-task.md](reverse-task.md#S2) |
| III The balanced Hopf differential and forward interfaces | [balanced-differential.md](balanced-differential.md#S3) |
| IV Global-frame method for the real Hopf chart | [global-real.md](global-real.md#S4) |
| V Global-frame method for the complex Hopf chart | [global-complex.md](global-complex.md#S5) |
| VI Checkpoint method: layer-local reverse gradients | [checkpoints.md](checkpoints.md#S6) |
| VII Backpropagation accuracy, resources, and protocol choice | [accuracy-resources.md](accuracy-resources.md#S7) |
| VIII Conclusion | [conclusion.md](conclusion.md#S8) |
| Acknowledgements. | [endmatter.md](endmatter.md#S8.acknowledgements1) |
| Data and code availability | [endmatter.md](endmatter.md#Sx1) |
| Generative AI disclosure | [endmatter.md](endmatter.md#Sx2) |
| References | [paper-bibliography.md](../references/paper-bibliography.md#bib) |
| Appendix A Four-qubit implementation companion | [four-qubit-example.md](four-qubit-example.md#A1) |
| Appendix B Technical foundations, proofs, and compiler derivations | [proofs-and-compilation.md](proofs-and-compilation.md#A2) |
