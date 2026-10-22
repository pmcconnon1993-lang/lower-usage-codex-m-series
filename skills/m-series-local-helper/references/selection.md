# Select a candidate, then qualify it

Ask exact chip **and unified memory** first. M6 16 GB and M5 Max 128 GB need different choices despite the higher generation number. Check macOS, available SSD capacity, the actual target host, desktop workload and required task quality. Never use a cloud runner's Linux/RAM as the user's Mac specification.

The catalog's memory thresholds are conservative maintainer policy, not benchmark-derived fit guarantees. They keep the 35B 8-bit target off smaller Macs and leave room for tools, context and the desktop. At least 25% RAM (minimum 6 GiB) is a starting reserve; inspect actual pressure/swap. Model file size is neither total RAM nor peak residency. Account for target, draft, KV/recurrent state, prefill workspace, server buffers and other applications. Context, concurrency and quantization change this budget.

Reuse an explicit preference. Otherwise ask this preference once the viable choices are known:

> “Would you prefer a focused local helper using Splash where supported, or oMLX for managing and switching among several models? I recommend [choice] for your Mac because [specific reason].”

**Default preference: Inco Splash where the exact model and hardware are supported.** This reflects the project's tested route and operator preference, not a universal runtime ranking. oMLX and Splash are compatible layers: oMLX can manage a Splash external engine. They are not always competing engines. A multi-model setup need not keep multiple large models resident. Start one job/model at a time and use idle unloading. Never silently replace an existing selected configuration.

- M3 and later + macOS 26.4+ + supported 35B target: focused Splash or oMLX-managed Splash, matching DFlash2.
- M1/M2: normal oMLX/MLX is the conservative portable path. The separate paperniuk Splash port is an opt-in candidate after reviewing its current compatibility and running local qualification; label its maintainer and support separately from Inco upstream.
- Smaller Qwen3.5 2B/4B/9B candidates: oMLX native MLX; verify the exact architecture and installed runtime version. Do not attach the 35B draft to them.
- macOS below runtime requirements: research a supported release/path or explain the limit. Do not prescribe OS upgrades as an implicit setup step.
- Unknown/future chips or variants: verify Apple sources and exact runtime support, then propose tests. More RAM or bandwidth alone does not establish a winner.

The published M5 Ultra 256 GB 35B 8-bit setup is an evidence anchor, not a recommendation to allocate 256 GB or use 64 GiB engine caps on every computer. A 48–64 GB model tier starts 4-bit, shorter context and a separately measured memory budget. Larger targets are challengers for a defined task; do not turn a fast helper into a giant main model just because it fits.

Compare candidates on required factual/tool quality, complete-task time including review and repairs, prefill/TTFT, warm reuse, decode, memory pressure, idle/reload behavior and stability. Report uncertainty and keep a working baseline. Cloud-only completion may be the better result for a task a small local model cannot reliably do.
