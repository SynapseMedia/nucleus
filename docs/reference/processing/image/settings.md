::: nucleus.sdk.processing.image.settings
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

## Coordinate System

"The Python Imaging Library uses a Cartesian pixel coordinate system, with (0,0) in the upper left corner. Note that the coordinates refer to the implied pixel corners; the centre of a pixel addressed as (0, 0) actually lies at (0.5, 0.5)." - [pillow](https://pillow.readthedocs.io/en/stable/handbook/concepts.html#coordinate-system)

::: nucleus.sdk.processing.image.settings.Coord
    handler: python
    options:
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: true
      show_root_full_path: false

!!! note
    During processing time, the setting classes are parsed as a method to dynamically call pillow image object.
    To know more about the settings implemented in this reference please see [pillow docs](https://pillow.readthedocs.io/en/stable/reference/Image.html).
