# Processing

This step is responsible for processing multimedia resources by performing transformations, transcoding, or other necessary operations based on the required parameters for each specific use case. This prepares the resources for consumption over the network.

## Engines

Engines are responsible for processing different types of media, providing configurations according to the nature of each multimedia type and its underlying library. These engines offer flexibility in modifying their behavior through their configurations and expose a standard output.

In this example, we use two distinct engines specifically designed for different types of multimedia and their corresponding configurations. Initializing an engine is simple by utilizing the functions provided by the processing package:

```python

import nucleus.sdk.harvest as harvest
import nucleus.sdk.processing as processing

from nucleus.core.types import Path
from nucleus.sdk.harvest import Image
from nucleus.sdk.processing import Engine

# initialize an Image type to pass into engine function
image = harvest.image(path=Path("image.jpg"))
# retrieve an Image engine from the input image
engine = processing.engine(image)

# ... below engine configuration

```

!!! tip
    The `engine` function from the `processing` package is a polymorphic function that automatically selects the appropriate engine based on the type of multimedia passed as a parameter. Please see more about [built-in engines](../dev/engines.md).

## Options

Each engine provides a set of built-in configuration options that modify the engine's output and are tailored to the specific characteristics of each multimedia type.

Configuring our engine is easy using the `configure` method.
Let's see an example of configuring the image engine:

```python

# import options from processing package
from nucleus.sdk.processing import Thumbnail, Coord

# we want to create a thumbnail from the image
# new thumb size is 50x50 output
engine.configure(Thumbnail(50,50))
# save our new image to our preferred path
output_image = engine.save(path=Path("image2.jpg"))

```

!!! info
    The options are derived from the methods or configurations established in each underlying library. Internally, the process involves preparing the library with the options provided during this stage. You can find more information about the available [options](../reference/processing/options.md).
