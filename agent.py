# SWE Agent - Software Engineering Agent


import os
import json
import subprocess
from pathlib import Path
from typing import Optional

ORG = "emberlamp"
CONFIG_URL = f"https://raw.githubusercontent.com/{ORG}/config/main/repos.json"
SKILLS_URL = f"https://raw.githubusercontent.com/{ORG}/skills/main"

TMP_BASE = "/tmp"


class SWEAgent:
    """Base class for software engineering agents."""

    def __init__(self, name: str, capabilities: list | None = None):
        self.name = name
        self.capabilities = capabilities or []
        self.repos = []
        self.skills = {}
        self._load_repos()
        self._load_skills()

    def _load_repos(self):
        """Load repos from config repo."""
        try:
            result = subprocess.run(
                ["curl", "-s", CONFIG_URL], capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                self.repos = data.get("repos", [])
        except Exception:
            self.repos = [
                "general",
                "react-template",
                "swe-agent",
                "gh-pin-repo",
                "config",
                "cli",
                "bot",
                "license",
                "warnings",
                "json-repo",
                "gitkeep",
                ".github",
                "skills",
            ]

    def _load_skills(self):
        """Load skills from skills repo."""
        skill_types = ["developer_tools", "personas"]
        for skill_type in skill_types:
            self.skills[skill_type] = []
            for repo in self.repos:
                if repo == "skills":
                    skill_path = (
                        Path(TMP_BASE)
                        / "emberlamp"
                        / "skills"
                        / "agent"
                        / f"{skill_type}.md"
                    )
                    if skill_path.exists():
                        self.skills[skill_type].append(skill_path.read_text())

    def get_repo_path(self, repo: str) -> Optional[Path]:
        """Get local path for a cloned repo in /tmp."""
        if repo == ".github":
            repo_path = Path(TMP_BASE) / "emberlamp" / ".github"
        else:
            repo_path = Path(TMP_BASE) / "emberlamp" / repo
        return repo_path if repo_path.exists() else None

    def is_repo_cloned(self, repo: str) -> bool:
        """Check if repo is cloned in /tmp."""
        return self.get_repo_path(repo) is not None

    def list_cloned_repos(self) -> list:
        """List all cloned emberlamp repos in /tmp."""
        return [repo for repo in self.repos if self.is_repo_cloned(repo)]

    def clone_repo(self, repo: str, force: bool = False) -> bool:
        """Clone a repo to /tmp/emberlamp/<repo>. Returns True if successful."""
        if self.is_repo_cloned(repo) and not force:
            return True
        target = self.get_repo_path(repo)
        if target is None:
            target = Path(TMP_BASE) / "emberlamp" / repo
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            if repo == ".github":
                url = f"https://github.com/{ORG}/.github.git"
            else:
                url = f"https://github.com/{ORG}/{repo}.git"
            subprocess.run(
                ["git", "clone", url, str(target)], capture_output=True, timeout=60
            )
            return target.exists()
        except Exception:
            return False

    def clone_all(self, force: bool = False) -> list:
        """Clone all repos to /tmp/emberlamp/. Returns list of cloned repos."""
        cloned = []
        for repo in self.repos:
            if self.clone_repo(repo, force):
                cloned.append(repo)
        return cloned

    def execute_task(self, task: str) -> dict:
        """Execute a software engineering task."""
        return {"status": "pending", "task": task, "result": None}

    def can_handle(self, task: str) -> bool:
        """Check if agent can handle this task."""
        return True

    def get_capabilities(self) -> dict:
        """Get agent capabilities including skills."""
        return {
            "name": self.name,
            "repos": self.repos,
            "cloned_repos": self.list_cloned_repos(),
            "skills": self.skills,
            "tmp_base": TMP_BASE,
        }


if __name__ == "__main__":
    agent = SWEAgent("emberlamp-agent")
    info = agent.get_capabilities()
    print(f"Agent: {info['name']}")
    print(f"Total repos: {len(info['repos'])}")
    print(f"Cloned repos: {info['cloned_repos']}")
    print(f"Skills loaded: {list(info['skills'].keys())}")
