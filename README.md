# Lower Usage Codex (M Series)

**A native Codex skill that helps a new Mac user choose, install and verify a local AI helper.** It asks which Mac you have, loads the relevant guidance, explains one recommendation, and asks before downloading models or setting up a runtime.

Codex remains your main assistant. The local helper handles selected reading, extraction, comparison and drafting tasks under Codex's review. This can move some inference onto your Mac; it is **not a measured promise of lower subscription usage**.

## Give this to Codex

Copy this entire prompt into Codex running on your Mac:

```text
Use https://github.com/pmcconnon1993-lang/lower-usage-codex-m-series
Read its README and native skill. First ask which exact Mac/chip and how much RAM I have, unless I already told you. Install only the m-series-local-helper skill using the built-in skill installer. Load only the guidance relevant to my machine. Explain the recommended helper, evidence, memory/storage needs and setup plan. Ask before downloading models or installing a runtime. Keep Codex as my main assistant and verify a real bounded local tool task before saying the helper works.
```

[Open the native skill](skills/m-series-local-helper/SKILL.md) · [How selection works](skills/m-series-local-helper/references/selection.md) · [Evidence](skills/m-series-local-helper/references/evidence.md) · [Contribute a result](CONTRIBUTING.md)

The skill folder is `skills/m-series-local-helper`. Codex's built-in `$skill-installer` can install this GitHub path. A direct local copy can go into `~/.agents/skills/m-series-local-helper` (or the skill directory supported by your Codex version). It contains plain Markdown, JSON and Python standard-library tools; no model weights, credentials, global hooks or background service are bundled. A skill install is small. Model/runtime installation is a separate approved step. See [official Codex skill documentation](https://developers.openai.com/codex/skills/).

## What it knows

M1, M2, M3, M4, M5 and M6 have separate guides. Base, Pro, Max and Ultra variants are recognized only where the hardware is documented. **RAM and workload decide the starting tier; generation decides runtime compatibility.** Unknown/future variants trigger research rather than a fabricated recommendation.

| Unified memory | Conservative starting candidate | Status |
| --- | --- | --- |
| 8–12 GB | Qwen3.5 2B MLX 4-bit, short extraction tasks | Needs local qualification |
| 16–24 GB | Qwen3.5 4B MLX 4-bit | Needs local qualification |
| 32–36 GB | Qwen3.5 9B MLX 4-bit | Needs local qualification |
| 48–64 GB | Qwen3.6 35B-A3B MLX 4-bit | Needs local qualification |
| 96 GB and higher | Qwen3.6 35B-A3B MLX 8-bit | Recorded M5 Ultra 256 GB setup; other hardware needs qualification |

These are cautious starting choices, not measured winners for every Mac. Models, exact revisions, licenses, artifact sizes and source links are in the [dated catalog](skills/m-series-local-helper/data/catalog.json). A lightly loaded 8 GB machine may still be unsuitable for reliable tool work; declining local delegation is a valid result.

The selected 35B helper combines a sparse Qwen target, a matching DFlash2 draft, and Apple-specific serving. The evidence also covers the separate 4-bit memory reviewer, dense 27B alternative, cache/session lessons, oMLX, MLX, Splash, M1/M2 differences, M2 offloading, tool formatting, headroom and failed experiments. It does not assume that more parameters or newer hardware always improve a helper.

## A community that can correct itself

Contributors run public/synthetic tasks on their own hardware and submit sanitized results grouped by chip and RAM. Reports include failures, exact software/model revisions, quality checks, total time, memory and cache state. Maintainers review evidence before changing recommendations. [Contribution instructions](CONTRIBUTING.md) and [result format](evidence/README.md) make that review repeatable.

The update hook checks for upstream changes and flags stale knowledge. It does not silently install updates, upload private work or turn self-reported benchmarks into winners. No claim is made that a skill runs continuously; refresh occurs when invoked. See [updates](skills/m-series-local-helper/references/updates.md).

## Development and verification

Python 3.10+ is required for the bundled scripts. They have no third-party Python dependencies.

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate.py
python3 skills/m-series-local-helper/scripts/advisor.py recommend --chip 'Apple M5 Max' --ram-gb 64 --macos 26.4 --free-gb 100
```

[Release verification and limits](docs/VERIFICATION.md) records what actually ran. A fresh machine installation and performance on every chip have not been demonstrated. Model licenses apply separately from this repository's MIT license.
