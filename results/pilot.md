# Pilot results

Benchmark: `tasks/test` (n=325), docker sandbox (`tbnano-sandbox:latest`,
`--network none`, fresh container per task), `--format json_tags`.

## Validation gate (`tbnano validate`)

* static + oracle + empty-run: **325/325 valid**, oracle 100%, leak-free
  (instruction + setup-file fingerprints disjoint vs a 300-task train sample).
* Docker sandbox smoke (40-task subset): 40/40 valid, oracle 100%.

## Pilot agents

| agent | n | pass@1 | CI95 | partial | inv% | turns | tok |
|---|---|---|---|---|---|---|---|
| oracle (reference `solution.sh`) | 325 | 100.0% | [98.8, 100.0] | 100.0% | 0.0% | 3.2 | 437 |
| quitter (`finish("")` on turn 1) | 325 | 0.0% | [0.0, 1.2] | 0.0% | 0.0% | 1.0 | 281 |

The oracle upper bound is 100% ≥ the 98% spec target; the quitter floor is
0% ≤ 2% target. Mean oracle trajectory ≈3.2 turns / ≈437 tokens of context —
well inside the 8192-token budget (L4 tasks peak ≈498 tok).

## By level (oracle)

| level | n | pass@1 | CI95 | turns | tok |
|---|---|---|---|---|---|
| L1 | 85 | 100.0% | [95.7, 100.0] | 3.0 | 409 |
| L2 | 120 | 100.0% | [96.9, 100.0] | 3.0 | 419 |
| L3 | 90 | 100.0% | [95.9, 100.0] | 3.6 | 468 |
| L4 | 30 | 100.0% | [88.6, 100.0] | 3.5 | 498 |

## Failure analysis

* **oracle**: no failures. End reasons: `finish` 100%.
* **quitter**: every task fails as intended — `answer` tasks have no submission,
  `files` tasks leave `/task` unchanged; end reasons `finish` 100% (a
  text-free `finish` is a valid call, so `no_call` does not trigger).

## Model pilots

Not run on this box: no GPU/HF weights or API keys were provisioned. The
`transformers`/`vllm`/`mlx`/`openai`/`ours` backends are wired and exercised by
unit tests with fake replies; to run a real pilot:

```bash
tbnano run --model liquid/lfm2.5-230m --format lfm_pythonic --backend vllm
tbnano run --model qwen/qwen3-0.6b    --format hermes      --backend transformers
```
