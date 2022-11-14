
async def migrate(sources: Sequence[str], recreate: bool = False) -> None:
    """Spawn nodejs subprocess

    :param sources: list of sources to migrate into orbit
    :param recreate: if recreate equal True new orbit repo is created else use existing
    :return: None since is just a subprocess call
    :rtype: None
    """

    # Formulate params
    recreate_param = recreate and "-g" or ""
    commands = map(
        lambda r: Subprocess(
            "migrate", (recreate_param, f"--key={r}", f"--source={r}")
        ),
        sources,
    )

    process_list = [command() for command in commands]
    await asyncio.gather(*process_list)
