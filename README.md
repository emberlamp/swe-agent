# SWE Agent - Emberlamp

Software engineering agent for emberlamp organization with emberlamp repos awareness.

## Overview

This agent knows all emberlamp repositories and can clone them to /tmp/emberlamp/ for operations.

## Features

- Loads repos dynamically from emberlamp/config
- Detects cloned repos in /tmp/emberlamp/
- Loads skills from emberlamp/skills
- CLI for repo management

## Usage

```bash
python agent.py list          # List all emberlamp repos
python agent.py cloned        # List cloned repos in /tmp
python agent.py clone <repo>  # Clone a specific repo
python agent.py clone-all     # Clone all 13 repos
python agent.py capabilities  # Show agent capabilities
```

## Examples

```bash
# Basic run - shows agent info
python agent.py

# List all 13 emberlamp repos
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