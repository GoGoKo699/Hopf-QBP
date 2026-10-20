# Complete paper map

This index maps [2610.14177v1](https://arxiv.org/abs/2610.14177v1) to its complete Markdown account. Labels follow the printed paper; links retain stable source identifiers. The [reviewer route](README.md) connects the principal claims to proofs and executable checks. The same inventory is available as [structured data](paper-map.json).

| Item type | Count |
|---|---:|
| Section | 60 |
| Statement | 5 |
| Equation | 73 |
| Figure | 9 |
| Table | 3 |
| Protocol | 2 |
| Reference | 49 |

## Sections

| Paper item | Markdown location |
|---|---|
| Abstract | [README.md](../science/README.md#abstract) |
| I — Introduction | [motivation.md](../science/motivation.md#S1) |
| II — The two-qubit clue and the reverse task | [reverse-task.md](../science/reverse-task.md#S2) |
| II A — One split, three directions | [reverse-task.md](../science/reverse-task.md#S2.SS1) |
| II B — What a reusable reverse record must provide | [reverse-task.md](../science/reverse-task.md#S2.SS2) |
| II C — Objective access and output target | [reverse-task.md](../science/reverse-task.md#S2.SS3) |
| II D — Three circuit contracts | [reverse-task.md](../science/reverse-task.md#S2.SS4) |
| III — The balanced Hopf differential and forward interfaces | [balanced-differential.md](../science/balanced-differential.md#S3) |
| III A — Repeating the local split across the tree | [balanced-differential.md](../science/balanced-differential.md#S3.SS1) |
| III B — Subtree states, complements, and weights | [balanced-differential.md](../science/balanced-differential.md#S3.SS2) |
| III C — Depth-ordered completion and the state-column contract | [balanced-differential.md](../science/balanced-differential.md#S3.SS3) |
| IV — Global-frame method for the real Hopf chart | [global-real.md](../science/global-real.md#S4) |
| IV A — Construction of the addressed frame | [global-real.md](../science/global-real.md#S4.SS1) |
| IV B — Why the inverse frame is readable | [global-real.md](../science/global-real.md#S4.SS2) |
| IV C — Circuit template, outcomes, and decoder | [global-real.md](../science/global-real.md#S4.SS3) |
| IV D — Global real guarantee and cost at a glance | [global-real.md](../science/global-real.md#S4.SS4) |
| V — Global-frame method for the complex Hopf chart | [global-complex.md](../science/global-complex.md#S5) |
| V A — Complex chart and phase-dressed frame | [global-complex.md](../science/global-complex.md#S5.SS1) |
| V B — Complex magnitude circuit and parity reuse | [global-complex.md](../science/global-complex.md#S5.SS2) |
| V C — Direct phase circuit and signed leaf histogram | [global-complex.md](../science/global-complex.md#S5.SS3) |
| V D — Complex guarantee and cost at a glance | [global-complex.md](../science/global-complex.md#S5.SS4) |
| VI — Checkpoint method: layer-local reverse gradients | [checkpoints.md](../science/checkpoints.md#S6) |
| VI A — From a complete frame to one active depth | [checkpoints.md](../science/checkpoints.md#S6.SS1) |
| VI B — Real checkpoint template and decoder | [checkpoints.md](../science/checkpoints.md#S6.SS2) |
| VI C — Complex active-interface extension | [checkpoints.md](../science/checkpoints.md#S6.SS3) |
| VI D — Checkpoint guarantee and cost at a glance | [checkpoints.md](../science/checkpoints.md#S6.SS4) |
| VII — Backpropagation accuracy, resources, and protocol choice | [accuracy-resources.md](../science/accuracy-resources.md#S7) |
| VII A — Reverse pullback and shared records | [accuracy-resources.md](../science/accuracy-resources.md#S7.SS1) |
| VII B — Fixed-norm records and complete-chart accuracy | [accuracy-resources.md](../science/accuracy-resources.md#S7.SS2) |
| VII C — Assigned Hopf CNOT work | [accuracy-resources.md](../science/accuracy-resources.md#S7.SS3) |
| VII D — Choosing the reverse protocol | [accuracy-resources.md](../science/accuracy-resources.md#S7.SS4) |
| VIII — Conclusion | [conclusion.md](../science/conclusion.md#S8) |
| Data and code availability | [endmatter.md](../science/endmatter.md#Sx1) |
| Generative AI disclosure | [endmatter.md](../science/endmatter.md#Sx2) |
| References | [paper-bibliography.md](../references/paper-bibliography.md#bib) |
| A — Four-qubit implementation companion | [four-qubit-example.md](../science/four-qubit-example.md#A1) |
| A 1 — How to read the four-qubit construction | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS1) |
| A 2 — Native real and complex preparation | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS2) |
| A 3 — Metric factors and tangent-state registry | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS3) |
| A 4 — Depth completion $`U_{\mathrm{chk}}`$ | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS4) |
| A 5 — Real addressed frame $`W_{\mathbb{R}}`$ | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS5) |
| A 6 — Complex magnitude frame $`W_{\mathbb{C}}`$ | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS6) |
| A 6 a — Addressed $`R_{\mathbb{C}}`$ compilation up to a compiler global phase | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS6.SSS1) |
| A 7 — Global gradient records | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS7) |
| A 8 — Checkpoint records and complex suffix $`B_{2,\mathbb{C}}`$ | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS8) |
| A 8 a — Complex depth- $`2`$ active-interface construction | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS8.SSS1) |
| A 9 — Four-qubit assigned Hopf CNOT ledger | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS9) |
| B — Technical foundations, proofs, and compiler derivations | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2) |
| B 1 — Controlled-interference identities | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS1) |
| B 2 — Balanced Hopf differential frame | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS2) |
| B 3 — Depth completion and forward-state substitution | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS3) |
| B 4 — Addressed real-frame columns | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS4) |
| B 5 — Global real readout and Walsh decoding | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS5) |
| B 6 — Complex magnitude and direct phase identities | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS6) |
| B 7 — Checkpoint transport and active-interface substitution | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS7) |
| B 8 — Fixed-norm concentration and complete-chart allocations | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS8) |
| B 9 — Assigned Hopf CNOT ledger and finite charges | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS9) |
| B 10 — Exact multiplexed recompilation | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS10) |
| B 11 — Proof of the complete-gradient Hopf quantum-backpropagation theorem | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.SS11) |
| Acknowledgements | [endmatter.md](../science/endmatter.md#S8.acknowledgements1) |

## Statements

| Paper item | Markdown location |
|---|---|
| Assumption 1 (Phase-calibrated controlled reflection) . | [reverse-task.md](../science/reverse-task.md#Thmassumption1) |
| Definition 1 (Complete-gradient accuracy) . | [reverse-task.md](../science/reverse-task.md#Thmdefinition1) |
| Definition 2 (State-coordinate quantum backpropagation) . | [reverse-task.md](../science/reverse-task.md#Thmdefinition2) |
| Theorem 1 (Quantum backpropagation and checkpointed reverse gradients with the Hopf ansatz) . | [accuracy-resources.md](../science/accuracy-resources.md#Thmtheorem1) |
| Lemma 1 (Subtree frame) . | [proofs-and-compilation.md](../science/proofs-and-compilation.md#Thmlemma1) |

## Protocols

| Paper item | Markdown location |
|---|---|
| Protocol 1 | [global-complex.md](../science/global-complex.md#S5.SS3.p6.pic1) |
| Protocol 2 | [checkpoints.md](../science/checkpoints.md#S6.SS3.p4.pic1) |

## Equations

| Paper item | Markdown location |
|---|---|
| Equation (1) | [reverse-task.md](../science/reverse-task.md#S2.E1) |
| Equation (2) | [reverse-task.md](../science/reverse-task.md#S2.E2) |
| Equation (3) | [reverse-task.md](../science/reverse-task.md#S2.E3) |
| Equation (4) | [reverse-task.md](../science/reverse-task.md#S2.E4) |
| Equation (5) | [reverse-task.md](../science/reverse-task.md#S2.E5) |
| Equation (6) | [balanced-differential.md](../science/balanced-differential.md#S3.E6) |
| Equation (7) | [balanced-differential.md](../science/balanced-differential.md#S3.E7) |
| Equation (8) | [balanced-differential.md](../science/balanced-differential.md#S3.E8) |
| Equation (9) | [balanced-differential.md](../science/balanced-differential.md#S3.E9) |
| Equation (10) | [balanced-differential.md](../science/balanced-differential.md#S3.E10) |
| Equation (11) | [balanced-differential.md](../science/balanced-differential.md#S3.E11) |
| Equation (12) | [balanced-differential.md](../science/balanced-differential.md#S3.E12) |
| Equation (13) | [balanced-differential.md](../science/balanced-differential.md#S3.E13) |
| Equation (14) | [balanced-differential.md](../science/balanced-differential.md#S3.E14) |
| Equation (15) | [balanced-differential.md](../science/balanced-differential.md#S3.E15) |
| Equation (16) | [global-real.md](../science/global-real.md#S4.E16) |
| Equation (17) | [global-real.md](../science/global-real.md#S4.E17) |
| Equation (18) | [global-real.md](../science/global-real.md#S4.E18) |
| Equation (19) | [global-real.md](../science/global-real.md#S4.E19) |
| Equation (20) | [global-real.md](../science/global-real.md#S4.E20) |
| Equation (21) | [global-real.md](../science/global-real.md#S4.E21) |
| Equation (22) | [global-real.md](../science/global-real.md#S4.E22) |
| Equation (23) | [global-real.md](../science/global-real.md#S4.E23) |
| Equation (24) | [global-real.md](../science/global-real.md#S4.E24) |
| Equation (25) | [global-real.md](../science/global-real.md#S4.E25) |
| Equation (26) | [global-real.md](../science/global-real.md#S4.E26) |
| Equation (27) | [global-real.md](../science/global-real.md#S4.E27) |
| Equation (28) | [global-real.md](../science/global-real.md#S4.E28) |
| Equation (29) | [global-complex.md](../science/global-complex.md#S5.E29) |
| Equation (30) | [global-complex.md](../science/global-complex.md#S5.E30) |
| Equation (31) | [global-complex.md](../science/global-complex.md#S5.E31) |
| Equation (32) | [global-complex.md](../science/global-complex.md#S5.E32) |
| Equation (33) | [global-complex.md](../science/global-complex.md#S5.E33) |
| Equation (34) | [global-complex.md](../science/global-complex.md#S5.E34) |
| Equation (35) | [global-complex.md](../science/global-complex.md#S5.E35) |
| Equation (36) | [global-complex.md](../science/global-complex.md#S5.E36) |
| Equation (37) | [global-complex.md](../science/global-complex.md#S5.E37) |
| Equation (38) | [global-complex.md](../science/global-complex.md#S5.E38) |
| Equation (39) | [global-complex.md](../science/global-complex.md#S5.E39) |
| Equation (40) | [checkpoints.md](../science/checkpoints.md#S6.E40) |
| Equation (41) | [checkpoints.md](../science/checkpoints.md#S6.E41) |
| Equation (42) | [checkpoints.md](../science/checkpoints.md#S6.E42) |
| Equation (43) | [checkpoints.md](../science/checkpoints.md#S6.E43) |
| Equation (44) | [checkpoints.md](../science/checkpoints.md#S6.E44) |
| Equation (45) | [checkpoints.md](../science/checkpoints.md#S6.E45) |
| Equation (46) | [checkpoints.md](../science/checkpoints.md#S6.E46) |
| Equation (47) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E47) |
| Equation (48) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E48) |
| Equation (49) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E49) |
| Equation (50) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E50) |
| Equation (51) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E51) |
| Equation (52) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E52) |
| Equation (53) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E53) |
| Equation (54) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E54) |
| Equation (55) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E55) |
| Equation (56) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E56) |
| Equation (57) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E57) |
| Equation (58) | [accuracy-resources.md](../science/accuracy-resources.md#S7.E58) |
| Equation (A1) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E59) |
| Equation (A2) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E60) |
| Equation (A3) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E61) |
| Equation (A4) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E62) |
| Equation (A5) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E63) |
| Equation (A6) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E64) |
| Equation (A7) | [four-qubit-example.md](../science/four-qubit-example.md#A1.E65) |
| Equation (B1) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E66) |
| Equation (B2) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E67) |
| Equation (B3) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E68) |
| Equation (B4) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E69) |
| Equation (B5) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E70) |
| Equation (B6) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E71) |
| Equation (B7) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E72) |
| Equation (B8) | [proofs-and-compilation.md](../science/proofs-and-compilation.md#A2.E73) |

## Figures

| Paper item | Markdown location |
|---|---|
| Figure 1 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS2.fig1) |
| Figure 2 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS2.fig2) |
| Figure 3 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS4.fig1) |
| Figure 4 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS5.fig1) |
| Figure 5 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS7.fig1) |
| Figure 6 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS7.fig2) |
| Figure 7 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS7.fig3) |
| Figure 8 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS8.fig2) |
| Figure 9 | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS8.SSS1.fig1) |

## Tables

| Paper item | Markdown location |
|---|---|
| Table I | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS3.fig1) |
| Table II | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS8.fig1) |
| Table III | [four-qubit-example.md](../science/four-qubit-example.md#A1.SS9.fig1) |

## References

| Paper item | Markdown location |
|---|---|
| Reference [1] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib6) |
| Reference [2] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib23) |
| Reference [3] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib1) |
| Reference [4] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib7) |
| Reference [5] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib43) |
| Reference [6] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib9) |
| Reference [7] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib10) |
| Reference [8] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib11) |
| Reference [9] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib44) |
| Reference [10] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib12) |
| Reference [11] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib17) |
| Reference [12] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib13) |
| Reference [13] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib45) |
| Reference [14] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib14) |
| Reference [15] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib15) |
| Reference [16] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib18) |
| Reference [17] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib20) |
| Reference [18] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib46) |
| Reference [19] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib19) |
| Reference [20] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib38) |
| Reference [21] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib39) |
| Reference [22] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib41) |
| Reference [23] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib40) |
| Reference [24] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib31) |
| Reference [25] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib33) |
| Reference [26] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib34) |
| Reference [27] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib26) |
| Reference [28] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib27) |
| Reference [29] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib28) |
| Reference [30] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib24) |
| Reference [31] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib30) |
| Reference [32] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib25) |
| Reference [33] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib32) |
| Reference [34] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib29) |
| Reference [35] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib35) |
| Reference [36] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib36) |
| Reference [37] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib37) |
| Reference [38] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib42) |
| Reference [39] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib2) |
| Reference [40] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib5) |
| Reference [41] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib4) |
| Reference [42] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib22) |
| Reference [43] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib21) |
| Reference [44] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib16) |
| Reference [45] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib8) |
| Reference [46] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib3) |
| Reference [47] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib47) |
| Reference [48] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib48) |
| Reference [49] | [paper-bibliography.md](../references/paper-bibliography.md#bib.bib49) |
