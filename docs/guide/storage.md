# Storage

In this guide, we will explore how to store processed media on the IPFS network using the storage package. We'll cover local storage, services, and clients. We have already learned how to collect multimedia resources and metadata, as well as basic aspects of multimedia processing.

## Local Storage

To store our media in the local IPFS node, we can use the `local storage` feature provided by the storage package. Initializing the local node is straightforward using the `ipfs` function.

Here's an example of how to store our processed image:

```python

import nucleus.sdk.storage as storage

local_storage = storage.ipfs("http://localhost:5001")
# in this case que are storing a File instance, we can obtain it from a processing output.
# if we have an already processed media we can create a custom File instance
stored_file_object = local_storage(output_image) 

```

In the example of video processing, HLS generates multiple files in the output directory. To ensure we capture all the files, including the entire directory, we have a solution for you (Don't worry, we've got your back).

Let's take a look at an example that shows how to handle this use case using the video processing example:

```python

import nucleus.sdk.storage as storage

local_storage = storage.ipfs("http://localhost:5001")
# we are not storing the File instance in this case since the File instance refers to the "index.m3u8" file only.
# instead, the output_directory is a Path instance that points to a directory containing the HLS files.
stored_directory_object = local_storage(output_directory) 

```

After storing the file locally, we can proceed to pin it or perform further actions.

!!! tip
    The `local_storage` is a repository of storage options in the form of a function that automatically selects the appropriate storage strategy based on the type of the parameter. Please see more about in [utilities](../reference/storage/utilities.md) reference.

## Services

Services are storage providers within the IPFS ecosystem. Currently, the SDK supports Estuary, a service that provides storage through the IPFS and Filecoin network. Here are some examples of how to configure the service and use it to store multimedia resources.

```python
from nucleus.sdk.storage import Estuary

estuary_endpoint = "https://api.estuary.tech"
estuary_key =  "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY" # fake key
estuary = Estuary(estuary_endpoint, estuary_key)

```

Alternatively, we can use the partial function to make it easier:

```python
import nucleus.sdk.storage as storage

# by default the endpoint is bundled inside the factory
estuary = storage.estuary(estuary_key)

```

Since our storage primarily takes place on our local node, we only need to pin our CID on the edge service.
Here's an example of how to pin the CID for our stored image:

```python

# ...
estuary.pin(stored_file_object)

```

!!! tip
    Any storage service that exposes an API is compatible and can be integrated into the SDK by implementing the [service protocol](../reference/storage/types.md). See more about [built-in services](../reference/storage/services.md) reference.
