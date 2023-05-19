import nucleus.core.subprocess as subprocess
from nucleus.core.types import Sequence


def migrate(*args: Sequence[str]):
    """Spawn nodejs subprocess to migrate data to orbitdb.

    :return: command to execute
    :rtype: Command
    """
    args_ = ' '.join(args)  # type: ignore
    command = f'npm run migrate -- {args_} --enc=json'
    sub = subprocess.call(command)
    _ = sub.communicate()
    # TODO what we dot with stdout?
