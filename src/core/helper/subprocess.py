from src.core import logger
import asyncio


async def run(cmd):
    """
    Start an async subprocess cmd
    :param cmd: Command to exec
    """
    proc = await asyncio.create_subprocess_shell(cmd)
    stdout, stderr = await proc.communicate()

    logger.info(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        logger.info(f'[stdout]\n{stdout.decode()}')
    if stderr:
        logger.error(f'[stderr]\n{stderr.decode()}')
