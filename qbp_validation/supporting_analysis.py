"""Qibo-free supporting analysis for Hopf-QBP.

This module collects consequences that are useful for scientific review and
engineering adaptation: complete-vector accuracy, conditional relative and
directional guarantees, magnitude-block natural-gradient conditioning,
common-phase gauge projection, reflection-sum term sampling, and analytic
readout-error transfer functions.
"""
from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _validate_probability(value: float, name: str) -> float:
    probability = float(value)
    if not 0.0 <= probability <= 1.0:
        raise ValueError(f"{name} must lie in [0, 1].")
    return probability


def fixed_norm_vector_shot_bound(
    record_norm: float,
    epsilon: float,
    failure_probability: float,
) -> int:
    """Return the manuscript's sufficient fixed-norm vector sample count."""

    radius = float(record_norm)
    accuracy = float(epsilon)
    eta = float(failure_probability)
    if radius < 0.0:
        raise ValueError("record_norm must be nonnegative.")
    if accuracy <= 0.0:
        raise ValueError("epsilon must be positive.")
    if not 0.0 < eta < 1.0:
        raise ValueError("failure_probability must lie strictly between 0 and 1.")
    factor = 1.0 + math.sqrt(2.0 * math.log(1.0 / eta))
    return int(math.ceil(radius * radius * factor * factor / (accuracy * accuracy)))


def complete_magnitude_record_norm(n: int) -> float:
    """Norm of all ``n`` global magnitude-depth records concatenated."""

    if n < 1:
        raise ValueError("n must be positive.")
    return 2.0 * math.sqrt(float(n))


def complete_magnitude_l2_shot_bound(
    n: int,
    epsilon_l2: float,
    failure_probability: float,
) -> int:
    """Sufficient executions for absolute complete-magnitude ``l2`` error."""

    return fixed_norm_vector_shot_bound(
        complete_magnitude_record_norm(n),
        epsilon_l2,
        failure_probability,
    )


def complete_magnitude_relative_l2_shot_bound(
    n: int,
    relative_error: float,
    gradient_norm: float,
    failure_probability: float,
) -> int:
    """Sufficient executions for relative ``l2`` error away from stationarity.

    The target absolute error is ``relative_error * gradient_norm``.  Requiring
    ``relative_error < 1`` also guarantees that the estimated negative gradient
    is a descent direction under the same event.
    """

    rho = float(relative_error)
    gradient = float(gradient_norm)
    if not 0.0 < rho < 1.0:
        raise ValueError("relative_error must lie strictly between 0 and 1.")
    if gradient <= 0.0:
        raise ValueError("gradient_norm must be positive.")
    return complete_magnitude_l2_shot_bound(
        n,
        rho * gradient,
        failure_probability,
    )


def direction_error_upper_bound(gradient_norm: float, error_norm: float) -> float:
    """Bound normalized-direction error when ``error_norm < gradient_norm``.

    Returns ``2*error_norm/gradient_norm``.  A finite directional guarantee is
    intentionally rejected at stationary points or when the error can reach the
    true gradient norm.
    """

    gradient = float(gradient_norm)
    error = float(error_norm)
    if gradient <= 0.0:
        raise ValueError("gradient_norm must be positive.")
    if error < 0.0:
        raise ValueError("error_norm must be nonnegative.")
    if error >= gradient:
        raise ValueError("directional control requires error_norm < gradient_norm.")
    return 2.0 * error / gradient


def descent_direction_is_guaranteed(gradient_norm: float, error_norm: float) -> bool:
    """Return whether ``-g_hat`` is guaranteed to descend for ``g_hat=g+e``."""

    gradient = float(gradient_norm)
    error = float(error_norm)
    if gradient < 0.0 or error < 0.0:
        raise ValueError("norms must be nonnegative.")
    return gradient > 0.0 and error < gradient


def ordinary_magnitude_record_second_moment(metric_factor: float) -> float:
    """Return ``E[Z_j^2] = 4*g_jj`` for an ordinary magnitude record."""

    metric = float(metric_factor)
    if metric < 0.0:
        raise ValueError("metric_factor must be nonnegative.")
    return 4.0 * metric


def natural_gradient_record_second_moment(metric_factor: float) -> float:
    """Return ``4/g_jj`` for the unregularized inverse-metric record."""

    metric = float(metric_factor)
    if metric <= 0.0:
        raise ValueError("metric_factor must be positive for an inverse metric.")
    return 4.0 / metric


def regularized_natural_gradient_record_second_moment(
    metric_factor: float,
    regularization: float,
) -> float:
    """Return ``4*g_jj/(g_jj+lambda)^2`` for a regularized inverse metric."""

    metric = float(metric_factor)
    lam = float(regularization)
    if metric < 0.0:
        raise ValueError("metric_factor must be nonnegative.")
    if lam <= 0.0:
        raise ValueError("regularization must be positive.")
    return 4.0 * metric / (metric + lam) ** 2


def regularized_natural_gradient_second_moment_bound(regularization: float) -> float:
    """Return the uniform bound ``1/lambda`` for the regularized second moment."""

    lam = float(regularization)
    if lam <= 0.0:
        raise ValueError("regularization must be positive.")
    return 1.0 / lam


