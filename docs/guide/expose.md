# Expose

After learning how to collect, process, and store our media, it's time to understand how to distribute it to reach our target audience. In this guide, we will explore the necessary steps to process the metadata standard and its corresponding distribution through the federated network.

## Standard

Assuming you are already familiar with the anatomy of the standard, let's now examine its implementation. The adoption of the standard is crucial in ensuring smooth integration and compatibility across the federated network. By adhering to the standard defined in SEP001, metadata is effectively handled through an interface that facilitates signing, payload assignment, and the necessary headers.

If you need more details about the specific requirements and guidelines of the standard, please refer to the [specification document](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md).

Now, let's delve into the implementation of the standard in Nucleus.

Primero que nada definamos el tipo de medio a distribuir en la cabecera del standard :

```python
    import nucleus.sdk.expose as expose

    # create a standard instance for "image/jpeg" media resource
    sep001 = expose.standard(media_type)  
```

Ahora podemos comenzar a establecer las operaciones y metodo de serializacion que deseamos para nuestros metadatos.
Veamos un ejemplo siguiendo la misma definicion del standard anterior:

``` python
    # Prepare serialization
    sep001.set_operation(Sign)
    sep001.set_serialization(DagJose)
```

Una parte importante en el proceso de distribucion de los metadatos es la "firma", que nos permite establecer el origen de los datos y comprobar la propiedad o autoria de nuestros recursos multimedia. Este proceso agregar la llave publica y la firma a la cabecera de los metadatos.

Para firmar es simple usando algunos algoritmos "built-in" en el SDK. 
Mas adelante veremos como podemos exportar e importar nuestras llaves de modo que podamos portarlas.

```python
    # Add signature/recipient key
    sep001.add_key(expose.es256())

```

Ahora es tiempo de asociar nuestros datos a la carga util de los metadatos, en este paso agregamos informacion relacionada a los procesos de "harvesting", "almacenamiento" y "procesamiento". Veamos de que manera toda esta informacion se consolida en los metadatos a exportar:
```python
    # add metadata into payload
    sep001.add_metadata(Descriptive(**dict(nucleus)))
    sep001.add_metadata(Structural(cid=stored_file_object.hash))
    sep001.add_metadata(Technical(size=size, width=width, height=height))
```

Ya hemos preparado nuestros metadatos, es tiempo de enviarlos al "meta lake" y compartirlos.
Almacenar el standard es sencillo utilizando el "store" (visto previamente en la guia de almacenamiento), el cual sabra donde debe almacenar nuestro standard en dependencia del tipo de serializacion establecido. En el caso de ser DagJose lo enviara al entorno de IPLD por medio del servicio DAG de IPFS, si es una version compacta lo enviara directo a un Raw Block, veamos el ejemplo:

```python
    # we get signed dag-jose serialization.. let's store it
    obj: Object = sep001.serialize().save_to(local_storage)
    # what we do with our new and cool CID?
    logger.console.print(obj.hash)

```
