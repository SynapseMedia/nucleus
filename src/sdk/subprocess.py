from . import logger
import asyncio


async def call_orbit(resolvers: list = None, recreate: bool = False):
    """Spawn nodejs subprocess

    :param resolvers: list of loaded resolvers
    :param recreate: if recreate=True new orbit repo is created else use existing
    """
    resolvers = resolvers or []
    is_mixed_migration = len(resolvers) > 0

    # Formulate params
    recreate_param = recreate and "-g" or ""
    command = f"npm run migrate -- {recreate_param}"

    # If mixed sources run each process to generate DB
    # else run all in one process and ingest all in same DB
    resolvers_call = (
        is_mixed_migration
        and [run(f"{command} --key={r} --source={r}") for r in resolvers]
        or [run(command)]
    )

    await asyncio.gather(*resolvers_call)


async def run(cmd: str):
    """Start an async subprocess cmd

    :param cmd: command to exec
    """
    proc = await asyncio.create_subprocess_shell(cmd)
    stdout, stderr = await proc.communicate()

    logger.log.info(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        logger.log.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logger.log.error(f"[stderr]\n{stderr.decode()}")
