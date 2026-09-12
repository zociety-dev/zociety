# Paginated JSON Index & Incremental Pipeline Integration

To guarantee rapid client-side page load times across the zociety web archive, we implement an incremental pipeline that compiles and publishes paginated index datasets.

## key architectural features
1. **paginated index compilation:** compiles event and cycle logs into fixed-size chunks (e.g. 20 events per JSON file) rather than generating one massive monolithic JSON index.
2. **incremental build generation:** rebuilds only the indexes of active or modified cycles. Historical, frozen cycles are untouched, cutting build processing time from linear to constant.
3. **schema compliance validation:** enforces JSON schema validation on every compiled index file during the CI check phase before deploying to production pages.
