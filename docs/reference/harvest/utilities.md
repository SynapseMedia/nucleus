::: nucleus.sdk.harvest.partials
    handler: python
    options:
      show_submodules: true
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false

## Built-in partials

```python
model = functools.partial(create_model, __base__=Model)
```

!!! note
    The partial `model` enhance the `create_model` pydantic factory function by extending the default [model](./models.md#nucleus.sdk.harvest.Model) as a base argument. This partial allows the fast creation of metadata models. For more information check [here](https://docs.pydantic.dev/latest/usage/models/).

```python
image = functools.partial(media_factory, base=Image)
video = functools.partial(media_factory, base=Video)
```

!!! tip
    We can extend the list of multimedia partials using `media_factory` and our own media type.
