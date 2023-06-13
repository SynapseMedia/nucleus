from dataclasses import asdict

from nucleus.core.types import Any, Raw, Tuple

# TODO write test


def asdict_sanitize(obj: Any, exclude: Tuple[str]) -> Raw:
    """Does the same as asdict with the exception that it excludes some elements in the conversion.
    Internally the key with underscore are transformed to hyphens

    :param obj: Dataclass object
    :param exclude: The list of fields to exclude in dict
    :return: Dataclass dict with excluded fields
    """
    return asdict(
        obj,
        dict_factory=lambda x: {k.replace('_', '-'): v for k, v in x if k not in exclude},
    )
