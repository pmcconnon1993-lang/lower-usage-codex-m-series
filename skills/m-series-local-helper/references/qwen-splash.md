# Qwen, Splash, oMLX and DFlash2

These are different layers:

| Layer | Job |
| --- | --- |
| Qwen target | The full assistant model that determines capability |
| MLX/GGUF + bit width | Weight representation; not a speed/quality verdict alone |
| DFlash2 draft | Target-specific speculative proposals verified by the full target |
| Splash | Specialized Apple Metal inference, target/draft execution and state reuse |
| oMLX | Serving/model management; may use native MLX or a Splash external engine |
| Qwen-Agent | Optional agent orchestration and tools; not a Metal engine |
| Codex | Task controller, selected evidence, verification and final actions |

The retained large-helper pair is `mlx-community/Qwen3.6-35B-A3B-8bit` + `incoai/Qwen3.6-35B-A3B-DFlash2`. Exact revisions and sizes are in `data/catalog.json`. The 4-bit 35B target shares the family, but is a separate configuration to test. DFlash2's small download is not a small standalone assistant. Consult the [author's collection](https://huggingface.co/collections/incoai/dflash-2), target card and runtime supported-model table together.

Sparse active parameters can lower per-token work; total weights still consume memory. Speculation depends on acceptance, block cost and target verification. Do not claim an isolated DFlash2 gain from an integrated workflow or cross-runtime timing. Preserve quality and total task latency in comparisons.

## Native tool calls

Send standard `tools`, preserve returned assistant `tool_calls`, and respond with the matching `tool_call_id`. The runtime owns serialization/parsing. Do not add an old Nous/ReAct template or literal tool markup as a second formatter.

For Qwen3.6 bounded extraction, `chat_template_kwargs: {enable_thinking: false}` is the source-supported control. `/think` and `/nothink` are not the control for this family. Choose reasoning for harder tasks and measure it. The preserved local route also supports `preserve_thinking: true`; verify forwarding on the selected runtime. Do not set Qwen-specific fields on unrelated models.

If Qwen-Agent is actually needed, its Qwen3.6 card recommends `model_type: qwenvl_oai` and `generate_cfg.use_raw_api: true`. Raw Qwen-Agent mode has its own streaming contract; the simpler native non-streaming worker is separate. At the studied Qwen-Agent revision, tool-result field conversion required checking against standard `tool_call_id`. Prove the actual emitted request, result association and final answer before claiming integration.

## Context and reuse

The recorded 8-bit helper used 32K context, BF16 KV, a 64 GiB Splash ceiling and 8 GiB SSD cache on a 256 GB Mac. Those are that setup's settings. Keep smaller machines/tasks smaller. KV quantization and cross-runtime cache policies require supported cache types and quality checks.

Stable prefixes and appended conversation history can allow state reuse. Historical recurrent/draft-state boundaries made superficially similar prompts miss the restorable prefix. Preserve exact source/history only when a bridge pins source hashes, runtime instance, version/configuration, model, format and context. A session label is not a cache hit; inspect reported cached tokens and elapsed task time. Never silently truncate source evidence to squeeze a prompt into a window.

Sources: [Qwen target](https://huggingface.co/Qwen/Qwen3.6-35B-A3B), [Qwen-Agent](https://github.com/QwenLM/Qwen-Agent), [Inco Splash](https://github.com/incoai/splash), [oMLX Splash integration](https://github.com/jundot/omlx/blob/main/docs/Splash.md), [M1/M2 port](https://github.com/paperniuk/splash), [MLX-LM](https://github.com/ml-explore/mlx-lm).
