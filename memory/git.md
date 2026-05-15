# memory/git.md — Git Workflow

- Always use `git@github-vader:` remotes, never `git@github.com:` or HTTPS, so Vader's dedicated SSH key is used.
- Every cloned repo must set local git identity immediately: `Vader <vader@miguel.ms>`; never rely on Vader's global git config.
- ACP subprocesss commit only, never push; I handle pushes.
