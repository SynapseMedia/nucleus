::: nucleus.sdk.processing.video.settings
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


## Defaults

::: nucleus.sdk.processing.video.settings
    handler: python
    options:
      members:
        - Screen
        - Bitrate
      annotations_path: source
      docstring_style: sphinx
      show_root_toc_entry: false
      show_root_heading: false
      show_root_full_path: false


!!! note
    During processing time, the setting classes are parsed as configuration arguments for [FFMPEG python library](https://github.com/kkroening/ffmpeg-python). To know more about the settings implemented in this reference please see [FFMPEG main options](https://ffmpeg.org/ffmpeg.html#Main-options).
