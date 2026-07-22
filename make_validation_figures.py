#!/usr/bin/env python3
"""Generate deterministic repository figures for the exact-logical QBP checks.

The figures summarize Qibo statevector identities already exercised by the
unit-test suite.  They are validation plots, not optimization, timing, scaling,
or finite-shot performance experiments.

Run from the repository root with::

    python make_validation_figures.py

By default, PNG outputs are written to the repository root.
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
from qibo import models

from qbp_validation.cases import (
    balanced_poly_tree,
    complex_theta_mag,
    observables,
    theta_ph,
    poly_angles,
    regular_theta_mag,
    singular_theta_mag,
    unbalanced_poly_tree,
)
from qbp_validation.circuits import (
    add_phase_layer,
    add_real_frame,
    complex_checkpoint_measurement_circuit,
    complex_magnitude_measurement_circuit,
    complex_phase_measurement_circuit,
    depth_preparation_circuit,
    frame_circuit,
    polyspherical_frame_circuit,
    polyspherical_global_measurement_circuit,
    probabilities,
    real_checkpoint_measurement_circuit,
    real_global_measurement_circuit,
    statevector,
)
from qbp_validation.conventions import marker_map, poly_relative_markers
from qbp_validation.decoders import (
    decode_balanced_magnitude_gradient,
    decode_checkpoint_gradient,
    decode_phase_gradient,
    decode_polyspherical_gradient,
)
from qbp_validation.reference import (
    complex_magnitude_gradient,
    complex_phase_gradient,
    complex_state,
    polyspherical_gradient,
    polyspherical_shifted_frame_matrix,
    polyspherical_tree_data,
    real_frame_matrix,
    real_gradient,
    real_tree_data,
)

BLUE = "#1f4e79"
INDIGO = "#4b5fa8"
TEAL = "#2a7f8f"
ORANGE = "#eb6426"
GRAY = "0.45"
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


def collect_validation_data() -> tuple[OrderedDict[str, float], OrderedDict[str, tuple[list[float], list[float]]]]:
    """Run the deterministic finite-size checks used by the README figures."""

    residuals: OrderedDict[str, float] = OrderedDict(
        (
            ("Real frame", 0.0),
            ("Real global estimator", 0.0),
            ("Complex magnitude", 0.0),
            ("Complex phase", 0.0),
            ("Real checkpoints", 0.0),
            ("Complex checkpoints", 0.0),
            ("Singular charts", 0.0),
            ("Polyspherical frames", 0.0),
            ("Four-qubit appendix", 0.0),
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

    # Balanced frames and exact global/checkpoint estimators for n=1,...,4.
    for n in range(1, 5):
        regular = regular_theta_mag(n)
        singular = singular_theta_mag(n)
        N = 1 << n

        for theta in (regular, singular):
            qibo_frame = np.asarray(frame_circuit(theta).unitary(), dtype=complex)
            reference_frame = np.asarray(real_frame_matrix(theta), dtype=complex)
            residuals["Real frame"] = max(
                residuals["Real frame"],
                _max_abs(qibo_frame, reference_frame),
                _max_abs(qibo_frame.conj().T @ qibo_frame, np.eye(N)),
                _max_abs(statevector(depth_preparation_circuit(theta)), real_tree_data(theta).state),
            )

        real_data = real_tree_data(regular)
        magnitudes = complex_theta_mag(n)
        leaf_theta_ph = theta_ph(n)
        complex_data = real_tree_data(magnitudes)

        # The phase-dressed frame is compared as a full matrix, not only column by column.
        phase_frame = models.Circuit(n)
        system = tuple(range(n))
        add_real_frame(phase_frame, magnitudes, system)
        add_phase_layer(phase_frame, leaf_theta_ph, system)
        qibo_phase_frame = np.asarray(phase_frame.unitary(), dtype=complex)
        expected_phase_frame = np.diag(np.exp(1j * leaf_theta_ph)) @ real_frame_matrix(magnitudes)
        residuals["Complex magnitude"] = max(
            residuals["Complex magnitude"],
            _max_abs(qibo_phase_frame, expected_phase_frame),
            _max_abs(qibo_phase_frame[:, 0], complex_state(magnitudes, leaf_theta_ph)),
        )

        for observable in observables(n):
            real_probs = probabilities(real_global_measurement_circuit(regular, observable))
            real_decoded = decode_balanced_magnitude_gradient(real_probs, real_data.sqrt_metric, n)
            real_exact = real_gradient(regular, observable)
            real_residual = _append_pair(parity_points, "Real global", real_exact, real_decoded)
            residuals["Real global estimator"] = max(
                residuals["Real global estimator"], real_residual, abs(float(real_probs.sum()) - 1.0)
            )

            mag_probs = probabilities(
                complex_magnitude_measurement_circuit(magnitudes, leaf_theta_ph, observable)
            )
            mag_decoded = decode_balanced_magnitude_gradient(mag_probs, complex_data.sqrt_metric, n)
            mag_exact = complex_magnitude_gradient(magnitudes, leaf_theta_ph, observable)
            residuals["Complex magnitude"] = max(
                residuals["Complex magnitude"],
                _append_pair(parity_points, "Complex magnitude", mag_exact, mag_decoded),
            )

            phase_probs = probabilities(
                complex_phase_measurement_circuit(magnitudes, leaf_theta_ph, observable)
            )
            phase_decoded = decode_phase_gradient(phase_probs)
            phase_exact = complex_phase_gradient(magnitudes, leaf_theta_ph, observable)
            residuals["Complex phase"] = max(
                residuals["Complex phase"],
                _append_pair(parity_points, "Complex phase", phase_exact, phase_decoded),
                abs(float(phase_decoded.sum())),
            )

            for depth in range(n):
                start = (1 << depth) - 1
                stop = (1 << (depth + 1)) - 1

                real_checkpoint = decode_checkpoint_gradient(
                    probabilities(real_checkpoint_measurement_circuit(regular, observable, depth)),
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
                        complex_checkpoint_measurement_circuit(
                            magnitudes, leaf_theta_ph, observable, depth
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

    # Singular-chart estimator checks, including exactly vanishing coordinates.
    for n in range(2, 5):
        theta = singular_theta_mag(n)
        data = real_tree_data(theta)
        leaf_theta_ph = theta_ph(n)
        observable = observables(n)[-1]
        exact_real = real_gradient(theta, observable)
        decoded_real = decode_balanced_magnitude_gradient(
            probabilities(real_global_measurement_circuit(theta, observable)), data.sqrt_metric, n
        )
        residuals["Singular charts"] = max(
            residuals["Singular charts"],
            _append_pair(parity_points, "Real global", exact_real, decoded_real),
        )
        zero_indices = np.flatnonzero(data.metric < 1.0e-28)
        if zero_indices.size:
            residuals["Singular charts"] = max(
                residuals["Singular charts"],
                float(np.max(np.abs(decoded_real[zero_indices]))),
            )

        exact_complex = complex_magnitude_gradient(theta, leaf_theta_ph, observable)
        for depth in range(n):
            start = (1 << depth) - 1
            stop = (1 << (depth + 1)) - 1
            decoded_real_checkpoint = decode_checkpoint_gradient(
                probabilities(real_checkpoint_measurement_circuit(theta, observable, depth)),
                n,
                depth,
            )
            decoded_complex_checkpoint = decode_checkpoint_gradient(
                probabilities(
                    complex_checkpoint_measurement_circuit(
                        theta, leaf_theta_ph, observable, depth
                    )
                ),
                n,
                depth,
            )
            residuals["Singular charts"] = max(
                residuals["Singular charts"],
                _append_pair(
                    parity_points,
                    "Checkpoints",
                    exact_real[start:stop],
                    decoded_real_checkpoint,
                ),
                _append_pair(
                    parity_points,
                    "Checkpoints",
                    exact_complex[start:stop],
                    decoded_complex_checkpoint,
                ),
            )

    # Zero-amplitude complex leaf-phase case.
    n = 3
    magnitudes = complex_theta_mag(n)
    magnitudes[0] = 0.0
    leaf_theta_ph = theta_ph(n)
    observable = observables(n)[-1]
    exact_phase = complex_phase_gradient(magnitudes, leaf_theta_ph, observable)
    decoded_phase = decode_phase_gradient(
        probabilities(complex_phase_measurement_circuit(magnitudes, leaf_theta_ph, observable))
    )
    residuals["Complex phase"] = max(
        residuals["Complex phase"],
        _append_pair(parity_points, "Complex phase", exact_phase, decoded_phase),
        float(np.max(np.abs(decoded_phase[4:]))),
    )

    # Representative balanced and unbalanced polyspherical trees.
    balanced = balanced_poly_tree(list(range(8)))
    poly_cases = (
        (balanced, poly_angles(balanced, 6100)),
        (unbalanced_poly_tree(), poly_angles(unbalanced_poly_tree(), 6200)),
    )
    for tree, angles in poly_cases:
        n = 3
        qibo_frame = np.asarray(polyspherical_frame_circuit(tree, angles, n).unitary())
        reference_frame = polyspherical_shifted_frame_matrix(tree, angles, n)
        residuals["Polyspherical frames"] = max(
            residuals["Polyspherical frames"],
            _max_abs(qibo_frame, reference_frame),
            _max_abs(qibo_frame.conj().T @ qibo_frame, np.eye(1 << n)),
        )
        data = polyspherical_tree_data(tree, angles, n)
        for observable in observables(n):
            decoded = decode_polyspherical_gradient(
                probabilities(
                    polyspherical_global_measurement_circuit(tree, angles, n, observable)
                ),
                data.sqrt_metric,
                poly_relative_markers(tree),
            )
            exact = polyspherical_gradient(tree, angles, n, observable)
            residuals["Polyspherical frames"] = max(
                residuals["Polyspherical frames"],
                max(abs(decoded[key] - exact[key]) for key in exact),
            )

    # Four-qubit appendix formulas, including every checkpoint depth.
    theta = regular_theta_mag(4)
    data = real_tree_data(theta)
    expected_markers = {
        1: 0b1000,
        2: 0b0100,
        3: 0b1100,
        4: 0b0010,
        5: 0b0110,
        6: 0b1010,
        7: 0b1110,
        8: 0b0001,
        9: 0b0011,
        10: 0b0101,
        11: 0b0111,
        12: 0b1001,
        13: 0b1011,
        14: 0b1101,
        15: 0b1111,
    }
    if marker_map(4) != expected_markers:
        raise AssertionError("The four-qubit marker map differs from the appendix table.")
    expected_node_five = np.zeros(16, dtype=float)
    expected_node_five[0b0100] = -np.sin(theta[4]) * np.cos(theta[9])
    expected_node_five[0b0101] = -np.sin(theta[4]) * np.sin(theta[9])
    expected_node_five[0b0110] = np.cos(theta[4]) * np.cos(theta[10])
    expected_node_five[0b0111] = np.cos(theta[4]) * np.sin(theta[10])
    residuals["Four-qubit appendix"] = max(
        residuals["Four-qubit appendix"],
        _max_abs(data.complements[5], expected_node_five),
        abs(data.sqrt_metric[4] - np.cos(theta[0]) * np.sin(theta[1])),
    )
    observable = observables(4)[-1]
    exact = real_gradient(theta, observable)
    for depth in range(4):
        start = (1 << depth) - 1
        stop = (1 << (depth + 1)) - 1
        decoded = decode_checkpoint_gradient(
            probabilities(real_checkpoint_measurement_circuit(theta, observable, depth)),
            4,
            depth,
        )
        residuals["Four-qubit appendix"] = max(
            residuals["Four-qubit appendix"],
            _max_abs(decoded, exact[start:stop]),
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
    values = np.asarray([max(residuals[label], DISPLAY_FLOOR) for label in labels], dtype=float)
    positions = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(7.2, 4.45))
    ax.scatter(values, positions, s=46, color=BLUE, zorder=3)
    for x, y, actual in zip(values, positions, residuals.values()):
        text = "0" if actual == 0.0 else f"{actual:.1e}"
        ax.annotate(text, (x, y), xytext=(7, 0), textcoords="offset points", va="center", fontsize=8)

    ax.axvline(TOLERANCE, color=GRAY, linestyle="--", linewidth=1.1, label=r"test tolerance $3\times10^{-12}$")
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
    styles = OrderedDict(
        (
            ("Real global", (BLUE, "o")),
            ("Complex magnitude", (INDIGO, "s")),
            ("Complex phase", (TEAL, "^")),
            ("Checkpoints", (ORANGE, "D")),
        )
    )

    all_values: list[float] = []
    maximum_residual = 0.0
    fig, ax = plt.subplots(figsize=(5.25, 4.45))
    for family, (analytic, decoded) in points.items():
        x = np.asarray(analytic, dtype=float)
        y = np.asarray(decoded, dtype=float)
        all_values.extend(x.tolist())
        all_values.extend(y.tolist())
        maximum_residual = max(maximum_residual, _max_abs(x, y))
        if x.size > 80:
            selected = np.unique(np.linspace(0, x.size - 1, 80, dtype=int))
            x_plot = x[selected]
            y_plot = y[selected]
        else:
            x_plot = x
            y_plot = y
        color, point_marker = styles[family]
        ax.scatter(
            x_plot,
            y_plot,
            s=24,
            marker=point_marker,
            facecolors="none" if family == "Checkpoints" else color,
            edgecolors=color,
            linewidths=0.8,
            alpha=0.68,
            label=family,
            zorder=3,
        )

    bound = max(abs(min(all_values)), abs(max(all_values))) if all_values else 1.0
    bound *= 1.08
    ax.plot([-bound, bound], [-bound, bound], color=GRAY, linestyle="--", linewidth=1.1, label="identity")
    ax.axhline(0.0, color="0.8", linewidth=0.7, zorder=0)
    ax.axvline(0.0, color="0.8", linewidth=0.7, zorder=0)
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
        color="0.35",
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
