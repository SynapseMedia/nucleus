!!! info
    Partial functions allow us to derive specific functions from complex functions, making their usage simpler. They are particularly useful when creating specialized versions of existing functions, reducing the number of arguments required for each call.

## Factories

::: nucleus.sdk.harvest.partials
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false

!!! tip
    We can extend the list of multimedia partials using `media_factory` and our own media type.

## Built-in partials

```python
model = functools.partial(create_model, __base__=Model)
```

!!! info
    The partial `model` enhance the `create_model` pydantic factory function by extending the default [model](./models.md#nucleus.sdk.harvest.Model) as a base argument. This partial allows the fast creation of metadata models. For more information check [here](https://docs.pydantic.dev/latest/usage/models/).

```python
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)
```

!!! info
    These partial allows the fast creation of [media types](./media.md).
