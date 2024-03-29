# Expose

After learning how to collect, process, and store our media, it's time to understand how to distribute our metadata to reach our target audience. In this guide, we will explore the necessary steps to process the metadata standard and its corresponding distribution through the federated network.

## SEP-001 Standard

Assuming you are already familiar with the anatomy of the standard, let's now examine its implementation. The adoption of the standard is crucial in ensuring smooth integration and compatibility across the federated network. By adhering to the standard defined in SEP-001, metadata is effectively handled through an interface that facilitates signing, payload assignment, and the necessary headers.

If you need more details about the specific requirements and guidelines of the standard, please refer to the [specification document](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md).

Now, let's delve into the implementation of the standard in Nucleus.
First, let's define the type of media to distribute in the standard header:

```python
import nucleus.sdk.expose as expose

# using media_type declared in processing guide
# create a standard instance for "image/jpeg" media resource
sep001 = expose.standard(media_type)  
```

## Cryptography & Serialization

!!! Note
    In Nucleus, it is possible to extend the signature/encryption algorithms using the [Keyring](../reference/expose/types.md) protocol. You can see the [JWA](https://datatracker.ietf.org/doc/html/rfc7518) standard specification for more.

Now we can start establishing the cryptographic operations and serialization method we want for our metadata. Let's see an example following the same definition as the previous standard:

``` python
from nucleus.sdk.expose import DagJose, Sign

# serialization and sign operation
sep001.set_operation(Sign)
sep001.set_serialization(DagJose)
```

An important part of the metadata distribution process is the "signature," which allows us to establish the origin of the data and verify the ownership or authorship of our multimedia resources. This process adds the public key and signature to the metadata header.

Signing is simple using some "built-in" algorithms in the SDK:

```python

key = expose.es256()
sep001.add_key(key)

```

!!! Example
    We can export/import our key using the methods defined in the [KeyRing](../reference/expose/types.md) protocol. Let's see a simple example of how to do it:

    ```python
    # Export the key to later import it
    exported_key = key.as_dict()
    # Restore key to original state
    key.from_dict(exported_key)
    ```

## Metadata & Storage

Now it's time to associate our metadata with the payload. In this step, we add information related to the "harvesting," "storage," and "processing" steps. Let's see how all this information is consolidated in the exported metadata:

```python

# using nucleus model from harvesting guide
sep001.add_metadata(Descriptive(**dict(nucleus)))
# using stored file object from storage guide
sep001.add_metadata(Structural(cid=stored_image_object.hash))
# using introspection from processing guide
sep001.add_metadata(Technical(size=size, width=width, height=height))
```

!!! warning
    When considering structural metadata, specifically in the context of storing processed videos according to the [multimedia storage guide](./storage.md), it's crucial to understand that the hash obtained from `local storage` represents the stored directory's hash with files associated with the HLS protocol. Hence, it is essential to specify the supplementary path within the Structural type. For instance:

    ```python

    # using stored directory object from storage guide
    sep001.add_metadata(Structural(cid=stored_directory_object.hash, path="index.m3u8"))

    ```

!!! tip
    In this code snippet, we use `**nucleus` to unpack the `nucleus` model as `**kwargs` and populate the `Descriptive` metadata model.

To store the standard, we can use the [local store](../reference/storage/utilities.md) function, which automatically determines the appropriate storage location based on the selected serialization type. If the serialization is set to DagJose, the metadata will be sent to the IPLD environment through the IPFS DAG service. If it is a compact version, it will be stored directly in a Raw Block. Let's see the example:

```python
import nucleus.core.logger as logger

# we get signed dag-jose serialization.. let's store it
obj = sep001.serialize().save_to(local_storage)
# What should we do with our new and cool CID?
logger.console.print(obj.hash)
```

!!! example
    It is easy to retrieve our metadata using the tools provided by IPFS. In this case, we can use [DAG](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-dag-get) to traverse DagJose or retrieve the compact version using [Block](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-block-get):

        ipfs dag get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
        ipfs block get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
