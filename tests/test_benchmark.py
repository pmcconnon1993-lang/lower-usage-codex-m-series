"""Meaningful protocol, grading and contribution-boundary checks; no model used."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "skills/m-series-local-helper/scripts/benchmark.py"
SPEC = importlib.util.spec_from_file_location("helper_benchmark", SCRIPT)
benchmark = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(benchmark)
MODEL = "fixture-model"


def metadata():
    machine = {"chip": "m2", "variant": "max", "ram_gb": 64,
               "macos_version": "27.0.1", "background_load": "idle"}
    configuration = {"runtime": "splash", "runtime_version": "1.4.0", "engine_version": "1.4.0",
                     "model_id": MODEL, "model_repository": "example/public-model", "model_revision": "a" * 40,
                     "quantization": "MLX-4bit", "draft": None, "context_tokens": 32768,
                     "max_tokens_per_turn": 512, "max_turns": 6, "concurrency": 1, "temperature": 0,
                     "reasoning": "server-default", "cache_condition": "uncontrolled-repeated-public-fixture",
                     "lifecycle": "existing-server-no-changes"}
    return machine, configuration


class SyntheticClient:
    endpoint = "http://127.0.0.1:9999/v1"

    def __init__(self, wrong=False, premature=False, usage=True):
        self.wrong = wrong
        self.premature = premature
        self.with_usage = usage
        self.verifications = 0
        self.requests = []

    def verify_model(self, model):
        if model != MODEL:
            raise benchmark.worker.WorkerError("Wrong fixture model.")
        self.verifications += 1

    def request(self, route, payload):
        self.requests.append(copy.deepcopy(payload))
        message = {"role": "assistant", "content": None}
        if "tools" in payload and not self.premature:
            message["tool_calls"] = [{"id": "fixture-read", "type": "function", "function": {
                "name": "read_file", "arguments": '{"path":"fixture.txt"}'}}]
            reason = "tool_calls"
        else:
            answer = dict(benchmark.EXPECTED)
            if self.wrong:
                answer["total_units"] = 99
            message["content"] = json.dumps(answer)
            reason = "stop"
        result = {"model": MODEL, "choices": [{"message": message, "finish_reason": reason}]}
        if self.with_usage:
            result["usage"] = {"prompt_tokens": 30, "completion_tokens": 10, "total_tokens": 40,
                               "prompt_tokens_details": {"cached_tokens": 4},
                               "private_server_field": "MUST_NOT_APPEAR"}
        return result


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def report(self, client=None):
        machine, configuration = metadata()
        return benchmark.run_repetitions(client or SyntheticClient(), machine, configuration, 3, self.root)

    def test_three_serial_real_worker_tool_loops_and_independent_grading(self):
        client = SyntheticClient()
        report = self.report(client)
        self.assertEqual(benchmark.validate_report(report), [])
        self.assertEqual(client.verifications, 3)
        self.assertEqual(len(client.requests), 6)
        self.assertEqual(["tools" in request for request in client.requests], [True, False] * 3)
        self.assertEqual(report["summary"]["passed"], 3)
        self.assertEqual(report["runs"][0]["usage"]["total_tokens"], 80)
        self.assertEqual(report["runs"][0]["usage"]["cached_tokens"], 8)
        self.assertEqual(report["runs"][0]["ttft_seconds"], {"value": None, "reason": "not_instrumented"})
        self.assertFalse(report["independently_verified"])
        self.assertFalse(report["usage_savings"]["measured"])
        serialized = json.dumps(report)
        for private in (str(self.root), client.endpoint, "MUST_NOT_APPEAR", benchmark.FIXTURE, "Authorization", "LOCAL_HELPER_API_KEY"):
            self.assertNotIn(private, serialized)

    def test_wrong_facts_fail_even_after_valid_protocol_and_json(self):
        report = self.report(SyntheticClient(wrong=True))
        self.assertEqual(benchmark.validate_report(report), [])
        self.assertEqual(report["summary"]["failed"], 3)
        for run in report["runs"]:
            self.assertTrue(run["protocol_complete"])
            self.assertTrue(run["source_coverage_complete"])
            self.assertFalse(run["quality_checks"]["total_units"])
            self.assertEqual(run["failure_category"], "quality")

    def test_early_final_keeps_every_failed_run_and_observed_usage(self):
        report = self.report(SyntheticClient(premature=True))
        self.assertEqual(benchmark.validate_report(report), [])
        self.assertEqual(report["summary"]["failed"], 3)
        for run in report["runs"]:
            self.assertEqual(run["failure_category"], "protocol")
            self.assertFalse(run["source_coverage_complete"])
            self.assertIsNone(run["answer_sha256"])
            self.assertEqual(run["usage"]["total_tokens"], 40)

    def test_missing_usage_is_null_not_zero(self):
        report = self.report(SyntheticClient(usage=False))
        self.assertEqual(benchmark.validate_report(report), [])
        self.assertIsNone(report["runs"][0]["usage"]["prompt_tokens"])
        self.assertEqual(report["runs"][0]["usage"]["reason"], "one_or_more_counts_unavailable")

    def test_exact_answer_requires_types_no_extra_keys_or_historical_status(self):
        for field, value in (("total_units", 42.0), ("approved", 0), ("current_status", "completed"), ("source", "/private/fixture.txt")):
            answer = dict(benchmark.EXPECTED)
            answer[field] = value
            self.assertFalse(all(benchmark.check_answer(answer).values()))
        answer = dict(benchmark.EXPECTED, explanation="unrequested")
        self.assertFalse(benchmark.check_answer(answer)["exact_keys"])

    def test_bad_metadata_rejected_before_any_model_call(self):
        machine, configuration = metadata()
        cases = [("machine", "ram_gb", True), ("machine", "ram_gb", 0),
                 ("machine", "macos_version", "unknown"), ("machine", "chip", "m0"),
                 ("configuration", "model_revision", "main"),
                 ("configuration", "model_repository", "/Users/private/model"),
                 ("configuration", "model_id", "sk-DO_NOT_RECORD"),
                 ("configuration", "concurrency", 2)]
        for section, key, value in cases:
            with self.subTest(section=section, key=key):
                current_machine, current_configuration = copy.deepcopy(machine), copy.deepcopy(configuration)
                (current_machine if section == "machine" else current_configuration)[key] = value
                client = SyntheticClient()
                with self.assertRaises(benchmark.worker.WorkerError):
                    benchmark.run_repetitions(client, current_machine, current_configuration, 3, self.root)
                self.assertEqual(client.verifications, 0)

    def test_validator_rejects_nan_infinity_false_savings_and_promotion(self):
        original = self.report()
        mutations = [lambda r: r["runs"][0].update(wall_task_seconds=float("nan")),
                     lambda r: r["runs"][0].update(wall_task_seconds=float("inf")),
                     lambda r: r["machine"].update(ram_gb=True),
                     lambda r: r["usage_savings"].update(measured=True, codex_usage_reduction_percent=30),
                     lambda r: r.update(evidence_status="independently_accepted"),
                     lambda r: r.update(recommendation_promoted=True),
                     lambda r: r.update(private_prompt="Do not publish me"),
                     lambda r: r["configuration"].update(model_revision="main"),
                     lambda r: r["runs"][0]["peak_memory_bytes"].update(value=0),
                     lambda r: r.update(created_at="2026-99-01T00:00:00Z")]
        for mutation in mutations:
            report = copy.deepcopy(original)
            mutation(report)
            self.assertTrue(benchmark.validate_report(report))

    def test_validator_checks_summary_truth_coverage_hash_and_all_run_indices(self):
        original = self.report()
        mutations = [lambda r: r["summary"].update(passed=2),
                     lambda r: r["summary"].update(median_wall_task_seconds_including_failures=999),
                     lambda r: r["runs"][1].update(index=1),
                     lambda r: r["runs"][0].update(source_coverage_complete=False),
                     lambda r: r["task"].update(fixture_sha256="0" * 64),
                     lambda r: r["runs"][0]["usage"].update(total_tokens=999),
                     lambda r: r["runs"].pop()]
        for mutation in mutations:
            report = copy.deepcopy(original)
            mutation(report)
            self.assertTrue(benchmark.validate_report(report))

    def test_offline_cli_uses_strict_json_and_never_calls_server(self):
        path = self.root / "report.json"
        path.write_text(json.dumps(self.report()))
        with mock.patch.object(benchmark.worker, "LocalClient", side_effect=AssertionError("No network")), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(benchmark.main(["--validate", str(path)]), 0)
        for bad in ('{"schema_version":1,"schema_version":1}', '{"schema_version":NaN}', '{"schema_version":1e999}'):
            path.write_text(bad)
            with mock.patch.object(benchmark.worker, "LocalClient", side_effect=AssertionError("No network")), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(benchmark.main(["--validate", str(path)]), 1)

    def test_execution_requires_explicit_output_root_before_network(self):
        arguments = ["--endpoint", "http://127.0.0.1:9999/v1", "--model", MODEL,
                     "--model-repository", "example/public-model", "--model-revision", "a" * 40,
                     "--quantization", "MLX-4bit", "--runtime", "splash", "--runtime-version", "1.4.0",
                     "--engine-version", "1.4.0", "--chip", "m2", "--variant", "max", "--ram-gb", "64",
                     "--macos-version", "27.0.1", "--background-load", "idle", "--context-tokens", "32768",
                     "--work-dir", str(self.root)]
        with mock.patch.object(benchmark.worker, "LocalClient", side_effect=AssertionError("No network")), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(benchmark.main(arguments), 1)

    def test_output_grouping_new_file_and_symlink_escape_rejection(self):
        report = self.report()
        output_root = self.root / "evidence"
        relative = benchmark.write_report(report, output_root)
        self.assertTrue(relative.startswith("m2-max/64gb/"))
        self.assertEqual(benchmark.validate_report(json.loads((output_root / relative).read_text())), [])
        with self.assertRaises(benchmark.worker.WorkerError):
            benchmark.write_report(report, output_root)
        escaped = self.root / "escaped"
        escaped.mkdir()
        other = self.root / "other"
        other.mkdir()
        (other / "m2-max").symlink_to(escaped, target_is_directory=True)
        with self.assertRaises(OSError):
            benchmark.write_report(report, other)
        self.assertEqual(list(escaped.iterdir()), [])

    def test_at_least_three_repetitions_and_global_serial_lock(self):
        machine, configuration = metadata()
        for repetitions in (0, 1, 2, 31, True):
            with self.assertRaises(benchmark.worker.WorkerError):
                benchmark.run_repetitions(SyntheticClient(), machine, configuration, repetitions, self.root)
        with mock.patch.object(benchmark.Path, "home", return_value=self.root):
            with benchmark.serial_job():
                with self.assertRaisesRegex(benchmark.worker.WorkerError, "Another benchmark"):
                    with benchmark.serial_job():
                        self.fail("A second benchmark entered the lock")


if __name__ == "__main__":
    unittest.main()
