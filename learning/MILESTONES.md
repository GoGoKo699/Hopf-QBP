# Project understanding map: 30 milestones

This map contains exactly **30 project-intrinsic milestones**. Its targets and
dependencies are common to all readers. The single educational anchor is
**Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th
Anniversary Edition**. The [anchor bridge](ANCHOR.md) specifies the edition,
notation and selected sections, and supplies the Hopf background locally.
Reading the companion repository is useful but not required to begin this route.

The allocation is **12 background/preliminaries milestones** and **18
narrative/innovation milestones**. The background joins states, coherent
circuits, differential directions and statistical targets into the reverse
task. The narrative develops the global and checkpoint mechanisms before
combining their accuracy and resource guarantees. Each phase moves from local
objects to the full operational picture. The map supports global understanding;
complete derivations remain in the scientific account.

| Phase | Milestones | Connection established |
|---|---|---|
| Background/preliminaries | M01–M04 | State vectors, phases, controlled splits and reflection objectives |
| Background/preliminaries | M05–M08 | Interference, local differentials, weights and reversible frames |
| Background/preliminaries | M09–M12 | Measurement records, error targets and the complete reverse task |
| Narrative/innovation | M13–M18 | Balanced differential frame, global real record and Walsh decoding |
| Narrative/innovation | M19–M23 | Complex records, checkpoint interfaces and a gate-level instance |
| Narrative/innovation | M24–M28 | Concentration, accuracy distinctions and matched compiler costs |
| Narrative/innovation | M29–M30 | Verification, attribution and the complete backpropagation result |

## Phase I: background and preliminaries

### M01 States, basis strings and amplitude dimension

**Central question.** What is the state space on which the reverse procedure acts?

**Understanding target.** Interpret $N=2^n$ amplitudes as an $n$-qubit vector,
read basis strings from most to least significant bit, and distinguish system,
interference ancilla and classical output registers.

**Prior dependencies.** None within this map.

**Conceptual connection.** Quantum width, Hilbert-space dimension and gradient
output length are different resources even though their notation is closely related.

