"""Hard budget constants from the tbnano spec (section 2)."""

# Whole episode context, counted with the evaluated model's tokenizer.
MAX_CONTEXT_TOKENS = 8192
# System prompt including the tool schemas.
MAX_SYSTEM_TOKENS = 600
# Task instruction.
MAX_INSTRUCTION_TOKENS = 300
# One tool output, with honest head/tail truncation.
MAX_TOOL_OUTPUT_TOKENS = 512
# Agent turns per episode (level 1 tasks use <= 6, set per-task).
MAX_TURNS = 12
# Tokens the model may produce in one reply.
MAX_RESPONSE_TOKENS = 256
# Wall-clock seconds of command execution per task.
MAX_EXEC_SECONDS = 60.0
# Per-run() call timeout.
RUN_TIMEOUT_SECONDS = 10.0
# Per-task timeout for the verification pytest run.
TEST_TIMEOUT_SECONDS = 60.0
