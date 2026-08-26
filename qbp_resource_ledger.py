#!/usr/bin/env python3
"""Print the manuscript's conservative compiler-relative assigned CNOT ledger.

This is the concrete no-clean-ancilla ledger used for the manuscript's finite
examples. It is not an optimal-synthesis claim. See
``qbp_optimized_resource_ledger.py`` for the uniformly controlled-rotation
companion.
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
    four_qubit_complex_frame_cnot_charge,
    four_qubit_complex_suffix_cnot_charge,
    frame_cnot_charge,
    inverse_suffix_cnot_charge,
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
    addressed_real_frame: int


def ledger_row(n: int) -> LedgerRow:
    return LedgerRow(
        n=n,
        native_real=native_real_cnot_charge(n),
        native_complex=native_complex_cnot_charge(n),
        checkpoint_preparation=depth_preparation_cnot_charge(n),
        addressed_real_frame=frame_cnot_charge(n),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the conservative assigned Hopf-QBP CNOT ledger."
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


def four_qubit_details() -> dict[str, object]:
    native_real = native_real_cnot_charge(4)
    native_complex = native_complex_cnot_charge(4)
    b2 = inverse_suffix_cnot_charge(4, 2)
    wc = four_qubit_complex_frame_cnot_charge()
    b2c = four_qubit_complex_suffix_cnot_charge()
    return {
        "compiler_objects": {
            "HopfReal": native_real,
            "HopfComplex": native_complex,
            "U_chk": depth_preparation_cnot_charge(4),
            "W_R": frame_cnot_charge(4),
            "W_C": wc,
            "B_2": b2,
            "B_2_C": b2c,
        },
        "depth_layers": [depth_layer_cnot_charge(depth) for depth in range(4)],
        "checkpoint_designated": [
            checkpoint_cnot_charge_without_observable(4, depth)
            for depth in range(4)
        ],
        "checkpoint_native_forward": [
            native_real + inverse_suffix_cnot_charge(4, depth)
            for depth in range(4)
        ],
        "record_circuits_excluding_observable_and_readout": {
            "real_global": native_real + frame_cnot_charge(4),
            "complex_global": native_complex + wc,
            "direct_complex_phase": native_complex,
            "real_checkpoint_depth2": native_real + b2,
            "complex_checkpoint_depth2": native_complex + b2c,
        },
    }


def _print_text(rows: list[LedgerRow]) -> None:
    print("Conservative assigned CNOT charges; controlled observable and phase-layer charge excluded")
    print("These finite counts are not an optimal-synthesis claim.")
    print("Optimized companion: python qbp_optimized_resource_ledger.py")
    print(
        f"{'n':>2} {'HopfReal':>12} {'HopfComplex':>14} "
        f"{'U_chk':>12} {'W_R':>12}"
    )
    for row in rows:
        print(
            f"{row.n:>2} {row.native_real:>12} {row.native_complex:>14} "
            f"{row.checkpoint_preparation:>12} {row.addressed_real_frame:>12}"
        )

    if any(row.n == 4 for row in rows):
        detail = four_qubit_details()
        objects = detail["compiler_objects"]
        records = detail["record_circuits_excluding_observable_and_readout"]
        assert isinstance(objects, dict) and isinstance(records, dict)
        print("\nFour-qubit manuscript detail")
        for name in ("HopfReal", "HopfComplex", "U_chk", "W_R", "W_C", "B_2", "B_2_C"):
            print(f"{name:<18} {objects[name]:>5}")
        print("\ndepth d                    0       1       2       3")
        print(
            "layer U_d             "
            + " ".join(f"{value:>7}" for value in detail["depth_layers"])
        )
        print(
            "designated checkpoint "
            + " ".join(f"{value:>7}" for value in detail["checkpoint_designated"])
        )
        print(
            "native-forward chk.   "
            + " ".join(f"{value:>7}" for value in detail["checkpoint_native_forward"])
        )
        print("\nRecord circuits before controlled-O and readout")
        for name, value in records.items():
            print(f"{name:<30} {value:>5}")
        print("\nSeparated complex ledgers retain the symbolic phase-layer charge C_ph.")


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
        payload = {
            "interpretation": "conservative assigned finite ledger, not optimal synthesis",
            "optimized_companion": "qbp_optimized_resource_ledger.py",
            "rows": [asdict(row) for row in rows],
            "four_qubit": four_qubit_details() if args.nmin <= 4 <= args.nmax else None,
        }
        print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
