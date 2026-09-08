# Updating the Claude Client in the Zociety Image

The Claude Code client is baked into the container image at build time
(`container/Containerfile`: `RUN npm install -g @anthropic-ai/claude-code`).
The container runs with a `--read-only` rootfs, so **you cannot update the
client inside a running container** — the update must happen at image-build time.

The install line is intentionally left **unpinned**. The CLI updates very
often; pinning a version creates constant churn and stale images. Do not add
`@<version>` to it.

## Updating the client

`bin/zociety --build` alone won't update the client: the `npm install` line is
unchanged, so podman reuses the cached layer and you get the *same old* client.
Force a fresh pull with a no-cache rebuild:

```bash
bin/zociety --rebuild      # podman build --no-cache — pulls the latest claude-code
```

This rebuilds the whole image (re-downloads Rust, uv, gh, etc.), so it is not
instant, but it is the correct way to move the client forward without pinning.

## Authentication

Mint a long-lived (~1yr) subscription OAuth token on the **host** and let the
wrapper inject it into the container. Interactive in-container `login` needs a
browser callback the headless, read-only container can't provide.

```bash
bin/zociety setup-token    # host browser flow → saves container/secrets/claude_oauth_token
```

The token is injected as `CLAUDE_CODE_OAUTH_TOKEN` on every `bin/zociety` run.
Do **not** create `container/secrets/anthropic_api_key` — an API key takes
precedence over OAuth and would disable the subscription token.

Rebuilding the image does not touch the token: it lives in `container/secrets/`
(and, for any in-container login, in the persistent `zociety-claude-home`
volume).

If auth still misbehaves after a rebuild, nuke the image + home volume for a
clean slate:

```bash
bin/zociety --clean        # removes image and zociety-claude-home volume
```

SSH and GPG keys are re-imported from `container/secrets/` by the entrypoint on
next run, so `--clean` only costs you the Claude login.

## Gotcha: two volume schemes

- `bin/zociety` (the wrapper) mounts the whole home as `zociety-claude-home`.
- `container/compose.yml` mounts only `.claude` as `claude-config`.

These are **different volumes**. Use the wrapper consistently, or you'll log in
to one volume and run the loop against the other.
