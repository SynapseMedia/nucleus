# Storage

We have learned how to collect multimedia resources and metadata, and we have also covered basic aspects of multimedia processing. Now, in this guide, we will discuss how to store the processed media on the IPFS network using the storage package.

## Store

Como parte del proceso de almacenamiento, primero debemos almacenar nuestros medios en el nodo local de IPFS, y eso es lo que se encarga del "local store". La inicialización de nuestro nodo local es sencilla utilizando la función "store" del paquete de almacenamiento.

A continuacion veamos un ejemplo de como almacenamos una imagen en el almacenamiento local.

```python

import nucleus.sdk.storage as storage

local_storage = storage.ipfs("http://localhost:5001")
stored_file_object = local_storage(output_image) 

# ... below pinning stored file

```

## Services

Services are storage providers based on the IPFS ecosystem. Any service that exposes an API is compatible and can be integrated into the SDK.

Nucleus refers to these services as "Edge" because it uses them as external storage mediums to the local IPFS node. Currently, the SDK supports Estuary, a service that provides storage through the IPFS and Filecoin network. Let's see some examples of how to configure our service and how we can use it to store our multimedia resources.

```python
from nucleus.sdk.storage import Estuary

estuary_endpoint = "https://api.estuary.tech"
estuary_key =  "ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY" # fake key

# lets initialize our service
estuary = Estuary(estuary_endpoint, estuary_key)

# ... below client initialization
```

O podriamos hacerlo mas sencillo usando la funcion fabricadora:

```python
import nucleus.sdk.storage as storage

estuary = storage.estuary(estuary_key)

```

Ahora que tenemos listo nuestro servicio veamos como inicializar nuestro cliente de estuary

## Clients

Los clientes estan a cargo de interactuar directamente con las API provistas por los edge services, en este caso mostraremos el uso del API estuary.

Ya que nuestro almacenamiento se lleva a cabo primeramente en nuestro nodo local, solo necesitamos hacer pin de nuestro CID en el servicio edge.
Veamos el ejemplo:

```python
import nucleus.sdk.storage as storage

edge_client = storage.client(estuary)
edge_client.pin(stored_file_object)

```

!!! tip
    The `client` function from the `storage` package is a polymorphic function that automatically selects the appropriate API client based on the type of service passed as a parameter. Please see more about [built-in clients](../reference/storage/clients.md) and [utilities](../reference/storage/utilities.md).

!!! note
    Es posible extender los clientes y los servicios implementando las interfaces Client y Services disponibles en los tipos del paquete storage. Ver mas sobre built-in clients y built-in services.