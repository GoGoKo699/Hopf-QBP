# Exact optimized compilation

One multiplexed recompilation preserves the prepared state, addressed frame,
and decoded Hopf-QBP estimator with `O(N)` Hopf work per execution. Its
elementary angles generally combine several Hopf coordinates, whereas the
[direct-angle compiler](ENGINEERING_GUIDE.md#direct-angle-hopf-compiler-contract)
keeps each coordinate at its designated tree-split or leaf-phase location.
The [complete derivation in Appendix B.10](../science/proofs-and-compilation.md#A2.SS10)
is the authoritative scientific account. This implementation companion records
the contracts, finite ledger fields, and executable factorization checks.

## 1. Compiler contracts

| Property | Direct-angle Hopf realization | Multiplexed compiler |
|---|---:|---:|
| Same prepared state | Yes | Yes |
| Same frame action or clean-flag system action | Yes | Yes |
| Same decoded Hopf-QBP estimator | Yes | Yes |
| One coordinate is one directly programmed physical angle | **Yes** | Generally no |
| Geometry remains explicit in the gate parameters | **Yes** | Generally no |
| Defines the paper's resource setting | **Yes** | No |

The two command-line ledgers therefore have different roles:

| Tool | Role | What is counted |
|---|---|---|
| `qbp_resource_ledger.py` | Direct-angle assigned ledger used by the paper | Independently decomposed coordinate-preserving controlled gates under the declared formulas |
| `qbp_optimized_resource_ledger.py` | Exact multiplexed companion | Uniformly controlled-rotation cores, with suffix-predicate work exposed separately |

Both ledgers count logical Hopf work; controlled-observable, readout, routing,
and approximate-synthesis costs are excluded.

Run them with:

```bash
python qbp_resource_ledger.py --nmin 2 --nmax 10
python qbp_optimized_resource_ledger.py --nmin 2 --nmax 10
```

## 2. Finite ledger and compiler interfaces

Write `N = 2**n`. The following bounds count uniformly controlled-rotation
cores. The uncontrolled layer uses no CNOT; adjacent-layer cancellation is not
assumed.

| Compiler object | Core CNOT upper bound | Implementation |
|---|---:|---|
| Forward depth preparation `U_chk` | `N - 2` | `forward_ucr_cnot_upper_bound` |
| Inverse suffix below depth `d` | `N - 2**(d+1)` | `inverse_suffix_ucr_cnot_upper_bound` |
| Addressed real frame, `n >= 2` | `3*N/2 - 2` | `frame_ucr_core_cnot_upper_bound` |

Each nonfinal addressed depth computes and uncomputes the all-zero lower-suffix
predicate into one reusable clean flag. The flag is the least-significant
register bit in the matrix fixtures. Its predicate widths are
`n-1, n-1, n-2, n-2, ..., 1, 1`; the final depth uses the ordinary prefix
multiplexor and leaves the unused flag unchanged.

The relevant API is in [`qbp_validation/optimized_compiler.py`](../qbp_validation/optimized_compiler.py):

| Function | Contract checked |
|---|---|
| `direct_addressed_depth_layer` | Prefix selects the Hopf angle, active only on a zero lower suffix. |
| `suffix_zero_flag_permutation` | Computes `flag ^= [lower suffix == 0]`; it is self-inverse. |
| `flagged_multiplexor_depth_layer` | Flag zero selects angle zero; flag one selects the prefix's angle. |
| `flagged_addressed_depth_layer` | Compute–multiplex–uncompute for one depth. |
| `flagged_real_frame` | Composition of the depth factorizations using the same clean flag. |
| `clean_flag_system_block` / `clean_flag_leakage_block` | Extracts the preserved system operator and tests zero leakage into flag one. |

The exact requirement is equality with `W_R` for **every system input** when
the flag starts at zero, together with return of that flag to zero. It is
stronger than a prepared-state-column comparison. The code checks this logical
factorization, while the [proof and cited synthesis constructions](../science/proofs-and-compilation.md#A2.SS10)
provide the elementary-gate resource argument.

## 3. Complete cost and matched comparison

The predicate ledger exposes widths rather than assigning one
compiler-independent finite constant. Standard exact multi-controlled-X
synthesis gives total predicate work `O(n**3)`; the uniformly controlled cores
have `O(N)` work. With `N = 2**n`, the complete real frame therefore has `O(N)`
work and one reusable clean flag. The complex separated frame
`W_C = D_ph W_R` additionally uses the paper's exact `O(N)` diagonal synthesis.

The matched scalar and global-record executions use the same state, system
size, controlled objective, and calibrated branch phase. Under this particular
multiplexed compilation, both have `O(N)` Hopf work per execution. Their
statistical repetition counts, classical Walsh decoding, materialized output,
and storage remain separate resources. The exact comparison and assumptions
are in [Appendix B.10](../science/proofs-and-compilation.md#A2.SS10).

## 4. Executable support

The Qibo-free reference implementation is in:

```text
qbp_validation/optimized_compiler.py
qbp_validation/tests/test_optimized_compiler.py
qbp_optimized_resource_ledger.py
```

The tests check:

- every addressed depth through `n = 5`;
- the complete addressed frame through `n = 4`;
- equality on the clean-flag input subspace;
- zero flag leakage;
- the multiplexor-core counts;
- inverse-suffix counts; and
- the full predicate-width ledger.

Run:

```bash
python validate_qbp.py --analytic
```

The matrix checks validate the exact flag factorization. The asymptotic CNOT
claim additionally uses the established Gray-code synthesis of uniformly
controlled rotations and standard multi-controlled-X constructions.

## 5. Primary references

- M. Möttönen, J. J. Vartiainen, V. Bergholm, and M. M. Salomaa,
  [Transformation of quantum states using uniformly controlled rotations](https://arxiv.org/abs/quant-ph/0407010),
  *Quantum Information and Computation* **5**, 467–473 (2005).
- V. Bergholm, J. J. Vartiainen, M. Möttönen, and M. M. Salomaa,
  [Quantum circuits with uniformly controlled one-qubit gates](https://arxiv.org/abs/quant-ph/0410066),
  *Physical Review A* **71**, 052330 (2005).
- V. V. Shende, S. S. Bullock, and I. L. Markov,
  [Synthesis of quantum-logic circuits](https://arxiv.org/abs/quant-ph/0406176),
  *IEEE Transactions on Computer-Aided Design* **25**, 1000–1010 (2006).
- A. Barenco et al.,
  [Elementary gates for quantum computation](https://arxiv.org/abs/quant-ph/9503016),
  *Physical Review A* **52**, 3457–3467 (1995).
- S. S. Bullock and I. L. Markov,
  [Smaller circuits for arbitrary n-qubit diagonal computations](https://arxiv.org/abs/quant-ph/0303039),
  *Quantum Information and Computation* **4**, 27–47 (2004).
