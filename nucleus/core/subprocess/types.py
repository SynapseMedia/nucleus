from __future__ import annotations

import asyncio
from dataclasses import dataclass

from nucleus.core.types import Any

SubProcess = asyncio.subprocess.Process
Reader = asyncio.StreamReader
Loop = asyncio.BaseEventLoop


@dataclass(slots=True)
class StdOut:
    exit_code: int
    output: Any
