# Pilot results (spec v2)

Benchmark: `tasks/test` (n=411, 74 distinct templates — disjoint from the 48
`tasks/train` templates; 60 level-0 tasks in guided/plain pairs), docker
sandbox (`tbnano-sandbox:latest`, `--network none`, fresh container per task,
tests never mounted during the episode), `--format json_tags`.

## Validation gate (`tbnano validate`)

* static + oracle + leak-check, local: **411/411 valid**, oracle 100%,
  `leak_overlap_count: 0`, `shared_templates: []` (74 test / 48 train
  templates, all train prefixed `t_`).
* static + oracle, **docker**: **411/411**, oracle 100%.
* Levels: L0 15% / L1 21% / L2 32% / L3 24% / L4 8% (60/88/131/100/32).
* L0: 10 test templates × 3 seeds × {guided, plain} = 60 tasks; 8 disjoint
  `t_l0_*` train templates; `track:` + `max_turns: 4` in task.yaml.

## Pilot agents (docker, full 411-task test set)

| agent | n | pass@1 | grounded | end | turns |
|---|---|---|---|---|---|
| oracle (`tbnano validate`, `solution.sh` in docker) | 411 | **100%** | — | — | — |
| quitter (`finish("")` on turn 1) | 411 | **0.0%** | 0% | 100% | 1.0 |
| ls_then_quit (`ls` then `finish("")`) | 411 | **0.0%** | **100%** | 100% | 2.0 |

Spec v2 §8 gates: oracle ≥98% (100%), quitter 0% everywhere (no
accidentally-correct empty answers), ls_then_quit 0% with
`grounded_first_call = 100%` — all pass.

## Spec v2 additions

* **Process metrics** per trajectory (`harness_error` excluded):
  `valid_call_rate`, `grounded_first_call`, `loop_rate`, `error_recovery`,
  `proper_end`, `refusal_rate` — implemented in `tbnano/procmetrics.py`,
  aggregated in `report.json`, recomputable on saved trajectories via
  `tbnano metrics runs/<name>`.
* **Early loop stop**: 3 identical consecutive valid calls →
  `end_reason: "loop"` (tests still run); `--no-loop-stop` restores the
  pilot behaviour for comparability.
* **Protocol recorded** in `report.json` (`format`, `final_answer`,
  `sampling` + actual values, `flat_tools`, `max_context`, tbnano
  version + git hash) + `tasks_hash`; `tbnano report` warns on differing
  protocols or task sets.
* **L0 track** per spec §2; file-less physics tasks now read inputs from
  `params.json`/CSV (§6.1a — numbers unchanged, delivery changed);
  `csv_join` solution is pure-python in the task dir (§6.1b);
  binary-stdout docker regression test (§6.3).
* New report row: `model protocol pass@1[L0g L0p L1 L2 L3 L4] partial
  valid grounded loop recover end refusal turns tok`.

## Reference pilot numbers to reproduce (spec v2 §3)

Trajectories from the pilot run will be scored with `tbnano metrics` —
expected values (64-task pilot set):

| model | pass | valid | grounded | loop | recover | end | refusal |
|---|---|---|---|---|---|---|---|
| LFM2.5-230M | 0% | 99% | 44% | 35% | 27% | 72% | 28% |
| Qwen3.5-0.8B | 4% | 96% | 89% | 39% | 50% | 42% | 0% |
| small_sft | 0% | 75% | 5% | 2% | 0% | 0% | 0% |

Protocol detail from the pilot: Qwen3.5-0.8B solved 2 tasks via `finish`
and 6 via text final — `--final-answer tool|text` is part of the result and
is recorded under `protocol` in every report.json.

## Regression coverage

`tests/` (174 tests): tests never visible during the episode, arg coercion
and nudges, `--unsafe-local` gate, presence tests weight 0 in `partial`,
per-template generation, loop-stop (`loop` end reason, interrupts reset the
streak), ls_then_quit grounded=100% in docker, binary tool output does not
crash the episode (local + docker), resume path preserves process metrics.

## Model pilots

```bash
tbnano build-image                                   # one shared image, once
pip install -e '.[mlx]'

# native-protocol runs (headline = best of tool/text finals at recommended sampling)
tbnano run --model hf:LiquidAI/LFM2.5-230M --format lfm_pythonic \
           --backend mlx --sandbox docker --jobs 1 --name lfm250m \
           --final-answer text --sampling model --flat-tools

tbnano run --model hf:Qwen/Qwen3.5-0.8B   --format hermes \
           --backend mlx --sandbox docker --jobs 1 --name qwen800m

# ours
TBNANO_OURS_REPO=../small-test-llm \
tbnano run --model ckpt:runs/vast_small/small_sft/ckpt.pt \
           --backend ours --format json_tags --name small-sft

tbnano report runs
```
