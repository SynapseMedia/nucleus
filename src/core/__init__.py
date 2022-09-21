"""
"The building block" packages here are intended to have minimal or no dependencies, those that have dependencies will be with 
the same internal packages and as far as possible they will be utility packages.

Convention:
    Importing:
    - Every package or exceptions should be imported using `import`, avoid use `from` for packages.
        eg. import src.core.cache as cache <- better reading and understanding for dev.
        eg. import src.core.exceptions as exceptions
            raise exceptions.InvalidPrivateKey() <- immediately obvious where the exception comes from.
    
    - For constants or types the better approach is to import using `from` instead of `import` directly since that could be annoying
      keep referencing the package for every usage of type or constant.
        eg. from src.core.types import URI <- easy to use URI anywhere.  
"""
