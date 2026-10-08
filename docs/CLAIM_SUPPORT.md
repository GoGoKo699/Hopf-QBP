# Claim support and validation map

This page is for readers auditing whether the implementation supports the claims
made by *Compass in the Mirror: Quantum Backpropagation with the Hopf Ansatz*.
It distinguishes paper-level results, Appendix-B supporting statements, and
additional executable extensions.

The [engineering guide](ENGINEERING_GUIDE.md) defines the direct-angle circuit
and decoder contracts. [Optimized compilation](OPTIMIZED_COMPILATION.md)
derives the exact multiplexed alternative and its separate resource ledger.

## Evidence levels

| Support type | Meaning |
|---|---|
| **Exact-logical circuit check** | A Qibo circuit is executed with the NumPy statevector backend and compared with an independent NumPy reference. |
| **Algebraic reference check** | A finite-dimensional identity, decoder, convention, or resource formula is evaluated without Qibo. |
| **Checked factorization plus synthesis theorem** | An exact logical factorization is tested, while its asymptotic elementary-gate cost uses an established synthesis result. |
| **Analytic deduction exposed by code** | The finite premises of a statistical or asymptotic statement are checked, while the dimension-independent conclusion is mathematical rather than numerical. |

No finite numerical experiment proves an asymptotic concentration or
complexity claim. The documentation therefore separates tested ingredients from
analytic deductions.

## Audit summary

| Paper-level or supporting claim | Status and support | Main implementation | Main tests | Boundary |
|---|---|---|---|---|
| Native real and complex preparations reproduce the Hopf state | Paper-level exact state-column checks | `native_schedule.py`, `reference.py`, `circuits.py` | `test_native_schedule.py`, `test_operator_contracts.py` | State-column equality, not full-unitary equality. |
| The balanced real frame contains the state and normalized magnitude directions | Paper-level complete matrix and column checks | `reference.py`, `circuits.py` | `test_real_frame.py`, `test_four_qubit_example.py` | Finite dimensions through the tested range. |
| The global real circuit decodes the complete raw coordinate gradient | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_real_global_estimator.py` | Exact phase-calibrated controlled reflection. |
| The global complex magnitude circuit decodes all magnitude derivatives | Paper-level exact complete-distribution check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_magnitude.py` | General implementation uses separated phase/frame blocks. |
| The direct complex phase circuit decodes all leaf-phase derivatives | Paper-level exact signed one-hot check | `circuits.py`, `decoders.py`, `reference.py` | `test_complex_phase.py` | Expectation objectives are invariant under a uniform leaf-phase shift. |
| A checkpoint circuit returns every derivative at a selected depth | Paper-level exact depth-block check | `circuits.py`, `decoders.py`, `reference.py` | `test_checkpoints.py` | Each selected depth uses its own circuit stream. |
| Integrated complex checkpoint substitution is valid on the active interface | Paper-level projected-matrix and decoded-mean checks | `reference.py`, `circuits.py`, `conventions.py` | `test_operator_contracts.py`, `test_four_qubit_example.py` | It need not preserve the full unitary or complete distribution. |
| Singular magnitude and zero-amplitude phase coordinates are handled without division | Paper-level exact singular checks | `reference.py`, `circuits.py`, `decoders.py` | `test_singular_cases.py`, `test_complex_phase.py` | Zero-weight magnitude records vanish. Zero-amplitude phase derivatives vanish, but individual phase records need not. |
| Every single-depth global, checkpoint, and direct-phase record has norm `2` | Paper-level algebraic record checks | `decoders.py`, `reference.py` | `test_decoders.py`, `test_checkpoints.py`, `test_complex_phase.py` | Finite premise of the concentration argument. |
| Global coordinatewise execution scaling is `O((1 + log(n/delta))/epsilon^2)` | Paper-level analytic deduction | Record definitions and norm tests | Norm and decoder tests above | Absolute raw-coordinate error. |
| The concatenated magnitude record has norm `2*sqrt(n)` and fixed `l_2` accuracy costs `O(n/epsilon_2^2)` up to confidence | Appendix-B analytic result with executable support | `supporting_analysis.py`, `STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` | Raw magnitude vector; the complex phase stream is separate. |
| Relative/directional control and magnitude-block natural-gradient conditioning follow from the `l_2` bound and metric factors | Appendix-B conditional result | `supporting_analysis.py`, `STATISTICAL_ACCURACY.md` | `test_supporting_analysis.py` | Requires a nonzero-gradient margin; damping is an optimizer choice. |
| Raw-coordinate accuracy does not imply normalized-frame accuracy without metric conditioning | Main-text interpretation with Appendix-B proof and exact executable support | `swap_reflection`, `STATISTICAL_ACCURACY.md` | `test_coordinate_frame_separation_with_hopf_split` | Real-chart existence result; no efficient compiler for the witness reflection is claimed. |
| The ambient-sphere phase metric is the adopted convention; the projective block describes the alternative quotient geometry | Main-text convention with Appendix-B derivation and executable support | `ambient_phase_metric`, `projective_phase_metric` | `test_phase_metric_conventions_and_support_rank` | The theorem uses the ambient-sphere convention. |
| The magnitude output objects obey the stated sufficient norm hierarchy | Supporting analytic result | norm-bound helpers, `STATISTICAL_ACCURACY.md` | `test_magnitude_norm_hierarchy` | Upper bounds for the displayed rescaling decoder, not converses. |
| The direct-angle assigned CNOT ledger matches the manuscript's compiler model | **Paper-level resource claim** | `conventions.py`, `native_schedule.py`, `qbp_resource_ledger.py` | `test_resource_ledger.py` | Finite assigned counts, not global optimality or routing. |
| One exact multiplexed realization preserves the estimator and the `O(N)` matched forward/frame scaling | **Appendix-B exact compiler result with detailed executable support** | `optimized_compiler.py`, `qbp_optimized_resource_ledger.py` | `test_optimized_compiler.py` | One reusable clean flag; elementary angles generally recombine Hopf coordinates. |
| A reflection sum admits unbiased coefficient-one-norm term sampling with a `Lambda**2` sufficient-shot factor | Main-text extension with executable support | `supporting_analysis.py`, `OBSERVABLES_AND_READOUT.md` | `test_supporting_analysis.py` | Portable upper bound, not an optimal Hamiltonian strategy. |
| Independent symmetric readout errors transform records by attenuation and bin mixing | Supporting analytic readout model | `supporting_analysis.py`, `OBSERVABLES_AND_READOUT.md` | `test_supporting_analysis.py` | Readout-only; no coherent gate-noise or mitigation claim. |

