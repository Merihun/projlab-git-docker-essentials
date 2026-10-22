# Git and Docker for Data Engineers: what this starter gives you

Fernhill's daily revenue report works on one laptop. In this project you put it under version control, work
with a team's history and branches, and package it so it runs the same everywhere: in a container, next to
the lab's database, and in CI.

| Provided | What it is |
|----------|------------|
| `report/` | The report: `python -m report IN.csv OUT.csv [--postgres]` writes revenue per country. Small on purpose; you don't change it. |
| `report/requirements.txt` | The report's own packages (psycopg, pytest), for its image. |
| `tests/test_report.py` | The report's tests. They run on your machine, in the container and in CI. |
| `data/sample_orders.csv` | 240 orders to run it on. |
| `practice/team.bundle` | A colleague team's Git repository in one file: a history to read and two branches that conflict. |
| `practice/broken/compose.yaml` | A Compose file that doesn't work, for you to fix. |
| `answers/history.txt` | Your answers about the team's history. |

## Where you run things

- **Git and Docker run on your own computer**, in a terminal in this folder (or the terminal of a Codespace or VS Code dev container, which has its own Docker inside):
  `git ...`, `docker build`, `docker run`, `docker compose ...`, `make ...`. Check that they're installed:
  `docker --version`, `docker compose version` and `git --version` each print a version.
- **On Windows, use a WSL terminal** for the Docker commands. Git Bash rewrites paths like `$PWD/data` and the
  mounts then point nowhere.
- **Python runs in the lab's workspace** if you don't have Python 3.12 yourself:
  `docker compose exec workspace python -m report data/sample_orders.csv out/summary.csv`.

## The practice repository

    git clone practice/team.bundle practice/team
    cd practice/team && git log --oneline --graph --all

A bundle is a whole repository in one file: cloning it gives you the full history and the branches `main`
and `feature/currency` (as `origin/...`). It is a separate repository from your project, and `practice/team/`
must not be committed into yours.

## On Linux

Containers run as their own user. A folder Docker creates for a bind mount belongs to root, and a container
running as another user can't write into folders it doesn't own. The commands in the steps handle both:
`mkdir -p out` before a run, and `--user "$(id -u):$(id -g)"` for `docker run`. Docker Desktop on macOS and
Windows maps users for you.
