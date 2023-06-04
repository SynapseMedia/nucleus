# Harvesting

The data harvesting stage involves obtaining "raw" information that is available to clean, structure, and validate it, and then distribute it on the network.

## Metadata

Metadata collection is carried out using models created based on the requirements of each user and following the [SEP001](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md) specification (the standard on which Nucleus is based for metadata management), which provides flexibility for different use cases.

Underneath the validation and schematization of the models is [pydantic](https://docs.pydantic.dev/latest/), so we can use [python standard library](https://docs.pydantic.dev/latest/usage/types/#standard-library-types) types to define fields.

Here's an example of how you can define models by extending the [Model](../reference/harvest/models.md) class as the base class:
In this example, we define a model called Nucleus that extends the Model class from the nucleus.sdk.harvest module. The fields name, description, and contributors are defined with their respective types (str and List[str]).

```python
from nucleus.sdk.harvest import Model

class Nucleus(Model):
    name: str
    description: str
    contributors: List[str]

```

If you are function lovers you could step this using a partial function:

```python

import nucleus.sdk.harvest as harvest

# create a model using partial function
nucleus_model = harvest.model(
    name=(str, ...), 
    description=(str, ...), 
    contributors=(List[str], ...)
)

```

To create an instance of the Nucleus model and populate it with data, you can do the following:

```python
# set our data in the model
nucleus: Model = Nucleus(
    name="Nucleus the SDK",
    description="Building block for multimedia decentralization",
    contributors=["Jacob", "Geo", "Dennis", "Mark"],
)

```

---

## Media

Let's discuss multimedia resources and their collection using the types defined or predetermined by the SDK.

In order to properly handle multimedia resources such as images, videos, music, text, and more, it is important to collect and categorize them using the appropriate types defined or provided by the SDK. These types allow for easy identification and handling of the resources during subsequent stages or processes in the pipeline.

For example, the SDK may provide builtin data types for each type of multimedia resource. This could include Image and Video types, each with their respective properties and methods for processing and manipulation.

```python

from nucleus.sdk.harvest import Image, Video

# Collecting an image using the Image type
image = Image(path=Path("/local/path/image.jpg"))
# Collecting a video using the Video type
video = Video(path=URL("https://example.com/video.mp4"))

```

Using partials:

```python
import nucleus.sdk.harvest as harvest

# Collecting an image using the Image type
image = harvest.image(path=Path("/local/path/image.jpg"))
# Collecting a video using the Video type
video = harvest.video(path=URL("https://example.com/video.mp4"))

```

!!! note
    It is also possible to create a generic multimedia type as long as it is accompanied by an engine that takes care of its processing.
    Please check [builtin media types source](../reference/harvest/media.md) to see media builtin-types and [engine development guide](../../dev/docs/engines.md).
