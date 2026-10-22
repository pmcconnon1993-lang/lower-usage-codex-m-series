# Evidence ledger

Historical curated findings live in the skill's
[evidence reference](../skills/m-series-local-helper/references/evidence.md).
New public/synthetic local-helper reports belong under:

```text
community/mX-variant/Ngb/YYYYMMDDTHHMMSSZ-uniqueid.json
```

The [benchmark](../skills/m-series-local-helper/scripts/benchmark.py) produces
these paths, runs one selected model sequentially, retains failures, and checks
the public fixture independently. It saves locally and never submits a report.
See the [contribution procedure](../skills/m-series-local-helper/references/contributing.md).

Every report remains `community_reported`, with `independently_verified: false`
and `recommendation_promoted: false`. Three runs are repeated measurements by
one contributor, not three independent replications. A passing fixture is a
narrow tool-and-fact extraction result, not broad intelligence, hardware support,
deployment readiness or Codex usage-savings evidence.

The closed [result schema](../skills/m-series-local-helper/data/result.schema.json)
requires machine/configuration identity, at least three runs, observed task
times, explicit failures and limitations. Memory and TTFT remain unmeasured/null
in this benchmark. Runtime caches and cold starts are uncontrolled and labelled.

Validate a selected report offline:

```sh
python3 skills/m-series-local-helper/scripts/benchmark.py --validate evidence/community/mX-variant/Ngb/report.json
```

Review the complete result before authorizing publication. Do not add private
inputs, raw model responses, credentials, local paths, machine usernames or
environment dumps. Keep failed and inconclusive results. Maintainers assess
recommendation changes separately; validation never auto-promotes a result.

Reports also include the SHA-256 of the benchmark runner and worker. Keep the repository commit/tag alongside the report when reproducing it; a current runner hash differing from an older report does not by itself invalidate the historical report. Inspect the corresponding source revision.
