# TerminalBench Nano (`tbnano`)

A tool-calling-in-terminal benchmark for **small models (50M–1B parameters)** with
short contexts (≤8k tokens). Based on the ideas and task format of
[TerminalBench 1.0](https://github.com/laude-institute/terminal-bench), compressed
so that a 1B model can realistically attempt it:

* the agent acts through **4 tools** — `run`, `read_file`, `write_file`, `finish` —
  instead of an interactive terminal session;
* hard **token budgets** everywhere (system prompt, instruction, tool output, reply);
* **one shared Docker image** for all tasks (TB1 builds an image per task);
* deterministic, seedable task generators producing a **test** and a **train**
  split with no leakage.

## Install

```bash
pip install -e .            # or: pipx / uv tool install .
# only Docker sandbox needs the image:
tbnano build-image
```

Python ≥3.10. Optional deps: `transformers`/`vllm`/`mlx` (HF backends),
`openai` + `tiktoken` (API backend).

## Quick start

```bash
# generate the shipped task set (325 test tasks are already in tasks/test/)
tbnano gen --split test --out tasks/test
tbnano gen --split train --out tasks/train --n 300

# validation: static checks + oracle agent must pass, empty run must fail,
# optional train/test leakage check
tbnano validate --tasks tasks/test --sandbox docker --jobs 8 \
    --check-leak --train tasks/train

# pilot agents
tbnano run --agent oracle  --sandbox docker --jobs 8 --name oracle
tbnano run --agent quitter --sandbox docker --jobs 8 --name quitter

# a real model
tbnano run --model liquid/lfm2.5-230m --format lfm_pythonic \
           --backend vllm --sandbox docker --jobs 4 --name lfm-230m
tbnano run --model qwen/qwen3-0.6b --format hermes --backend transformers

# results
tbnano report --runs runs/
```

`--sandbox local` runs commands in a subprocess (no Docker) — debug mode only.

## How an episode works

Per task, the harness builds a fresh sandbox (new container, task dir mounted at
`/task`), then runs a loop of at most `max_turns` (≤12, L1 ≤6):

1. The model sees the system prompt (≤600 tok) + instruction (≤300 tok).
2. Its reply (≤256 tok) is parsed by the **format adapter** into a tool call or text.
3. The tool executes in the sandbox; output is truncated to ≤512 tok
   (head / `... [N lines cut] ...` / tail) and appended as a tool message.
4. End reasons: `finish(answer)`, `max_turns`, `context_overflow` (>8192 tok of
   the model's own tokenizer — always a failure), `timeout` (60 s cumulative exec),
   `no_call` (two consecutive text-only replies end as `finish("")`).
5. After the episode, pytest tests (`tests/test.py` inside the task) score the
   resulting `/task` directory and the submitted answer.

### Tool schemas (OpenAI function format)

| tool | args |
|---|---|
| `run` | `cmd` — bash command in `/task`, 10 s wall clock per call |
| `read_file` | `path`, `start=1`, `lines=60` |
| `write_file` | `path`, `content` |
| `finish` | `answer` — for `answer`/`both` tasks |

### Format adapters

| `--format` | wire format | parser |
|---|---|---|
| `json_tags` | `<|tool_call|>{"name":"run","arguments":{...}}<|tool_call_end|>` | JSON |
| `lfm_pythonic` | `<|tool_call_start|>[run(cmd='ls')]<|tool_call_end|>` | `ast` only — **no eval** |
| `hermes` | `<tool_call>{"name":...}</tool_call>` | JSON |
| `openai` | native `tool_calls` | — |

`--backend` picks the model runner: `transformers`, `vllm`, `mlx`, `openai`
(API), `ours` (external repo via `TBNANO_OURS_REPO` providing `agent.py` /
`chat_format.py`), `scripted`.

## Task format

```
tasks/<id>/
  task.yaml        # id, level 1-4, category, instruction, answer_mode,
                   # max_turns, tags, seed, split, origin?, rel_tol?
  setup/           # files copied into /task
  setup.sh         # optional, runs after copying setup/
  tests/test.py    # pytest, run post-episode (partial credit = frac passed)
  solution.sh      # reference solution (oracle agent must pass)
```

`answer_mode`: `files` (score the dir), `answer` (score submitted answer),
`both`. For `answer` tasks the reference `solution.sh` writes `answer.txt` in
`/task`; the harness writes the agent's `finish` answer to
`/task/.submission/answer.txt`.

Test set: 325 tasks — L1 26% / L2 37% / L3 28% / L4 9%; categories
files_text 28%, data 18%, code 18%, env 9%, physics 26%; 70 tasks adapted from
TerminalBench 1.0 carry `origin: tb1/<id>`. Train split is generated with a
disjoint seed base and disjoint name pools; `tbnano validate --check-leak`
verifies no instruction/setup-file hash collides.

## Metrics

`runs/<name>/report.json` + printed table: pass@1 (resolved tasks) with Wilson
95% CI, partial (fraction of tests passed), invalid_call_rate, mean turns/tokens,
end_reasons. Per-level and per-category breakdowns included. `pass@k` (unbiased
estimator) with `--samples k`.

## Adding tasks / backends

* New generated family: add `gen_*` to `tbnano/generators/`, register in
  `FAMILIES`/`TEST_COUNTS` in `generators/__init__.py`.
* Hand-written task: drop a dir matching the format into `tasks/<split>/` and run
  `tbnano validate`.
* New backend: subclass `Backend` in `tbnano/backends/base.py` (`generate`,
  `count_context`), register in `cli.py`.
* New wire format: subclass `Adapter` in `tbnano/adapters/base.py`.
