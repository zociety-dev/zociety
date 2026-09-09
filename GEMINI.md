# Gemini Standard Operating Procedures: Zociety Workspace

This document defines the development workflows, standards, and conventions agreed upon for the Zociety repository. All interactive and autonomous assistants must strictly adhere to these practices.

---

## 👥 Small Team Git Workflow

To maintain a clean, stable, and traceable commit history, we use a standard **Branch ➔ PR ➔ Merge ➔ Sync** workflow:

### 1. Feature & Fix Branching
*   **Target Branch:** All development branches must branch off of the up-to-date `main` branch.
*   **Naming Convention:** Use descriptive kebab-case names, optionally prefixed with the category of change:
    *   `fix/zloop-interrupt`
    *   `feature/new-stop-mode`
    *   `docs/api-guide`

### 2. Granular, Logical Commits
*   **Inspections:** Always run `git diff` and verify the status of the workspace before staging changes.
*   **Granularity:** Group changes into small, logical, self-contained units. Avoid committing unrelated edits.
*   **Commit Message Style:**
    *   Use the imperative mood (e.g., "Add flag", "Fix bug") and a concise subject line.
    *   For git-native events, strictly follow the structured commit prefixes listed in `CLAUDE.md` (e.g., `[join]`, `[vote]`, `[stuff]`).

### 3. Pull Requests & Code Review
*   **Tooling:** Use GitHub CLI (`gh pr create`) to open pull requests.
*   **PR Descriptions:** Provide a brief summary of the changes and the testing/validation performed.
*   **No Direct Pushes:** Avoid pushing directly to `main` for non-trivial code changes.

### 4. Merging & Synchronization
*   Once a PR is validated and approved, merge it.
*   Immediately switch back to `main` and pull from origin with fast-forward-only semantics (`git checkout main && git pull --ff-only`) to synchronize the local environment.

---

## 🧪 Quality Control & Testing

Before proposing any changes, verify correctness using:
*   `shellcheck <script>` for shell script validation.
*   `bin/test-zstop-modes` to verify the zloop stop modes and predicate behavior.
*   `bin/test-zevent-system` to test the git-native event sourcing system.
