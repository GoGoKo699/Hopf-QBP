#!/usr/bin/env python3
"""Generate deterministic summary figures for exact-logical Hopf-QBP checks.

The figures summarize statevector identities already exercised by the unit-test
suite. They are validation plots, not optimization, timing, scaling, finite-shot,
or hardware-performance experiments.
"""
from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["pdf.fonttype"] = 42
matplotlib.rcParams["ps.fonttype"] = 42
matplotlib.rcParams["svg.fonttype"] = "none"

import matplotlib.pyplot as plt
import numpy as np

from qbp_validation.cases import (
    complex_theta_mag,
    observables,
    regular_theta_mag,
    singular_theta_mag,
    theta_ph,
)
from qbp_validation.circuits import (
    b2c_4q_circuit,
    complex_checkpoint_integrated_depth2_4q_circuit,
    complex_checkpoint_separated_circuit,
    complex_frame_rc_4q_circuit,
    complex_frame_separated_circuit,
    complex_magnitude_integrated_4q_circuit,
    complex_magnitude_separated_circuit,
    complex_phase_measurement_circuit,
    depth_preparation_circuit,
    frame_circuit,
    native_complex_circuit,
    native_real_circuit,
    probabilities,
    real_checkpoint_measurement_circuit,
    real_global_measurement_circuit,
)
from qbp_validation.conventions import checkpoint_interface_projector, marker_map
from qbp_validation.decoders import (
    decode_balanced_magnitude_gradient,
    decode_checkpoint_gradient,
    decode_phase_gradient,
)
from qbp_validation.reference import (
    addressed_rc_frame_matrix_4q,
    centered_leaf_phases,
    complex_frame_matrix,
    complex_magnitude_gradient,
    complex_phase_gradient,
    complex_state,
    depth_suffix_matrix,
    phase_layer_matrix,
    real_frame_matrix,
    real_gradient,
    real_state,
    real_tree_data,
)

TOLERANCE = 3.0e-12
DISPLAY_FLOOR = 1.0e-17


def _max_abs(first: np.ndarray | Iterable[float], second: np.ndarray | Iterable[float]) -> float:
    a = np.asarray(first, dtype=complex)
    b = np.asarray(second, dtype=complex)
    if a.shape != b.shape:
        raise ValueError(f"Residual operands have different shapes: {a.shape} and {b.shape}.")
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def _append_pair(
    points: OrderedDict[str, tuple[list[float], list[float]]],
    family: str,
    analytic: np.ndarray | Iterable[float],
    decoded: np.ndarray | Iterable[float],
) -> float:
    x = np.asarray(analytic, dtype=float).reshape(-1)
    y = np.asarray(decoded, dtype=float).reshape(-1)
    if x.shape != y.shape:
        raise ValueError(f"Parity operands have different shapes: {x.shape} and {y.shape}.")
    points[family][0].extend(x.tolist())
    points[family][1].extend(y.tolist())
    return _max_abs(x, y)


