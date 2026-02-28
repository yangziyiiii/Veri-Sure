from __future__ import annotations

import json
import os
import shutil
from subprocess import PIPE, Popen, TimeoutExpired
from typing import Tuple

from pydantic import BaseModel


class CommandResult(BaseModel):
    stdout: str
    stderr: str


def run_bash_command(
    cmd: str,
    timeout: float | None = None,
    *,
    cwd: str | None = None,
) -> Tuple[bool, str]:
    env = os.environ.copy()
    # Verilator 5.x may emit C++ flags unsupported by old system compilers
    # (e.g. -fcoroutines). Prefer GCC 13 toolchain when available.
    if not env.get("CXX"):
        cxx13 = shutil.which("g++-13")
        if cxx13:
            env["CXX"] = cxx13
    if not env.get("CC"):
        cc13 = shutil.which("gcc-13")
        if cc13:
            env["CC"] = cc13

    process = Popen(
        cmd,
        shell=True,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        cwd=cwd,
        env=env,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except TimeoutExpired:
        process.kill()
        err_msg = f"Timeout {timeout}s reached."
        return (
            False,
            json.dumps(
                CommandResult(stdout="", stderr=err_msg).model_dump(), indent=4
            ),
        )
    return (
        process.returncode == 0,
        json.dumps(CommandResult(stdout=stdout, stderr=stderr).model_dump(), indent=4),
    )