def project_common_phase_gradient(gradient: object) -> np.ndarray:
    """Project a phase-gradient estimate onto the zero-sum physical subspace."""

    values = np.asarray(gradient, dtype=float).reshape(-1)
    if values.size == 0:
        raise ValueError("gradient must be nonempty.")
    return values - float(np.mean(values))


def reflection_sampling_probabilities(coefficients: object) -> np.ndarray:
    """Return ``|c_alpha| / sum |c_alpha|`` for a reflection decomposition."""

    values = np.asarray(coefficients, dtype=float).reshape(-1)
    if values.size == 0:
        raise ValueError("coefficients must be nonempty.")
    one_norm = float(np.sum(np.abs(values)))
    if one_norm == 0.0:
        raise ValueError("the all-zero Hamiltonian needs no sampling distribution.")
    return np.abs(values) / one_norm


def scaled_reflection_record(
    term_record: object,
    coefficient: float,
    coefficient_one_norm: float,
) -> np.ndarray:
    """Scale one sampled term record for unbiased reflection-sum estimation."""

    one_norm = float(coefficient_one_norm)
    value = float(coefficient)
    if one_norm <= 0.0:
        raise ValueError("coefficient_one_norm must be positive.")
    if abs(value) > one_norm + 1e-15:
        raise ValueError("coefficient magnitude cannot exceed the supplied one-norm.")
    return one_norm * float(np.sign(value)) * np.asarray(term_record, dtype=float)


def reflection_sum_expected_record(
    coefficients: object,
    term_records: object,
) -> np.ndarray:
    """Return the expectation of the one-norm term-sampling record."""

    values = np.asarray(coefficients, dtype=float).reshape(-1)
    records = np.asarray(term_records, dtype=float)
    if records.ndim < 2 or records.shape[0] != values.size:
        raise ValueError("term_records must have one leading entry per coefficient.")
    probabilities = reflection_sampling_probabilities(values)
    one_norm = float(np.sum(np.abs(values)))
    scaled = np.stack(
        [
            scaled_reflection_record(records[index], values[index], one_norm)
            for index in range(values.size)
        ],
        axis=0,
    )
    return np.tensordot(probabilities, scaled, axes=(0, 0))


def reflection_sum_record_norm_bound(
    coefficient_one_norm: float,
    base_record_norm: float = 2.0,
) -> float:
    """Return ``Lambda`` times the base fixed-norm record bound."""

    one_norm = float(coefficient_one_norm)
    base = float(base_record_norm)
    if one_norm < 0.0 or base < 0.0:
        raise ValueError("norm bounds must be nonnegative.")
    return one_norm * base


def parity_readout_attenuation(error_probabilities: Sequence[float]) -> float:
    """Attenuation of a parity under independent symmetric readout flips."""

    attenuation = 1.0
    for index, probability in enumerate(error_probabilities):
        p = _validate_probability(probability, f"error_probabilities[{index}]")
        attenuation *= 1.0 - 2.0 * p
    return float(attenuation)


def global_marker_readout_attenuation(
    marker: int,
    n: int,
    ancilla_error_probability: float,
    system_error_probabilities: Sequence[float],
) -> float:
    """Attenuation of ``(-1)^(b + marker dot y)`` under readout flips.

    System probabilities use the repository's big-endian system order.
    Only marker-supported bits enter the parity factor.
    """

    if n < 1:
        raise ValueError("n must be positive.")
    if not 0 <= int(marker) < 1 << n:
        raise ValueError("marker lies outside the n-bit system register.")
    if len(system_error_probabilities) != n:
        raise ValueError("system_error_probabilities must contain n entries.")

    selected = [_validate_probability(ancilla_error_probability, "ancilla_error_probability")]
    for system_index, probability in enumerate(system_error_probabilities):
        p = _validate_probability(probability, f"system_error_probabilities[{system_index}]")
        bit = (int(marker) >> (n - 1 - system_index)) & 1
        if bit:
            selected.append(p)
    return parity_readout_attenuation(selected)


def checkpoint_sign_readout_attenuation(
    ancilla_error_probability: float,
    target_error_probability: float,
) -> float:
    """Attenuation of the checkpoint sign ``(-1)^(b_c+b_t)``."""

    return parity_readout_attenuation(
        (ancilla_error_probability, target_error_probability)
    )


def phase_sign_readout_attenuation(ancilla_error_probability: float) -> float:
    """Attenuation of the direct phase-record sign."""

    return parity_readout_attenuation((ancilla_error_probability,))


def independent_bitflip_channel(error_probabilities: Sequence[float]) -> np.ndarray:
    """Return the classical bin-mixing matrix for independent readout flips."""

    channel = np.asarray([[1.0]], dtype=float)
    for index, probability in enumerate(error_probabilities):
        p = _validate_probability(probability, f"error_probabilities[{index}]")
        local = np.asarray([[1.0 - p, p], [p, 1.0 - p]], dtype=float)
        channel = np.kron(channel, local)
    return channel
