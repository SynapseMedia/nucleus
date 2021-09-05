from . import logger
import asyncio


async def call_orbit(resolvers=None, regen=False):
    """
    Spawn nodejs subprocess
    :param resolvers: List of loaded resolvers
    :param regen: Regenerate db
    """
    resolvers = resolvers or []
    is_mixed_migration = len(resolvers) > 0

    # Formulate params
    regen_param = regen and "-g" or ""
    command = f"npm run migrate -- {regen_param}"

    # If mixed sources run each process to generate DB
    # else run all in one process and ingest all in same DB
    resolvers_call = (
        is_mixed_migration
        and [run(f"{command} --key={r} --source={r}") for r in resolvers]
        or [run(command)]
    )

    await asyncio.gather(*resolvers_call)


async def run(cmd):
    """
    Start an async subprocess cmd
    :param cmd: Command to exec
    """
    proc = await asyncio.create_subprocess_shell(cmd)
    stdout, stderr = await proc.communicate()

    logger.info(f"[{cmd!r} exited with {proc.returncode}]")
    if stdout:
        logger.info(f"[stdout]\n{stdout.decode()}")
    if stderr:
        logger.error(f"[stderr]\n{stderr.decode()}")
