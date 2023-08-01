
# Architecture

``` mermaid
graph LR
  A[Raw] --> B[Harvesting];
  B --> C[Expose];
  B -.-> D[Processing];
  B -.-> E[Storage]
  D -.-> E[Storage]
  E -.-> C[Expose]
  C --> F[Metalake]
  C -.-> G[Mint]
  F -.-> G[Mint]
```

Nucleus proposes a sequence of steps (pipeline) for the processing and decentralization of multimedia:

1. **Harvesting**: Collect metadata associated with the multimedia content.
2. **Processing**: Performing media processing tasks.
3. **Storage**:  Store the processed content in the IPFS network.
4. **Expose**: Distribute metadata through the IPFS ecosystem.
5. **Mint**: Create metadata as NFTs (Non-Fungible Tokens).
6. **Retrieval**: Facilitates the retrieval and unmarshalling of metadata from IPFS ecosystem.

The pipeline is modular and adheres to the decoupling principle, enabling flexible use cases. For instance, the **storage** component can be optional if data is already stored on the IPFS network. Similarly, the **mint** component can be skipped if there is no need to create NFTs for the metadata. The **processing** component may also be unnecessary if the media is already prepared for storage.

!!! tip
    Harvesting and Expose are the sole essential components necessary for operating the pipeline.

## Transmission/Distribution

As part of the interoperability and metadata federation, **Metalake** emerges as a new concept in the Nucleus ecosystem. It refers to the "global metadata public good" stored in the IPFS ecosystem, serving as a valuable information resource where everyone can freely exchange information. The [serialization](https://github.com/SynapseMedia/sep/blob/main/SEP/SEP-001.md) process of the metadata determines the transmission medium, with IPLD and Raw Blocks being among the means used by Nucleus eg:

``` mermaid
graph LR
  R[Expose] --> A[DagJose]
  A --> B[IPLD];
  D[Compact] --> F[Raw Block]
  R --> D[Compact]
```
