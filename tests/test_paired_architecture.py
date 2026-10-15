from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "paired_architecture.py"
SPEC = importlib.util.spec_from_file_location("paired_architecture", SCRIPT)
assert SPEC and SPEC.loader
pa = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pa)


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def save_lines(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def fixture_experiment(root: Path) -> None:
    groups = {"concept-a": 6, "concept-b": 10, "concept-c": 10, "concept-d": 4}
    new = {concept: [f"source:{concept}:{i}" for i in range(count)] for concept, count in groups.items()}
    excluded = [f"source:excluded:{i}" for i in range(9)]
    cohort = {"new_by_concept": new, "changed_source_record_ids": excluded}
    save(root / "cohort.json", cohort)
    cases = []
    categories = ["broad_guidance_setup", "paraphrase", "exact_technical_lookup", "exact_technical_lookup",
                  "multi_hop", "multi_hop", "version_sensitive", "ambiguous",
                  "no_answer_abstention", "no_answer_abstention"]
    for concept, sources in new.items():
        for i, category in enumerate(categories):
            cases.append({"id": f"case:{concept}:{i}", "question": f"What operation covers {concept} scenario {i}?",
                          "concept_id": concept, "category": category,
                          "expected_source_record_ids": [sources[0]] if i < 8 else [],
                          "acceptable_source_record_ids": [], "required_evidence_points": ["Private answer-key point."],
                          "forbidden_or_unsupported_claims": ["Private unsupported claim."],
                          "expected_answerability": "answerable" if i < 6 else "partial" if i < 8 else "no_answer",
                          "expected_version_behavior": "Keep version scope.", "rationale": "Private answer-key rationale.",
                          "citation_required": True, "max_retrieval_rank": 3 if category == "exact_technical_lookup" else 5})
    save(root / "paired-eval/evaluation-contract.json", {
        "cohort": {"excluded_changed_source_record_ids": excluded, "concept_ids": list(groups)}, "cases": cases})
    (root / "paired-eval/methodology.md").write_text("Synthetic methodology.\n")
    (root / "paired-eval/build_eval.py").write_text("# Synthetic historical renderer.\n")
    inputs, projection = [], []
    for sid in [s for values in new.values() for s in values] + excluded:
        candidate = "candidate:" + sid
        snapshot = {"source_record_id": sid, "source_snapshot_id": "snapshot:" + sid,
                    "source_id": "synthetic", "content_hash": "synthetic-content-hash",
                    "canonical_url": "https://example.org/" + sid, "title": "Source " + sid,
                    "upstream_revision": "v19.0"}
        text = "Official synthetic source unit for " + sid
        unit = {"source_unit_id": "unit:" + sid, "source_snapshot_id": snapshot["source_snapshot_id"],
                "text": text, "normalized_content_hash": pa.digest(text.encode()), "heading_path": ["Reference"], "ordinal": 1}
        inputs.append({"candidate_id": candidate, "source_input_hash": "synthetic-input-hash",
                       "source_snapshot": snapshot, "source_units": [unit]})
        artifact = {"artifact_key": "reference", "artifact_type": "task_card", "title": "Task " + sid,
                    "independent_question": "How does this synthetic source apply?", "retrieval_text": "A synthetic operation is supported.",
                    "payload": {"summary": "A synthetic summary.", "steps": [
                        {"order": 1, "instruction": "Read the synthetic reference."},
                        {"order": 2, "instruction": "Check the synthetic scope."}]}}
        save(root / f"generated/shard-1/{candidate.replace(':', '-')}.json",
             {"articles": [{"candidate_id": candidate, "source_input_hash": "synthetic-input-hash", "artifacts": [artifact]}]})
        if sid in excluded:
            continue
        rendered = pa.artifact_text(artifact)
        projection.append({"section_id": "distillation-section:" + pa.canonical_hash({
            "candidate_id": candidate, "artifact_key": "reference", "source_input_hash": "synthetic-input-hash"})[:32],
            "source_record_id": sid, "source_snapshot_id": snapshot["source_snapshot_id"],
            "artifact_type": artifact["artifact_type"],
            "source_content_hash": snapshot["content_hash"], "source_title": snapshot["title"],
            "source_url": snapshot["canonical_url"], "upstream_revision": "v19.0",
            "source_unit_ids": [unit["source_unit_id"]], "text": rendered,
            "section_text_char_count": len(rendered), "section_text_hash": pa.canonical_hash(rendered)})
    save_lines(root / "candidates/distillation-input.jsonl", inputs)
    by_source = {r["source_record_id"]: r for r in projection}
    for arm in ("a", "b"):
        directory = root / f"paired-eval/architecture-{arm}-final"
        save_lines(directory / "projection.private.jsonl", projection)
        save(directory / "projection-report.private.json", {
            "projection_hash": pa.canonical_hash(projection), "row_count": 30, "source_record_count": 30})
        packets, retrieval = [], []
        for case in cases:
            rows = [by_source[sid] for sid in new[case["concept_id"]][:3]]
            packets.append({"schema": "synthetic", "private_only": True, "case_id": case["id"],
                            "question": case["question"], "instructions": "Same historical instructions.", "evidence": [{
                                "label": f"S{rank}", "source_record_id": row["source_record_id"], "title": row["source_title"],
                                "url": row["source_url"], "text": row["text"]} for rank, row in enumerate(rows, 1)]})
            retrieval.append({"case_id": case["id"], "retrieved": [{"rank": rank, "source_record_id": row["source_record_id"],
                                                                      "section_id": row["section_id"]}
                                                                     for rank, row in enumerate(rows, 1)]})
        save_lines(directory / "answer-inputs.private.jsonl", packets)
        save_lines(directory / "retrieval-results.private.jsonl", retrieval)
        save(directory / "retrieval-evaluation.private.json", {"answer_input_hash": pa.canonical_hash(packets), "case_count": 40})


class PairedArchitectureUnitTests(unittest.TestCase):
    def test_hash_domains_differ_for_equivalent_json(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a.json", Path(directory) / "b.json"
            a.write_text('{"z":2,"a":1}')
            b.write_text('{\n  "a": 1, "z": 2\n}\n')
            self.assertEqual(pa.hashes(a)["canonical_json_sha256"], pa.hashes(b)["canonical_json_sha256"])
            self.assertNotEqual(pa.hashes(a)["file_bytes_sha256"], pa.hashes(b)["file_bytes_sha256"])

    def test_jsonl_hash_is_ordered_array(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rows.jsonl"
            rows = [{"b": 2}, {"a": 1}]
            save_lines(path, rows)
            self.assertEqual(pa.hashes(path)["canonical_json_sha256"], pa.canonical_hash(rows))
            self.assertNotEqual(pa.canonical_hash(rows), pa.canonical_hash(rows[::-1]))

    def test_duplicate_keys_and_nonfinite_json_fail(self):
        for text in ('{"case_id":"one","case_id":"two"}', '{"score":NaN}', '{"score":Infinity}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                pa.parse_json(text)

    def test_dict_steps_render_instructions(self):
        artifact = {"title": "Task", "payload": {"steps": [
            {"order": 1, "instruction": "Check the input."}, {"order": 2, "instruction": "Read the result."}]}}
        rendered = pa.artifact_text(artifact)
        self.assertIn("Step 1: Check the input.\nStep 2: Read the result.", rendered)
        self.assertNotIn("'instruction'", rendered)
        with self.assertRaisesRegex(ValueError, "no instruction"):
            pa.artifact_text({"payload": {"steps": [{"order": 1}]}})

    def test_answer_citations_and_schema(self):
        packet = {"case_id": "q-test", "evidence": [{"label": "S1"}]}
        answer = {"case_id": "q-test", "answerability": "partial", "answer": "A supported boundary. [S1]", "citations": ["S1"]}
        pa.validate_answer(answer, packet)
        invalid = [dict(answer, case_id="wrong"), dict(answer, citations=["S2"]),
                   dict(answer, answer="No inline label."), dict(answer, citations=["S1", "S1"]),
                   dict(answer, expected_answerability="partial"), dict(answer, answer="  ")]
        for row in invalid:
            with self.subTest(row=row), self.assertRaises(ValueError):
                pa.validate_answer(row, packet)

    def test_evidence_origin_spans_preserve_mixed_context_and_revision(self):
        source_text, paraphrase = "Literal caf\u00e9 text.", "An editorial paraphrase."
        evidence = {"label": "S1", "source_record_id": "source:one", "title": "A source",
                    "url": "https://example.org/one", "text": source_text + "\n\n" + paraphrase, "version": "v19.0"}
        projection = {
            "contextual-section:one": {"source_record_id": "source:one", "source_content_hash": "content-hash",
                                       "source_unit_ids": ["unit:one"], "text": source_text},
            "distillation-section:two": {"source_record_id": "source:one", "source_content_hash": "content-hash",
                                        "artifact_type": "claim", "text": paraphrase},
        }
        units = {"unit:one": {"text": source_text}}
        labels = pa.evidence_origin_labels(evidence, list(projection), projection, units, "content-hash")
        self.assertEqual(labels["text"], evidence["text"])
        self.assertEqual(labels["text_origin"], "mixed_context")
        self.assertNotIn("version", labels)
        self.assertEqual(labels["observed_document_revision"], "v19.0")
        self.assertEqual(labels["rock_version_scope"], "not_established_by_revision_metadata")
        self.assertEqual(labels["text_spans"], [
            {"start": 0, "end": len(source_text), "text_origin": "source_text"},
            {"start": len(source_text) + 2, "end": len(evidence["text"]), "text_origin": "reviewed_paraphrase"},
        ])
        for section_id, origin in (("contextual-section:one", "source_text"),
                                   ("distillation-section:two", "reviewed_paraphrase")):
            hit = dict(evidence, text=projection[section_id]["text"])
            self.assertEqual(pa.evidence_origin_labels(hit, [section_id], projection, units, "content-hash")["text_origin"], origin)

    def test_source_origin_rejects_nonliteral_text_and_reordered_context(self):
        evidence = {"source_record_id": "source:one", "text": "Edited text.", "version": "v19.0"}
        projection = {"contextual-section:one": {"source_record_id": "source:one", "source_content_hash": "content-hash",
                                                "source_unit_ids": ["unit:one"], "text": "Edited text."}}
        with self.assertRaisesRegex(ValueError, "not literal"):
            pa.evidence_origin_labels(evidence, list(projection), projection, {"unit:one": {"text": "Literal text."}}, "content-hash")
        projection["contextual-section:one"]["text"] = "Literal text."
        with self.assertRaisesRegex(ValueError, "context order changed"):
            pa.evidence_origin_labels(evidence, list(projection), projection, {"unit:one": {"text": "Literal text."}}, "content-hash")


class PairedArchitectureIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.repo = Path(self.temporary.name).resolve()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text("data/\n")
        self.experiment = self.repo / "data/review/historical"
        self.destination = self.repo / "data/review/paired"
        fixture_experiment(self.experiment)

    def seal(self):
        with patch.object(pa, "reconcile_sources", return_value={
            "counts": {"unchanged": 39}, "origin_main": "synthetic-main", "worktree_head": "synthetic-old"}):
            return pa.seal(self.repo, self.experiment, self.destination)

    def write_outputs(self, destination=None):
        destination = destination or self.destination
        dispatch = pa.read_json(destination / "generator/dispatch.json")["packets"]
        for row in dispatch:
            packet = pa.read_json(destination / row["packet"])
            save(destination / row["output"], {"case_id": packet["case_id"], "answerability": "no_answer",
                                                   "answer": "This source set does not establish the requested behavior.", "citations": []})
        return dispatch

    def test_round2_relabels_all40_without_changing_round1_or_evidence(self):
        self.seal()
        self.write_outputs()
        save(self.destination / "judge-outputs/grader-one.json", {"synthetic_grade": True})
        before = pa.file_byte_inventory(self.destination)
        round2 = self.repo / "data/review/evidence-labels"
        with patch.object(pa, "git", return_value="synthetic-main"):
            result = pa.seal_evidence_labels(self.repo, self.destination, self.experiment, round2)
        self.assertEqual(result["generator_packets"], 80)
        self.assertTrue(result["development_test"])
        self.assertFalse(result["new_holdout"])
        old_map = pa.read_json(self.destination / "private/arm-map.json")["pairs"]
        old_pairs = {pair["original_case_id"]: pair for pair in old_map}
        mapping = pa.read_json(round2 / "private/arm-map.json")["pairs"]
        old_ids = {p["packet_id"] for pair in old_map for p in pair["packets"].values()}
        dispatch = pa.read_json(round2 / "generator/dispatch.json")["packets"]
        self.assertTrue(old_ids.isdisjoint(row["packet_id"] for row in dispatch))
        self.assertTrue({pair["case_id"] for pair in old_map}.isdisjoint(pair["case_id"] for pair in mapping))
        position = {row["packet_id"]: i for i, row in enumerate(dispatch)}
        self.assertEqual(sum(position[p["packets"]["a"]["packet_id"]] < position[p["packets"]["b"]["packet_id"]]
                             for p in mapping), 20)
        for pair in mapping:
            for arm in ("a", "b"):
                old_id = old_pairs[pair["original_case_id"]]["packets"][arm]["packet_id"]
                new_id = pair["packets"][arm]["packet_id"]
                old_packet = pa.read_json(self.destination / f"generator/packets/{old_id}.json")
                new_packet = pa.read_json(round2 / f"generator/packets/{new_id}.json")
                self.assertEqual(old_packet["question"], new_packet["question"])
                self.assertEqual(new_packet["instructions"], pa.EVIDENCE_LABEL_INSTRUCTIONS)
                for old, new in zip(old_packet["evidence"], new_packet["evidence"]):
                    restored = {k: v for k, v in new.items() if k not in (
                        "text_origin", "text_spans", "observed_document_revision", "rock_version_scope")}
                    restored["version"] = new["observed_document_revision"]
                    self.assertEqual(restored, old)
                    self.assertEqual(new["text_origin"], "reviewed_paraphrase")
        self.assertEqual(before, pa.file_byte_inventory(self.destination))
        proof = pa.read_json(round2 / "private/evidence-preservation.json")
        self.assertEqual(proof["previous_file_bytes_sha256"], before)
        self.assertEqual(len(proof["packets"]), 80)
        pa.verify(round2)
        pa.verify(self.destination)
        self.write_outputs(round2)
        pa.prepare_judges(round2)
        entry = pa.read_json(round2 / "judges/manifest.json")["packets"][0]
        judge = pa.read_json(round2 / entry["packet"])
        for candidate in judge["candidates"]:
            for citation in candidate["citation_catalog"]:
                self.assertNotIn("version", citation)
                self.assertEqual(citation["rock_version_scope"], "not_established_by_revision_metadata")
        self.assertTrue(all("version" not in row for row in judge["official_source_evidence"]))
        self.assertEqual(before, pa.file_byte_inventory(self.destination))

    def citation_mismatch(self, row):
        path = self.destination / row["output"]
        answer = pa.read_json(path)
        answer.update(answerability="partial", answer="Original claims. [S1] [S2] [S3]", citations=["S1"])
        save(path, answer)
        return answer

    def test_default_rejects_citation_mismatch_and_records_all_outcomes(self):
        self.seal()
        dispatch = self.write_outputs()
        row = dispatch[63]
        self.citation_mismatch(row)
        original = (self.destination / row["output"]).read_bytes()
        for operation in (pa.collect_outputs, pa.prepare_judges):
            with self.assertRaisesRegex(ValueError, "inline citations and citation list differ"):
                operation(self.destination)
        self.assertFalse((self.destination / "judges").exists())
        self.assertEqual(original, (self.destination / row["output"]).read_bytes())
        for path in (self.destination / "validation-reports").glob("*.json"):
            report = pa.read_json(path)
            self.assertEqual(report["policy"], "strict")
            self.assertEqual(report["output_count"], 80)
            self.assertEqual(report["strict_invalid_count"], 1)
            self.assertFalse(report["strict_validation_passed"])
            self.assertEqual(report["release_readiness"], "blocked_validation_failures")

    def test_diagnostic_inclusion_preserves_originals_seal_and_candidate_errors(self):
        self.seal()
        dispatch = self.write_outputs()
        row = dispatch[63]
        answer = self.citation_mismatch(row)
        original = (self.destination / row["output"]).read_bytes()
        sealed = (self.destination / "seal.json").read_bytes()
        generator_hashes = {p: p.read_bytes() for p in (self.destination / "generator").rglob("*.json")}
        collected = pa.collect_outputs(self.destination, include_validation_failures=True)
        self.assertEqual(collected[row["packet_id"]], answer)
        result = pa.prepare_judges(self.destination, include_validation_failures=True)
        self.assertEqual(result["status"], "judge_packets_ready_with_validation_failures")
        self.assertFalse(result["strict_validation_passed"])
        self.assertEqual(result["strict_invalid_count"], 1)
        manifest = pa.read_json(self.destination / "judges/manifest.json")
        report = pa.read_json(self.destination / manifest["validation_report"])
        self.assertEqual(report["policy"], "include_validation_failures")
        outcome = next(o for o in report["outcomes"] if o["packet_id"] == row["packet_id"])
        self.assertEqual(outcome["validation_errors"], ["inline citations and citation list differ"])
        self.assertTrue(outcome["schema_valid"])
        self.assertEqual(outcome["file_bytes_sha256"], pa.digest(original))
        included = []
        for item in manifest["packets"]:
            packet = pa.read_json(self.destination / item["packet"])
            self.assertEqual(packet["validation_policy"], "include_validation_failures")
            self.assertEqual(packet["release_readiness"], "blocked_validation_failures")
            included.extend(c for c in packet["candidates"] if c["answer"] == answer)
        self.assertEqual(len(included), 2)
        for candidate in included:
            self.assertEqual(candidate["answer"], answer)
            self.assertFalse(candidate["validation"]["strict_validation_passed"])
            self.assertEqual(candidate["validation"]["errors"], outcome["validation_errors"])
            self.assertEqual(candidate["validation"]["file_bytes_sha256"], pa.digest(original))
        self.assertEqual(original, (self.destination / row["output"]).read_bytes())
        self.assertEqual(sealed, (self.destination / "seal.json").read_bytes())
        self.assertEqual(generator_hashes, {p: p.read_bytes() for p in generator_hashes})
        pa.verify(self.destination)

    def test_unknown_citation_remains_a_measured_failure_in_diagnostic_mode(self):
        self.seal()
        row = self.write_outputs()[0]
        path = self.destination / row["output"]
        answer = pa.read_json(path)
        answer.update(answerability="partial", answer="An unknown citation. [S99]", citations=["S99"])
        save(path, answer)
        with self.assertRaisesRegex(ValueError, "unknown evidence citation"):
            pa.collect_outputs(self.destination)
        result = pa.prepare_judges(self.destination, include_validation_failures=True)
        report = pa.read_json(self.destination / result["validation_report"])
        outcome = next(o for o in report["outcomes"] if o["packet_id"] == row["packet_id"])
        self.assertEqual(outcome["validation_errors"], ["unknown evidence citation"])
        self.assertFalse(outcome["strict_validation_passed"])
        self.assertEqual(pa.read_json(path), answer)

    def test_diagnostic_inclusion_uses_identical_policy_for_both_arms(self):
        self.seal()
        dispatch = {row["packet_id"]: row for row in self.write_outputs()}
        pair = pa.read_json(self.destination / "private/arm-map.json")["pairs"][0]
        answers = [self.citation_mismatch(dispatch[pair["packets"][arm]["packet_id"]]) for arm in ("a", "b")]
        with self.assertRaises(ValueError):
            pa.collect_outputs(self.destination)
        collected = pa.collect_outputs(self.destination, include_validation_failures=True)
        self.assertEqual(len(collected), 80)
        result = pa.prepare_judges(self.destination, include_validation_failures=True)
        report = pa.read_json(self.destination / result["validation_report"])
        self.assertEqual(report["policy_scope"], "all_outputs_both_arms")
        self.assertEqual(report["strict_invalid_count"], 2)
        for arm, answer in zip(("a", "b"), answers):
            packet_id = pair["packets"][arm]["packet_id"]
            self.assertEqual(collected[packet_id], answer)
            outcome = next(o for o in report["outcomes"] if o["packet_id"] == packet_id)
            self.assertEqual(outcome["validation_errors"], ["inline citations and citation list differ"])

    def test_diagnostic_mode_rejects_answers_outside_json_schema(self):
        self.seal()
        row = self.write_outputs()[0]
        path = self.destination / row["output"]
        original = pa.read_json(path)
        invalid = [dict(original, extra="unexpected"), dict(original, citations=["S1", "S1"]),
                   dict(original, citations=["other"]), dict(original, answer=12)]
        for answer in invalid:
            with self.subTest(answer=answer):
                save(path, answer)
                with self.assertRaises(ValueError):
                    pa.collect_outputs(self.destination, include_validation_failures=True)
                self.assertEqual(pa.read_json(path), answer)
        path.write_text("{not-json")
        with self.assertRaises(ValueError):
            pa.prepare_judges(self.destination, include_validation_failures=True)
        self.assertFalse((self.destination / "judges").exists())

    def test_diagnostic_validation_cli_keeps_failure_exit_status(self):
        self.seal()
        row = self.write_outputs()[0]
        self.citation_mismatch(row)
        result = subprocess.run([sys.executable, str(SCRIPT), "validate-outputs", "--destination", str(self.destination),
                                 "--include-validation-failures"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "validation_failed_diagnostic_only")
        self.assertEqual(report["strict_invalid_count"], 1)
        self.assertFalse(report["strict_validation_passed"])
        self.assertEqual(report["release_readiness"], "blocked_validation_failures")

    def test_packet_body_for_stdin_excludes_instructions_schema_and_keys(self):
        self.seal()
        row = pa.read_json(self.destination / "generator/dispatch.json")["packets"][0]
        body = pa.packet_body(self.destination, row["packet_id"])
        self.assertEqual(set(body), {"case_id", "question", "evidence"})
        self.assertEqual(body["evidence"], pa.read_json(self.destination / row["packet"])["evidence"])
        with self.assertRaisesRegex(ValueError, "unknown packet ID"):
            pa.packet_body(self.destination, "missing")

    def test_base_binding_preserves_generator_bytes_and_rejects_a_new_main(self):
        self.seal()
        before = pa.read_json(self.destination / "seal.json")["files"]
        with patch.object(pa, "git", return_value="synthetic-main"):
            self.assertEqual(pa.bind_base(self.repo, self.destination)["base_commit"], "synthetic-main")
        after = pa.read_json(self.destination / "seal.json")["files"]
        self.assertEqual({k: v for k, v in before.items() if k != "private/audit.json"},
                         {k: v for k, v in after.items() if k != "private/audit.json"})
        with patch.object(pa, "git", return_value="different-main"), self.assertRaisesRegex(ValueError, "audited origin/main"):
            pa.bind_base(self.repo, self.destination)

    def test_shared_historical_retrieval_text_drift_preserves_final_packets(self):
        path = next((self.experiment / "generated").glob("shard-*/*concept-a-0.json"))
        generated = pa.read_json(path)
        generated["articles"][0]["artifacts"][0]["retrieval_text"] = "A revised synthetic retrieval sentence."
        save(path, generated)
        audit, _ = pa.audit_experiment(self.experiment)
        self.assertEqual(len(audit["historical_retrieval_text_drift"]), 2)
        generated["articles"][0]["artifacts"][0]["payload"]["steps"][0]["instruction"] = "A revised procedural step."
        save(path, generated)
        with self.assertRaisesRegex(ValueError, "outside retrieval_text"):
            pa.audit_experiment(self.experiment)

    def test_seal_all40_blinding_and_tamper_detection(self):
        result = self.seal()
        self.assertEqual(result["generator_packets"], 80)
        dispatch = pa.read_json(self.destination / "generator/dispatch.json")["packets"]
        mapping = pa.read_json(self.destination / "private/arm-map.json")["pairs"]
        self.assertEqual(len(mapping), 40)
        position = {r["packet_id"]: i for i, r in enumerate(dispatch)}
        self.assertEqual(sum(position[p["packets"]["a"]["packet_id"]] < position[p["packets"]["b"]["packet_id"]]
                             for p in mapping), 20)
        for row in dispatch:
            packet = pa.read_json(self.destination / row["packet"])
            serialized = json.dumps(packet)
            for marker in (*pa.KEY_MARKERS, "Private answer-key", "architecture-a", "architecture-b", "original_case_id"):
                self.assertNotIn(marker, serialized)
            self.assertEqual(packet["instructions"], pa.GENERATOR_INSTRUCTIONS)
        self.assertFalse(list((self.destination / "outputs").iterdir()))
        packet_path = self.destination / dispatch[0]["packet"]
        packet_path.write_text(packet_path.read_text() + "\n")
        with self.assertRaisesRegex(ValueError, "sealed file hash mismatch"):
            pa.verify(self.destination)

    def test_contract_duplicate_case_and_noncohort_source_fail(self):
        contract_path = self.experiment / "paired-eval/evaluation-contract.json"
        original = pa.read_json(contract_path)
        for mutate in (lambda c: c["cases"][0].update(id=c["cases"][1]["id"]),
                       lambda c: c["cases"][0].update(expected_source_record_ids=["source:excluded:0"])):
            contract = copy.deepcopy(original)
            mutate(contract)
            save(contract_path, contract)
            with self.assertRaises(ValueError):
                pa.audit_experiment(self.experiment)

    def test_evidence_mutation_and_answer_key_fields_fail(self):
        path = self.experiment / "paired-eval/architecture-a-final/answer-inputs.private.jsonl"
        original = pa.read_jsonl(path)
        for mutate in (lambda r: r[0]["evidence"][0].update(text="An injected answer."),
                       lambda r: r[0].update(required_evidence_points=["Private key"])):
            rows = copy.deepcopy(original)
            mutate(rows)
            save_lines(path, rows)
            report = self.experiment / "paired-eval/architecture-a-final/retrieval-evaluation.private.json"
            save(report, {"answer_input_hash": pa.canonical_hash(rows), "case_count": 40})
            with self.assertRaises(ValueError):
                pa.audit_experiment(self.experiment)

    def test_judges_require_all_outputs_and_contain_only_official_evidence(self):
        self.seal()
        with self.assertRaisesRegex(ValueError, "missing or extra"):
            pa.prepare_judges(self.destination)
        self.assertFalse((self.destination / "judges").exists())
        self.write_outputs()
        self.assertEqual(len(pa.collect_outputs(self.destination)), 80)
        result = pa.prepare_judges(self.destination)
        self.assertEqual(result["packets"], 80)
        for row in pa.read_json(self.destination / "judges/manifest.json")["packets"]:
            packet = pa.read_json(self.destination / row["packet"])
            self.assertEqual(len(packet["official_source_evidence"]), 30)
            self.assertEqual({c["label"] for c in packet["candidates"]}, {"X", "Y"})
            self.assertNotIn("Task source:", json.dumps(packet["official_source_evidence"]))
            self.assertNotIn("Private answer-key", json.dumps(packet))
            self.assertFalse(any("text" in citation for c in packet["candidates"] for citation in c["citation_catalog"]))
        judge_mapping = pa.read_json(self.destination / "private/judge-map.json")
        for first, second in zip(judge_mapping[::2], judge_mapping[1::2]):
            self.assertEqual(first["labels"]["X"], second["labels"]["Y"])
            self.assertEqual(first["labels"]["Y"], second["labels"]["X"])

    def test_destination_rejects_nonignored_paths_symlinks_and_resealing(self):
        with self.assertRaisesRegex(ValueError, "ignored data/review"):
            pa.private_destination(self.repo, self.repo / "published")
        link = self.repo / "data/review/link"
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(self.repo, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            pa.private_destination(self.repo, link / "packet")
        self.seal()
        with self.assertRaisesRegex(ValueError, "already exists"):
            self.seal()


class PairedArchitectureSummaryTests(unittest.TestCase):
    setUp = PairedArchitectureIntegrationTests.setUp
    seal = PairedArchitectureIntegrationTests.seal
    write_outputs = PairedArchitectureIntegrationTests.write_outputs
    citation_mismatch = PairedArchitectureIntegrationTests.citation_mismatch

    def grades(self, *, invalid_output=False):
        self.seal()
        dispatch = self.write_outputs()
        if invalid_output:
            self.citation_mismatch(dispatch[0])
        pa.prepare_judges(self.destination, include_validation_failures=invalid_output)
        sources = pa.read_json(self.destination / "private/source-evidence.json")
        self.unit_id = sources[0]["units"][0]["source_unit_id"]
        pairs = pa.read_json(self.destination / "private/arm-map.json")["pairs"]
        arms = {pair["packets"][arm]["packet_id"]: arm for pair in pairs for arm in ("a", "b")}
        self.judge_map = pa.read_json(self.destination / "private/judge-map.json")
        paths = []
        for grader in (1, 2):
            reviews = []
            for mapping in self.judge_map:
                if mapping["grader"] != grader:
                    continue
                scores = []
                for label, packet_id in mapping["labels"].items():
                    score = 2 if arms[packet_id] == "a" else 4
                    dimensions = {d: score for d in pa.DIMENSIONS}
                    dimensions["privacy_public_safety"] = 4
                    scores.append({"label": label, "dimensions": dimensions, "rationale": "A synthetic source-grounded score.",
                                   "source_unit_ids": [self.unit_id], "safety_failures": []})
                reviews.append({"case_id": mapping["judge_case_id"], "scores": scores})
            path = self.repo / f"grader-{grader}.json"
            save(path, {"grader": grader, "model": "synthetic-independent-grader", "reviews": reviews})
            paths.append(path)
        return paths

    def test_summary_descriptive_means_categories_clusters_and_unavailable_cost(self):
        paths = self.grades()
        before = pa.file_byte_inventory(self.destination)
        result = pa.summarize_paired(self.destination, *paths)
        self.assertEqual(result["status"], "descriptive_summary_complete")
        self.assertEqual(result["case_count"], 40)
        self.assertEqual(result["scores_per_grader"], 80)
        self.assertEqual(result["arms"]["a"]["primary_70_30_mean"], 2)
        self.assertEqual(result["arms"]["b"]["primary_70_30_mean"], 4)
        self.assertEqual(result["by_category"]["exact_technical_lookup"]["a"]["case_count"], 8)
        self.assertEqual(result["by_source_cluster"]["concept-a"]["arms"]["a"]["case_count"], 10)
        self.assertEqual(result["strict_invalid_count"], 0)
        self.assertEqual(result["safety_failure_count"], 0)
        self.assertIsNone(result["human_review_cost"]["minutes"])
        self.assertIsNone(result["generation"]["arms"]["all"]["latency_seconds"]["mean"])
        self.assertFalse(result["release_ready"])
        self.assertIsNone(result["threshold_provenance"]["absolute_thresholds"])
        self.assertEqual(result["threshold_provenance"]["absolute_threshold_preregistration"], "not_established")
        self.assertTrue(result["maps_prebound_at_preparation"])
        self.assertEqual(before, pa.file_byte_inventory(self.destination))

    def test_summary_rejects_incomplete_duplicate_foreign_and_malformed_grades(self):
        paths = self.grades()
        original = pa.read_json(paths[0])
        changes = [lambda v: v["reviews"].pop(),
                   lambda v: v["reviews"].__setitem__(0, copy.deepcopy(v["reviews"][1])),
                   lambda v: v["reviews"][0].update(case_id="foreign"),
                   lambda v: v.update(extra="not permitted"),
                   lambda v: v["reviews"][0]["scores"].pop(),
                   lambda v: v["reviews"][0]["scores"][0]["dimensions"].update(factual_correctness=True),
                   lambda v: v["reviews"][0]["scores"][0]["dimensions"].update(factual_correctness=5),
                   lambda v: v["reviews"][0]["scores"][0]["dimensions"].update(extra_dimension=3),
                   lambda v: v["reviews"][0]["scores"][0].update(source_unit_ids=["unknown-source-unit"]),
                   lambda v: v["reviews"][0]["scores"][0].update(label={"wrong": "type"})]
        for change in changes:
            value = copy.deepcopy(original)
            change(value)
            save(paths[0], value)
            with self.subTest(change=change), self.assertRaises(ValueError):
                pa.summarize_paired(self.destination, *paths)

    def test_summary_blocks_large_disagreement_until_hash_bound_adjudication(self):
        paths = self.grades()
        second = pa.read_json(paths[1])
        second["reviews"][0]["scores"][0]["dimensions"]["factual_correctness"] = 0
        save(paths[1], second)
        blocked = pa.summarize_paired(self.destination, *paths)
        self.assertEqual(blocked["status"], "blocked_adjudication")
        self.assertEqual(blocked["unresolved_disagreement_count"], 1)
        disagreement = blocked["disagreements"][0]
        adjudication = {"schema": "paired-architecture-adjudication-v1", "bindings": blocked["bindings"],
                        "adjudicator": "synthetic-reviewer", "decisions": [{
                            "case_id": disagreement["case_id"], "arm": disagreement["arm"],
                            "dimension": disagreement["dimension"], "score": 3,
                            "rationale": "The cited source supports the resolved score.", "source_unit_ids": [self.unit_id]}]}
        path = self.repo / "adjudication.json"
        save(path, adjudication)
        resolved = pa.summarize_paired(self.destination, *paths, path)
        self.assertEqual(resolved["status"], "descriptive_summary_complete")
        self.assertEqual(resolved["unresolved_disagreement_count"], 0)
        self.assertEqual(resolved["disagreements"][0]["adjudicated_score"], 3)
        adjudication["bindings"]["judge_map"]["file_bytes_sha256"] = "stale"
        save(path, adjudication)
        with self.assertRaisesRegex(ValueError, "input hashes"):
            pa.summarize_paired(self.destination, *paths, path)

    def test_summary_rejects_changed_maps_judge_packets_and_original_outputs(self):
        paths = self.grades()
        manifest = pa.read_json(self.destination / "judges/manifest.json")
        targets = [self.destination / "private/judge-map.json", self.destination / manifest["packets"][0]["packet"],
                   self.destination / next(iter(manifest["generator_outputs"]))]
        for path in targets:
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "hash|changed"):
                pa.summarize_paired(self.destination, *paths)
            path.write_bytes(original)

    def test_summary_retains_format_failures_safety_flags_and_estimated_runtime_metrics(self):
        paths = self.grades(invalid_output=True)
        grade = pa.read_json(paths[0])
        grade["reviews"][0]["scores"][0]["safety_failures"] = ["A synthetic safety issue."]
        save(paths[0], grade)
        dispatch = pa.read_json(self.destination / "generator/dispatch.json")["packets"]
        row = dispatch[0]
        receipt = {"packet_id": row["packet_id"], "attempt": 1, "status": "validation_failure",
                   "packet_hash": row["canonical_json_sha256"],
                   "output_hash": pa.hashes(self.destination / row["output"])["canonical_json_sha256"],
                   "elapsed_seconds": 2, "reported_list_price_usd": 0.02,
                   "usage": {"input_tokens": 100, "cache_creation_input_tokens": 20,
                             "cache_read_input_tokens": 30, "output_tokens": 50}}
        receipt_path = self.destination / f"execution/{row['packet_id']}.attempt-1.json"
        save(receipt_path, receipt)
        result = pa.summarize_paired(self.destination, *paths)
        self.assertEqual(result["strict_invalid_count"], 1)
        self.assertEqual(result["safety_failure_count"], 1)
        self.assertIn("strict_validation_failures", result["release_blockers"])
        self.assertIn("safety_failures", result["release_blockers"])
        metrics = result["generation"]["arms"]["all"]
        self.assertEqual(metrics["latency_seconds"]["mean"], 2)
        self.assertEqual(metrics["latency_seconds"]["missing_count"], 79)
        self.assertEqual(metrics["tokens"]["output_tokens"]["sum"], 50)
        self.assertEqual(metrics["reported_list_price_estimate_usd_not_charged"]["sum"], 0.02)
        receipt["output_hash"] = "wrong"
        save(receipt_path, receipt)
        with self.assertRaisesRegex(ValueError, "receipt hash mismatch"):
            pa.summarize_paired(self.destination, *paths)

    def test_summary_cli_returns_failure_for_unresolved_disagreement(self):
        paths = self.grades()
        second = pa.read_json(paths[1])
        second["reviews"][0]["scores"][0]["dimensions"]["actionability"] = 0
        save(paths[1], second)
        result = subprocess.run([sys.executable, str(SCRIPT), "summarize-paired", "--destination", str(self.destination),
                                 "--grader-1", str(paths[0]), "--grader-2", str(paths[1])], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["status"], "blocked_adjudication")

    def test_summary_records_planning_targets_without_turning_them_into_preregistered_gates(self):
        paths = self.grades()
        source = self.repo / "planning-proposal.md"
        source.write_text("Proposed production gates:\nFinal-answer correctness: >=90\nCitation entailment and evidence coverage: >=95\n")
        result = pa.summarize_paired(self.destination, *paths, threshold_source_path=source)
        provenance = result["threshold_provenance"]
        self.assertEqual(provenance["absolute_threshold_origin"]["file_bytes_sha256"], pa.digest(source.read_bytes()))
        self.assertFalse(provenance["absolute_threshold_origin"]["applied_to_scores"])
        self.assertEqual(provenance["absolute_threshold_preregistration"], "not_established")
        self.assertIsNone(provenance["absolute_thresholds"])
        self.assertNotIn("absolute_quality_gate_not_evaluated", result["release_blockers"])
        self.assertEqual(result["arms"]["a"]["primary_70_30_mean"], 2)

    def test_privacy_score_concern_is_not_reported_as_an_explicit_safety_failure(self):
        paths = self.grades()
        value = pa.read_json(paths[0])
        value["reviews"][0]["scores"][0]["dimensions"]["privacy_public_safety"] = 3
        save(paths[0], value)
        result = pa.summarize_paired(self.destination, *paths)
        self.assertEqual(result["safety_failure_count"], 0)
        self.assertEqual(result["privacy_score_concern_count"], 1)
        self.assertIn("privacy_score_concerns", result["release_blockers"])


if __name__ == "__main__":
    unittest.main()
