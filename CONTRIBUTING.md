# Contributing

Help by reporting reproducible successes **and failures**, clarifying an exact
runtime/model contract, or adding a supported machine profile with evidence.
Please distinguish source documentation, publisher/community measurements,
local observations and estimates. There is no universal winning helper to defend.

For a machine result, use the
[public synthetic benchmark procedure](skills/m-series-local-helper/references/contributing.md).
It runs the bundled read-only worker against your existing helper and writes a
privacy-minimized report under `evidence/community/`. It does not install models,
modify the runtime, upload data or claim subscription savings. Inspect and
authorize a pull request before publishing the report.

For a source correction, cite the official repository/model card and the exact
revision or release. Explain which previous statement changes and why. Preserve
dated historical findings and add the correction instead of rewriting a failed
experiment into a success. A main-branch feature is not automatically present in
a packaged release.

Before proposing a recommendation change, include the task/quality requirement,
exact hardware and model/runtime identity, relevant failures, resource limits,
and a matched comparison or independent replication where available. A valid
schema or repeated run by one person is not independent confirmation. Do not
change the catalog solely because a new result has the highest tokens/second.

Run the repository checks and meaningful tests for your change. The standard
library benchmark tests need no model or network:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 skills/m-series-local-helper/scripts/benchmark.py --validate /path/to/result.json
```

Keep changes focused. A new fixture or report meaning needs a schema/task version
and migration explanation. Do not add auto-executing remote hooks, automatic
private-data uploads, permission bypasses or silent model substitution. Findings
should remain reviewable data, with the user's Codex retaining final judgment.
