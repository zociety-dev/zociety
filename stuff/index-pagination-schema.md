# Paginated Index Schema for Git-Native Archives

To prevent the index files from growing indefinitely, we propose a partition/pagination schema for tracking historical cycle logs.

## Index Structure
Instead of a single `cycles.json`, the index is split into segments:
- `index.json`: Contains metadata and references to paginated chunk files (e.g., `chunk-1.json`, `chunk-2.json`).
- `chunks/chunk-N.json`: Contains a fixed batch of cycle summaries (e.g., 50 cycles per chunk).

## Advantages
1. **Faster Load Times:** Client browsers only need to fetch the latest chunk plus metadata.
2. **Minimal Git Diffs:** Only the active chunk file is modified during new cycles.
3. **Optimized Build Steps:** Build generation tools only rewrite the active chunk, leaving historical chunk files completely static.
