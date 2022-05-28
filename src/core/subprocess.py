from . import logger
from .types import Command
from typing import List
from asyncio.subprocess import Process
import asyncio


async def call_orbit(resolvers: List[Command], recreate: bool = False) -> None:
    """Spawn nodejs subprocess

    :param resolvers: list of loaded resolvers
    :param recreate: if recreate=True new orbit repo is created else use existing
    :return: None since is just a subprocess call
    :rtype: None
    """
    resolvers = resolvers or []
    is_mixed_migration = len(resolvers) > 0

    # Formulate params
    recreate_param = recreate and "-g" or ""
    command = Command(f"npm run migrate -- {recreate_param}")  # Single command
    commands = [
        Command(f"{command} --key={r} --source={r}") for r in resolvers
    ]  # multiple commands

    # If mixed sources run each process to generate DB
    # else run all in one process and ingest all in same DB
    process_list = (
        [run(command) for command in commands] if is_mixed_migration else [run(command)]
    )
    
    await asyncio.gather(*process_list)


async def run(cmd: Command) -> Process:
    """Start an async subprocess cmd

    :param cmd: command to exec
    :return: None since is just a subprocess call
    :rtype: Process
    """
    proc = await asyncio.create_subprocess_shell(cmd)
    stdout, stderr = await proc.communicate()

    logger.log.info(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        logger.log.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logger.log.error(f"[stderr]\n{stderr.decode()}")
    return proc
