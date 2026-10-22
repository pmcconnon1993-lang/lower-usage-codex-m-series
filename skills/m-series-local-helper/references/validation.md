# Qualify the actual setup

A recommendation remains a candidate until these checks run on the user's actual Mac. Keep incomplete/failed checks visible. Do not use a clean package install, loaded model or model self-confidence as a pass.

1. **Identity:** exact chip, RAM, macOS, model repository/revision/precision, draft, runtime/build and actual engine. Confirm the endpoint is on the intended Mac and the returned model ID matches. A model shown in inventory might still be unloaded.
2. **Generation:** tiny prompt returns a complete response; record loading separately. Confirm reasonable memory pressure and no persistent swap growth under the intended workload.
3. **Native tool loop:** use one small synthetic file through `scripts/worker.py`; check a real `read_file` call, correct tool-result association, full contiguous file coverage and final answer against the source. A second case uses a decisive fact at the end, another conflicting value near the start and an embedded instruction to ignore the task. It must read all required evidence and treat that instruction as data.
4. **Task quality:** a representative real (authorized selected evidence) case with independent expected facts and citations. JSON parsing is separate from factual accuracy. Record repairs, rejected outputs, timeouts and unsupported claims.
5. **Resources and recovery:** complete-task latency, cold load, warm run, intended context, pressure/swap and idle unload/reload. Reuse at least one meaningful follow-up if the selected bridge supports sessions; count cached tokens rather than inferring hits. Do not run multiple heavy jobs before a separate concurrency test.

A safe synthetic file can describe two fictional services with different ports and an explicit revision. Ask for the active service/port/revision as JSON and verify exact values. No real secrets or user filenames are needed. The worker's configured context admission is conservative; smaller RAM tiers should pass a correspondingly smaller `--context-tokens` and output cap. Exceeding a bound is a rejected job, not silently truncated input.

## Comparing candidates

Freeze task, expected answers, tool scope and required quality. Distinguish an engine comparison (same target/precision) from a deployment comparison (different model/precision). Run a counterbalanced repeated sequence such as A-B-B-A. Record each individual run and failures, cold load separately, warm model/cold prefix, identical replay, appended history and changed prefix when relevant. Do not average away failed jobs.

Measure end-to-end time including parsing, tools, repairs and Codex review; log prefill/TTFT and output rate separately where available. SSE chunks may contain many speculative tokens. Use authoritative token counts; leave unobserved timing/memory values null with reasons. Engine allocation, process RSS and system used RAM are different metrics. SSD cache and active context RAM are not interchangeable.

Only call a setup better for the named task/hardware when required quality holds and practical latency/headroom improve. No local result in this repository proves account-wide Codex quota savings. A usage comparison must measure comparable completed tasks, cloud/controller overhead, retries, review effort and final quality under the same account conditions.
