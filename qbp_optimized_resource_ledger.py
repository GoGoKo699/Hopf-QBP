#!/usr/bin/env python3
"""Print the multiplexed robustness companion to the Hopf-QBP ledger.

The direct-angle Hopf compiler used by the papers keeps one coordinate as one
directly programmed physical angle at its designated tree-split or leaf-phase
location.  This command instead reports one exact state-equivalent uniformly
controlled-rotation recompilation.  It tests whether the estimator identities
and asymptotic resource comparison survive after leaving that defining compiler
setting; it does not redefine the ansatz.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict

from qbp_validation.optimized_compiler import (
    optimized_compiler_row,
    suffix_predicate_control_widths,
    suffix_predicate_quadratic_proxy,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print the repository-only multiplexed robustness ledger: "
            "uniformly-controlled-rotation core counts and separately exposed "
            "suffix-predicate structure."
        )
    )
    parser.add_argument("--nmin", type=int, default=2)
    parser.add_argument("--nmax", type=int, default=10)
    parser.add_argument(
        "--format",
        choices=("text", "csv", "json"),
        default="text",
    )
    return parser.parse_args()


def _validate_range(nmin: int, nmax: int) -> None:
    if nmin < 1 or nmax < nmin:
        raise ValueError("Require 1 <= nmin <= nmax.")


def _print_text(rows: list[dict[str, int]]) -> None:
    print("Multiplexed Hopf-QBP robustness companion")
    print("This is repository-only analysis outside the direct-angle compiler setting.")
    print("Numeric CNOT columns count uniformly controlled R_y cores only.")
    print("Suffix predicates are exact compute/uncompute operations with compiler-dependent finite counts.")
    print(
        f"{'n':>2} {'N':>8} {'U_chk core':>12} {'W_R core':>12} "
        f"{'pred. calls':>12} {'max ctrls':>10} {'flags':>7}"
    )
    for row in rows:
        print(
            f"{row['n']:>2} {row['dimension']:>8} "
            f"{row['forward_ucr_cnot_upper_bound']:>12} "
            f"{row['frame_ucr_core_cnot_upper_bound']:>12} "
            f"{row['suffix_predicate_calls']:>12} "
            f"{row['maximum_predicate_controls']:>10} "
            f"{row['reusable_clean_flags']:>7}"
        )
    print("\nFor each n, the predicate control widths and quadratic proxy are:")
    for row in rows:
        n = row["n"]
        print(
            f"n={n}: widths={list(suffix_predicate_control_widths(n))}, "
            f"sum(width^2)={suffix_predicate_quadratic_proxy(n)}"
        )
    print("\nBoth U_chk and W_R are O(N); the predicate proxy is O(n^3)=O(log^3 N).")
    print("One clean flag is reused and returned to |0> after every addressed depth.")
    print("Elementary multiplexor angles generally need not equal the Hopf coordinates one by one.")


def _print_csv(rows: list[dict[str, int]]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
    args = parse_args()
    try:
        _validate_range(args.nmin, args.nmax)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    row_objects = [optimized_compiler_row(n) for n in range(args.nmin, args.nmax + 1)]
    rows = [asdict(row) for row in row_objects]
    if args.format == "text":
        _print_text(rows)
    elif args.format == "csv":
        _print_csv(rows)
    else:
        payload = {
            "scope": "repository-only robustness beyond the direct-angle Hopf compiler",
            "direct_angle_setting": "one Hopf coordinate is one directly programmed physical angle at its designated tree-split or leaf-phase location",
            "rows": rows,
            "predicate_details": {
                str(row["n"]): {
                    "control_widths": list(suffix_predicate_control_widths(row["n"])),
                    "quadratic_proxy": suffix_predicate_quadratic_proxy(row["n"]),
                }
                for row in rows
            },
            "interpretation": {
                "numeric_cnot_columns": "uniformly controlled R_y cores only",
                "predicate_cost": "compiler-dependent polynomial overhead, exposed separately",
                "clean_flag": "one reusable flag for n > 1",
                "coordinate_transparency": "not preserved in general by elementary multiplexor angles",
                "ansatz_status": "robustness analysis, not a redefinition of the Hopf ansatz",
            },
        }
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
