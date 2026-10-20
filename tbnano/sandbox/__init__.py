"""Sandboxes: where /task lives and commands/tests execute."""

from .base import ExecResult, Sandbox, TestResult
from .local import LocalSandbox


def make_sandbox(kind: str, **kwargs) -> Sandbox:
    if kind == "local":
        return LocalSandbox(**kwargs)
    if kind == "docker":
        from .docker import DockerSandbox

        return DockerSandbox(**kwargs)
    raise ValueError(f"unknown sandbox {kind!r}; use 'docker' or 'local'")


__all__ = ["Sandbox", "ExecResult", "TestResult", "LocalSandbox", "make_sandbox"]
