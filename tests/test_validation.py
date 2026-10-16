import importlib.util
from pathlib import Path
import sys
import unittest

from engine.product_factory.spec import ProductSpec
from engine.validation.policy import is_eligible


def load_legacy_module(name):
    path = Path(__file__).parents[1] / "media-engine" / "src" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


state = load_legacy_module("state")
quality_gate = load_legacy_module("quality_gate")


class ValidationTests(unittest.TestCase):
    def test_invalid_risk_scores_cannot_advance(self):
        for score in [float("inf"), float("nan"), -1, 101, None, "bad"]:
            with self.subTest(score=score):
                self.assertFalse(is_eligible(ip_risk=score))
        self.assertTrue(is_eligible(ip_risk=60))
        self.assertFalse(is_eligible(ip_risk=100, blocked_reasons={"unclear_ip_rights"}))

    def test_infinite_price_is_not_launchable(self):
        spec = ProductSpec("name", "buyer", "problem", "outcome", "PDF",
                           float("inf"), "etsy", "difference")
        self.assertFalse(spec.is_launchable())

    def test_job_cannot_skip_quality_and_publish(self):
        job = state.JobRecord("j1", "c1")
        original_time = job.updated_at
        with self.assertRaises(ValueError):
            job.transition(state.JobState.PUBLISHED)
        self.assertEqual(job.state, state.JobState.DISCOVERED)
        self.assertEqual(job.updated_at, original_time)
        job.transition(state.JobState.RESEARCHED)
        job.transition(state.JobState.FAILED, "retry")
        self.assertEqual(job.attempt, 1)
        self.assertEqual(job.last_error, "retry")

    def test_quality_gate_rejects_nan_and_invalid_thresholds(self):
        for value in [float("nan"), float("inf"), -0.1, 1.1]:
            with self.subTest(value=value):
                result = quality_gate.evaluate(quality_score=value,
                    originality_score=1, rights_confidence=1)
                self.assertFalse(result.approved)
        result = quality_gate.evaluate(quality_score=1, originality_score=1,
            rights_confidence=1, minimum_rights=float("nan"))
        self.assertFalse(result.approved)


if __name__ == "__main__":
    unittest.main()
