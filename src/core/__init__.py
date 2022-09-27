"""
"The building block" packages here are intended to have minimal or no dependencies, those that have dependencies will be with 
the same internal packages and as far as possible they will be utility packages.

Convention:
    Importing:
    - Every package or exceptions for should be imported using `import`, avoid use `from` for packages.
        eg. import src.core.cache as cache <- better reading and understanding.
        eg. import src.core.exceptions as exceptions
            raise exceptions.InvalidPrivateKey() <- immediately obvious where the exception comes from.
            
      IMPORTANT! An exception for this rule could be the package internal/relative import. 
        eg. from .manager import exec
      
    - For constants or types the better approach is to import using `from` instead of `import` directly since that could be annoying
      keep referencing the package for every usage of type or constant.
        eg. from src.core.types import URI <- easy to use URI anywhere.  
      
"""
