import itertools
import functools
import operator


def acc_gens(lists):
    """
    Merge accumulative iterables
    """
    from_iter = itertools.chain.from_iterable(lists)
    return functools.reduce(operator.add, from_iter)


__all__ = ['acc_gens']