def collect_validation_data() -> tuple[
    OrderedDict[str, float], OrderedDict[str, tuple[list[float], list[float]]]
]:
    residuals: OrderedDict[str, float] = OrderedDict(
        (
            ("State-column contracts", 0.0),
            ("Real frame", 0.0),
            (r"Complex $W_C$ frame", 0.0),
            ("Real global", 0.0),
            ("Complex magnitude", 0.0),
            ("Complex phase", 0.0),
            ("Real checkpoints", 0.0),
            ("Complex checkpoints", 0.0),
            (r"$B_{2,C}$ interface", 0.0),
            ("Singular coordinates", 0.0),
            ("Four-qubit ledger", 0.0),
        )
    )
    parity_points: OrderedDict[str, tuple[list[float], list[float]]] = OrderedDict(
        (
            ("Real global", ([], [])),
            ("Complex magnitude", ([], [])),
            ("Complex phase", ([], [])),
            ("Checkpoints", ([], [])),
        )
    )

    for n in range(1, 5):
        real_theta = regular_theta_mag(n)
        mag = complex_theta_mag(n)
        phase = theta_ph(n)
        real_data = real_tree_data(real_theta)
        complex_data = real_tree_data(mag)

        native_real = np.asarray(native_real_circuit(real_theta).unitary())
        depth_real = np.asarray(depth_preparation_circuit(real_theta).unitary())
        frame_real = np.asarray(frame_circuit(real_theta).unitary())
        residuals["State-column contracts"] = max(
            residuals["State-column contracts"],
            _max_abs(native_real[:, 0], real_state(real_theta)),
            _max_abs(depth_real[:, 0], real_state(real_theta)),
            _max_abs(frame_real[:, 0], real_state(real_theta)),
        )
        residuals["Real frame"] = max(
            residuals["Real frame"], _max_abs(frame_real, real_frame_matrix(real_theta))
        )

        native_complex = np.asarray(native_complex_circuit(mag, phase).unitary())
        separated_frame = np.asarray(complex_frame_separated_circuit(mag, phase).unitary())
        residuals["State-column contracts"] = max(
            residuals["State-column contracts"],
            _max_abs(native_complex[:, 0], complex_state(mag, phase)),
            _max_abs(separated_frame[:, 0], complex_state(mag, phase)),
        )
        residuals[r"Complex $W_C$ frame"] = max(
            residuals[r"Complex $W_C$ frame"],
            _max_abs(separated_frame, complex_frame_matrix(mag, phase)),
        )

        for observable in observables(n):
            real_probs = probabilities(real_global_measurement_circuit(real_theta, observable))
            real_decoded = decode_balanced_magnitude_gradient(
                real_probs, real_data.sqrt_metric, n
            )
            real_exact = real_gradient(real_theta, observable)
            residuals["Real global"] = max(
                residuals["Real global"],
                _append_pair(parity_points, "Real global", real_exact, real_decoded),
            )

            mag_probs = probabilities(
                complex_magnitude_separated_circuit(mag, phase, observable)
            )
            mag_decoded = decode_balanced_magnitude_gradient(
                mag_probs, complex_data.sqrt_metric, n
            )
            mag_exact = complex_magnitude_gradient(mag, phase, observable)
            residuals["Complex magnitude"] = max(
                residuals["Complex magnitude"],
                _append_pair(
                    parity_points, "Complex magnitude", mag_exact, mag_decoded
                ),
            )

            phase_probs = probabilities(
                complex_phase_measurement_circuit(mag, phase, observable)
            )
            phase_decoded = decode_phase_gradient(phase_probs)
            phase_exact = complex_phase_gradient(mag, phase, observable)
            residuals["Complex phase"] = max(
                residuals["Complex phase"],
                _append_pair(parity_points, "Complex phase", phase_exact, phase_decoded),
                abs(float(phase_decoded.sum())),
            )

            for depth in range(n):
                start = (1 << depth) - 1
                stop = (1 << (depth + 1)) - 1
                real_checkpoint = decode_checkpoint_gradient(
                    probabilities(
                        real_checkpoint_measurement_circuit(
                            real_theta, observable, depth
                        )
                    ),
                    n,
                    depth,
                )
                residuals["Real checkpoints"] = max(
                    residuals["Real checkpoints"],
                    _append_pair(
                        parity_points,
                        "Checkpoints",
                        real_exact[start:stop],
                        real_checkpoint,
                    ),
                )
                complex_checkpoint = decode_checkpoint_gradient(
                    probabilities(
                        complex_checkpoint_separated_circuit(
                            mag, phase, observable, depth
                        )
                    ),
                    n,
                    depth,
                )
                residuals["Complex checkpoints"] = max(
                    residuals["Complex checkpoints"],
                    _append_pair(
                        parity_points,
                        "Checkpoints",
                        mag_exact[start:stop],
                        complex_checkpoint,
                    ),
                )

    # Four-qubit integrated complex frame and checkpoint interface.
    mag = complex_theta_mag(4)
    phase = theta_ph(4)
    mean, _ = centered_leaf_phases(phase)
    integrated_frame = np.asarray(complex_frame_rc_4q_circuit(mag, phase).unitary())
    residuals[r"Complex $W_C$ frame"] = max(
        residuals[r"Complex $W_C$ frame"],
        _max_abs(integrated_frame, addressed_rc_frame_matrix_4q(mag, phase)),
        _max_abs(integrated_frame, np.exp(-1j * mean) * complex_frame_matrix(mag, phase)),
    )

    b2c = np.asarray(b2c_4q_circuit(mag, phase).unitary())
    separated_b2c = phase_layer_matrix(phase) @ depth_suffix_matrix(mag, 2)
    projector = checkpoint_interface_projector(4, 2)
    residuals[r"$B_{2,C}$ interface"] = max(
        residuals[r"$B_{2,C}$ interface"],
        _max_abs(b2c @ projector, separated_b2c @ projector),
    )

    for observable in observables(4):
        exact = complex_magnitude_gradient(mag, phase, observable)
        integrated_global = decode_balanced_magnitude_gradient(
            probabilities(
                complex_magnitude_integrated_4q_circuit(mag, phase, observable)
            ),
            real_tree_data(mag).sqrt_metric,
            4,
        )
        residuals["Complex magnitude"] = max(
            residuals["Complex magnitude"],
            _append_pair(
                parity_points, "Complex magnitude", exact, integrated_global
            ),
        )
        integrated_checkpoint = decode_checkpoint_gradient(
            probabilities(
                complex_checkpoint_integrated_depth2_4q_circuit(
                    mag, phase, observable
                )
            ),
            4,
            2,
        )
        residuals[r"$B_{2,C}$ interface"] = max(
            residuals[r"$B_{2,C}$ interface"],
            _append_pair(
                parity_points, "Checkpoints", exact[3:7], integrated_checkpoint
            ),
        )

    # Singular-coordinate checks.
    for n in range(2, 5):
        theta = singular_theta_mag(n)
        data = real_tree_data(theta)
        observable = observables(n)[-1]
        exact = real_gradient(theta, observable)
        decoded = decode_balanced_magnitude_gradient(
            probabilities(real_global_measurement_circuit(theta, observable)),
            data.sqrt_metric,
            n,
        )
        residuals["Singular coordinates"] = max(
            residuals["Singular coordinates"], _max_abs(decoded, exact)
        )

    # Appendix marker map and ledger values.
    expected_markers = {
        1: 8, 2: 4, 3: 12, 4: 2, 5: 6, 6: 10, 7: 14,
        8: 1, 9: 3, 10: 5, 11: 7, 12: 9, 13: 11, 14: 13, 15: 15,
    }
    residuals["Four-qubit ledger"] = max(
        residuals["Four-qubit ledger"],
        0.0 if marker_map(4) == expected_markers else 1.0,
    )

    return residuals, parity_points


