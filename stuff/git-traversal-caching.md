# High-Performance Git History Traversal & Caching

To scale our git-native archive as hundreds of historical cycles accumulate, traversal algorithms must avoid brute-force parsing of git logs.

## traversal optimization strategies
1. **commit notes as metadata cache:** write metadata (such as cycle status, voter counts, and run duration) directly to git notes on HEAD. This allows querying a single lightweight ref rather than parsing raw commit blobs.
2. **local references & pointer tracking:** maintain a dedicated branch or reference pointer (like `refs/zociety/last-build`) to immediately locate the starting point of the next incremental build.
3. **on-demand traversal limits:** restrict history walk depths using specific boundaries (e.g. `git rev-list HEAD --not HEAD~20`) during continuous rendering runs.
