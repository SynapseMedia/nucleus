# Harvesting

The data harvesting stage involves obtaining "raw" information that is available to clean, structure, and validate it, and then distribute it on the network.

## Metadata

Metadata collection is carried out using models created based on the requirements of each user and following the [SEP001](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md) specification (the standard on which Nucleus is based for metadata management), which provides flexibility for different use cases.

Underneath the validation and schematization of the models is [pydantic](https://docs.pydantic.dev/latest/), so we can use [python standard library](https://docs.pydantic.dev/latest/usage/types/#standard-library-types) types to define fields.

In the example below, we have a model called Nucleus that extends the [Model](../reference/harvest/models.md) class. It includes fields such as name, description, and contributors, each defined with their respective types (str and List[str]).

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

nucleus_model = harvest.model(
    name=(str, ...), 
    description=(str, ...), 
    contributors=(List[str], ...)
)

```

To create an instance of the Nucleus model and populate it with data, you can do the following:

```python

nucleus: Model = Nucleus(
    name="Nucleus the SDK",
    description="Building block for multimedia decentralization",
    contributors=["Jacob", "Geo", "Dennis", "Mark"],
)

```

---

## Media

Let's explore multimedia resources and how to collect them using the SDK's built-in types.

In order to properly handle multimedia resources such as images, videos, music, text, and more, it is important to collect and categorize them using the appropriate types defined or provided by the SDK. These types allow for easy identification and handling of the resources during subsequent stages or processes in the pipeline.

Here's an example of how to collect media using the built-in media types:

```python

from nucleus.sdk.harvest import Image, Video

image = Image(path=Path("/local/path/image.jpg"))
video = Video(path=URL("/local/path/video.mp4"))

```

Alternatively, we can use the partial function to make it easier:

```python
import nucleus.sdk.harvest as harvest

image = harvest.image(path=Path("/local/path/image.jpg"))
video = harvest.video(path=URL("/local/path/video.mp4"))

```

!!! note
    It is also possible to create our own multimedia type as long as it is accompanied by an engine that takes care of its processing.
    Please check [built-in media types](../reference/harvest/media.md) and [built-in engines](../reference/processing/engines.md).
