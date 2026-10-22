# Evidence behind the starting recommendations

Reviewed 22 October 2026. This is an evidence ledger, not a permanent leaderboard. “Best helper” means a supported configuration that completes the user's tasks at the required quality while leaving the Mac usable. A chip name or token-rate table alone cannot choose it.

The local cases below are maintainer-retained observations. Their raw private receipts are not published; this file publishes selected settings, outcomes and limitations. Primary public documentation is linked for the model/runtime contracts. New hardware needs its own acceptance test. No local record establishes a universal winner across M1–M6 or a quantified reduction in Codex subscription use.

## Evidence classes

| Label | Meaning |
|---|---|
| Local observation | A dated task or runtime result on the maintainer's machine |
| Documented | A capability or contract in identified source/documentation; not a local result |
| Publisher measurement | A model/runtime/hardware publisher's own reported experiment |
| Community measurement | An external contributor's reported experiment |
| Calculation / estimate | Derived planning arithmetic or a model; not measured performance |
| Recommendation | A judgment for a stated task and constraints, not another measurement |

Record negative and inconclusive results with the same care as successes. A working historical configuration remains historical evidence if a later request fails; the later failure still controls claims of current readiness.

## Current high-memory starting candidate: Qwen3.6-35B-A3B 8-bit

**Local observation, 22 October 2026.** The recorded 256 GB M5 Ultra case selected this sparse helper to replace a dense 27B general helper. Codex remained the controller and final reviewer.

