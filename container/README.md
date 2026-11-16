# Zociety Container

Fully containerized Claude Code environment for zociety agent loops. Claude Code itself runs inside the container, providing complete isolation from the host system.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Host System                         │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Podman Container                      │  │
│  │                                                    │  │
│  │   ┌─────────────┐    ┌─────────────────────────┐  │  │
│  │   │ Claude Code │───▶│ bash, git, bin/*        │  │  │
│  │   └─────────────┘    └─────────────────────────┘  │  │
│  │          │                       │                 │  │
│  │          ▼                       ▼                 │  │
│  │   /home/agent/.claude     /repo (mounted)         │  │
│  │                                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                             │
│           Volumes: repo, credentials, plugins           │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Configure credentials (see "Setting Up Credentials" below)

# 2. Build the image
bin/zociety --build

# 3. Run interactive Claude session
bin/zociety

# 4. Or run the agent loop directly
bin/zloop 60
```

## Setting Up Credentials

The container uses dedicated credentials for the zociety agent identity. All files go in `container/secrets/` (gitignored).

### Claude authentication

Use the existing `claude_oauth_token` for subscription authentication, or
provide an API key:

```bash
echo 'sk-ant-api03-...' > container/secrets/anthropic_api_key
chmod 600 container/secrets/anthropic_api_key
```

### GitHub mirror credentials (optional)

GitLab is the primary forge; see **GitLab Service Account** below for its
credentials. The existing GitHub identity can still administer the mirror.

Generate a dedicated SSH key for agent@zociety.dev:

```bash
ssh-keygen -t ed25519 -C "agent@zociety.dev" \
    -f container/secrets/zociety_ssh_key -N ""
chmod 600 container/secrets/zociety_ssh_key
```

Then add the public key to the zociety GitHub account:
1. Copy the contents of `container/secrets/zociety_ssh_key.pub`
2. Go to GitHub → Settings → SSH and GPG keys → New SSH key
3. Paste the public key

### GPG Signing Key (for verified commits)

Generate a GPG key for agent@zociety.dev:

```bash
gpg --full-generate-key
# Choose: RSA and RSA, 4096 bits, no expiration
# Name: Zociety Agent
# Email: agent@zociety.dev
```

Export the key:

```bash
gpg --export-secret-keys --armor agent@zociety.dev > container/secrets/gpg_signing_key.asc
chmod 600 container/secrets/gpg_signing_key.asc
```

Add the public key to GitHub for verified commits:

```bash
gpg --export --armor agent@zociety.dev
# Copy output → GitHub Settings → SSH and GPG keys → New GPG key
```

### Summary: Local Credential Files

```
container/secrets/
├── claude_oauth_token       # Claude subscription token, or use an API key
├── anthropic_api_key        # Alternative Claude authentication
├── gitlab_token             # GitLab service-account API token
├── gitlab_account.json      # Nonsecret account and expiration metadata
├── zociety_gitlab_ssh_key    # Dedicated GitLab push key
├── zociety_gitlab_ssh_key.pub
├── gpg_signing_key.asc      # Commit/tag signing key
├── zociety_ssh_key          # Existing GitHub administration key (optional)
├── zociety_ssh_key.pub
└── github_token             # Existing gh CLI token (optional)
```

## GitHub Account Setup

The existing GitHub account administers the downstream mirror. New changes
and merge requests belong on GitLab.

### 1. Email Access

Set up forwarding from `agent@zociety.dev` to yourself (temporarily or permanently). This lets verification emails reach you while keeping the agent's email as the account identity.

### 2. Human-Assisted Registration

You create the account (CAPTCHA requires human eyes):
- Username: `zociety-dev`
- Email: `agent@zociety.dev`
- Complete CAPTCHA, click verification link

This is the one step that genuinely requires a human.

### 3. Add SSH Key to Account

```bash
cat container/secrets/zociety_ssh_key.pub
# Copy output → GitHub Settings → SSH keys → New
```

### 4. Add GPG Key to Account (for verified commits)

```bash
gpg --export --armor agent@zociety.dev
# Copy output → GitHub Settings → GPG keys → New
```

### 5. Create GitHub Token (for API/CLI access)

Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens:
- Token name: `zociety-container`
- Expiration: 90 days (or custom)
- Repository access: Select `zociety-dev/zociety`
- Permissions: Contents (read/write), Metadata (read)

Save the token:

```bash
echo "github_pat_xxxxxxxxxxxx" > container/secrets/github_token
chmod 600 container/secrets/github_token
```

### 6. Authenticate gh CLI

**Inside the container:** Authentication is automatic. The entrypoint exports `GITHUB_TOKEN` and `GH_TOKEN` from `/run/secrets/github_token`, and `gh` reads these env vars.

```bash
bin/zociety bash
gh auth status  # Should show logged in
```

**Outside the container (on host):** Use `--with-token` to authenticate non-interactively:

```bash
# Authenticate from the token file
gh auth login --with-token < container/secrets/github_token

# Or pipe it
cat container/secrets/github_token | gh auth login --with-token

# Verify
gh auth status
```

To set the git protocol explicitly (SSH vs HTTPS):

```bash
gh auth login --with-token --git-protocol ssh < container/secrets/github_token
```

The `--with-token` flag tells `gh` to read a PAT from stdin rather than launching the interactive browser flow.

### 7. Update Remote URL

Keep GitLab as origin and GitHub as the mirror remote:

```bash
git remote set-url origin git@gitlab.com:zociety/zociety.git
git remote set-url github git@github.com:zociety-dev/zociety.git
```

### What the Agent Can Do Independently

Once set up:
- Push/pull via SSH
- Create repos, issues, PRs via `gh` CLI
- Manage its own SSH/GPG keys via API
- Rotate tokens (with appropriate scopes)

### What Still Needs a Human

- Initial account creation (CAPTCHA)
- Recovery if 2FA device is lost
- Responding to GitHub support/abuse inquiries

## G󠄁i󠄁t󠄁L󠄁a󠄁b󠄁 a󠄁u󠄁t󠄁o󠄁m󠄁a󠄁t󠄁i󠄁o󠄁n󠄁

T󠄁h󠄁e󠄁 G󠄁i󠄁t󠄁L󠄁a󠄁b󠄁 h󠄁o󠄁m󠄁e󠄁 i󠄁s󠄁 [z󠄁o󠄁c󠄁i󠄁e󠄁t󠄁y󠄁/󠄁z󠄁o󠄁c󠄁i󠄁e󠄁t󠄁y󠄁](https://gitlab.com/zociety/zociety).󠄁
T󠄁h󠄁e󠄁 h󠄁u󠄁m󠄁a󠄁n󠄁 g󠄁r󠄁o󠄁u󠄁p󠄁 O󠄁w󠄁n󠄁e󠄁r󠄁 p󠄁r󠄁o󠄁v󠄁i󠄁s󠄁i󠄁o󠄁n󠄁s󠄁 t󠄁h󠄁e󠄁 n󠄁a󠄁t󠄁i󠄁v󠄁e󠄁 g󠄁r󠄁o󠄁u󠄁p󠄁 s󠄁e󠄁r󠄁v󠄁i󠄁c󠄁e󠄁 a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁
`zociety-dev`.󠄁 I󠄁t󠄁 h󠄁a󠄁s󠄁 M󠄁a󠄁i󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁 a󠄁c󠄁c󠄁e󠄁s󠄁s󠄁 t󠄁o󠄁 t󠄁h󠄁i󠄁s󠄁 p󠄁r󠄁o󠄁j󠄁e󠄁c󠄁t󠄁 a󠄁n󠄁d󠄁 n󠄁o󠄁 g󠄁r󠄁o󠄁u󠄁p󠄁
a󠄁d󠄁m󠄁i󠄁n󠄁i󠄁s󠄁t󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 r󠄁o󠄁l󠄁e󠄁.󠄁 `main` a󠄁c󠄁c󠄁e󠄁p󠄁t󠄁s󠄁 m󠄁e󠄁r󠄁g󠄁e󠄁s󠄁 b󠄁y󠄁 M󠄁a󠄁i󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁s󠄁;󠄁 d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁 a󠄁n󠄁d󠄁 f󠄁o󠄁r󠄁c󠄁e󠄁
p󠄁u󠄁s󠄁h󠄁e󠄁s󠄁 a󠄁r󠄁e󠄁 d󠄁i󠄁s󠄁a󠄁b󠄁l󠄁e󠄁d󠄁.󠄁 S󠄁e󠄁e󠄁 [G󠄁i󠄁t󠄁L󠄁a󠄁b󠄁 s󠄁e󠄁r󠄁v󠄁i󠄁c󠄁e󠄁 a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁s󠄁](https://docs.gitlab.com/user/profile/service_accounts/).󠄁

T󠄁h󠄁e󠄁 g󠄁i󠄁t󠄁i󠄁g󠄁n󠄁o󠄁r󠄁e󠄁d󠄁 `container/secrets/` d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁o󠄁r󠄁y󠄁 h󠄁o󠄁l󠄁d󠄁s󠄁 `gitlab_token` (󠄁a󠄁n󠄁
e󠄁x󠄁p󠄁i󠄁r󠄁i󠄁n󠄁g󠄁 s󠄁e󠄁r󠄁v󠄁i󠄁c󠄁e󠄁-󠄁a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 w󠄁i󠄁t󠄁h󠄁 `api` a󠄁n󠄁d󠄁 `write_repository` s󠄁c󠄁o󠄁p󠄁e󠄁s󠄁)󠄁,󠄁
`zociety_gitlab_ssh_key` (󠄁a󠄁 d󠄁e󠄁d󠄁i󠄁c󠄁a󠄁t󠄁e󠄁d󠄁 E󠄁D󠄁2󠄁5󠄁5󠄁1󠄁9󠄁 k󠄁e󠄁y󠄁)󠄁,󠄁 a󠄁n󠄁d󠄁 `gitlab_account.json`
(󠄁a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁,󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 I󠄁D󠄁 a󠄁n󠄁d󠄁 e󠄁x󠄁p󠄁i󠄁r󠄁y󠄁 m󠄁e󠄁t󠄁a󠄁d󠄁a󠄁t󠄁a󠄁 w󠄁i󠄁t󠄁h󠄁o󠄁u󠄁t󠄁 t󠄁h󠄁e󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 v󠄁a󠄁l󠄁u󠄁e󠄁)󠄁.󠄁 K󠄁e󠄁e󠄁p󠄁 p󠄁r󠄁i󠄁v󠄁a󠄁t󠄁e󠄁
f󠄁i󠄁l󠄁e󠄁s󠄁 m󠄁o󠄁d󠄁e󠄁 `0600`.󠄁 T󠄁h󠄁e󠄁 l󠄁a󠄁u󠄁n󠄁c󠄁h󠄁e󠄁r󠄁 m󠄁o󠄁u󠄁n󠄁t󠄁s󠄁 t󠄁h󠄁i󠄁s󠄁 d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁o󠄁r󠄁y󠄁 r󠄁e󠄁a󠄁d󠄁-󠄁o󠄁n󠄁l󠄁y󠄁 a󠄁t󠄁
`/run/secrets`.󠄁

`container/glab` l󠄁o󠄁a󠄁d󠄁s󠄁 t󠄁h󠄁e󠄁 m󠄁o󠄁u󠄁n󠄁t󠄁e󠄁d󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 f󠄁o󠄁r󠄁 e󠄁a󠄁c󠄁h󠄁 C󠄁L󠄁I󠄁 i󠄁n󠄁v󠄁o󠄁c󠄁a󠄁t󠄁i󠄁o󠄁n󠄁,󠄁 i󠄁n󠄁c󠄁l󠄁u󠄁d󠄁i󠄁n󠄁g󠄁
`podman exec`,󠄁 w󠄁i󠄁t󠄁h󠄁o󠄁u󠄁t󠄁 e󠄁x󠄁p󠄁o󠄁r󠄁t󠄁i󠄁n󠄁g󠄁 i󠄁t󠄁 t󠄁o󠄁 e󠄁v󠄁e󠄁r󠄁y󠄁 e󠄁n󠄁t󠄁r󠄁y󠄁p󠄁o󠄁i󠄁n󠄁t󠄁 c󠄁h󠄁i󠄁l󠄁d󠄁.󠄁 M󠄁i󠄁s󠄁s󠄁i󠄁n󠄁g󠄁 o󠄁r󠄁
e󠄁m󠄁p󠄁t󠄁y󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁s󠄁 c󠄁a󠄁u󠄁s󠄁e󠄁 A󠄁P󠄁I󠄁 c󠄁o󠄁m󠄁m󠄁a󠄁n󠄁d󠄁s󠄁 t󠄁o󠄁 f󠄁a󠄁i󠄁l󠄁 i󠄁n󠄁s󠄁t󠄁e󠄁a󠄁d󠄁 o󠄁f󠄁 u󠄁s󠄁i󠄁n󠄁g󠄁 i󠄁n󠄁h󠄁e󠄁r󠄁i󠄁t󠄁e󠄁d󠄁 c󠄁r󠄁e󠄁d󠄁e󠄁n󠄁t󠄁i󠄁a󠄁l󠄁s󠄁
o󠄁r󠄁 s󠄁t󠄁o󠄁r󠄁e󠄁d󠄁 l󠄁o󠄁g󠄁i󠄁n󠄁s󠄁.󠄁 S󠄁S󠄁H󠄁 u󠄁s󠄁e󠄁s󠄁 t󠄁h󠄁e󠄁 s󠄁e󠄁p󠄁a󠄁r󠄁a󠄁t󠄁e󠄁 G󠄁i󠄁t󠄁L󠄁a󠄁b󠄁 k󠄁e󠄁y󠄁 a󠄁n󠄁d󠄁 G󠄁i󠄁t󠄁L󠄁a󠄁b󠄁.󠄁c󠄁o󠄁m󠄁'󠄁s󠄁 p󠄁u󠄁b󠄁l󠄁i󠄁s󠄁h󠄁e󠄁d󠄁
E󠄁D󠄁2󠄁5󠄁5󠄁1󠄁9󠄁 h󠄁o󠄁s󠄁t󠄁 k󠄁e󠄁y󠄁 w󠄁i󠄁t󠄁h󠄁 s󠄁t󠄁r󠄁i󠄁c󠄁t󠄁 c󠄁h󠄁e󠄁c󠄁k󠄁i󠄁n󠄁g󠄁.󠄁 R󠄁e󠄁m󠄁o󠄁v󠄁i󠄁n󠄁g󠄁 t󠄁h󠄁e󠄁 m󠄁o󠄁u󠄁n󠄁t󠄁e󠄁d󠄁 S󠄁S󠄁H󠄁 k󠄁e󠄁y󠄁 c󠄁l󠄁e󠄁a󠄁r󠄁s󠄁
i󠄁t󠄁s󠄁 m󠄁a󠄁n󠄁a󠄁g󠄁e󠄁d󠄁 c󠄁o󠄁p󠄁y󠄁 a󠄁t󠄁 t󠄁h󠄁e󠄁 n󠄁e󠄁x󠄁t󠄁 c󠄁o󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁 s󠄁t󠄁a󠄁r󠄁t󠄁u󠄁p󠄁.󠄁

```bash
bin/zociety --build
bin/zglab api user | jq '{id, username}'
bin/zglab mr list --repo zociety/zociety
```

T󠄁h󠄁e󠄁 i󠄁d󠄁e󠄁n󠄁t󠄁i󠄁t󠄁y󠄁 c󠄁h󠄁e󠄁c󠄁k󠄁 m󠄁u󠄁s󠄁t󠄁 r󠄁e󠄁t󠄁u󠄁r󠄁n󠄁 `zociety-dev`.󠄁 `bin/zglab` u󠄁s󠄁e󠄁s󠄁 a󠄁 r󠄁u󠄁n󠄁n󠄁i󠄁n󠄁g󠄁
c󠄁o󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁 o󠄁r󠄁 s󠄁t󠄁a󠄁r󠄁t󠄁s󠄁 o󠄁n󠄁e󠄁 f󠄁o󠄁r󠄁 t󠄁h󠄁e󠄁 c󠄁o󠄁m󠄁m󠄁a󠄁n󠄁d󠄁.󠄁 T󠄁h󠄁e󠄁 r󠄁e󠄁p󠄁o󠄁'󠄁s󠄁 `glab` P󠄁A󠄁T󠄁H󠄁 s󠄁h󠄁i󠄁m󠄁 d󠄁o󠄁e󠄁s󠄁
t󠄁h󠄁e󠄁 s󠄁a󠄁m󠄁e󠄁;󠄁 `glab orbit` s󠄁t󠄁a󠄁y󠄁s󠄁 o󠄁n󠄁 t󠄁h󠄁e󠄁 h󠄁o󠄁s󠄁t󠄁 f󠄁o󠄁r󠄁 i󠄁t󠄁s󠄁 l󠄁o󠄁c󠄁a󠄁l󠄁 c󠄁o󠄁d󠄁e󠄁 i󠄁n󠄁d󠄁e󠄁x󠄁.󠄁 O󠄁u󠄁t󠄁s󠄁i󠄁d󠄁e󠄁
t󠄁h󠄁e󠄁 r󠄁e󠄁p󠄁o󠄁,󠄁 t󠄁h󠄁e󠄁 s󠄁h󠄁i󠄁m󠄁 u󠄁s󠄁e󠄁s󠄁 t󠄁h󠄁e󠄁 h󠄁o󠄁s󠄁t󠄁 C󠄁L󠄁I󠄁.󠄁 C󠄁r󠄁e󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 c󠄁o󠄁m󠄁m󠄁a󠄁n󠄁d󠄁s󠄁 n󠄁e󠄁e󠄁d󠄁 `--title`,󠄁
`--description` (󠄁o󠄁r󠄁 `--fill`)󠄁,󠄁 a󠄁n󠄁d󠄁 `--yes`.󠄁 B󠄁r󠄁o󠄁w󠄁s󠄁e󠄁r󠄁,󠄁 e󠄁d󠄁i󠄁t󠄁o󠄁r󠄁 a󠄁n󠄁d󠄁 s󠄁t󠄁d󠄁i󠄁n󠄁 f󠄁o󠄁r󠄁m󠄁s󠄁
a󠄁r󠄁e󠄁 r󠄁e󠄁f󠄁u󠄁s󠄁e󠄁d󠄁.󠄁

U󠄁s󠄁e󠄁 t󠄁h󠄁e󠄁 h󠄁u󠄁m󠄁a󠄁n󠄁 O󠄁w󠄁n󠄁e󠄁r󠄁'󠄁s󠄁 h󠄁o󠄁s󠄁t󠄁 c󠄁r󠄁e󠄁d󠄁e󠄁n󠄁t󠄁i󠄁a󠄁l󠄁s󠄁 f󠄁o󠄁r󠄁 a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁 a󠄁d󠄁m󠄁i󠄁n󠄁i󠄁s󠄁t󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁,󠄁 o󠄁u󠄁t󠄁s󠄁i󠄁d󠄁e󠄁
t󠄁h󠄁i󠄁s󠄁 r󠄁e󠄁p󠄁o󠄁 o󠄁r󠄁 w󠄁i󠄁t󠄁h󠄁 `env -u ZOCIETY_ROOT glab ...`.󠄁 U󠄁s󠄁e󠄁 t󠄁h󠄁e󠄁 [s󠄁e󠄁r󠄁v󠄁i󠄁c󠄁e󠄁 a󠄁c󠄁c󠄁o󠄁u󠄁n󠄁t󠄁s󠄁 A󠄁P󠄁I󠄁](https://docs.gitlab.com/api/service_accounts/)
t󠄁o󠄁 i󠄁s󠄁s󠄁u󠄁e󠄁 a󠄁 r󠄁e󠄁p󠄁l󠄁a󠄁c󠄁e󠄁m󠄁e󠄁n󠄁t󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁,󠄁 s󠄁a󠄁v󠄁e󠄁 i󠄁t󠄁 d󠄁i󠄁r󠄁e󠄁c󠄁t󠄁l󠄁y󠄁 t󠄁o󠄁 t󠄁h󠄁e󠄁 m󠄁o󠄁u󠄁n󠄁t󠄁e󠄁d󠄁 f󠄁i󠄁l󠄁e󠄁,󠄁 v󠄁e󠄁r󠄁i󠄁f󠄁y󠄁
t󠄁h󠄁e󠄁 c󠄁o󠄁n󠄁t󠄁a󠄁i󠄁n󠄁e󠄁r󠄁 i󠄁d󠄁e󠄁n󠄁t󠄁i󠄁t󠄁y󠄁,󠄁 t󠄁h󠄁e󠄁n󠄁 r󠄁e󠄁v󠄁o󠄁k󠄁e󠄁 t󠄁h󠄁e󠄁 o󠄁l󠄁d󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁.󠄁 C󠄁h󠄁e󠄁c󠄁k󠄁 t󠄁h󠄁e󠄁 l󠄁o󠄁c󠄁a󠄁l󠄁 m󠄁e󠄁t󠄁a󠄁d󠄁a󠄁t󠄁a󠄁
f󠄁o󠄁r󠄁 e󠄁x󠄁p󠄁i󠄁r󠄁y󠄁;󠄁 t󠄁h󠄁e󠄁 i󠄁n󠄁i󠄁t󠄁i󠄁a󠄁l󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 a󠄁n󠄁d󠄁 S󠄁S󠄁H󠄁 k󠄁e󠄁y󠄁 h󠄁a󠄁v󠄁e󠄁 a󠄁 9󠄁0󠄁-󠄁d󠄁a󠄁y󠄁 l󠄁i󠄁f󠄁e󠄁t󠄁i󠄁m󠄁e󠄁.󠄁 K󠄁e󠄁e󠄁p󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁
v󠄁a󠄁l󠄁u󠄁e󠄁s󠄁 o󠄁u󠄁t󠄁 o󠄁f󠄁 c󠄁o󠄁m󠄁m󠄁a󠄁n󠄁d󠄁 a󠄁r󠄁g󠄁u󠄁m󠄁e󠄁n󠄁t󠄁s󠄁,󠄁 t󠄁r󠄁a󠄁c󠄁k󠄁e󠄁d󠄁 f󠄁i󠄁l󠄁e󠄁s󠄁,󠄁 d󠄁i󠄁s󠄁c󠄁u󠄁s󠄁s󠄁i󠄁o󠄁n󠄁s󠄁 a󠄁n󠄁d󠄁 l󠄁o󠄁g󠄁s󠄁.󠄁

GitLab is `origin` and owns cycle landing and CI. The `github` remote is
GitLab's native downstream SSH mirror, using a dedicated write-enabled deploy
key and pinned GitHub host key. Divergent downstream refs are retained and
reported rather than overwritten. Pages deployment is unchanged by this
migration.

The native mirror covers branches and tags. Git notes are replicated directly
to the `github` remote by the native runner's provenance tools, using ordinary
fast-forward pushes so divergent notes are reported rather than overwritten.
CI enables this supplement only when its separately approved GitHub token
file is present.

`bin/test-zglab` e󠄁x󠄁e󠄁r󠄁c󠄁i󠄁s󠄁e󠄁s󠄁 c󠄁r󠄁e󠄁d󠄁e󠄁n󠄁t󠄁i󠄁a󠄁l󠄁 r󠄁e󠄁f󠄁u󠄁s󠄁a󠄁l󠄁,󠄁 t󠄁o󠄁k󠄁e󠄁n󠄁 p󠄁r󠄁e󠄁c󠄁e󠄁d󠄁e󠄁n󠄁c󠄁e󠄁,󠄁 r󠄁u󠄁n󠄁 a󠄁n󠄁d󠄁 e󠄁x󠄁e󠄁c󠄁
r󠄁o󠄁u󠄁t󠄁i󠄁n󠄁g󠄁,󠄁 h󠄁o󠄁s󠄁t󠄁 p󠄁a󠄁s󠄁s󠄁t󠄁h󠄁r󠄁o󠄁u󠄁g󠄁h󠄁,󠄁 n󠄁o󠄁n󠄁-󠄁i󠄁n󠄁t󠄁e󠄁r󠄁a󠄁c󠄁t󠄁i󠄁v󠄁e󠄁 a󠄁r󠄁g󠄁u󠄁m󠄁e󠄁n󠄁t󠄁s󠄁 a󠄁n󠄁d󠄁 S󠄁S󠄁H󠄁 c󠄁o󠄁n󠄁f󠄁i󠄁g󠄁u󠄁r󠄁a󠄁t󠄁i󠄁o󠄁n󠄁 i󠄁n󠄁
t󠄁h󠄁r󠄁o󠄁w󠄁a󠄁w󠄁a󠄁y󠄁 f󠄁i󠄁x󠄁t󠄁u󠄁r󠄁e󠄁s󠄁.󠄁 I󠄁t󠄁 i󠄁s󠄁 i󠄁n󠄁c󠄁l󠄁u󠄁d󠄁e󠄁d󠄁 i󠄁n󠄁 t󠄁h󠄁e󠄁 t󠄁o󠄁o󠄁l󠄁i󠄁n󠄁g󠄁 C󠄁I󠄁 m󠄁a󠄁t󠄁r󠄁i󠄁x󠄁.󠄁

## GitLab CI

MR/default-branch pipelines run state validation. Tooling changes also run
shellcheck, gitleaks, fixture harnesses, the secret-transfer proof, and static-site tests with full
history and tags. Tests have no `autonomous` environment or model credentials.
Agent-proposed workflows target `.gitlab/ci/` and become active only after
approval and merge.

To enable CI automation, explicitly approve copying the following local
credentials into this project's GitLab CI variables. Use type **File**,
**Protected**, **Raw**, **Masked and hidden**, and environment scope
**autonomous**. Keep values out of command arguments and logs.

| GitLab variable | Mounted file under `/run/secrets` | Purpose |
| --- | --- | --- |
| `ZOCIETY_GITLAB_TOKEN_FILE` | `gitlab_token` | Service-account Git/API access |
| `ZOCIETY_CLAUDE_OAUTH_TOKEN_FILE` | `claude_oauth_token` | Claude subscription authentication |
| `ZOCIETY_GPG_SIGNING_KEY_FILE` | `gpg_signing_key.asc` | Optional commit/tag signing |
| `ZOCIETY_BLIND_KEY_FILE` | `blind_key` | The shared provenance sealing key |
| `ZOCIETY_GITHUB_TOKEN_FILE` | `github_token` | Replicate provenance notes to the GitHub mirror |

Use the reviewed operator command after approving that destination and scope.
All five files must already be available through the container's secret mount,
including `blind_key` containing the existing provenance passphrase. The
provisioner never generates or rotates that passphrase and never falls back
to a host environment variable. It uses the mounted armored signing key
directly; do not import the agent's private key into the host keyring.

Run from the repository root in your own terminal. Start the container with
`bin/zociety bash` in another terminal if it is not running. The provisioner
uses that running container and fails if it is unavailable.

```bash
# Reproducible proof: synthetic credentials only, no network or model calls.
bin/test-zci-secrets --report .zociety/secret-transfer-proof.json
bin/test-zci-secrets-provision
# Actual host wrapper and launcher, isolated Podman container, no network:
bin/test-zci-secrets-provision --podman

# Pin the launcher, host wrapper, container implementation, and backend.
/usr/bin/git diff --quiet a87846363d6860d5f6a5f4318030464a7f780ad6 \
  -- bin/zociety bin/zci-secrets-provision \
     bin/zci-secrets-provision-container bin/zci-secrets \
  && ./bin/zci-secrets-provision
```

`bin/zci-secrets-provision` is a thin host launcher. It clears inherited
credentials and debug settings, uses a fixed host PATH without repository
shims, and delegates through `bin/zociety exec` to the container's
`/usr/bin/python3 -I`. It neither prompts for nor reads secrets on the host.
The running, reviewed container image and Podman installation are trusted
prerequisites; the git check pins repository code, not those installed tools.

`bin/zci-secrets-provision-container` checks for a container and requires
`/tmp` to be tmpfs before accessing inputs. It creates a private directory
there, ignoring inherited `TMPDIR`, copies the five mounted files into it with
private permissions, and removes the copies on success, failure, and handled
interrupts. It rejects missing, empty, oversized, symlinked or non-maskable
inputs and checks public token prefixes before the first network request.
The signing key remains opaque data; no GPG command or host keyring is used.

The output proof covers these programs' supported execution paths. It does
not deny filesystem access to an agent or another process already authorized
inside the container. Run provisioning without a concurrent agent or loop.

The command writes `.zociety/ci-secrets-provisioned.json`. That receipt reports
only variable presence and security settings. The `--set` operation already
reads those settings back after every create or update; GitLab does not return
hidden values, so neither the command nor the receipt claims to compare them.

The low-level `bin/zci-secrets` backend keeps existing variables unless it is
run directly inside the container with `--force`; the wrapper does not force replacements.
An existing visible variable requires deliberate recreation because GitLab
cannot make it hidden with an update. All source values are validated before
the first write.
The multiline GPG key is stored with a `base64:` prefix so it can be masked
and hidden; `bin/zci-loop` decodes it before importing it. Existing raw armored
key files remain supported.

Normal-mode output contains only the fixed project ID, scope, variable names
and statuses. The same schema is used for receipts. No value hashes, previews,
API response bodies, exception messages or tracebacks are emitted. Credentials
travel from mounted files through Python memory inside the container to the
fixed GitLab HTTPS endpoint; no child process receives them. Redirects and
proxy-environment overrides are disabled. Once the container guard succeeds,
the command removes any old receipt before staging. Check the command's exit
status; a receipt left by an earlier run is not proof that a failed launch ran.

The proof uses freshly generated canaries and checks raw, JSON-escaped,
hexadecimal and base64 representations against stdout, stderr, reports, argv
and URLs. It also injects reflected secrets into API errors, malformed JSON,
exceptions and interrupts. Eight unrelated valid credential sets must produce
identical normal transcripts. Test failures themselves suppress captured data.
GitLab publishes the metadata-only proof artifact from `secret-transfer-proof`.

The provisioning proof captures the host wrapper's output, checks its fixed
arguments and sanitized environment, and exercises the actual container
implementation with a fake API. `--podman` uses the production launcher with
only its container name changed for isolation, mounts only the test fixture,
disables networking, and instruments the container process with synthetic
sources and transport. It checks exact uploaded values, identical transcripts
for unrelated valid inputs, preflight rejection, private staging permissions,
and cleanup after API errors and SIGTERM. CI runs the runtime-double version;
the Podman variant is an explicit local integration check.

Intentional operator QA inside the container can disclose values through the
low-level backend with both `--debug-show-values`
and `--confirm-secret-disclosure`, with stdin and stdout attached to a terminal.
The proof exercises this exception with synthetic credentials. Real credential
provisioning and agent-facing status checks use normal mode. This establishes
the transfer's output boundary; it does not revoke filesystem or API access
already held by an agent running as the same user.

An API-authenticated installation can use `ZOCIETY_ANTHROPIC_API_KEY_FILE`
instead of the OAuth file. Keep the existing blind key; replacing it prevents
other runners from revealing archived model seals.

After provisioning, start the manual `autonomous-preflight` job on protected
`main`. It checks the service account, Git credential helper and installed
client without starting an agent turn. Then create a web pipeline with
`run_autonomous=true`, review its validated inputs and start the manual
`autonomous` job. Defaults are 30 turns, 90 minutes, $5 and one cycle. The job
has a two-hour hard timeout and a `resource_group` serializes CI runs. Stop
local runs before starting CI: that resource group does not lock host loops.

The wrapper resumes a remote successor cycle when one exists, calls native
`bin/zloop`, and publishes committed progress and provenance notes on exit.
A recorded normal time/turn/cost cap is successful CI completion; failures
retain their non-zero status. Only run metadata is retained as a restricted
artifact. A hard kill can still lose uncommitted work, as on the host.

The agent job uses an immutable ARM64 image digest from the project registry.
The optional `build-agent-image` job builds with rootless BuildKit on protected
main and publishes an immutable commit tag. Verify it and update the digest
in a reviewed change; the build does not replace a running job's image.

## Security Properties

| Property | Implementation |
|----------|----------------|
| Read-only filesystem | `--read-only` with tmpfs for /tmp, /run |
| Non-root execution | UID 1000, no privilege escalation |
| Resource limits | 1GB RAM, 2 CPUs |
| Credential isolation | File-based in /run/secrets/ |
| Dedicated identity | Own SSH/GPG keys, not host credentials |
| Network | Bridge mode (required for API + git) |

## Commands

```bash
# Interactive Claude session
bin/zociety

# Run the agent loop
bin/zloop 60

# Shell access for debugging
bin/zociety bash

# Run any command
bin/zociety bin/check-genesis
bin/zociety git log --oneline -10

# Management
bin/zociety --build      # Build image
bin/zociety --rebuild    # Rebuild without cache
bin/zociety --status     # Check image/volume status
bin/zociety --clean      # Remove image and volumes
bin/zociety --help       # Full help
```

## Directory Structure

```
container/
├── Containerfile           # Image definition (Node + Claude Code)
├── docker-entrypoint.sh    # Credential loading, identity setup
├── compose.yml             # Alternative: podman-compose config
├── secrets/
│   ├── .gitkeep
│   ├── anthropic_api_key   # API key (gitignored)
│   ├── zociety_ssh_key     # SSH private key (gitignored)
│   ├── zociety_ssh_key.pub # SSH public key (gitignored)
│   ├── gpg_signing_key.asc # GPG key (gitignored)
│   └── github_token        # GitHub PAT (gitignored)
├── quadlet/
│   └── zociety.container   # Systemd integration
└── README.md
```

## Volumes

| Mount | Source | Purpose |
|-------|--------|---------|
| `/repo` | zociety directory | Working directory (read-write) |
| `/home/agent` | Named volume | Home dir persistence (.gnupg, .claude, etc.) |
| `/home/agent/.claude-plugins` | Host plugins dir | Claude Code plugins (optional) |
| `/run/secrets` | container/secrets/ | All credentials (read-only) |

Note: The container does NOT mount host SSH keys or gitconfig. The agent has its own identity configured in the entrypoint script.

## Plugin Configuration

The container mounts your host's Claude plugins directory. Set the location:

```bash
# Default location
export CLAUDE_PLUGINS_DIR="$HOME/.claude/plugins"

# Or specify when running
CLAUDE_PLUGINS_DIR=/path/to/plugins bin/zociety
```

Plugins are optional. The core loop (`bin/zloop`) is native to zociety.

## Podman Compose (Alternative)

If you prefer compose over the wrapper script:

```bash
cd container

# Start long-running container
podman-compose up -d

# Execute commands
podman exec -it zociety-sandbox claude
podman exec -it zociety-sandbox bin/check-genesis

# Stop
podman-compose down
```

## Systemd Integration (Linux)

For running as a user service:

```bash
# Install quadlet
mkdir -p ~/.config/containers/systemd
cp container/quadlet/zociety.container ~/.config/containers/systemd/

# Edit paths in the file
vim ~/.config/containers/systemd/zociety.container

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now zociety

# Access
podman exec -it zociety-sandbox claude
```

## Troubleshooting

### "API key not configured"

```bash
echo 'sk-ant-...' > container/secrets/anthropic_api_key
chmod 600 container/secrets/anthropic_api_key
```

### "Image not found"

```bash
bin/zociety --build
```

### Plugins not loading

Check plugin mount (if using plugins):
```bash
bin/zociety bash
ls -la /home/agent/.claude-plugins/
```

Note: The core loop (`bin/zloop`) is native and doesn't require plugins.

### Permission denied on repo files

Container runs as UID 1000. Ensure files are accessible:
```bash
# Check current ownership
ls -la

# If needed, fix on host
sudo chown -R 1000:1000 /path/to/zociety
```

### Git push fails (SSH)

Verify SSH key is loaded:
```bash
bin/zociety bash
ls -la /home/agent/.ssh/
cat /home/agent/.ssh/config
ssh -T git@gitlab.com
```

Check that the dedicated GitLab public key is registered to the service account.

### Git push fails (wrong remote)

Check the remote is using SSH URL:
```bash
git remote -v
# Origin should show: git@gitlab.com:zociety/zociety.git
# The github remote should show: git@github.com:zociety-dev/zociety.git

# Fix if needed:
git remote set-url origin git@gitlab.com:zociety/zociety.git
```

### GPG signing fails

The GPG key is imported on first use, but the `.gnupg` directory must exist. If signing fails:

```bash
bin/zociety bash

# Check if key is imported
gpg --list-secret-keys

# If empty, import manually
gpg --batch --import /run/secrets/gpg_signing_key.asc

# Verify
gpg --list-secret-keys agent@zociety.dev
```

The home volume persists `.gnupg`, so this only needs to happen once. If you see "No secret key" errors after a `--clean`, just import again.

To commit without signing (temporary workaround):
```bash
git commit --no-gpg-sign -m "message"
```

### Commits not showing as verified on GitHub

1. GPG key must be imported in container (see above)
2. Public key must be added to GitHub account
3. Email must match: `agent@zociety.dev`

Check git config:
```bash
git config --global user.signingkey
git config --global commit.gpgsign
git config --global user.email
```

### gh CLI not authenticated

**Inside container:**
```bash
bin/zociety bash
echo $GH_TOKEN | head -c 20  # Should show token prefix
gh auth status
```

If `GH_TOKEN` is empty, check that the secret file exists:
```bash
ls -la /run/secrets/github_token
```

**Outside container:**
```bash
# Re-authenticate
gh auth login --with-token < container/secrets/github_token
gh auth status
```

If you see "not logged into any GitHub hosts", the token may be invalid or expired. Generate a new one in GitHub Settings → Developer settings → Personal access tokens.

### Container won't start

Check for port conflicts or existing containers:
```bash
podman ps -a | grep zociety
podman rm -f zociety-sandbox
bin/zociety --status
```

### GPG key not persisting between sessions

The home volume (`zociety-claude-home`) stores `.gnupg`. If you ran `bin/zociety --clean`, the volume was deleted. Re-import:

```bash
bin/zociety bash
gpg --batch --import /run/secrets/gpg_signing_key.asc
```

## Development

To modify the container:

```bash
# Edit Containerfile or entrypoint
vim container/Containerfile
vim container/docker-entrypoint.sh

# Rebuild
bin/zociety --rebuild

# Test
bin/zociety bash
```

## What's NOT in the container

- No sudo/root access
- No package manager access (apt removed after build)
- No access to host filesystem outside mounted volumes
- No access to host network services (only bridge networking)
- No persistent changes to container filesystem
- No access to host SSH keys or git identity (uses dedicated agent identity)
