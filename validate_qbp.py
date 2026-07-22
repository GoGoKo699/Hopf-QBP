#!/usr/bin/env python3
"""Command-line entry point for the Hopf-QBP validation suite."""
from __future__ import annotations

import argparse
import importlib
import platform
import sys
import unittest
from pathlib import Path

import numpy as np


ANALYTIC_MODULES = (
    "qbp_validation.tests.test_conventions",
    "qbp_validation.tests.test_decoders",
    "qbp_validation.tests.test_native_schedule",
    "qbp_validation.tests.test_resource_ledger",
)

SMOKE_TESTS = (
    "qbp_validation.tests.test_circuit_conventions",
    "qbp_validation.tests.test_asymmetric_completions",
    "qbp_validation.tests.test_real_frame.RealFrameTests.test_regular_frames_n1_to_n4",
    "qbp_validation.tests.test_real_global_estimator.RealGlobalEstimatorTests.test_exact_distribution_returns_complete_gradient",
    "qbp_validation.tests.test_complex_phase.ComplexPhaseTests.test_signed_one_hot_phase_estimator",
    "qbp_validation.tests.test_checkpoints.CheckpointTests.test_real_checkpoint_all_depths",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run deterministic exact-logical Hopf-QBP validation."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--analytic",
        action="store_true",
        help="Run the Qibo-free convention, decoder, native-schedule, and ledger checks.",
    )
    mode.add_argument(
        "--smoke",
        action="store_true",
        help="Run the analytic checks plus a representative Qibo circuit subset.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Use compact unittest output.",
    )
    return parser.parse_args()


def _load_modules(module_names: tuple[str, ...]) -> unittest.TestSuite:
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for module_name in module_names:
        module = importlib.import_module(module_name)
        suite.addTests(loader.loadTestsFromModule(module))
    return suite


def _load_names(test_names: tuple[str, ...]) -> unittest.TestSuite:
    return unittest.defaultTestLoader.loadTestsFromNames(test_names)


def _require_qibo() -> str:
    try:
        import qibo
    except Exception as exc:  # pragma: no cover - depends on local environment
        raise RuntimeError(
            "Qibo is required for --smoke and full validation. Install both "
            "requirements.txt and requirements-optional.txt."
        ) from exc
    return str(getattr(qibo, "__version__", "unknown"))


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent
    if Path.cwd().resolve() != repo_root:
        print(f"Repository root: {repo_root}")

    print(f"Python: {platform.python_version()}", flush=True)
    print(f"NumPy: {np.__version__}", flush=True)

    if args.analytic:
        suite = _load_modules(ANALYTIC_MODULES)
        print("Qibo: not required for analytic mode", flush=True)
    else:
        try:
            qibo_version = _require_qibo()
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        print(f"Qibo: {qibo_version} (NumPy backend selected by qbp_validation.circuits)", flush=True)
        if args.smoke:
            suite = unittest.TestSuite()
            suite.addTests(_load_modules(ANALYTIC_MODULES))
            suite.addTests(_load_names(SMOKE_TESTS))
        else:
            suite = unittest.defaultTestLoader.discover(
                str(repo_root / "qbp_validation" / "tests"),
                pattern="test_*.py",
                top_level_dir=str(repo_root),
            )

    runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=1 if args.quiet else 2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
