# Partials

Partial functions allow us to derive specific functions from complex functions, making their usage simpler. They are particularly useful when creating specialized versions of existing functions, reducing the number of arguments required for each call.

## Built-in partials

In the context of this document, partial functions are used to facilitate the quick creation of multimedia types or data models.

::: nucleus.sdk.harvest.partials.model
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_heading: true
      show_root_full_path: false

!!! note
    Extend the default Model base and use `create_model` from pydantic to create ready-to-use models.
    Learn more about `create_model` [here](https://docs.pydantic.dev/latest/usage/models/)

---
::: nucleus.sdk.harvest.partials.image
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_heading: true
      show_root_full_path: false


::: nucleus.sdk.harvest.partials.video
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_heading: true
      show_root_full_path: false

!!! note
    We use utility [media_factory](./utilities.md) create "out of the box" media models derived from media types.
