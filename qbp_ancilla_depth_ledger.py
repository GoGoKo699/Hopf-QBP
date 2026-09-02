#!/usr/bin/env python3
"""Print the ancilla--depth term ledger for the global Hopf frame.

This command supports the research companion in
``docs/ANCILLA_DEPTH_ROBUSTNESS.md``. It reports exact structural counts and
unit-coefficient proxies for the asymptotic terms inherited from the
Sun--Tian--Yang--Yuan--Zhang compiler theorems. It is not a routed hardware
estimate and does not report exact elementary-gate depth.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import asdict

from qbp_validation.ancilla_depth_compiler import ancilla_depth_rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Print the candidate ancilla-depth robustness term ledger for the "
            "clean global Hopf frame."
        )
    )
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument(
        "--ancillas",
        type=str,
        default=None,
        help=(
            "Comma-separated state-compiler workspace budgets. The frame uses "
            "one additional reusable clean flag."
        ),
    )
    parser.add_argument(
        "--format",
        choices=("text", "csv", "json"),
        default="text",
    )
    return parser.parse_args()


def _default_budgets(n: int) -> list[int]:
    N = 1 << n
    log_n = max(1, math.ceil(math.log2(max(2, n))))
    return sorted(
        {
            0,
            n,
            2 * n,
            max(1, N // max(1, n * n)),
            max(1, N // max(1, n * log_n)),
            max(1, N // max(1, n)),
            N,
            3 * N,
        }
    )


def _parse_budgets(raw: str | None, n: int) -> list[int]:
    if raw is None:
        return _default_budgets(n)
    pieces = [piece.strip() for piece in raw.split(",")]
    if not pieces or any(not piece for piece in pieces):
        raise ValueError("--ancillas must be a comma-separated list of integers.")
    try:
        budgets = [int(piece) for piece in pieces]
    except ValueError as exc:
        raise ValueError(
            "--ancillas must be a comma-separated list of integers."
        ) from exc
    if any(value < 0 for value in budgets):
        raise ValueError("Ancillary budgets must be nonnegative.")
    return budgets


def _print_text(rows: list[dict[str, int]]) -> None:
    print("Global Hopf-frame ancilla-depth research ledger")
    print("Depth columns are unit-coefficient asymptotic term proxies, not exact depths.")
    print("The frame budget is the state-compiler workspace plus one clean suffix flag.")
    print(
        f"{'n':>3} {'N':>9} {'m':>9} {'frame':>9} {'t':>4} {'unary':>9} "
        f"{'tail':>5} {'prefix':>8} {'pred':>8} {'UCG-lin':>8} "
        f"{'UCG-exp':>8} {'total':>8} {'N/(n+m)':>9} {'n(n-t+1)':>10}"
    )
    for row in rows:
        print(
            f"{row['n']:>3} {row['dimension']:>9} "
            f"{row['state_ancillas']:>9} {row['frame_ancillas']:>9} "
            f"{row['unary_prefix_qubits']:>4} "
            f"{row['unary_prefix_ancilla_upper_bound']:>9} "
            f"{row['tail_layers']:>5} {row['prefix_depth_proxy']:>8} "
            f"{row['tail_predicate_depth_proxy']:>8} "
            f"{row['ucg_linear_depth_proxy']:>8} "
            f"{row['ucg_exponential_depth_proxy']:>8} "
            f"{row['total_frame_depth_proxy']:>8} "
            f"{row['theorem_geometric_term']:>9} "
            f"{row['theorem_sequential_term']:>10}"
        )
    print("\nCandidate theorem form:")
    print("  size = O(N)")
    print("  depth = O(n (n - t + 1) + N/(n + m))")
    print("  t = min(n, max(0, floor(log2(m/3))))")
    print("The exact Hopf bridge and unary-code identities are tested separately.")


def _print_csv(rows: list[dict[str, int]]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)


def main() -> int:
    args = parse_args()
    if args.n < 1:
        print("error: n must be positive.", file=sys.stderr)
        return 2
    try:
        budgets = _parse_budgets(args.ancillas, args.n)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rows = [asdict(row) for row in ancilla_depth_rows(args.n, budgets)]
    if args.format == "text":
        _print_text(rows)
    elif args.format == "csv":
        _print_csv(rows)
    else:
        payload = {
            "status": "research companion; not yet a manuscript-level claim",
            "scope": "exact all-to-all one-qubit-plus-CNOT global Hopf frame",
            "workspace_convention": {
                "state_compiler": "m clean ancillary qubits",
                "frame_compiler": "m plus one reusable clean suffix flag",
            },
            "depth_formula": "O(n*(n-t+1) + 2**n/(n+m))",
            "prefix_choice": "t=min(n,max(0,floor(log2(m/3))))",
            "rows": rows,
            "interpretation": {
                "numeric_depth_columns": (
                    "unit-coefficient proxies for asymptotic contributions, "
                    "not exact gate depths"
                ),
                "finite_exact_checks": (
                    "conditioned-prefix frame identity and unary-code action"
                ),
                "external_theorems": (
                    "uniformly controlled gate and unary-to-binary synthesis"
                ),
                "checkpoint_scope": "not covered",
            },
        }
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