## Scope relative to the first paper

The first Hopf paper supplies the balanced real and complex charts, inverse map,
diagonal pullback metric, normalized coordinate directions, indexed tangent and
signed-branch estimators, native schedules, and the direct-angle
coordinate-to-control interpretation.

The present project supplies the computationally addressed differential frame,
one magnitude record shared across coordinates and depths, Walsh decoding, the
direct complete phase record, complete-gradient concentration, checkpoint
suffixes and active-interface contracts, and the supporting compiler,
statistical, observable, readout, and method-positioning analyses listed above.

## Validation matrix

| Test | Main responsibility |
|---|---|
| `test_conventions.py` | Tree indexing, basis order, parameter splitting, markers, and interfaces. |
| `test_native_schedule.py` | Native real and complex schedules and state columns. |
| `test_circuit_conventions.py` | Qibo bit significance and ancilla-`Y` sign. |
| `test_operator_contracts.py` | Full-unitary, state-column, and active-interface distinctions. |
| `test_real_frame.py` | Complete real frame and inverse. |
| `test_complex_frame.py` | Separated complex frame and four-qubit integrated compiler. |
| `test_real_global_estimator.py` | Complete real global gradient and Walsh decoder. |
| `test_complex_magnitude.py` | Complex magnitude gradient. |
| `test_complex_phase.py` | Direct phase gradient and zero-amplitude leaves. |
| `test_checkpoints.py` | Real and complex selected-depth gradients. |
| `test_singular_cases.py` | Exact singular-coordinate behavior. |
| `test_decoders.py` | Walsh, signed histograms, marginalization, and fixed-norm records. |
| `test_four_qubit_example.py` | Explicit compiler fixtures and interfaces. |
| `test_resource_ledger.py` | Direct-angle assigned charges. |
| `test_optimized_compiler.py` | Clean-flag factorization and multiplexor ledger. |
| `test_supporting_analysis.py` | `l_2`, direction, separation, phase metrics, norm hierarchy, reflection sums, and readout. |
| `test_documentation.py` | UTF-8 integrity, control characters, local link targets, fence balance, and claim-map structure. |
