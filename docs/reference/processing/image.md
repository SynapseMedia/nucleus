
!!! note
    All these setting options are defined by pillow library.
    During processing time the options classes are parsed as a method to dynamically call pillow image object.
    For more information please see all available options in [pillow docs](https://pillow.readthedocs.io/en/stable/reference/Image.html).

::: nucleus.sdk.processing.image.options
    handler: python
    options:
      members:
        - Crop
        - Thumbnail
        - Resize
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false
