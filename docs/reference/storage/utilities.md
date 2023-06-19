
!!! info
    `Store` is a repository of storage options in the form of a function that automatically selects the appropriate storage strategy based on the type of the parameter

::: nucleus.sdk.storage.store
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false

## Built-in partials

```python
# default request to https://api.estuary.tech
estuary = functools.partial(Estuary, ESTUARY_API_BASE)
```

!!! info
    These partial allows the fast creation of [services](./services.md).
