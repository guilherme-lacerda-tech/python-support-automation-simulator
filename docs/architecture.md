    # Architecture

    ## Design Goal

    Simulate a support automation workflow with fictional tickets and configurable generic rules.

    ## Current Boundaries

    - Standard library first.
    - Synthetic input only.
    - Generated output ignored by Git.
    - No real systems, endpoints or credentials.

    ## Decisions

    - Keep rules data-driven.
- Persist only synthetic tickets.
- Separate classification from storage.

    ## Future Layers

    ```mermaid
    flowchart TB
        A["Mock inputs"] --> B["Collector / Loader"]
        B --> C["Domain validation"]
        C --> D["Rules / Processing"]
        D --> E["Persistence"]
        E --> F["API / Reporting"]
        F --> G["Automation workflows"]
    ```
