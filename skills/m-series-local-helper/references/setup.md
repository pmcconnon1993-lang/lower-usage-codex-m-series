# From a blank Mac to an approved, verified helper

This is an agent-operated recipe. Do not ask a novice to invent paths, commands or configuration flags. Resolve those from the actual Mac and current documentation. Ask the short hardware question before any installation; downloading this knowledge is separate from downloading models.

## 1. Inspect and propose

Read the selected machine guide, catalog row and current upstream instructions. Check Python 3.10+ before using bundled scripts. If unavailable, use About This Mac or the built-in read-only `sysctl -n machdep.cpu.brand_string`, `sysctl -n hw.memsize` and `sw_vers -productVersion` commands; include Python in the approved setup plan only if needed. Record exact chip/RAM/macOS, target workload, existing local runtimes, selected model storage and free space. Do not scan unrelated user documents or print credentials. Check whether the shell is on the user's Mac. If remote, ask for About This Mac details and execute setup only on the authorized target.

Ask the runtime preference described in [selection](selection.md): **focused Inco Splash**, where supported, or **oMLX model management**, which can itself host Splash and native MLX models. Offer more than one model when useful (for example a small short-task helper and the 35B quality candidate), with individual model sizes and one-heavy-model-at-a-time as the initial policy. Do not download every catalog tier.

Give one concrete plan before requesting approval. Include exact source URLs/revisions, runtime version and requirements, target + draft, download and temporary/cache space, destination, app/virtual environment locations, endpoint/port, context/output limits, launch method, proposed persistent profile/wrapper and optional narrow Codex guidance, and removal/rollback steps. Exclude startup/login changes unless separately requested. Recheck that the port is unused; do not evict another service.

## 2. Implement the chosen route after approval

### Inco Splash (preferred when supported)

Read the current [Inco README/releases](https://github.com/incoai/splash) and exact model-format support before installation. The researched upstream requires M3+ and macOS 26.4+. Install the official release using its documented method. Review a downloaded installer/script before execution; never pipe an unreviewed URL into a shell. Use its own `--help` and model preparation contract to load the chosen MLX target and matching DFlash2. Do not substitute the retired `incoai/*-Splash` packages for the target/draft pair.

Read actual supported flags before constructing the launch command. Apply the chosen short context and resource ceiling; the historical 64 GiB/32K/BF16 settings belong to a 256 GB M5. Bind to loopback, preserve authentication, and verify the actual served model ID. Official Splash and the M1/M2 port are different builds. For older chips, explicitly offer the fork tradeoff and review [the port](https://github.com/paperniuk/splash) before using it.

### oMLX with Splash or native MLX

Use the [official macOS release](https://github.com/jundot/omlx/releases) and [Splash integration guide](https://github.com/jundot/omlx/blob/main/docs/Splash.md). The studied release requires macOS 15+; Splash has its own stricter OS/chip requirements. Native app packaging includes custom kernels that source-only installs can miss. Set the model/cache directory to the selected SSD before large downloads. Preserve existing settings and keep credentials out of logs.

For a supported 35B pair, choose its Splash external-engine profile. For smaller Qwen3.5 candidates, select native MLX with exact family support. Configure idle unloading and one active heavy job first. Native MLX DFlash/MTP options and Splash external-engine controls are distinct. Confirm which engine actually serves the model; an oMLX window alone does not prove the route.

If the current app cannot import a pinned revision through its UI, download that snapshot into the approved model root and import the local folder using its supported contract. Do not fake revision pinning from a model display name.

### Isolated MLX-LM fallback

Use when it has a concrete compatibility/simplicity advantage or the preferred route is unavailable, after explaining the change. Install only after the runtime/package plan is approved. Use an isolated virtual environment on the selected storage, not a managed app's Python. Choose current compatible package versions from their official sources, record the resolved lock/freeze and run a dependency advisory check before operational deployment.

An example sequence for Codex to instantiate with real approved absolute paths:

```sh
python3 -m venv /approved/storage/helper-venv
/approved/storage/helper-venv/bin/python -m pip install 'mlx-lm==REVIEWED_VERSION' 'huggingface-hub==REVIEWED_VERSION'
/approved/storage/helper-venv/bin/hf download MODEL_ID --revision COMMIT_SHA --local-dir /approved/storage/models/SELECTED_MODEL
```

The uppercase values are intentional plan variables, not commands ready to execute. Resolve them from the selected catalog and current upstream, show them in the approval plan, and verify `hf download --help`. No `trust_remote_code` is needed for these selected routes; if a future model asks for it, review that code and explain the new requirement.

Current MLX-LM's documented server shape (verify installed `--help`):

```sh
/approved/storage/helper-venv/bin/mlx_lm.server --model /approved/storage/models/SELECTED_MODEL --host 127.0.0.1 --port AVAILABLE_PORT --max-tokens 1024 --decode-concurrency 1 --prompt-concurrency 1 --prefill-step-size 512 --prompt-cache-size 1 --prompt-cache-bytes 512M --chat-template-args '{"enable_thinking":false}'
```

The researched server has no `--max-context` or `--max-kv-size` flag. Limit request context in the calling bridge and inspect memory. Do not invent such flags. Text-only loading of these multimodal Qwen3.5 checkpoints is supported in the studied MLX-LM adapter; this does not verify a vision tool pipeline.

## 3. Verify, then make ordinary use simple

Follow [validation](validation.md), including a real read-only file tool call and complete checked answer. Save exact runtime/model revision, serving alias, endpoint, precision/context/cache settings, source URLs, destination, validation date, tool command and rollback paths in a small local profile. Keep credentials separate, in the runtime's existing secret storage or process environment. Public reports never include that private profile.

If included in the approved plan, create a small launcher/wrapper using verified CLI arguments and the portable worker. It should load only the selected local model on demand, fail when the external disk is unavailable, and never download replacements or change Codex's main model. A launcher is not a login service. A second invocation must detect existing service/model state rather than duplicate it.

For automatic reuse, include this narrow instruction in the user's chosen Codex instructions file, with the real local profile path:

> For suitable bounded selected-file reading, extraction and comparison, use the verified local helper profile at [path] through m-series-local-helper. Keep Codex as controller and reviewer. Check live model identity, send only selected evidence, use one job at a time, and fall back to Codex if unavailable. Do not change models or download weights without approval.

Do not overwrite unrelated instructions; show the exact small addition in the setup plan. A remote Codex session needs access to the helper on the actual Mac; loopback on a cloud host is not the user's Mac. Do not expose an unauthenticated public port to solve this.

## Rollback

Record newly created files before modifying anything. Stop only the service launched for this setup, remove its wrapper/profile/instruction addition if requested, and restore the backed-up settings only when unchanged by later work. Keep existing runtimes/models and originals intact. Model deletion is a separate user decision. Never apply another person's complete global settings file.
