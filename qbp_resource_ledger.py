#!/usr/bin/env python3
"""Print the assigned logical CNOT ledger used by the Hopf-QBP manuscript.

The values are compiler-relative charges from the manuscript's no-clean-ancilla
model.  They are not Qibo transpiler counts and exclude the controlled observable
and any separately assigned phase-layer workspace or synthesis cost.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass

from qbp_validation.conventions import (
    checkpoint_cnot_charge_without_observable,
    depth_layer_cnot_charge,
    depth_preparation_cnot_charge,
    frame_cnot_charge,
)
from qbp_validation.native_schedule import (
    native_complex_cnot_charge,
    native_real_cnot_charge,
)


@dataclass(frozen=True)
class LedgerRow:
    n: int
    native_real: int
    native_complex: int
    checkpoint_preparation: int
    addressed_frame: int


def ledger_row(n: int) -> LedgerRow:
    return LedgerRow(
        n=n,
        native_real=native_real_cnot_charge(n),
        native_complex=native_complex_cnot_charge(n),
        checkpoint_preparation=depth_preparation_cnot_charge(n),
        addressed_frame=frame_cnot_charge(n),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the Hopf-QBP assigned CNOT ledger."
    )
    parser.add_argument("--nmin", type=int, default=2)
    parser.add_argument("--nmax", type=int, default=10)
    parser.add_argument(
        "--format",
        choices=("text", "csv", "json"),
        default="text",
        help="Output format (default: text).",
    )
    return parser.parse_args()


def _validate_range(nmin: int, nmax: int) -> None:
    if nmin < 1 or nmax < nmin:
        raise ValueError("Require 1 <= nmin <= nmax.")


def _print_text(rows: list[LedgerRow]) -> None:
    print("Assigned CNOT charges; controlled observable and phase-layer charge excluded")
    print(
        f"{'n':>2} {'HopfReal':>12} {'HopfComplex':>14} "
        f"{'U_chk':>12} {'W_R':>12}"
    )
    for row in rows:
        print(
            f"{row.n:>2} {row.native_real:>12} {row.native_complex:>14} "
            f"{row.checkpoint_preparation:>12} {row.addressed_frame:>12}"
        )

    if any(row.n == 4 for row in rows):
        print("\nFour-qubit detail")
        print("depth d                 0       1       2       3")
        layers = [depth_layer_cnot_charge(depth) for depth in range(4)]
        checkpoints = [
            checkpoint_cnot_charge_without_observable(4, depth)
            for depth in range(4)
        ]
        print("layer U_d          " + " ".join(f"{value:>7}" for value in layers))
        print("checkpoint total   " + " ".join(f"{value:>7}" for value in checkpoints))
        print("completion comparison: HopfReal=100, U_chk=140, W_R=210")


def _print_csv(rows: list[LedgerRow]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=list(asdict(rows[0])))
    writer.writeheader()
    writer.writerows(asdict(row) for row in rows)


def main() -> int:
    args = parse_args()
    try:
        _validate_range(args.nmin, args.nmax)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    rows = [ledger_row(n) for n in range(args.nmin, args.nmax + 1)]
    if args.format == "text":
        _print_text(rows)
    elif args.format == "csv":
        _print_csv(rows)
    else:
        print(json.dumps([asdict(row) for row in rows], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
