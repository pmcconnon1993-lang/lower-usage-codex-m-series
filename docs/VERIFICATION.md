# Release verification — 2026-10-22

This release was built on an Apple M5 Ultra reporting 256 GiB memory and macOS 27.0.1. The repository, research and temporary validation environment are on an external SSD. No new model weights were downloaded and no existing model/runtime selection was changed.

## What ran

- Native skill-creator validation passed. Its PyYAML prerequisite was isolated in a temporary validation environment; the shipped tools require no third-party Python packages.
- The Python behavior suite exercises hardware/RAM routing, unsupported variants, OS/storage gates, loopback-only transport, source confinement, strict JSON, coverage, truncation, bounded context/tools and synthetic contribution validation. Final test count and CI status are visible in GitHub Actions.
- A portable worker performed two actual native-tool tasks through the existing `Qwen3.6-35B-A3B-8bit` endpoint. It read each selected source completely and returned the checked current service, port, revision and marker. The second case included retired data and an embedded misleading instruction. Observed elapsed worker times were 0.717220 s and 0.612647 s. Both used one file call and two model turns; reported cached tokens were zero. These are tiny observations, not comparative benchmarks or guaranteed latency.
- Independent forward review covered an unknown machine, M6 16 GB, M2 Max with an explicit Splash preference, and an unsupported automatic-promotion/private-transcript request. It found hardware-plausibility and context-budget issues that were fixed. A read-only synthetic 4K-context/512-output tool loop confirmed that the smallest bridge budget can complete a tiny task; this does not establish small-model quality.
- Primary model metadata was refreshed: exact model/draft revisions, public availability and licenses matched the catalog. Runtime source heads were retrieved. The first prepublication freshness run retained the expected missing-new-repository error; later checks must retain real network failures rather than silently advancing the review date.

The bundled public synthetic benchmark also completed three serial runs with all exact-field quality checks passing. Its report is in `evidence/community/m5-ultra/256gb/`; it remains labeled community-reported, with memory/TTFT unmeasured and no recommendation promotion.

## Security and dependency scope

The local static scanner reported no findings in analyzed first-party code/configuration. It does not provide a security certification or a full dependency audit. Test files without applicable rules can be reported as not analyzed; their behavior is exercised by the unit suite and source-reviewed. The recorded scan's counts and exclusions are recorded in the release receipt. No model-based security triage was necessary when the static scanner produced zero candidate findings.

The package itself uses Python's standard library and has no pip/npm dependencies or installers. GitHub Actions are pinned to commit hashes. Model/runtime dependencies are outside this package and require their own current advisory/license checks when a user approves actual setup.

## Public installation and update-hook checks

The native Codex skill-installer downloaded the published skill into a clean test destination and the maintainer's skill directory. All 25 files matched the reviewed GitHub source byte-for-byte. The installed advisor ran outside the repository working directory. Its installed freshness hook checked six model repositories plus four runtime repositories and this public repository with zero retrieval errors; it applied no changes. GitHub recognizes both workflows as active. At the time of this receipt, hosted CI and the manual freshness run were queued without an assigned runner; do not call those hosted runs passed. The local test suite and live endpoint checks above are separate completed evidence.

## Preserved negative results

The older local bridge's session request failed to identify the selected Splash child, and its two-document one-shot task answered before complete source coverage. Those failures were rejected and no runtime was changed. The new bridge's two tiny successes do not erase those integration/reliability limits. Its portable release intentionally omits persistent sessions until runtime identity/restart handling is generalized and verified.

## What remains unverified

- Fresh-machine end-to-end runtime/model installation.
- Performance and required task quality across M1–M6, all memory tiers and future variants.
- Broad coding quality, long-context behavior, heavy concurrency and restart recovery for the portable bridge.
- Current M2 reachability; historical M2 work is dated evidence.
- Peak memory, cold-load time and controlled cache behavior in these small smoke tests.
- A measured reduction in Codex subscription usage or cost.
- Complete semantic review of the historical archive: the graph still reported over 5,300 pending semantic sources and eight unavailable conversations. Targeted relevant originals were reviewed; private archives were not published.

Use the skill's acceptance protocol before operational reliance and its contribution format for new measurements. Keep candidate recommendations and measured results distinct.
