import itertools
import functools
import operator


def reduce_gens(generators: iter):
    """Execute generator function list and merge call results

    :param generators: Generator yielded by __call__ method
    :type generators: Generator[list]
    :return Reduced and merged generators results
    :rtype: list
    """

    from_iter = itertools.chain.from_iterable(
        generators)  # [[], [], []] -> flatten
    return functools.reduce(operator.add, from_iter)


__all__ = ["reduce_gens"]
