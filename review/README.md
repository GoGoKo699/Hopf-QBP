# Reviewer route

This route connects **Compass in the Mirror: Quantum Backpropagation with the
Hopf Ansatz**, [arXiv:2610.14177v1](https://arxiv.org/abs/2610.14177v1), to the
complete [scientific account](../science/README.md), reference implementation,
and executable checks. The [complete paper map](PAPER_MAP.md) resolves every
original section, equation, statement, protocol, figure, table and reference
identifier to its Markdown home. Use [verification and reproduction](../verification/README.md)
for environments, exact commands, outputs and tolerances.

## A direct path through the argument

1. Fix the [objective access, output target and substitution contracts](../science/reverse-task.md).
   Assumption 1 is phase-calibrated controlled-reflection access; Definition 1
   asks for simultaneous additive raw-coordinate accuracy. State-column,
   full-unitary and active-interface equality have different uses.
2. Read the [balanced differential](../science/balanced-differential.md), then
   the [real global frame](../science/global-real.md). Follow the column
   construction to all-`X` parity reuse and Walsh decoding.
3. Inspect the [complex magnitude and direct phase records](../science/global-complex.md)
   and the [checkpoint construction](../science/checkpoints.md), keeping the
   two complex streams and selected-depth scheduling explicit.
4. Check [Theorem 1 and the complete resource account](../science/accuracy-resources.md#Thmtheorem1).
   Its record norms, concentration, fixed-accuracy execution count, Hopf work,
   classical decoding, and materialized output are separate quantities.
5. Follow the proof map below and the [four-qubit implementation](../science/four-qubit-example.md).
   Run the analytic suite, then the full circuit suite. Check the exact finite
   ledger before comparing asymptotic resource models.

## Audit summary

The table gives each principal result one route from statement to proof and
implementation. Test filenames are under `qbp_validation/tests/`; implementation
modules are under `qbp_validation/` unless a root-level script is named.

| Result and paper statement | Complete proof or construction | Implementation / check | Scope of the evidence |
|---|---|---|---|
| Objective access and complete-gradient task, Assumption 1 and Definitions 1–2 | [Access and output](../science/reverse-task.md#Thmassumption1); [controlled interference](../science/proofs-and-compilation.md#A2.SS1) | `conventions.py`, `circuits.py`; `test_circuit_conventions.py` | The objective is a known Hermitian unitary with phase-calibrated controlled access. The requested output is the complete raw-coordinate vector with simultaneous additive accuracy. |
| Native preparation and three substitution contracts, Section II D | [Contracts](../science/reverse-task.md#S2.SS4); [forward substitution](../science/proofs-and-compilation.md#A2.SS3) and [active-interface substitution](../science/proofs-and-compilation.md#A2.SS7) | `native_schedule.py`, `reference.py`, `circuits.py`; `test_native_schedule.py`, `test_operator_contracts.py`, `test_conventions.py` | State-column, full-unitary and active-interface equality serve different purposes. Checkpoint substitution preserves the required means without necessarily preserving the full output distribution. |
| Balanced differential and addressed real frame, Lemma 1 and Section IV | [Subtree frame lemma](../science/proofs-and-compilation.md#Thmlemma1); [addressed columns](../science/proofs-and-compilation.md#A2.SS4) | `reference.py`, `circuits.py`; `test_real_frame.py`, `test_four_qubit_example.py` | Complete matrix and column checks cover finite dimensions; the recursive proof establishes the all-size frame. |
| Global real gradient record | [Real global method](../science/global-real.md); [readout and Walsh proof](../science/proofs-and-compilation.md#A2.SS5) | `circuits.py`, `decoders.py`, `reference.py`; `test_real_global_estimator.py`, `test_decoders.py` | Complete output distributions yield the full raw-coordinate gradient under calibrated controlled-reflection access. |
| Complex magnitude and direct phase records, [Protocol 1](../science/global-complex.md#S5.SS3.p6.pic1) | [Complex global method](../science/global-complex.md); [proof](../science/proofs-and-compilation.md#A2.SS6) | `circuits.py`, `decoders.py`, `reference.py`; `test_complex_magnitude.py`, `test_complex_phase.py`, `test_complex_frame.py` | Magnitude and phase are separate streams. The general magnitude implementation separates phase and frame blocks; expectation objectives are invariant under a uniform leaf-phase shift. |
| Selected-depth checkpoint record, [Protocol 2](../science/checkpoints.md#S6.SS3.p4.pic1) | [Checkpoint method](../science/checkpoints.md); [transport and active-interface proof](../science/proofs-and-compilation.md#A2.SS7) | `circuits.py`, `decoders.py`, `reference.py`; `test_checkpoints.py`, `test_operator_contracts.py`, `test_four_qubit_example.py` | Each depth uses its own stream. Integrated complex substitution is verified on its active interface. |
| Singular-coordinate behavior | [Balanced differential](../science/balanced-differential.md) and [complex phase identity](../science/proofs-and-compilation.md#A2.SS6) | `reference.py`, `circuits.py`, `decoders.py`; `test_singular_cases.py`, `test_complex_phase.py` | Zero-weight magnitude records vanish. Zero-amplitude phase derivatives vanish, although individual phase records need not vanish. No metric division is used in the ordinary records. |
| Complete-gradient guarantee, Theorem 1 | [Statement](../science/accuracy-resources.md#Thmtheorem1); [fixed-norm concentration and allocation](../science/proofs-and-compilation.md#A2.SS8), [theorem proof](../science/proofs-and-compilation.md#A2.SS11) | Record-norm and decoder checks in `test_decoders.py`, `test_checkpoints.py`, `test_complex_phase.py`, `test_supporting_analysis.py` | Each depth or phase record has norm `2`. The proof gives global execution scaling `O((1 + log(n/delta))/epsilon^2)` for absolute raw-coordinate error; finite checks verify its premises. |
| Assigned direct-angle Hopf work | [Resource account](../science/accuracy-resources.md#S7.SS3); [finite charges](../science/proofs-and-compilation.md#A2.SS9) | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py`; `test_resource_ledger.py` | Finite assigned counts in the paper's compiler model, with controlled-objective and other separately charged resources explicit. [Four-qubit integers](../verification/README.md#expected-finite-values-and-figure-checks) must agree exactly. |
| Exact multiplexed recompilation | [Full derivation](../science/proofs-and-compilation.md#A2.SS10); [implementation companion](../docs/OPTIMIZED_COMPILATION.md) | `optimized_compiler.py`, `qbp_optimized_resource_ledger.py`; `test_optimized_compiler.py` | One reusable clean flag; exact frame action on the clean-flag input. Elementary angles generally recombine Hopf coordinates. The `O(N)` cost also uses the cited synthesis results. |

## Supporting outputs and readout models

These rows cover additional output targets and model extensions. Their executable
formulas are in `supporting_analysis.py`, with tests in
`test_supporting_analysis.py`.

| Supporting result | Derivation and executable evidence | Consequential scope |
|---|---|---|
| Complete raw magnitude-vector Euclidean accuracy | [Appendix B.8](../science/proofs-and-compilation.md#A2.SS8); `test_complete_magnitude_record_norm_and_shot_bound` | The concatenated magnitude record has norm `2*sqrt(n)`; fixed `l_2` accuracy has sufficient cost `O(n/epsilon_2^2)` up to confidence. The complex phase stream is separate. |
| Relative/directional guarantees and inverse-metric conditioning | [Output geometry](../docs/STATISTICAL_ACCURACY.md); `test_relative_shot_bound_and_directional_guarantees`, `test_metric_conditioning_and_regularization` | Requires a nonzero-gradient margin. Small metric factors affect rescaled outputs; damping is an optimizer choice. |
| Raw-coordinate / normalized-frame separation | [Appendix B.8](../science/proofs-and-compilation.md#A2.SS8); `swap_reflection`, `test_coordinate_frame_separation_with_hopf_split` | The real-chart witness shows that raw-coordinate accuracy alone does not control frame error. Controlled access to the witness reflection is a separate assumption. |
| Ambient versus projective phase metrics and zero-sum projection | [Metric convention](../docs/STATISTICAL_ACCURACY.md#7-complex-phase-metric-convention); `test_phase_metric_conventions_and_support_rank`, `test_common_phase_projection_is_unbiased_and_nonexpansive` | Hopf-QBP uses the ambient-sphere metric. The projective block describes a different geometry; zero-sum objective-gradient projection is optional classical postprocessing. |
| Magnitude-output norm hierarchy | [Norm hierarchy](../docs/STATISTICAL_ACCURACY.md#5-magnitude-block-norm-hierarchy); `test_magnitude_norm_hierarchy` | Sufficient upper bounds for the displayed rescaling decoder, with its active-support and metric conditions. |
| Reflection-sum sampling | [Reflection-sum derivation](../docs/OBSERVABLES_AND_READOUT.md#2-reflection-sum-objectives); `test_reflection_term_sampling_is_unbiased` | Unbiased coefficient-one-norm term sampling gives a sufficient `Lambda**2` shot factor under calibrated controlled access to each term. |
| Independent symmetric readout errors | [Readout transfer model](../docs/OBSERVABLES_AND_READOUT.md#3-global-parity-under-independent-readout-flips); `test_readout_transfer_functions` | Parity attenuation and address-bin mixing under a readout-only model; inverting calibrated factors changes variance. |

## Four-qubit construction and verification

The [four-qubit companion](../science/four-qubit-example.md) contains every
explicit gate, addressed column, interface, circuit diagram and finite charge:
Figures 1–9 and Tables I–III. `test_four_qubit_example.py` checks the marker
registry, integrated complex frame, and depth-2 suffix fixtures;
`test_operator_contracts.py` checks the allowed substitutions. The ledger tests
compare Table III's integers exactly. The [complete paper map](PAPER_MAP.md)
links each numbered construction directly.

Qibo checks use the NumPy statevector backend and compare complete states,
matrices or output probability distributions with independent NumPy references.
Algebraic checks run without Qibo. Concentration and asymptotic gate bounds use
the linked mathematical proofs and synthesis results; finite tests check their
premises. The [verification guide](../verification/README.md) specifies test
ranges, commands, tolerances and expected outputs. `test_documentation.py`
checks UTF-8, local file links, fences and the audit table's integrity.

## Scope relative to the first paper

The first Hopf paper supplies the chart, inverse, metric, normalized coordinate
directions, indexed tangent/branch access and native direct-angle schedules.
This paper supplies the addressed differential frame, shared magnitude record,
Walsh decoding, complete phase record, complete-gradient concentration and
checkpoint interface. The [method comparison](../docs/METHOD_COMPARISON.md)
places these results against other gradient tasks and access models.
