# Incremental Build Pipeline for Git-Native Archives

To avoid rebuilding the entire archive site from scratch for every new cycle event, we outline an incremental build strategy.

## Pipeline Architecture
1. **Change Detection:** Compare the current git commit with the previous build's commit reference (stored in a lightweight `.build-metadata.json` file).
2. **Surgical Rendering:** Only parse and render cycles and event logs that have changed or been added since the last build.
3. **Static Page Injection:** Inject newly generated cycle pages into the pre-existing archive index without rewriting previously generated HTML files.

## Benefits
- Reduces continuous integration (CI) run times from minutes to seconds.
- Minimizes CPU and disk I/O load.
- Prevents unnecessary cache invalidations on hosting platforms (like GitHub Pages).
