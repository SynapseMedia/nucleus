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

Example processing a video:

```python
from nucleus.sdk.processing import HLS, VP9, Screen, Bitrate

# let's define how the output of our video should be.
video_engine.configure(HLS(VP9()))
video_engine.configure(Screen.Q1080)
video_engine.configure(Bitrate.B1080)
video_engine.save(Path("index.m3u8"))


```


!!! info
    Given that the engines emulate the underlying libraries, the available settings are based on the methods or configurations set within each respective library. For further details on the available settings, please refer to the [video](../reference/processing/video/settings.md) or [image](../reference/processing/image/settings.md) documentation.

