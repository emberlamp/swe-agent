# SWE Agent - Emberlamp

Software engineering agent for emberlamp organization with emberlamp repos awareness.

## Overview

This agent knows all emberlamp repositories and can clone them to /tmp/emberlamp/ for operations.

## Features

- Loads repos dynamically from emberlamp/config
- Detects cloned repos in /tmp/emberlamp/
- Loads skills from emberlamp/skills
- CLI for repo management

## Workflows

All 14 emberlamp repos have three workflows:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI** | push/PR to main | Lint & test |
| **Release** | push to main (auto) or manual | Auto version bump & release |
| **Automation** | daily schedule + manual | Sync, backup, report |

### Automated Release

Release is fully automated - no manual tagging needed!

**How it works:**
1. On push to `main`, checks commits since last tag
2. If `feat:` commits → bump **minor** version (e.g., v1.0 → v1.1.0)
3. If `fix:` commits → bump **patch** version (e.g., v1.1.0 → v1.1.1)
4. Creates tag automatically
5. Generates release notes with features, bug fixes, docs
6. Creates GitHub release

**Conventional commits:**
```
feat: add new feature     # → minor release
fix: bug fix              # → patch release
docs: update readme       # → no release
```

**Manual trigger:**
```bash
gh workflow run release.yml -f version=minor -R emberlamp/repo
```

**Release workflow file:**
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version bump (major, minor, patch)'
        default: 'patch'
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
```

Workflows added to all repos:

```bash
$ for dir in /tmp/emberlamp/*/; do
    repo=$(basename "$dir")
    mkdir -p "$dir/.github/workflows"
    cp workflows/*.yml "$dir/.github/workflows/"
    git -C "$dir" add -A && git -C "$dir" commit -m "feat: include workflows"
    git -C "$dir" push
  done
Added workflows to bot
Added workflows to cli
Added workflows to config
Added workflows to general
Added workflows to gh-pin-repo
Added workflows to json-repo
Added workflows to license
Added workflows to react-template
Added workflows to skills
Added workflows to swe-agent
Added workflows to warnings
To https://github.com/emberlamp/general.git
To https://github.com/emberlamp/skills.git
To https://github.com/emberlamp/gh-pin-repo.git
To https://github.com/emberlamp/bot.git
To https://github.com/emberlamp/react-template.git
To https://github.com/emberlamp/warnings.git
To https://github.com/emberlamp/cli.git
To https://github.com/emberlamp/json-repo.git
To https://github.com/emberlamp/config.git
To https://github.com/emberlamp/license.git
To https://github.com/emberlamp/gitkeep.git
```

## Usage

```bash
python agent.py list          # List all emberlamp repos
python agent.py cloned        # List cloned repos in /tmp
python agent.py clone <repo>  # Clone a specific repo
python agent.py clone-all     # Clone all 14 repos
python agent.py capabilities  # Show agent capabilities
```

## Examples

```bash
# Basic run - shows agent info
python agent.py

# List all 14 emberlamp repos
python agent.py list

# Clone a specific repo
python agent.py clone bot

# Clone all repos to /tmp/emberlamp/
python agent.py clone-all

# Show full capabilities with skills
python agent.py capabilities
```

## Structure

```
swe-agent/
├── agent.py        # Main agent with repo awareness
├── README.md       # This file
└── .pre-commit-config.yaml
```

## Repos

The agent manages these emberlamp repos:
- general, react-template, swe-agent, gh-pin-repo, config, cli, bot, license, warnings, json-repo, gitkeep, .github, skills

## Skills

Skills are loaded from emberlamp/skills repo:
- Developer tools, personas

## Experiment

Testing the agent in action:

```bash
# Show capabilities (all 14 repos cloned, skills loaded)
$ python3 /tmp/swe-agent/agent.py capabilities
Agent: emberlamp-agent
Total repos: 14
Cloned repos: ['general', 'react-template', 'swe-agent', 'gh-pin-repo', 'config', 'cli', 'bot', 'license', 'warnings', 'json-repo', 'gitkeep', '.github', 'skills']
Skills loaded: ['developer_tools', 'personas']

# Clone all repos
$ python3 /tmp/swe-agent/agent.py clone-all
Cloning all repos...
Cloned: ['general', 'react-template', 'swe-agent', 'gh-pin-repo', 'config', 'cli', 'bot', 'license', 'warnings', 'json-repo', 'gitkeep', '.github', 'skills']

# Clone single repo
$ python3 /tmp/swe-agent/agent.py clone bot
Cloning bot...
Success: True

# List all repos
$ python3 /tmp/swe-agent/agent.py list
Emberlamp Repositories:
  - general
  - react-template
  - swe-agent
  - gh-pin-repo
  - config
  - cli
  - bot
  - license
  - warnings
  - json-repo
  - gitkeep
  - .github
  - skills

# Python API usage
$ python3 -c "
from agent import SWEAgent
agent = SWEAgent('test')
result = agent.clone_repo('config')
print(f'Clone config: {result}')
print(f'Cloned repos: {agent.list_cloned_repos()}')
"
Clone config: True
Cloned repos: ['config', 'skills']

# Basic run
$ python3 /tmp/swe-agent/agent.py
Agent: emberlamp-agent
Total repos: 14
Cloned repos: ['skills']
Skills loaded: ['developer_tools', 'personas']
```