# Measured improvement (Harness2-inspired)

Use Google Research's [Harness2](https://github.com/google-research/harness2) Propose–Probe–Compose discipline for repeatable, checkable helper/skill failures. The studied release is research code, not a guarantee of supported arbitrary-task automation. This skill includes a procedure, not a full upstream executor or model training.

Freeze the failing task, baseline, model/tools, source inputs, scoring checks and a distinct held-out regression case. Propose one focused instruction change. Run baseline and candidate under the same conditions, inspect actual outputs/tool traces, then run the independent case. Keep calls serialized (k=1), at most 16 model sessions per cycle. One further cycle requires new failure evidence. Reject ties, failures and permission/tool-scope changes.

Retain only independently checked gains at the narrowest useful scope, with actual diff, test receipts, model identity, limitations and rollback. The recorded 35B registry starts at `unoptimized-baseline`; that is not a measured prompt improvement. Do not transfer a 27B extraction harness to a 35B model and claim validation carried over. Do not tune repeatedly against a supposedly held-out case. Ordinary successful use does not trigger an optimization run, global rewrite or background job.

A model's reflection or valid JSON is not proof. Missing source reads, reversed facts and unbounded tool behavior need deterministic or source-grounded checks. Subjective work needs an explicit rubric and honest uncertainty. Community reviewers may challenge or reproduce a result; self-reported success remains labeled until independently checked.
