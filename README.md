# TerminalBench Nano (`tbnano`)

A tool-calling-in-terminal benchmark for **small models (50M–1B parameters)** with
short contexts (≤8k tokens). Based on the ideas and task format of
[TerminalBench 1.0](https://github.com/laude-institute/terminal-bench), compressed
so that a 1B model can realistically attempt it:

* the agent acts through **4 tools** — `run`, `read_file`, `write_file`, `finish` —
  instead of an interactive terminal session;
* hard **token budgets** everywhere (system prompt, instruction, tool output, reply);
* **one shared Docker image** for all tasks (TB1 builds an image per task);
* deterministic task generators producing a **test** split (64 templates) and a
  **train** split (40 disjoint templates) — the template sets never intersect.

## Install

```bash
pip install -e .            # or: pipx / uv tool install .
tbnano build-image          # docker sandbox image (tbnano-sandbox:latest)
```

Python ≥3.10. Optional deps: `transformers` / `vllm` / `mlx-lm` (local model
backends), `openai` + `tiktoken` (API backend), `tokenizers` (`ours` backend).

## Quick start

```bash
# the shipped set: 351 test tasks (64 templates) + 305 train tasks (40 templates)
tbnano gen --split test --out tasks/test
tbnano gen --split train --out tasks/train

# validation: static checks + oracle must pass, empty run must fail, leak check
tbnano validate --tasks tasks/test --sandbox docker --jobs 8 \
    --check-leak --train tasks/train

# pilot agents
tbnano run --agent oracle  --sandbox docker --jobs 8 --name oracle
tbnano run --agent quitter --sandbox docker --jobs 8 --name quitter

# real models (as named in the ТЗ)
tbnano run --model hf:LiquidAI/LFM2.5-230M --format lfm_pythonic \
           --backend mlx --sandbox docker --jobs 1 --name lfm-230m
tbnano run --model hf:Qwen3.5-0.8B        --format hermes \
           --backend mlx --sandbox docker --jobs 1 --name qwen-08b
# or serve with vllm and use the API backend:
#   vllm serve LiquidAI/LFM2.5-230M
#   tbnano run --model api:LiquidAI/LFM2.5-230M --backend openai \
#              --format openai --base-url http://localhost:8000/v1
# our own checkpoint:
#   TBNANO_OURS_REPO=../small-test-llm \
#   tbnano run --model ckpt:runs/vast_small/small_sft/ckpt.pt \
#              --backend ours --format json_tags

# results
tbnano report --runs runs/
```

> **WARNING — `--sandbox local`**: it executes model-generated commands directly
> on this host with only `HOME` pointed at the task dir — there is no
> container boundary. It is intended for scripted agents (oracle/quitter)
> and debugging. With any real model backend the CLI refuses unless you add
> `--unsafe-local` explicitly. Use `--sandbox docker` for real runs.

## How an episode works

Per task, the harness builds a fresh sandbox (new container, task dir at
`/task`, `HOME` = task dir), then loops at most `max_turns` (≤12, L1 ≤6):

1. The model sees the system prompt (≤600 tok) + instruction (≤300 tok).
2. Its reply (≤256 tok) is parsed by the **format adapter** into a tool call.
3. The tool executes in the sandbox; output is truncated to ≤512 tok
   (head / `... [N lines cut] ...` / tail) and appended as a tool message.
4. The context is re-counted **after every appended message** — tool result,
   nudge, or error — against `min(8192, model context)` in the model's own
   tokenizer.
5. End reasons: `finish(answer)`, `max_turns`, `context_overflow` (always a
   failure), `timeout` (60 s cumulative exec, 10 s per call), `no_call` (two
   consecutive text-only replies end as `finish("")`), and `harness_error`
   (any internal harness exception — counted separately, target 0).
6. **Tests are never present in the sandbox during the episode.** The agent
   cannot `cat` the checker. After the episode ends, `run_tests` spins up a
   separate one-shot container with `/task` mounted **read-only** and the
   tests copied in, then runs pytest.

### Errors and nudges (protocol)

A malformed call — unparseable reply, unknown tool, or arguments of the wrong
type — never crashes the run: the model gets a `Tool call error: <reason>`
tool message and may retry (`invalid_calls += 1`). Scalar argument coercion is
lenient (P2-14): numbers/bools for string args are stringified, strings like
`"60"` for `start`/`lines` are coerced to int; anything else is an invalid call.

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

For `lfm_pythonic`/`hermes`/`openai` the HF backends pass `tools=TOOL_SCHEMAS`
to `apply_chat_template` with a short system prompt; if a tokenizer's template
does not accept `tools=`, the backend renders without it and logs a
`[tbnano] ... does not accept tools=` line (and keeps the adapter parsing the
raw text).

### Backends (`--backend`)

| backend | notes |
|---|---|
| `transformers` | `AutoModelForCausalLM` + `apply_chat_template` |
| `vllm` | `vllm.LLM` offline; or `vllm serve` + `--backend openai --base-url` |
| `mlx` | `mlx_lm.load` / `mlx_lm.generate` (Apple silicon) |
| `openai` | OpenAI-compatible API (`--base-url`, `OPENAI_API_KEY`, `TBNANO_API_BASE`) |
| `ours` | `TBNANO_OURS_REPO` repo providing `agent.py` (`load()->(model,tok,device)`, `generate(model,tok,ids,device,max_new,temp)` on token ids), `chat_format.py` (`render(messages, tools=)` + we append `<|im_start|>assistant\n`), `tokenizer/tokenizer.json` (`tokenizers.Tokenizer`). Trained ctx 1024 → `context_overflow` at 1024. |
| `scripted` | fake replies for tests and `--agent oracle/quitter` |

## Task format

```
tasks/<id>/
  task.yaml        # id, level 1-4, category, instruction, answer_mode,
                   # max_turns, tags, seed, split, template, origin?, rel_tol?
  setup/           # files copied into /task
  setup.sh         # optional, runs after copying setup/
  tests/test.py    # pytest — NEVER inside the sandbox during the episode
  solution.sh      # reference solution (oracle agent must pass)
```

`answer_mode`: `files` (score the dir), `answer` (score submitted answer),
`both`. For `answer` tasks the reference `solution.sh` writes `answer.txt`;
the agent's `finish` answer lands in `/task/.submission/answer.txt`.

Set composition (351 test tasks): L1 25% / L2 37% / L3 28% / L4 9%;
files_text 24%, data 18%, code 17%, env 9%, physics 32%. Each task carries a
`template` field — its generator archetype; the test split uses **64
templates** (3–16 seeded variants each), the train split **40 distinct
templates**, and `validate --check-leak` verifies both that no
instruction/setup-file hash collides and that the template sets are disjoint.
A few archetypes were adapted from TerminalBench 1.0 (`origin: tb1/<id>`).

**Presence tests**: checks named `test_*_present*` only assert an artifact
exists. They count for `resolved` but carry zero weight in `partial` — so a
junk file can't score 50%.

## Metrics

`runs/<name>/report.json` + `tbnano report`: pass@1 (resolved) with Wilson
95% CI **and a cluster bootstrap CI resampled by template** (variants of one
template are not independent — plain per-task CI underestimates), partial,
invalid_call_rate, harness_error count, mean turns/tokens, end_reasons,
per-level / per-category / per-template breakdowns. `pass@k` (unbiased) with
`--samples k`.

## Adding tasks / backends

* New template: add a function in `tbnano/generators/{ft,dt,ct,et,pt}.py`,
  register it + its count in `generators/__init__.py` (`TEST_TEMPLATES` /
  `TRAIN_TEMPLATES` must stay disjoint).
* Hand-written task: drop a dir matching the format into `tasks/<split>/` and
  run `tbnano validate`.
* New backend: implement `generate`/`count_context` from
  `tbnano/backends/base.py`, register in `backends/__init__.py`.
* New wire format: subclass `Adapter` in `tbnano/adapters/base.py`.
