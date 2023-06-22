# Expose

After learning how to collect, process, and store our media, it's time to understand how to distribute our metadata to reach our target audience. In this guide, we will explore the necessary steps to process the metadata standard and its corresponding distribution through the federated network.

## SEP001 Standard

Assuming you are already familiar with the anatomy of the standard, let's now examine its implementation. The adoption of the standard is crucial in ensuring smooth integration and compatibility across the federated network. By adhering to the standard defined in SEP001, metadata is effectively handled through an interface that facilitates signing, payload assignment, and the necessary headers.

If you need more details about the specific requirements and guidelines of the standard, please refer to the [specification document](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md).

Now, let's delve into the implementation of the standard in Nucleus.

First, let's define the type of media to distribute in the standard header:

```python
import nucleus.sdk.expose as expose

# create a standard instance for "image/jpeg" media resource
sep001 = expose.standard(media_type)  
```

## Cryptography & Serialization

!!! Note
    In Nucleus, it is possible to extend the signature/encryption algorithms using the [KeyRing](../reference/expose/types.md) protocol. You can see the [JWA](https://datatracker.ietf.org/doc/html/rfc7518) standard specification for more.

Now we can start establishing the cryptographic operations and serialization method we want for our metadata. Let's see an example following the same definition as the previous standard:

``` python
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

Now it's time to associate our data with the payload of the metadata. In this step, we add information related to the "harvesting," "storage," and "processing" steps. Let's see how all this information is consolidated in the exported metadata:

```python
# append metadata into payload
sep001.add_metadata(Descriptive(**dict(nucleus)))
sep001.add_metadata(Structural(cid=stored_file_object.hash))
sep001.add_metadata(Technical(size=size, width=width, height=height))
```

To store the standard, we can use the "store" function, which automatically determines the appropriate storage location based on the selected serialization type. If the serialization is set to DagJose, the metadata will be sent to the IPLD environment through the IPFS DAG service. If it is a compact version, it will be stored directly in a Raw Block. Let's see the example:

```python
# we get signed dag-jose serialization.. let's store it
obj = sep001.serialize().save_to(local_storage)
# What should we do with our new and cool CID?
logger.console.print(obj.hash)
```

!!! Example
    It is easy to retrieve our metadata using the tools provided by IPFS. In this case, we can use [DAG](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-dag-get) to traverse DagJose or the compact version using [Block](https://docs.ipfs.tech/reference/kubo/cli/#ipfs-block-get):

        ipfs dag get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
        ipfs block get bagcqceraajwo66kumbcrxf2todw7wjrmayh7tjwaegwigcgpzk745my4qa5a
