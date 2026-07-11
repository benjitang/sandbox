# Getting Started with uv

[`uv`](https://github.com/astral-sh/uv) is a fast Python package and project manager, written in Rust. It replaces `pip`, `venv`, `virtualenv`, and `pip-tools` with a single tool.

## 1. Install uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Via pip (any platform):**
```bash
pip install uv
```

Verify it installed:
```bash
uv --version
```

## 2. Start a new project

```bash
uv init my-project
cd my-project
```

This creates:
```
my-project/
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── main.py
```

`pyproject.toml` is where your dependencies and project metadata live.

## 3. Add dependencies

```bash
uv add requests
uv add "fastapi[standard]"
```

This updates `pyproject.toml`, creates/updates `uv.lock`, and installs into a project-local virtual environment (`.venv`) automatically — no need to manually create or activate one.

Remove a dependency:
```bash
uv remove requests
```

## 3.5 Where does the virtual environment live?

When you run `uv add`, `uv sync`, or `uv run` inside a project, uv automatically creates a virtual environment **inside the project root**, at:

```
my-project/.venv
```

So after `uv add requests`, your project looks like:

```
my-project/
├── .venv/              ← the virtual environment (auto-created)
├── .python-version
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
└── main.py
```

A few key points:

- `.venv` is created relative to the **nearest `pyproject.toml`** — so always run `uv` commands from inside your project folder (or a subfolder of it).
- It's already listed in `.gitignore` by default — don't commit it.
- You normally don't need to activate it manually (`uv run` handles that for you), but you can if you want:
  ```bash
  source .venv/bin/activate      # macOS/Linux
  .venv\Scripts\activate         # Windows
  ```
- To point your editor (VS Code, PyCharm, etc.) at the right interpreter, select:
  ```
  my-project/.venv/bin/python      # macOS/Linux
  my-project/.venv/Scripts/python.exe  # Windows
  ```
- If you delete `.venv`, it's safe — just run `uv sync` again and it will be rebuilt from `uv.lock`.

## 4. Run a file

Use `uv run` to execute a script inside the project's virtual environment (it will create/sync `.venv` automatically if needed):

```bash
uv run main.py
```

Run a script with arguments:
```bash
uv run main.py --arg1 value
```

Run an arbitrary command in the environment (e.g. pytest):
```bash
uv run pytest
```

## 5. Working with an existing project

If you clone a repo that already has a `pyproject.toml` / `uv.lock`:

```bash
uv sync
```

This installs the exact locked dependency versions into `.venv`.

## 6. Standalone scripts (no project)

For a single-file script, you don't need a full project. Add inline dependency metadata:

```bash
uv add --script my_script.py requests
```

Then just run it — uv will handle the dependencies automatically:
```bash
uv run my_script.py
```

## 7. Managing Python versions

Install a specific Python version:
```bash
uv python install 3.12
```

Pin a project to a version:
```bash
uv python pin 3.12
```

## 8. Formatting & linting with black and ruff

Add them as dev dependencies (keeps them out of your production dependency list):

```bash
uv add --dev black ruff
```

**Format code with black:**
```bash
uv run black .
```

Check formatting without changing files:
```bash
uv run black --check .
```

**Lint (and auto-fix) with ruff:**
```bash
uv run ruff check .
uv run ruff check --fix .
```

Ruff can also format code (as a faster alternative/complement to black):
```bash
uv run ruff format .
```

### Optional: configure them in `pyproject.toml`

```toml
[tool.black]
line-length = 88
target-version = ["py312"]

[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I"]  # pyflakes, pycodestyle, isort rules
```

Once configured, `uv run black .` and `uv run ruff check .` will pick up these settings automatically.

## Quick Reference

| Command | Purpose |
|---|---|
| `uv init` | Create a new project |
| `uv add <pkg>` | Add a dependency |
| `uv remove <pkg>` | Remove a dependency |
| `uv run <file>` | Run a script in the project env |
| `uv sync` | Install locked dependencies |
| `uv python install <ver>` | Install a Python version |
| `uv venv` | Manually create a virtual environment |
| `uv pip install <pkg>` | pip-compatible install (low-level) |
| `uv add --dev black ruff` | Add formatter/linter as dev deps |
| `uv run black .` | Format code with black |
| `uv run ruff check .` | Lint code with ruff |
| `uv run ruff format .` | Format code with ruff |