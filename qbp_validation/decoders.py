"""Exact-distribution and record-level decoders for Hopf-QBP validation."""
from __future__ import annotations

import numpy as np

from .conventions import marker_label, parity


def fwht(values: np.ndarray) -> np.ndarray:
    """Return the unnormalized Walsh-Hadamard transform of a copy."""

    out = np.asarray(values, dtype=float).reshape(-1).copy()
    length = out.size
    if length == 0 or length & (length - 1):
        raise ValueError("FWHT input length must be a positive power of two.")
    width = 1
    while width < length:
        for start in range(0, length, 2 * width):
            first = out[start : start + width].copy()
            second = out[start + width : start + 2 * width].copy()
            out[start : start + width] = first + second
            out[start + width : start + 2 * width] = first - second
        width *= 2
    return out


def reshape_ancilla_system(probabilities: np.ndarray) -> np.ndarray:
    probs = np.asarray(probabilities, dtype=float).reshape(-1)
    if probs.size < 4 or probs.size & (probs.size - 1):
        raise ValueError(
            "Probability vector must describe one ancilla and at least one system qubit."
        )
    return probs.reshape(2, probs.size // 2)


def signed_system_histogram(probabilities: np.ndarray) -> np.ndarray:
    probs = reshape_ancilla_system(probabilities)
    return probs[0] - probs[1]


def global_moments_direct(probabilities: np.ndarray) -> np.ndarray:
    signed = signed_system_histogram(probabilities)
    N = signed.size
    moments = np.zeros(N, dtype=float)
    for label in range(N):
        moments[label] = sum(
            value * (-1.0 if parity(label, outcome) else 1.0)
            for outcome, value in enumerate(signed)
        )
    return moments


def global_moments_fwht(probabilities: np.ndarray) -> np.ndarray:
    return fwht(signed_system_histogram(probabilities))


def decode_balanced_magnitude_gradient(
    probabilities: np.ndarray,
    sqrt_metric: np.ndarray,
    n: int,
    *,
    use_fwht: bool = True,
) -> np.ndarray:
    """Decode all magnitude derivatives from one global-frame distribution."""

    sqrt_metric = np.asarray(sqrt_metric, dtype=float).reshape(-1)
    if sqrt_metric.size != (1 << n) - 1:
        raise ValueError("sqrt_metric length does not match n.")
    moments = (
        global_moments_fwht(probabilities)
        if use_fwht
        else global_moments_direct(probabilities)
    )
    return np.asarray(
        [
            2.0 * sqrt_metric[node - 1] * moments[marker_label(node, n)]
            for node in range(1, 1 << n)
        ],
        dtype=float,
    )


def decode_phase_gradient(probabilities: np.ndarray) -> np.ndarray:
    probs = reshape_ancilla_system(probabilities)
    return 2.0 * (probs[0] - probs[1])


def decode_checkpoint_gradient(probabilities: np.ndarray, n: int, depth: int) -> np.ndarray:
    if not 0 <= depth < n:
        raise ValueError("Depth must lie in 0, ..., n-1.")
    probs = reshape_ancilla_system(probabilities)
    width = 1 << depth
    result = np.zeros(width, dtype=float)
    target_shift = n - depth - 1
    for ancilla in (0, 1):
        for system_label in range(1 << n):
            prefix = system_label >> (n - depth) if depth else 0
            target = (system_label >> target_shift) & 1
            sign = -2.0 * (-1.0 if (ancilla + target) & 1 else 1.0)
            result[prefix] += sign * probs[ancilla, system_label]
    return result


def phase_record(ancilla_bit: int, leaf: int, N: int) -> np.ndarray:
    record = np.zeros(N, dtype=float)
    record[leaf] = 2.0 * (-1.0 if ancilla_bit else 1.0)
    return record


def checkpoint_record(
    ancilla_bit: int, target_bit: int, prefix: int, width: int
) -> np.ndarray:
    record = np.zeros(width, dtype=float)
    record[prefix] = -2.0 * (-1.0 if (ancilla_bit + target_bit) & 1 else 1.0)
    return record
