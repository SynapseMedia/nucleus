# Overview

Nucleus follows a modular and layered design approach:

1. **The Core**: This layer contains the building block packages that have minimal or no external dependencies. Any dependencies within the core layer will be limited to other internal packages.

2. **The SDK**: The SDK exposes the programming-level API to interact with the core functions in a safe and conformant way.

3. **The CLI and HTTP API**: These components utilize the SDK to provide services through command-line interfaces (CLI) and HTTP API endpoints.

<!-- Add graph here -->

## Development tools

{% include-markdown "../../README.md"
    start="Development"
%}
