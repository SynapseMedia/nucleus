# Processing

This step involves processing multimedia resources by performing transformations, transcoding, or other necessary operations based on the required parameters for each specific use case. These operations prepare the resources for consumption over the network.

## Engines

Engines are responsible for processing different types of media, providing configurations according to the nature of each multimedia type and its underlying library. These engines offer flexibility in modifying their behavior through their configurations and expose a standard output.

In this example, we will invoke the image processing engine and its configuration process based on the `settings`. Initializing an engine is straightforward with the functions offered by the processing package:

```python

import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing

from nucleus.core.types import Path

# harvest media using media types
image = harvest.image(path=Path("image.jpg"))
video = harvest.video(path=Path("video.mp4"))

# get engines based on media type
image_engine = processing.engine(image)
video_engine = processing.engine(video)

```

!!! tip
    The `engine` function from the `processing` package automatically selects the appropriate engine based on the [type of multimedia](../reference/harvest/media.md) passed as a parameter. Please see more about [built-in engines](../reference/processing/engines.md) and [utilities](../reference/processing/utilities.md) reference.

## Settings

Each engine provides a set of built-in settings that modify the engine's output and are tailored to the specific characteristics of each multimedia type.

Configuring our engine is straightforward with the use of the `configure` method.
Let's explore an example of how to configure the image engine:

```python
from nucleus.sdk.processing import Thumbnail

# let's define how the output of our image should be.
image_engine.configure(Thumbnail(50,50)) # 50x50 px
output_image = engine.save(Path("image2.jpg"))

```

Example processing a video to HLS/VP9:

```python
from nucleus.sdk.processing import HLS, VP9, Screen, Bitrate

# let's define how the output of our video should be.
video_engine.configure(HLS(VP9()))
# set the screen quality to 1080p (Full HD).
video_engine.configure(Screen.Q1080)
# set the bitrate to 1080p (Full HD).
video_engine.configure(Bitrate.B1080)

output_file_name = 'index.m3u8'
output_directory = Path('my/output/dir')

# create the output directory if it doesn't already exist.
if not output_directory.exists():
    output_directory.mkdir()

# save HLS files to the new output path
output_path = Path(f'{output_directory}/{output_file_name}')
output_file = video_engine.save(output_path)

```

!!! info
    Given that the engines emulate the underlying libraries, the available settings are based on the methods or configurations set within each respective library. For further details on the available settings, please refer to the [video](../reference/processing/video/settings.md) or [image](../reference/processing/image/settings.md) documentation.

## Introspection

In the context of multimedia, introspection refers to the ability to obtain detailed and descriptive information about the elements and characteristics of a multimedia file. In the following example, we can see how to access the introspection obtained by the video engine:

```python

size = output_file.meta.size
width = output_file.meta.width
height = output_file.meta.height
media_type = output_file.meta.type
```

!!! tip
    The output of the engine returns a [File](../reference/processing/types.md) type object that contains an attribute called meta, which is essentially the result of introspecting the output multimedia file.

Another way we can use introspection is by using the engine with the `introspect` method. Let's also see an example:

```python

# get technical details from "video.mp4`
introspection = video_engine.introspect(Path("video.mp4"))

```

!!! warning
    [Introspection](../reference/processing/types.md) holds internal media information and technical details from media resources.
    Media introspection may vary based on the media type and underlying library.
    In the code snippet, introspection is obtained from `ffprobe`.
