# import inspect
# import pkgutil


# def loader(path: str):
#     """Import submodules from a given path
    
#     :param path: The path to search for submodules.
#     :returns: Generator of matched modules.
#     :rtype: Generator[Any, Any, Any]
#     """
#     for loader, name, is_pkg in pkgutil.walk_packages(path):
#         module = loader.find_module(name).load_module(name)
#         for _, obj in inspect.getmembers(module):
#             if inspect.isclass(obj) and is_pkg:
#                 yield obj


# __all__ = ["loader"]
