import itertools
import functools
import operator


def acc_gens(generators: iter) -> list:
    """
    Exec and Merge accumulative generators
    :param generators: Generator yielded by __call__ method
    :type generators: Generator[list]
    :returns Reduced and merged generators results
    """
    from_iter = itertools.chain.from_iterable(generators)
    return functools.reduce(operator.add, from_iter)


__all__ = ['acc_gens']
