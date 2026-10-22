# Upstream evidence and refresh rules

Source review: **2026-10-22**. These are documented capabilities and public artifact identities, not a matched benchmark across every Mac. Model size in the catalog means repository disk bytes, not peak runtime memory. Local observations, publisher measurements and proposed candidates must remain separate.

## Runtime selection

| Runtime source | Verified version/scope | Decision |
|---|---|---|
| [oMLX README](https://github.com/jundot/omlx/blob/main/README.md), [v0.7.2 release](https://github.com/jundot/omlx/releases/tag/v0.7.2) | Latest checked release published 2026-10-21; macOS 15+; Apple Silicon; native app includes precompiled custom kernels | Friendly management/API default. Use its MLX engine for small models; verify actual backend and limits. |
| [oMLX Splash integration](https://github.com/jundot/omlx/blob/main/docs/Splash.md) | External Splash process, matched draft, local weight links, memory accounting; per-engine settings differ | oMLX can manage Splash without running the request through MLX. Do not combine their acceleration settings indiscriminately. |
| [Splash 1.4.0 README](https://github.com/incoai/splash/blob/1.4.0/README.md), [release](https://github.com/incoai/splash/releases/tag/1.4.0) | Published 2026-10-20; official M3+ and macOS 26.4+; 4-bit examples require 36 GB, recommend 48 GB | Candidate for specifically supported large Qwen targets; not a small-model universal backend. |
| [Splash M1/M2 fork](https://github.com/paperniuk/splash), [1.3.2-m1.2](https://github.com/paperniuk/splash/releases/tag/1.3.2-m1.2) | Explicitly unofficial; release notes report M1 Max/M2 Max testing and no sub-64-GB testing for this build | Optional experiment, not official support or an automatic old-Mac default. |
| [MLX installation](https://ml-explore.github.io/mlx/build/html/install.html), [MLX-LM v0.32.2](https://github.com/ml-explore/mlx-lm/releases/tag/v0.32.2) | Native Apple Silicon Python; framework docs state Python 3.10+ and macOS 14+; actual package wheel constraints still apply | Lightweight text helper fallback, with its own measured baseline and bounded client. |

oMLX source/Homebrew installs can omit native custom kernels; Qwen3.5 then uses slower generic paths. The official app bundles them. A successful install is not proof that the intended kernel or model executed. The reviewed README explicitly names M1-M5; M6 execution needs a real startup check.

Splash serves supported targets using specialized Metal kernels and a matching DFlash2 draft. Its source documents affine MLX 2-8-bit targets and supported GGUF variants. GGUF identifies a format, not llama.cpp. Original prepacked `incoai/*-Splash` targets are retired in the reviewed oMLX path. Use the target checkpoint and family-matched draft instead. [Splash documentation](https://github.com/incoai/splash/blob/1.4.0/README.md), [oMLX integration](https://github.com/jundot/omlx/blob/main/docs/Splash.md).

Public Splash numbers are publisher measurements on specific prompts and M5 Pro configurations. The M1/M2 port's numbers are maintainer/contributor observations on its stated systems. Neither establishes a universal winner. Compare actual correct task completion, cold and reused context, memory and retries.

## Model sources

| Role | Original publisher | Selected conversion/artifact |
|---|---|---|
| Very small fallback | [Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | [MLX 4-bit](https://huggingface.co/mlx-community/Qwen3.5-0.8B-MLX-4bit) |
| Small helper | [Qwen3.5-2B](https://huggingface.co/Qwen/Qwen3.5-2B) | [MLX 4-bit](https://huggingface.co/mlx-community/Qwen3.5-2B-MLX-4bit) |
| Compact helper | [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | [MLX 4-bit](https://huggingface.co/mlx-community/Qwen3.5-4B-MLX-4bit) |
| Mid-size helper | [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | [MLX 4-bit](https://huggingface.co/mlx-community/Qwen3.5-9B-MLX-4bit) |
| Sparse large helper | [Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | [MLX 4-bit](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-4bit), [MLX 8-bit](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-8bit) |
| Matching accelerator | [Inco Qwen3.6 DFlash2](https://huggingface.co/incoai/Qwen3.6-35B-A3B-DFlash2) | This draft belongs with the named target; it is not a standalone helper. |
| Alternative needing new evidence | [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | [MLX 8-bit](https://huggingface.co/mlx-community/Qwen3.8-27B-8bit); preserve distinct dense-model behavior and measurements. |

The selected repositories were public, ungated and Apache-2.0 at review. Preserve full IDs and pinned revisions. Similar names can refer to different conversion provenance. In particular, the selected small repositories contain `-MLX-4bit`; do not silently substitute `-4bit` repositories whose metadata differed.

The original Qwen cards describe broad model capability, including agent/tool use and native context. A converted quantization can behave differently. A 35B sparse model's roughly 3B active parameters do not mean only 3B of weights occupy memory. Draft weights, state, scratch and cache also need room. Candidate RAM tiers are conservative starting rules, not published hardware guarantees.

Qwen3.5-2B defaults to non-thinking. The 4B/9B and larger families must use their actual model template and supported settings. Qwen3.6 has optional reasoning preservation for suitable multi-turn work. Do not copy the original cards' multi-GPU vLLM/SGLang commands onto a Mac, or equate a 262K model context with a safe background-helper context. [Qwen 2B card](https://huggingface.co/Qwen/Qwen3.5-2B), [Qwen 35B card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B).

[Qwen-Agent](https://github.com/QwenLM/Qwen-Agent) is a separate application framework. It is useful reference material for tool conventions; a bounded Codex helper does not need the full framework or code interpreter merely to send selected text to a local API.

## Verified MLX-LM fallback contract

The [v0.32.2 Qwen implementation](https://github.com/ml-explore/mlx-lm/blob/v0.32.2/mlx_lm/models/qwen3_5.py) supports text-only loading and discards vision weights. The [server parser](https://github.com/ml-explore/mlx-lm/blob/v0.32.2/mlx_lm/server.py) exposes model/host/port, output default, template arguments, concurrency, prefill chunk size and prompt-cache limits.

There is **no server `--max-context` or `--max-kv-size` flag** in that version. `--max-tokens` limits output by default, not total context. The helper client must bound selected input and reject oversized work. Check installed `--help`; use `mlx_lm.server` or `python -m mlx_lm server`. Direct `python -m mlx_lm.server` is deprecated. Generic draft support is not proof of DFlash2 compatibility.

## Hardware sources

The machine guides link exact product specs. Verified variant labels at this review are:

```json
{
  "M1": ["base", "Pro", "Max", "Ultra"],
  "M2": ["base", "Pro", "Max", "Ultra"],
  "M3": ["base", "Pro", "Max", "Ultra"],
  "M4": ["base", "Pro", "Max"],
  "M5": ["base", "Pro", "Max", "Ultra"],
  "M6": ["base"]
}
```

[Apple M1 family](https://www.apple.com/newsroom/2021/10/introducing-m1-pro-and-m1-max-the-most-powerful-chips-apple-has-ever-built/), [M1 Studio](https://support.apple.com/en-us/111900), [M2 family](https://www.apple.com/newsroom/2023/01/apple-unveils-m2-pro-and-m2-max-next-generation-chips-for-next-level-workflows/), [M2 Studio](https://support.apple.com/en-us/111835), [M3 family](https://www.apple.com/newsroom/2023/10/apple-unveils-m3-m3-pro-and-m3-max-the-most-advanced-chips-for-a-personal-computer/), [M3 Ultra](https://www.apple.com/newsroom/2025/03/apple-reveals-m3-ultra-taking-apple-silicon-to-a-new-extreme/), [M4 family](https://www.apple.com/newsroom/2024/10/apple-introduces-m4-pro-and-m4-max/), [M5 Pro/Max](https://www.apple.com/ca/newsroom/2026/03/apple-debuts-m5-pro-and-m5-max-to-supercharge-the-most-demanding-pro-workflows/), [M5 Studio](https://support.apple.com/en-asia/128107), [M6 mini](https://support.apple.com/en-us/128108).

Unknown or future labels require discovery and a primary-source refresh. A current store configuration is not a complete history of owned Macs. Product RAM options are conditional on the actual product and CPU/GPU variant.

## Refresh and promotion

Before a new installation, refresh release requirements, model metadata/revision, license, file sizes and the selected hardware page. Record failed retrievals; keep the previous accepted snapshot without calling it fresh. Recheck upstream settings after a runtime upgrade.

New evidence belongs in a review queue with hardware, exact model/draft/runtime, workload, quality checks, memory and latency. Preserve negative results and prior accepted versions. Only independently reviewed evidence promotes a candidate. An update hook is not authorization to run contributor code, replace models, download weights, change services, or publish private files.

## Existing skill search

[Local Inference Optimizer](https://github.com/ForgetMeAI/local-inference-optimizer-skill) provides broad hardware/workload selection, while [Local Qwen Delegate](https://github.com/languor-daiduode/local-qwen-delegate) provides a Codex-compatible delegation skill. Both were inspected as related work. Neither supplied this requested all-Mac hardware/RAM evidence and setup workflow. This package is original guidance; do not import third-party commands as authority or assume their reported savings transfer.
