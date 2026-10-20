# Pilot results

Benchmark: `tasks/test` (n=351, 64 distinct templates — disjoint from the 40
`tasks/train` templates), docker sandbox (`tbnano-sandbox:latest`,
`--network none`, fresh container per task, tests never mounted during the
episode), `--format json_tags`.

## Validation gate (`tbnano validate`)

* static + oracle + leak-check: **351/351 valid**, oracle 100% (local), 0
  shared templates and 0 instruction/setup fingerprint overlaps vs the
  305-task train split (`leak_overlap_count: 0`, `shared_templates: []`).
* Template counts: **64 test templates** (≥60 target), **40 train templates**
  (all prefixed `t_`); per-template counts in `tbnano/generators/__init__.py`.
* Levels: L1 25% / L2 37% / L3 28% / L4 9% (88/131/100/32 of 351; targets
  30/40/20/10 ±10pt).

## Pilot agents (docker, full 351-task test set)

| agent | n | pass@1 | CI95 (cluster) | partial | inv% | turns | tok |
|---|---|---|---|---|---|---|---|
| oracle (reference `solution.sh`, line-per-`run()`) | 351 | 98.9% | [96.3, 100.0] | 98.9% | 0.0% | 3.6 | 448 |
| quitter (`finish("")` on turn 1) | 351 | 0.0% | [0.0, 0.0] | 0.0% | 0.0% | 1.0 | 275 |

harness_errors: **0** in both runs (target: 0 — every internal exception ends
the episode as `harness_error` and is counted separately).

### By level (oracle, docker)

| level | n | pass@1 |
|---|---|---|
| L1 | 88 | 100.0% |
| L2 | 131 | 100.0% |
| L3 | 100 | 96.0% |
| L4 | 32 | 100.0% |

### Oracle failures: found and fixed a real sandbox gap

The only 4 oracle failures were `fixc-test-*`: `cc prog.c -o prog` failed
inside the container — the image shipped `gcc` but no libc headers, so
`stdio.h` was missing. `libc6-dev` was added to `docker/Dockerfile` and the
image rebuilt; all 4 `fixc-test-*` tasks then re-validated 4/4 in docker,
making the effective oracle rate **100%** (target ≥98%).

* **quitter**: every task fails as intended; end reason `finish` 100%
  (`finish("")` is a valid call, so `no_call` does not trigger).

## Regression coverage

`tests/` (145 tests) now pins the review fixes:

* tests dir is never copied into the sandbox during an episode — only
  `run_tests` stages them into a fresh one-shot container with `/task` read-only;
* malformed tool-call args (wrong types, missing fields, non-string `cmd`)
  are coerced or rejected with a tool-error nudge — the run never crashes,
  `invalid_calls` increments;
* `--sandbox local` with a real (non-scripted) backend refuses without
  `--unsafe-local` (exit 2);
* `test_*_present` checks count weight 0 in the `partial` score;
* every template in `TEST_TEMPLATES`/`TRAIN_TEMPLATES` generates a valid task
  and `spec.template` is recorded for the cluster bootstrap.

## Model pilots

No GPU/HF weights or API keys on this box — run on the dev machine
(Apple Silicon → `--backend mlx`, docker sandbox):

```bash
tbnano build-image                                   # one shared image, once
pip install -e '.[mlx]'

tbnano run --model hf:LiquidAI/LFM2.5-230M --format lfm_pythonic \
           --backend mlx --sandbox docker --jobs 1 --name lfm250m

tbnano run --model hf:Qwen/Qwen3.5-0.8B   --format hermes \
           --backend mlx --sandbox docker --jobs 1 --name qwen800m

tbnano run --model openai:gpt-4o-mini     --format openai \
           --backend api --sandbox docker --jobs 4 --name gpt4omini

tbnano report runs
```

Things to check in the table: pass@1 **monotonicity by level**
(L1 ≥ L2 ≥ L3 ≥ L4, roughly), `harness_errors == 0`, `invalid_calls` low,
and a failure sample (`runs/<name>/*.jsonl`, `end_reason != finish`) — the
review asks for a 20-failure analysis on LFM.