def _save(
    fig: plt.Figure,
    output_dir: Path,
    stem: str,
    formats: tuple[str, ...],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for extension in formats:
        path = output_dir / f"{stem}.{extension}"
        if extension == "png":
            fig.savefig(path, dpi=300, bbox_inches="tight")
        else:
            fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def plot_residual_summary(
    residuals: OrderedDict[str, float],
    output_dir: Path,
    formats: tuple[str, ...],
) -> None:
    labels = list(residuals)
    values = np.asarray(
        [max(residuals[label], DISPLAY_FLOOR) for label in labels], dtype=float
    )
    positions = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    ax.scatter(values, positions, s=44, zorder=3)
    for x, y, actual in zip(values, positions, residuals.values()):
        text = "0" if actual == 0.0 else f"{actual:.1e}"
        ax.annotate(
            text,
            (x, y),
            xytext=(7, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
        )
    ax.axvline(
        TOLERANCE,
        linestyle="--",
        linewidth=1.1,
        label=r"test tolerance $3\times10^{-12}$",
    )
    ax.set_xscale("log")
    ax.set_xlim(DISPLAY_FLOOR * 0.7, TOLERANCE * 7.0)
    ax.set_yticks(positions)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Maximum absolute Qibo–reference residual")
    ax.grid(True, axis="x", which="both", alpha=0.22)
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    fig.tight_layout()
    _save(fig, output_dir, "exact_logical_validation_residuals", formats)


def plot_gradient_parity(
    points: OrderedDict[str, tuple[list[float], list[float]]],
    output_dir: Path,
    formats: tuple[str, ...],
) -> None:
    markers = {
        "Real global": "o",
        "Complex magnitude": "s",
        "Complex phase": "^",
        "Checkpoints": "D",
    }
    all_values: list[float] = []
    maximum_residual = 0.0
    fig, ax = plt.subplots(figsize=(5.25, 4.45))
    for family, (analytic, decoded) in points.items():
        x = np.asarray(analytic, dtype=float)
        y = np.asarray(decoded, dtype=float)
        all_values.extend(x.tolist())
        all_values.extend(y.tolist())
        maximum_residual = max(maximum_residual, _max_abs(x, y))
        if x.size > 90:
            selected = np.unique(np.linspace(0, x.size - 1, 90, dtype=int))
            x = x[selected]
            y = y[selected]
        ax.scatter(x, y, s=24, marker=markers[family], alpha=0.68, label=family)

    bound = max(abs(min(all_values)), abs(max(all_values))) if all_values else 1.0
    bound *= 1.08
    ax.plot([-bound, bound], [-bound, bound], linestyle="--", linewidth=1.1, label="identity")
    ax.axhline(0.0, linewidth=0.7, zorder=0)
    ax.axvline(0.0, linewidth=0.7, zorder=0)
    ax.set_xlim(-bound, bound)
    ax.set_ylim(-bound, bound)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Independent analytic derivative")
    ax.set_ylabel("Qibo circuit-decoded derivative")
    ax.grid(True, alpha=0.18)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.text(
        0.98,
        0.03,
        rf"max $|\Delta|={maximum_residual:.1e}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
    )
    fig.tight_layout()
    _save(fig, output_dir, "circuit_decoded_gradient_parity", formats)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Regenerate deterministic Hopf-QBP validation figures."
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Output directory (default: repository root).",
    )
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=("png", "pdf", "svg"),
        default=("png",),
        help="One or more output formats (default: png).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    formats = tuple(dict.fromkeys(args.formats))
    residuals, parity_points = collect_validation_data()
    plot_residual_summary(residuals, args.outdir, formats)
    plot_gradient_parity(parity_points, args.outdir, formats)

    print("Exact-logical validation residuals:")
    for label, value in residuals.items():
        print(f"  {label:<26} {value:.6e}")
    print(f"Wrote {', '.join(formats)} figures to {args.outdir.resolve()}")


if __name__ == "__main__":
    main()