**Sources.** N&C §§2.1.1–2.1.7, 2.2.8;
[notation and output](ANCHOR.md#notation-and-output);
[reverse task](../science/reverse-task.md#S2.SS3).

### M02 Physical phase and coherent relative phase

**Central question.** When does a phase that is invisible in a state become measurable?

**Understanding target.** Distinguish a common phase of an isolated state
from a phase between controlled branches. Explain why state fidelity does not
certify the phase convention required by an interference decoder.

**Prior dependencies.** M01.

**Conceptual connection.** Forward state preparation and controlled objective
access have different phase-sensitive obligations.

**Sources.** N&C §§2.2.7, 9.2.2;
[interference bridge](ANCHOR.md#3-controlled-reflection-turns-a-derivative-into-interference);
[objective assumption](../science/reverse-task.md#Thmassumption1).

### M03 Controlled rotations and local tree splits

**Central question.** How does one angle become a conditional amplitude split?

**Understanding target.** Apply the paper's $R_y(\theta)=e^{-i\theta Y}$,
translate its software half-angle convention, and interpret positive and
negative controls addressing a subtree.

**Prior dependencies.** M01–M02.

**Conceptual connection.** The same angle labels a geometric derivative and
a designated physical operation in the direct-angle compiler setting.

**Sources.** N&C §§4.2–4.3;
[local Hopf geometry](ANCHOR.md#1-reconstruct-the-local-hopf-geometry);
[forward interfaces](../science/balanced-differential.md#S3.SS3).

### M04 Reflection objectives and coordinate derivatives

**Central question.** What scalar is differentiated, and which coherent operation is assumed?

**Understanding target.** Define $E_O=\langle\psi\mid O\mid\psi\rangle$
with $O=O^\dagger$ and $O^2=I$, and derive
$\partial_jE_O=2\mathrm{Re}\langle\partial_j\psi\mid O\mid\psi\rangle$.

**Prior dependencies.** M01.

**Conceptual connection.** The Hermitian-unitary contract makes the objective
compatible with a controlled unitary while fixing the derivative being estimated.

**Sources.** N&C §§2.1.6, 2.2.3, 6.1;
[objective and output](../science/reverse-task.md#S2.SS3);
[controlled reflection](ANCHOR.md#3-controlled-reflection-turns-a-derivative-into-interference).

### M05 Ancilla interference and measured quadratures

**Central question.** How are real and imaginary transition moments retained in a measurement?

**Understanding target.** Construct
$(\lvert0\rangle\psi+\lvert1\rangle O\psi)/\sqrt2$ and relate ancilla
$X$ and $Y$ measurements to its branch coherence. Track the known branch phase.

**Prior dependencies.** M02–M04.

**Conceptual connection.** Controlled interference provides signed responses
that an ordinary scalar expectation sample does not contain.

**Sources.** N&C §§4.3–4.4;
[controlled-interference identities](../science/proofs-and-compilation.md#A2.SS1);
[interference bridge](ANCHOR.md#3-controlled-reflection-turns-a-derivative-into-interference).

### M06 A split and its complement

**Central question.** Why is the derivative of one normalized split a unit orthogonal direction?

**Understanding target.** For orthonormal $u,v$, differentiate
$\cos\theta\,u+\sin\theta\,v$, verify orthogonality and normalization,
and identify the three magnitude directions in the two-qubit example.

**Prior dependencies.** M01, M03–M04.

**Conceptual connection.** This local pair is the building block of a complete
reversible differential frame.

**Sources.** N&C §§2.1.4, 4.2;
[two-qubit clue](../science/reverse-task.md#S2.SS1);
[worked geometry](ANCHOR.md#1-reconstruct-the-local-hopf-geometry).

### M07 Subtree weights and raw coordinate speed

**Central question.** Why is a normalized direction different from a raw coordinate derivative?

**Understanding target.** Interpret
$\partial_j\psi=w_j e_j$, $g_{jj}=w_j^2$, and the depth identity
$\sum_{j\text{ at }d}g_{jj}=1$. Handle a zero weight without dividing by it.

**Prior dependencies.** M03, M06.

**Conceptual connection.** Subtree probability controls the scale of a raw
derivative and later fixes the norm of a complete depth record.

**Sources.** N&C §§2.1.4, 2.2.3;
[subtree states and weights](../science/balanced-differential.md#S3.SS2);
[geometry bridge](ANCHOR.md#1-reconstruct-the-local-hopf-geometry).

### M08 Unitary columns and substitution contracts

**Central question.** What does preparing the correct state say about the rest of a unitary?

**Understanding target.** Distinguish full-unitary, initialized-state-column
and active-interface equality. Use $I$ versus $Z$ on $\lvert0\rangle$
to explain why state-column equality alone cannot justify a reverse replacement.

**Prior dependencies.** M01–M03, M06.

**Conceptual connection.** The reverse computation uses more information
about a circuit than its prepared state, so every substitution needs the right contract.

**Sources.** N&C §§2.2.2, 4.3–4.5;
[three contracts](../science/reverse-task.md#S2.SS4);
[contract bridge](ANCHOR.md#2-a-forward-state-column-does-not-determine-a-reverse-circuit).

### M09 Measurement bits, parities and vector records

**Central question.** How can one observed bit string provide several signed statistics?

**Understanding target.** Convert an $X$-basis bit to its eigenvalue
$(-1)^b$, interpret a bit parity as a product observable, and distinguish a
physical outcome from the vector of functions computed from it.

**Prior dependencies.** M01, M05.

**Conceptual connection.** Reusing one outcome for many coordinates is a
classical decoding operation whose unbiasedness must follow from the joint quantum distribution.

**Sources.** N&C §§2.2.3, 4.4;
[readable inverse frame](../science/global-real.md#S4.SS2);
[parity bridge](ANCHOR.md#4-the-frame-makes-every-magnitude-direction-readable).

### M10 Independent executions and error norms

**Central question.** What does simultaneous accuracy of a complete vector mean?

**Understanding target.** State the probability event
$\lVert\widehat q-q\rVert_\infty\le\varepsilon$, distinguish it from
Euclidean and relative accuracy, and separate within-record correlations from
independence between fresh executions.

**Prior dependencies.** M04, M09.

**Conceptual connection.** A statistical guarantee must specify its output
norm and confidence before its scaling in parameter count is meaningful.

**Sources.** N&C Appendix 1;
[complete-gradient accuracy](../science/reverse-task.md#Thmdefinition1);
[statistical bridge](ANCHOR.md#8-fixed-norm-explains-the-complete-coordinate-shot-bound).

### M11 Comparing complete computational costs

**Central question.** Which quantities must be included in a matched gradient comparison?

**Understanding target.** Separate controlled-objective access, assigned Hopf
CNOT work, classical histogram/transform work, input storage and the $M$-entry
output. Identify the scalar comparator's shared access assumptions.

**Prior dependencies.** M03–M05, M08–M10.

**Conceptual connection.** Reducing executions is one part of a complete
resource statement; the compiler and output target determine the remaining costs.

**Sources.** N&C §§3.2.1, 4.5.1–4.5.2;
[backpropagation definition](../science/reverse-task.md#Thmdefinition2);
[resource interpretation](ANCHOR.md#9-error-norms-and-costs-complete-the-interpretation).

### M12 The complete reverse task

**Central question.** What must be constructed to turn local derivative access into a reusable complete-gradient record?

**Understanding target.** Combine the state chart, weighted directions,
phase-calibrated objective, circuit contracts, record decoder and accuracy
target into one operational specification.

**Prior dependencies.** M01–M11.

**Conceptual connection.** This closes the background phase by identifying
both the useful output and the information the reverse interface must preserve.

**Sources.** N&C §§4.3–4.6;
[reusable reverse record](../science/reverse-task.md#S2.SS2);
[reverse-task model](../science/reverse-task.md#S2).

## Phase II: narrative and innovation

### M13 The balanced differential frame

**Central question.** Why do all magnitude complements form a complete orthonormal frame with the state?

**Understanding target.** Extend the local split/complement argument by
recursion, prove mutual orthogonality, and retain the weight in every raw
coordinate differential, including singular representatives.

**Prior dependencies.** M06–M08, M12.

**Conceptual connection.** Local derivative directions become the columns of
one basis change, which is the structural prerequisite for collective readout.

**Sources.** N&C §§2.1.1, 2.1.4;
[balanced differential](../science/balanced-differential.md#S3.SS2);
[subtree-frame lemma and proof](../science/proofs-and-compilation.md#A2.SS2).

### M14 Depth completion and forward substitution

**Central question.** How can different forward circuits prepare the same Hopf state?

**Understanding target.** Construct $U_{\mathrm{chk}}=U_{n-1}\cdots U_0$,
explain depth-conditioned rotations, and apply only the initialized-column
contract when replacing a forward preparation.

**Prior dependencies.** M03, M08, M13.

**Conceptual connection.** A depth organization exposes checkpoint boundaries
without requiring the native schedule and depth completion to be identical unitaries.

**Sources.** N&C §§4.2–4.3;
[depth completion](../science/balanced-differential.md#S3.SS3);
[forward-state proof](../science/proofs-and-compilation.md#A2.SS3).

### M15 Computational addresses for the full real frame

**Central question.** How is each magnitude direction assigned to a definite column?

**Understanding target.** Derive the anchor and marker labels for
$j=2^d+r$, follow the addressed two-level rotations, and verify the state and
complement column identities.

**Prior dependencies.** M02–M03, M08, M13.

**Conceptual connection.** The complete frame turns geometric directions into
computational addresses that can be decoded by parity measurements.

**Sources.** N&C §§4.3, 4.5.1;
[addressed frame](../science/global-real.md#S4.SS1);
[frame-column proof](../science/proofs-and-compilation.md#A2.SS4).

### M16 Why the inverse frame exposes the objective response

**Central question.** What information appears at marker $\lambda(j)$ after the reverse frame?

**Understanding target.** Show that
$(W_{\mathbb R}^\dagger O\psi)_{\lambda(j)}=\langle e_j\mid O\mid\psi\rangle$
and derive its relation to an all-$`X`$ ancilla–system parity correlator.

**Prior dependencies.** M04–M05, M09, M15.

**Conceptual connection.** The inverse frame converts a transition moment
into a directly readable amplitude coordinate without measuring a tangent label first.

**Sources.** N&C §§2.1.2, 4.4;
[inverse-frame mechanism](../science/global-real.md#S4.SS2);
[controlled interference](../science/proofs-and-compilation.md#A2.SS1).

### M17 One global outcome supplies every magnitude coordinate

**Central question.** Why is $Z_j=2w_j(-1)^{b+\lambda(j)\cdot y}$ unbiased for every $j$?

**Understanding target.** Combine the frame identity, parity correlator and
metric multiplier; compute the two-qubit example and identify the correlations
between coordinates of one record.

**Prior dependencies.** M07, M09–M10, M16.

**Conceptual connection.** The saving is shared use of each quantum outcome
across coordinates and depths, with the entire output still materialized classically.

**Sources.** N&C §4.4, Appendix 1;
[global record](../science/global-real.md#S4.SS3);
[worked parity record](ANCHOR.md#4-the-frame-makes-every-magnitude-direction-readable);
[decoder proof](../science/proofs-and-compilation.md#A2.SS5).

### M18 Signed histograms and the Walsh transform

**Central question.** How can all parity averages be computed without updating every coordinate after every shot?

**Understanding target.** Form a normalized signed histogram, apply the
unnormalized Walsh transform, select marker entries and rescale by $2w_j$.
Account for $O(S+N\log N)$ decoding work and $O(N)$ storage.

**Prior dependencies.** M09, M11, M17.

**Conceptual connection.** The decoder gives an efficient classical realization
of record reuse and makes the output cost explicit.

**Sources.** N&C §§2.1.2, 3.2.1;
[Walsh bridge](ANCHOR.md#5-walsh-decoding-reuses-a-classical-histogram);
[global decoder proof](../science/proofs-and-compilation.md#A2.SS5).

### M19 Phase dressing preserves magnitude readout

**Central question.** How does the real frame extend to complex amplitudes?

**Understanding target.** Define $D_{\mathrm{ph}}$ and
$W_{\mathbb C}=D_{\mathrm{ph}}W_{\mathbb R}$, remove phases in the reverse
circuit, and retain the same magnitude weights and marker parity rule.

**Prior dependencies.** M02, M13, M15–M17.

**Conceptual connection.** The complex chart changes the state and frame
through a phase layer while preserving the magnitude differential structure.

**Sources.** N&C §§2.2.7, 4.2–4.3;
[complex frame](../science/global-complex.md#S5.SS1);
[complex magnitude protocol](../science/global-complex.md#S5.SS2).

### M20 The direct signed phase histogram

**Central question.** Why can phase derivatives be read without an inverse frame?

**Understanding target.** Derive the leaf-local phase differential and the
signed one-hot record from ancilla-$`Y`$/system-$`Z`$ measurement. Explain zero
expected derivatives at zero leaves and the zero sum under a common phase shift.

**Prior dependencies.** M02, M04–M05, M10, M19.

**Conceptual connection.** Magnitudes and phases need different physical
records but combine into the same complete raw-coordinate output.

**Sources.** N&C §§2.2.7, 4.4;
[direct phase protocol](../science/global-complex.md#S5.SS3);
[complex identities](../science/proofs-and-compilation.md#A2.SS6);
[phase and metric bridge](ANCHOR.md#6-complex-phases-have-a-separate-direct-record).

### M21 A real checkpoint returns one depth block

**Central question.** How does reversing only the lower suffix reveal the selected layer's response?

**Understanding target.** Identify $B_d=U_{n-1}\cdots U_{d+1}$,
follow the prefix and split-target measurements, and derive the signed
one-hot record $-2(-1)^{b_c+b_t}e_r$.

**Prior dependencies.** M05, M07–M09, M14.

**Conceptual connection.** Checkpointing exchanges cross-depth reuse for a
layer-local reverse circuit, whose final-depth suffix is empty in the real case.

**Sources.** N&C §§4.3–4.4;
[checkpoint construction](../science/checkpoints.md#S6.SS1);
[real protocol](../science/checkpoints.md#S6.SS2);
[checkpoint proof](../science/proofs-and-compilation.md#A2.SS7).

### M22 Complex active-interface substitution

**Central question.** What equality is sufficient to integrate phases into a checkpoint suffix?

**Understanding target.** Identify the active-interface projector and the
exact columns it selects. Follow the correlator-preservation proof without
promoting it to an equality of arbitrary inputs or complete output distributions.

**Prior dependencies.** M02, M08, M19–M21.

**Conceptual connection.** A restricted operator contract can be sufficient
for a specified estimator even when it is insufficient for a general reverse substitution.

**Sources.** N&C §§2.1.2, 4.3;
[complex checkpoint extension](../science/checkpoints.md#S6.SS3);
[active-interface proof](../science/proofs-and-compilation.md#A2.SS7).

### M23 The four-qubit implementation companion

**Central question.** Can the abstract contracts be inspected in a complete gate-level example?

**Understanding target.** Match coordinates, metric factors, marker columns,
forward completion, integrated complex frame and depth-two suffix to their
four-qubit gates and resource charges.

**Prior dependencies.** M13–M22.

**Conceptual connection.** One finite instance joins the chart, compiler,
measurement and decoder while preserving which identities hold only on an interface.

**Sources.** N&C §§4.2–4.5;
[four-qubit companion](../science/four-qubit-example.md#A1);
[frame compilation](../science/four-qubit-example.md#A1.SS6.SSS1);
[active-interface construction](../science/four-qubit-example.md#A1.SS8.SSS1).

### M24 Fixed-norm records and vector concentration

**Central question.** Why does one depth block have a width-independent statistical scale?

**Understanding target.** Prove $\lVert Z_d\rVert_2=2$ from the depth weight
identity, compare the one-hot checkpoint and phase records, and connect this
premise to concentration of their sample means.

**Prior dependencies.** M07, M10, M17, M20–M21.

**Conceptual connection.** Vector concentration controls a whole depth at
once and avoids a separate coordinatewise union bound across its width.

**Sources.** N&C Appendix 1;
[fixed-norm argument](../science/accuracy-resources.md#S7.SS2);
[concentration proof](../science/proofs-and-compilation.md#A2.SS8);
[worked allocation bridge](ANCHOR.md#8-fixed-norm-explains-the-complete-coordinate-shot-bound).

### M25 Complete-chart allocations and global reuse

**Central question.** How do block guarantees produce the stated complete-gradient execution counts?

**Understanding target.** Allocate confidence across $n$ depths and the
complex phase stream, distinguish reused global shots from separately
executed checkpoint streams, and convert $n$ scaling into $M$ scaling.

**Prior dependencies.** M10, M17–M21, M24.

**Conceptual connection.** Cross-depth record reuse is exactly the source of
the difference between the global and complete checkpoint execution bounds.

**Sources.** N&C Appendix 1, §3.2.1;
[complete-chart accuracy](../science/accuracy-resources.md#S7.SS2);
[allocation proof](../science/proofs-and-compilation.md#A2.SS8).

### M26 Other error targets and geometric conditioning

**Central question.** What changes when the requested output is a direction or a metric-rescaled gradient?

**Understanding target.** Derive the concatenated magnitude-record norm
$2\sqrt n$, require a nonzero signal for relative/directional bounds, and
track amplification by $1/\sqrt{g_{jj}}$ or $1/g_{jj}$ for rescaled coordinates.

**Prior dependencies.** M07, M10, M20, M24–M25.

**Conceptual connection.** A small raw coordinate derivative can be accurately
estimated while its normalized-frame counterpart remains uncertain; the
accuracy target and metric convention remain part of the theorem.

**Sources.** N&C §§2.1.4, 9.2.2, Appendix 1;
[accuracy refinements](../science/proofs-and-compilation.md#A2.SS8);
[error-norm bridge](ANCHOR.md#9-error-norms-and-costs-complete-the-interpretation).

### M27 The matched direct-angle resource theorem

**Central question.** How do the executions, compiled circuits and classical outputs combine into the claimed backpropagation overhead?

**Understanding target.** Apply the declared forward/frame/suffix CNOT
charges, add controlled-objective access separately, and compare with a scalar
evaluation under the same compiler and access model. Track decoding and storage.

**Prior dependencies.** M11, M14–M15, M18, M23–M25.

**Conceptual connection.** A complete overhead claim is a matched accounting
statement for the specified construction, not a globally optimal synthesis bound.

**Sources.** N&C §§3.2.1, 4.5.1–4.5.2;
[resource theorem](../science/accuracy-resources.md#Thmtheorem1);
[assigned ledger](../science/proofs-and-compilation.md#A2.SS9);
[theorem proof](../science/proofs-and-compilation.md#A2.SS11).

### M28 Exact multiplexed recompilation

**Central question.** Which properties survive a compiler that recombines physical angles?

**Understanding target.** State the clean-flag system-action contract, follow
the exact logical factorization and its matched forward/frame cost, and
separate estimator preservation from direct-angle coordinate preservation.

**Prior dependencies.** M08, M15, M23, M27.

**Conceptual connection.** Compiler alternatives can preserve the scientific
readout while changing elementary angle interpretation, workspace and resource charges.

**Sources.** N&C §§4.3–4.5;
[exact multiplexed recompilation](../science/proofs-and-compilation.md#A2.SS10).

### M29 Verification, attribution and protocol choice

**Central question.** What evidence and task information support choosing a global or checkpoint implementation?

**Understanding target.** Trace a claim to its proof and independent circuit
check; distinguish exact distributions from shot estimates; identify inherited
Hopf geometry and the new shared-record mechanism. Compare protocols for the
requested depth set under their actual compiled costs.

**Prior dependencies.** M12–M28.

**Conceptual connection.** The mathematical result, implementation evidence
and intended output jointly determine which protocol is useful.

**Sources.** N&C §§3.2.1, 4.4;
[attribution and motivation](../science/motivation.md#S1);
[protocol choice](../science/accuracy-resources.md#S7.SS4);
[reproduction](../verification/README.md).

### M30 The complete Hopf quantum-backpropagation mechanism

**Central question.** How does the Hopf chart carry a state forward and its complete coordinate response backward?

**Understanding target.** Present a connected argument from weighted
orthogonal directions through addressed frames, calibrated interference,
shared records, Walsh/leaf decoding, concentration and matched resources.
State the output norm, access assumptions and compiler contracts alongside
the resulting complete-gradient guarantee.

**Prior dependencies.** M12–M29.

**Conceptual connection.** The local split mechanism becomes a reusable
complete-vector interface, with checkpointing and recompilation interpreted
within the same operational account.

**Sources.** N&C §§3.2.1, 4.6;
[main theorem](../science/accuracy-resources.md#Thmtheorem1);
[complete proof](../science/proofs-and-compilation.md#A2.SS11);
[conclusion](../science/conclusion.md#S8);
[bridge synthesis](ANCHOR.md#10-assemble-and-check-the-complete-mechanism).
