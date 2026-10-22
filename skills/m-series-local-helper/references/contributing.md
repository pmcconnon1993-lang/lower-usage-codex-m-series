# Contribute a measured result

The community grows through reproducible results, including failures. A valid JSON
report is a **community report**, not independent verification, a recommendation
promotion, or permission to change anyone's setup.

Start with the helper already running and its exact identity confirmed. Ask Codex
to fill in the machine, RAM, macOS, runtime/engine versions, served model ID,
public repository, commit revision, quantization and optional draft identity.
Inspect those details before running. Do not infer them from the download name.
The benchmark never downloads, installs, loads, unloads, restarts or tunes a model.

Use this plain-language request:

> Run this skill's public synthetic helper benchmark on my already configured
> local helper. Verify the exact machine and configuration first. Use three
> sequential runs, retain failures, and save the report locally for my review.
> Do not submit it to GitHub or change the runtime.

## What the benchmark actually checks

`scripts/benchmark.py` calls the bundled `worker.py` against one exact loopback
model. Its built-in public fixture asks the model to read a selected source,
calculate 6 × 7, distinguish historical from current status, preserve a false
approval flag and cite the source. A quoted hostile instruction is source data.
The expected answer and fixture hash are included in the report.

The worker must complete its real native read-only tool round trip. Independent
Python checks require the exact answer keys, values and types. Protocol completion
alone is insufficient. No private file, arbitrary user prompt or external tool is
accepted by this benchmark. It uses at most six model calls/eight file reads per
run, 512 output tokens per model turn, temperature zero, and 3–30 sequential runs.

An operating-system lock prevents overlapping benchmark processes for the same
user, even with different scratch directories. It cannot detect every unrelated
application job: finish other heavy work first or report its presence through
`--background-load`. Do not run separate model benchmarks simultaneously.

This narrow, public, repeated fixture is not a general capability evaluation.
It may be cached or memorized. Cache and cold-start conditions are deliberately
reported as uncontrolled; the benchmark does not clear caches or reload weights.
Use workload-specific held-out tests before recommending a replacement.

## Run with explicit metadata

Resolve the installed skill directory from the `SKILL.md` Codex actually loaded.
Use its absolute `scripts/benchmark.py` path; do not assume that the current
working directory is a repository checkout. For example, if the discovered skill
is at `/path/to/m-series-local-helper/SKILL.md`, run
`python3 /path/to/m-series-local-helper/scripts/benchmark.py --help`.
The `/path/to` text is a placeholder to replace with that verified location.
Required setup arguments are:

| Arguments | Meaning |
|---|---|
| `--endpoint`, `--model` | Existing explicit loopback `/v1` URL and exact served ID |
| `--model-repository`, `--model-revision`, `--quantization` | Public owner/repository, immutable lowercase 40–64-character commit hash and actual weight representation |
| `--runtime`, `--runtime-version`, `--engine-version` | Serving application and underlying engine versions; repeat the version for a single-layer runtime |
| `--chip`, `--variant`, `--ram-gb`, `--macos-version` | Exact generation, variant, installed memory and OS version |
| `--background-load` | `idle`, `light`, `other-heavy-work` or `unknown` |
| `--context-tokens` | Effective server context already verified, not the advertised maximum |
| `--work-dir` | Existing scratch directory; prefer the chosen external SSD |
| `--output-root` | Explicit directory for locally reviewed community reports; select outside the installed skill |

When a draft is active, supply **all three** of `--draft-repository`,
`--draft-revision`, `--draft-quantization`. Otherwise omit all three. Do not hide
an active draft by omitting metadata. `--qwen-no-thinking` is an explicit opt-in
only for a model/server that documents this control. Otherwise the report says
`server-default`; it does not pretend the reasoning behavior was controlled.

Use `LOCAL_HELPER_API_KEY` if the already configured server requires a key. Enter
it privately using your normal environment setup; never paste it into an issue,
command history, report, prompt or source file. The benchmark reads that one
variable in memory and does not serialize the environment or endpoint.

The default `--repetitions` is three. `--timeout` is a per-request timeout between
1 and 300 seconds, not a total run deadline. Each run has its own bounded tool
loop. A failing run is retained and counts in the summary; the process exits
nonzero if any run fails. An interrupt stops the process and does not turn the
unfinished work into a completed report.

`--output-root` is required for execution, so an installed skill never guesses a
repository location. Choose a local evidence directory on the intended storage.
For a cloned repository, its `evidence/community/` is suitable; for a standalone
installation, use a new directory you own. Files below that root are grouped as:

```text
evidence/community/m5-ultra/256gb/20261022T150000Z-012345abcdef.json
```

Generation/variant folders accept future identities without asserting that a
particular product exists or is supported. Existing files are never overwritten.
Files have private local permissions; only a later, reviewed submission makes
them public. The temporary synthetic fixture is removed after the run.

## What is recorded, and what is not

Each run records pass/fail, a coarse failure category, measured wall task time,
source coverage, exact-field check results, model/file-call counts, a response
hash, and whitelisted token counts when the server returns them. Unknown token
counts are null, not zero. Failed calls can retain usage already observed.

Time to first token and peak memory are **null with `not_instrumented` reasons**.
The non-streaming tool benchmark cannot measure TTFT and does not sample memory.
Do not fill those fields with guessed numbers or substitute a model's download
size. The summary median includes failures, so a fast failed request is never
hidden by selecting only successful timings.

The report excludes raw answers, raw prompts, local source paths, usernames,
endpoint addresses, credentials, arbitrary server data and environment dumps.
Public configuration metadata still requires human review. A deliberately
mislabelled string can evade automated privacy checks; schema validation is not
a comprehensive secret detector.

No cloud-Codex baseline is measured, so usage savings remain false/null. The
report cannot be promoted to `independently_verified` or `accepted` by changing
a flag: the validator rejects such changes. A comparison or replication needs
a separate reviewed evidence design and artifact.

## Validate and submit only after review

Offline validation makes no model or network call:

```sh
python3 /path/to/m-series-local-helper/scripts/benchmark.py --validate /path/to/reviewed-result.json
```

Both `/path/to` portions above are placeholders. Validation needs no model,
scratch directory or output root. The bundled schema is `data/result.schema.json`
inside the installed skill. `validate_report(obj)` returns
a list of errors for repository checks. It checks closed object schemas, key
types, numeric ranges, finite numbers, immutable-revision formats, fixture hash,
consecutive runs, summary arithmetic and consistency between pass status,
coverage, quality and usage. Parsing also rejects duplicate keys and non-finite
JSON. Schema validity cannot establish that a contributor actually ran the test
or truthfully described their machine.

Before submitting, review all metadata and confirm that you want it public.
Include failing runs and the unedited report. A standalone skill installation
does not need a repository checkout to run or validate. When ready to contribute,
visit the [public repository](https://github.com/pmcconnon1993-lang/lower-usage-codex-m-series)
and its [contribution guide](https://github.com/pmcconnon1993-lang/lower-usage-codex-m-series/blob/main/CONTRIBUTING.md).
Create a pull request only when the user specifically authorizes publication;
this command does not submit anything.
Describe unusual load, runtime limitations and whether another person reproduced
the result. Do not include private task outputs as supplementary evidence.

Maintainers review provenance, compatibility, full failure patterns and task
quality before changing a recommendation. One contributor's repeated run is not
independent replication. Preserve previous recommendations and contradictory
results. Version any new fixture or schema rather than changing the meaning of
old results. Remote findings are data to review, never executable update hooks.