| Component | Recorded configuration |
|---|---|
| Target | [mlx-community/Qwen3.6-35B-A3B-8bit](https://huggingface.co/mlx-community/Qwen3.6-35B-A3B-8bit) |
| Target revision | `e06a74e6236a60c8367e1a3214e83d8b61b637b0` |
| Draft | [incoai/Qwen3.6-35B-A3B-DFlash2](https://huggingface.co/incoai/Qwen3.6-35B-A3B-DFlash2) |
| Draft revision | `51ef7b6923ad6c14cb1bb41c37a9041446496ab6` |
| Server / engine | oMLX 0.7.2 managing native Splash 1.4.0 |
| Context / KV precision | 32,768 tokens / BF16 |
| Engine memory ceiling / persistent SSD cache | 64 GiB / 8 GiB |
| Idle unloading | 600 seconds |
| Extraction reasoning | Disabled for the bounded configuration-reading task |
| Target file bytes | 37,748,367,994 |

One activation task made a real selected-file read, returned valid configuration JSON, and completed in **0.568 seconds** after readiness. A follow-up completed in **0.245 seconds** without reading the same file again. Both reported **zero cached input tokens**. These are tiny integrated checks, not cold-start timings, broad quality measurements or cache-hit evidence.

The 64 GiB setting is an engine ceiling, not peak process memory or required RAM. The runtime separately reported an `actual_size` value of 40,349,673,000 bytes; it must not be confused with file bytes or total system memory. The eight-bit target was a deliberate quality/headroom choice for this high-memory machine. It is not the default for every Mac.

Why this is a useful candidate: its sparse architecture reduces executed model work while retaining a larger total target, the selected precision fits the recorded machine, and the exact native engine/draft pair completed bounded tool use. Total weights and runtime state still consume memory. This does not establish universal superiority over dense models or other runtimes. See the [Qwen target](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [Splash model support](https://github.com/incoai/splash) and [oMLX integration](https://github.com/jundot/omlx/blob/main/docs/Splash.md).

### Current negative evidence must travel with the success

During this skill's assembly on 22 October, the controller's new preflight reported the selected helper ready and the model inventory matched. An explicit session request then failed to identify the selected Splash child instance. A separate one-shot request over two short sources produced a final answer before full required source coverage, which the bounded helper rejected. No runtime settings were changed.

This is a current integration/protocol limitation. The historical successful receipts do not justify claiming that every current request succeeds. Preserve the exact failure layer, reject incomplete evidence, and continue the task with Codex. Do not silently substitute another target, remove coverage checks, or promise a speedup to conceal the failure.

## Separate proven 4-bit memory reviewer

**Local observation, 20 October 2026.** This earlier route is a distinct workload and configuration:

`DeepSeek cloud extraction → native Splash local quality review → applied knowledge records`.

- Engine: Splash 1.3.2, directly served, rather than the general helper's oMLX-managed engine.
- Target: [unsloth/Qwen3.6-35B-A3B-GGUF](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF), `UD-Q4_K_M`, revision `a483e9e6cbd595906af30beda3187c2663a1118c`.
- Same 35B-family DFlash2 draft, revision `51ef7b6923ad6c14cb1bb41c37a9041446496ab6`.
- Recorded scope: text-only short reviews, 16K context, 48G Metal ceiling, reasoning disabled, persistent disk prefix cache disabled.

| Check | Expected outcome | Observed time after loading |
|---|---|---:|
| Supported fact | Accept | 0.388 s |
| Invented claim | Reject | 0.249 s |
| Reversed reason | Reject | 0.350 s |
| Historical/current confusion | Reject | 0.176 s |
| Embedded instruction in a source | Reject | 0.300 s |

All five checks passed. Runtime counters recorded 609 drafted and 247 accepted draft tokens, so speculation executed. There were zero full prefix-cache hits and five cold misses. These timings cannot be attributed to warm prefix reuse. Real reviewed results were subsequently applied to nine sources in the first resumed batch.

A later dated snapshot recorded 215 completed requests, zero failures, normal system memory pressure and about 38.7 GiB allocated by the engine. That metric is not total system RAM. The operator observed better desktop responsiveness. Architecture, quantization, native execution, speculation and moving extraction to cloud all contributed to the changed system; no isolated multiplier or heavy-job concurrency result was measured.

The public [Aerodynamic AI for M5s collection](https://github.com/pmcconnon1993-lang/Aerodynamic-AI-for-M5s) preserves the architecture study and this proof summary. Preserve the narrow proof without presenting its five short checks as a general model-quality score. Native Splash can load supported GGUF weights; GGUF does not imply llama.cpp.

## Retained dense 27B helper

**Local observation, 20–21 October 2026; superseded as this installation's general default on 22 October.**

The previous target was [mlx-community/Qwen3.8-27B-8bit](https://huggingface.co/mlx-community/Qwen3.8-27B-8bit), revision `815b83c0df8ffd1d1b5244cf75fd6ef14fca9ef9`, paired with [incoai/Qwen3.8-27B-DFlash2](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2), revision `015e795645c74b1a0eeef3b570031fb62e769bc5`.

Recorded checks covered model-file sizes and selected hashes, selected-file tool use, image understanding, schema-enforced image output, and launcher restart followed by another tool call. The initial engine was native Splash 1.3.2 with 32K context; later session work used 1.4.0. These were small synthetic tasks. Full-context quality, concurrency and distributed inference were not measured.

The original Harness2 worker registry belongs to this exact 27B model and a software-configuration extraction domain. Its checked revision is a JSON-enforced baseline. Do not relabel that evidence as optimization or validation of the new 35B model, another precision, or a different task domain.

## Session/cache lessons from a real failure

**Local diagnosis and small task observations, 21 October 2026, on the previous 27B route.**

A changed question shared 3,732 tokens with a reference, below its 3,744-token restorable recurrent/draft-state boundary. Matching KV pages alone did not provide a usable complete state. Appending the follow-up to unchanged history reused 3,744 tokens. This was a prefix/state-boundary issue, not demonstrated eviction.

Two small comparisons recorded documentation follow-ups of 3.620 s fresh versus 0.744 s continued, and independent launcher/code follow-ups of 6.469 s versus 1.095 s. Checked facts and citations passed after fixing a double-numbered test fixture. A later 1.4.0 continuation needed one citation-length repair. These are individual observations, not a general speedup or reliability rate.

Transferable procedure:

- Use the same explicit session from the first call when useful follow-ups will use the same selected evidence.
- Append messages; preserve unchanged system/tool/source prefixes.
- Pin source hashes, model, endpoint, running engine instance/build, worker code, harness and output format. Changed identity starts fresh.
- Fail on context exhaustion or incomplete source coverage; never silently trim the evidence to claim success.
- Check actual cached-token counts, tool calls, factual quality and complete-task time. Session reuse alone proves no runtime cache hit.
- Keep weights, persistent caches and temporary spill locations separate in the storage plan. SSD caching does not remove active-context RAM requirements.

## Qwen-Agent knowledge: useful without adding another framework

**Documented source study, 22 October 2026.** [QwenLM/Qwen-Agent](https://github.com/QwenLM/Qwen-Agent/tree/31a4d36d123688581a9e9744427272b33ce940e0) was inspected at `31a4d36d123688581a9e9744427272b33ce940e0`. The native helper ran; an end-to-end Qwen-Agent framework installation did not run in this study.

- Choose one owner for tool formatting. The Qwen3.6 card recommends native tools with `model_type: qwenvl_oai` and `generate_cfg.use_raw_api: true`. Do not add a second ReAct/Nous/raw-tool-call prompt formatter.
- Match reasoning controls to the server. Local APIs use `extra_body.chat_template_kwargs`; cloud examples can differ. `/think` and `/nothink` are not the selected family's API controls.
- `enable_thinking: false` suits bounded extraction; difficult reasoning may need another setting. `preserve_thinking` and stable history can support reuse when the runtime forwards them.
- Studied framework defaults (58K input and 20 calls) exceed the old bounded helper's 32K/six-turn/eight-tool-call envelope. Framework defaults do not enlarge application permissions or memory budgets.
- Emitting several calls is not concurrent execution: the studied FnCallAgent loop runs them serially.
- Prove a harmless tool call, matching result IDs, final answer and bounds before claiming integration. An import or model tool-call field is insufficient.

Primary pointers: [native configuration example](https://github.com/QwenLM/Qwen-Agent/blob/31a4d36d123688581a9e9744427272b33ce940e0/examples/assistant_qwen3.5.py), [API conversion](https://github.com/QwenLM/Qwen-Agent/blob/31a4d36d123688581a9e9744427272b33ce940e0/qwen_agent/llm/base.py), [tool loop](https://github.com/QwenLM/Qwen-Agent/blob/31a4d36d123688581a9e9744427272b33ce940e0/qwen_agent/agents/fncall_agent.py), [Qwen model card](https://huggingface.co/Qwen/Qwen3.6-35B-A3B).

## Draft choice and older chips

**Documented, retained review 22 October 2026; refresh before setup.** The [Inco DFlash 2 collection](https://huggingface.co/collections/incoai/dflash-2) contains target-specific draft checkpoints. A small draft download is not a small standalone assistant. Pin target, draft, tokenizer/template and engine support together.

The retained review found ten entries covering seven target families, including format conversions. Qwen3.6-35B and Qwen3.8-27B drafts match the corresponding targets. Flash-Next, Ornith, GLM and Muse drafts require their full targets and exact supported implementations. NVIDIA evaluation in a card does not establish Apple support. A format conversion does not make a target compatible with every backend.

Official [Splash](https://github.com/incoai/splash) documented M3-or-newer support; the separate [M1/M2 port](https://github.com/paperniuk/splash) supplies an older-GPU route. The retained fork documentation lists Qwen3.6-35B-A3B MLX 4-bit as a fast MoE option and reports M2 Max use; its published timing is principally M1 Max. A 4-bit target was the practical starting recommendation for a recorded 64 GB M2 Max, retaining space for its desktop and services. That recommendation was not an executed installation in the latest review.

The latest retained M2 reachability check timed out. Earlier M2 K2 and desktop checks succeeded; preserve both dates. Do not infer current availability from either installed files or an old successful request.

## Other routes that informed the design

- **M2 K2 background helper:** a 64 GB M2 Max used an existing K2 Horizon MoVA 36B-A4B Q4_K_M, 16K context. A first 4,096-token request exhausted its answer budget; one narrower retry returned correct JSON in 5.18 s (~49.5 generated tok/s reported). This is small-task connectivity evidence, not coding-quality or interactive-speed superiority.
- **Narrow screenshot extraction:** deterministic Apple Vision OCR first, with an offline Qwen3.5-2B 4-bit model for unresolved fields. Small structured field checks and scoped rollback were tested. It does not establish general visual reasoning. [Model](https://huggingface.co/mlx-community/Qwen3.5-2B-4bit).
- **Security specialist:** a separate OrcaCyber Nano model used its existing Metal llama-server backend for advisory triage. No supported Splash conversion was established. A general helper should preserve specialized services rather than replace every model.
- **EXO:** distributing a model can increase usable capacity; it does not make remote RAM one physical unified pool or guarantee lower latency. RDMA/JACCL is transport, while EXO is an execution system. An older/slower node can help capacity and hurt latency. A visible node dashboard is not a loaded model or completed tool task. [EXO](https://github.com/exo-explore/exo), [MLX distributed guidance](https://ml-explore.github.io/mlx/build/html/usage/distributed.html).

These optional routes should not all be installed for a beginner's single-Mac helper.

## Runtime distinctions and estimator limits

The system-wide studies inspected MLX/MLX-LM, oMLX, Splash, Ollama, llama.cpp, LM Studio and EXO. The portable lessons are:

- Trace the actual model → artifact → engine → cache/compute path. MLX is a framework; oMLX is a service; Splash is a specialized engine; GGUF is a container. Inspected Ollama source can select MLX or llama-server depending on the model; product names do not uniquely identify a backend.
- Budget resident weights, KV/recurrent state, drafts, temporary prefill/verification buffers, caches, concurrency and the desktop. Active MoE parameters do not measure total residency.
- Distinguish prefill, decode, throughput and complete tool-task time. Retries and repairs count.
- Keep weight quantization, KV quantization, activation approximation, expert offload, ANE and GPU kernels separate. They are not an all-enabled preset. Apple GPU neural accelerators and the separate Apple Neural Engine differ.
- Prefer supported resident execution when it fits. Expert streaming is a capacity tradeoff; external SSD performance cannot be inferred from an internal-SSD report.
- A source feature or compiled kernel is not proof the installed build executes it.

At the inspected oMLX pin `737254287bdae3a53488baa73fe02368b7f18a4b`, its model recommender uses hard-coded quality-retention and speed assumptions, including 0.96 for oQ4e, 0.75 bandwidth efficiency and 1.5 MTP speedup. These are estimator inputs, not measured accuracy or throughput. Use the catalog to find candidates, then test them. [Pinned recommender](https://github.com/jundot/omlx/blob/737254287bdae3a53488baa73fe02368b7f18a4b/omlx/admin/model_recommender.py).

Primary runtime entry points: [MLX](https://github.com/ml-explore/mlx), [MLX-LM](https://github.com/ml-explore/mlx-lm), [oMLX](https://github.com/jundot/omlx), [Ollama](https://github.com/ollama/ollama), [llama.cpp](https://github.com/ggml-org/llama.cpp), [LM Studio mlx-engine](https://github.com/lmstudio-ai/mlx-engine). Verify current version, model format and API contracts before generating installation commands.

## External experiments retained as leads

| Evidence | Useful finding | What it does not establish |
|---|---|---|
| [NetworkChuck M5 Ultra/M3 Ultra study](https://github.com/theNetworkChuck/mac-studio-m5-ultra-local-ai/tree/0bdde4b5b0c6eff494a4edd0635b8bdf8d0a704b) | Author-reported cache-free Qwen3.6-35B-A3B MLX 4-bit at nominal 32K: 6,012 prompt tok/s, 109.1 output tok/s, 5.405 s first text. Independent arithmetic audit matched 42 cells/1,008 calculations. | No independent hardware rerun, quality ranking or MLX-versus-Splash result. Credit NetworkChuck; upstream measurements/documentation are CC BY 4.0. |
| [M5 Pro community comparison](https://www.reddit.com/r/oMLX/comments/1xajt4w/qwen3827b_local_speed_comparison_on_an_apple_m5/) and [TensorFold recipe](https://github.com/ashhart/TensorFold/blob/main/docs/recipes/qwen3.8-27b.md) | Reported TensorFold+DFlash2 and oMLX Lightning MTP configurations are worthwhile matched-test candidates. | Short unmatched runs, different precision/settings and shared engines cannot rank whole-task quality or establish a universal engine winner. |
| [DeepSeek V4.1 Flash community report](https://www.reddit.com/r/oMLX/comments/1xbdel0/fullprecision_deepseek_v41_flash_2025_toks_tg_500/) and [model card](https://huggingface.co/mlx-community/DeepSeek-V4.1-Flash-1017-oQ4e-mtp) | Reported M5 Ultra generation 18.8–30.8 tok/s, long prefill 516–532 tok/s and ~196–204 GB peak illustrate a heavy offloaded configuration. | No API-equivalent intelligence, spare desktop capacity, external-SSD performance or reproducible winner. Runtime/storage/cache/repetition definitions were incomplete; “65% offload” direction was ambiguous. |
| Maintainer metadata-only model scout | A 19-candidate sweep used configs/headers and published anchors to prioritize possible future tests without downloading weights. | Estimated sparse-model throughput could be substantially optimistic. A scout is neither a benchmark nor a quality evaluation. |

The scout considered alternatives such as Qwen3-Coder-Next, GPT-OSS-20B, Gemma 4 26B-A4B, GLM-4.7-Flash and Nemotron-3.5-Lightning. Preserve them as discovery leads until the exact current artifacts, Apple execution paths and task quality are established.

## How a new result earns a recommendation change

Use the [Google Research Harness2](https://github.com/google-research/harness2) idea of measured, checkable improvement without treating a prompt optimizer as a hardware benchmark. Freeze the task, baseline, independent checks and separate regression case. Compare real executions under the same model/tools/input when testing an instruction change. One focused change and a bounded serialized cycle are easier to assess than an unbounded optimization loop. A skill update does not train model weights.

For runtime/model comparisons, distinguish an implementation comparison (same target/precision, different implementation) from a deployment comparison (different configurations for the same useful task). Record exact chip/RAM/OS, model and draft revisions, runtime build, context, reasoning/sampling, concurrency, cache conditions, quality outcome, tool calls/repairs/failures, full task time, pressure/swap and storage growth. Report missing measurements as null with a reason.

Use repeated paired conditions such as ABBA or a recorded randomized schedule. Separate cold load, warm model/cold prefix, replay, appended tool results and changed prefixes. SSE events can contain several speculative tokens: chunks are not tokens. Acceptance ratio alone is not complete-cycle yield or speedup.

Critical correctness and source coverage precede speed. Retain failed/inconclusive runs. A contribution should contain public or synthetic tasks and reviewed, redacted metadata, with explicit permission to submit. Findings are reviewed data; they must not become arbitrary executable update hooks. Preserve the old recommendation and rollback until a candidate meets the stated quality, latency, headroom, storage and recovery requirements.

## Coverage and open questions

This synthesis used installed specialist knowledge, relevant memory records, targeted original receipts, prior source studies and the local knowledge graph. The graph had 5,304 semantic sources pending, eight unavailable conversations, and two pending code projects at inspection. It was used to find evidence, not as proof every historical record was understood. No new model download, runtime change or broad benchmark was performed for this inventory.

Missing evidence remains material: a matched all-chip/RAM matrix; M6 local results; broad 35B long-context/tool quality; heavy concurrency; restart/recovery across every route; and quality-adjusted Codex-usage savings. Support new or unverified chips through hardware discovery and current source checks, then a bounded local trial. Do not manufacture a model winner to fill an empty machine folder.

## Later same-day registry clarification

The selected 35B helper now has its own separate `unoptimized-baseline` source-reading registry. It preserves exact model identity and keeps the old 27B registry separate. The initial 35B registry has no adopted optimized prompt; its existence is configuration evidence, not a measured prompt gain. This supersedes any reading of earlier activation notes as implying that the 35B can never have a separate registry.
