
::: nucleus.sdk.processing.video.options
    handler: python
    options:
      members:
        - FPS
        - BR
        - Custom
        - FrameSize
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false


----

!!! warning
    During processing time the options classes are parsed as configuration arguments for [FFMPEG python library](https://github.com/kkroening/ffmpeg-python). To know more about the options implemented in this reference please see [FFMPEG main options](https://ffmpeg.org/ffmpeg.html#Main-options).

## Defaults

::: nucleus.sdk.processing.video.options.Bitrate
    handler: python
    options:
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: true
      show_root_full_path: false

----

::: nucleus.sdk.processing.video.options.Screen
    handler: python
    options:
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: true
      show_root_full_path: false

