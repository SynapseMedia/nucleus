"""
The building block" packages here are intended to have minimal or no dependencies, those that have dependencies will be with
the same internal packages and as far as possible they will be utility packages.

Convention:
    Importing:
      - Every module or exceptions for SHOULD be imported using `import`, avoid use `from` for packages.
          eg. import src.core.cache as cache <- better reading and understanding.
          eg. import src.core.exceptions as exceptions
              raise exceptions.InvalidPrivateKey() <- immediately obvious where the exception comes from.
        IMPORTANT! An exception for this rule could be the package internal/relative import.
          eg. from .manager import exec
          
      - Even in cases where we are seeing some duplication between the type and the functions exposed by the package we SHOULD
        try to keep this convention so that the code is understood in a separate context between the abstractions and the executable commands/functions.
          eg.
            import src.sdk.harvest as harvest <- exposed module to being used
            from src.sdk.harvest import Movie <- imported type

            collected = harvest.load(...)
            harvest.merge_as(Movie, collected)

      - For constants or types the better approach is to import using `from` instead of `import` directly since that could be annoying
        keep referencing the package for every usage of type or constant.
          eg. from src.core.types import URI <- easy to use URI anywhere.

    Types:
    
      ## Dict vs Mapping
      - typing.Dict SHOULD be used to indicate a literal dict
      - typing.Mapping SHOULD be used for dynamic allocations
      
      ## Abstractions
      - strict: runtime check eg. ABC
      - soft: type hint check eg. Protocol
      - hybrid: allow both usages. e.:

          class Abstraction(Protocol, metaclass=ABCMeta):

              @abstractmethod
              def abc123(self):
                  ...

          .....

          # The client accept Abstraction in the same way with both use cases,
          # the difference lies in the implementation:

          class ImplicitImplementation:

              def abc123(self):
                  return "abc123

          class ExplicitImplementation(Abstraction):

              def abc123(self):
                  return "abc123


          def client(ExplicitImplementation()): ...
          def client(ImplicitImplementation()): ...
"""
