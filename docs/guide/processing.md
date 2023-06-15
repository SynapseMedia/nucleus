# Processing

This step involves processing multimedia resources by performing transformations, transcoding, or other necessary operations based on the required parameters for each specific use case. These operations prepare the resources for consumption over the network.

## Engines

Engines are responsible for processing different types of media, providing configurations according to the nature of each multimedia type and its underlying library. These engines offer flexibility in modifying their behavior through their configurations and expose a standard output.

In this example, we will invoke the image processing engine and its configuration process based on the `settings`. Initializing an engine is straightforward with the functions offered by the processing package:

```python

import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing

from nucleus.core.types import Path
from nucleus.sdk.harvest import Image
from nucleus.sdk.processing import Engine

# initialize an Image type to pass into engine function
image = harvest.image(path=Path("image.jpg"))
# get back an Image engine from the input type
engine = processing.engine(image)

# ... below engine configuration

```

!!! tip
    The `engine` function from the `processing` package is a polymorphic function that automatically selects the appropriate engine based on the [type of multimedia](../reference/harvest/media.md) passed as a parameter. Please see more about [built-in engines](../reference/processing/engines.md) and [utilities](../reference/processing/utilities.md).

## Settings

Each engine provides a set of built-in settings that modify the engine's output and are tailored to the specific characteristics of each multimedia type.

Configuring our engine is straightforward with the use of the `configure` method.
Let's explore an example of how to configure the image engine:

```python

# import settings from processing package
from nucleus.sdk.processing import Thumbnail

# we want to create a thumbnail from the image
# new thumb size is 50x50 output
engine.configure(Thumbnail(50,50))
# save our new image to our preferred path
output_image = engine.save(path=Path("image2.jpg"))

```

!!! info
    Given that the engines emulate the underlying libraries, the available settings are based on the methods or configurations set within each respective library. For further details on the available settings, please refer to the [video](../reference/processing/video.md) or [image](../reference/processing/image.md) documentation.
