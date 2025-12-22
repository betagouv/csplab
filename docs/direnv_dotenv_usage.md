# Intro

*  `direnv` hooks into your shell and automatically loads and unloads environment variables from a `.envrc` file as you enter and leave project directories, keeping your global shell configuration clean while enforcing per-directory configuration boundaries.
* `python-dotenv` is a Python library that focuses on the application layer, loading variables from `.env` files into `os.environ` at runtime so your Python code can rely on a consistent, versionable configuration source.
* Combinated, they provide a seamless way to handle environment-specific configurations—whether for local development, testing, or deployment. By integrating these tools, you can avoid hardcoding sensitive data, reduce setup errors, and streamline collaboration across teams.

# Installation

## direnv

Install `direnv` using Homebrew (recommended for macOS), or your favorite package manager on Linux.

```sh
brew install direnv
```

Then, add the following to your shell configuration file (e.g., `~/.zshrc` or `~/.bashrc`):

```sh
eval "$(direnv hook zsh)"  # For Zsh
# OR
eval "$(direnv hook bash)"  # For Bash
```

Reload your shell:
```sh
source ~/.zshrc  # or ~/.bashrc
```

## python-dotenv

Install the `python-dotenv` package using `pip`:

```sh
pip install python-dotenv
```

`dotenv` uses `.env`-style file to setup environment variables:

```text
SECRET_KEY=supersecret
DEBUG=True
```

`load_dotenv` will search upwaid from the current working directory until it finds a `.env` file and load its key-value pairs.

```python
from dotenv import load_dotenv
import os

load_dotenv()  # by default, looks for .env in current or parent dirs[web:5]

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
```

# Usage

Common pattern, `.env` as the single source of truth:
1. Put your key-value pairs in `.env`,
2. In .envrc, add `dotenv` so direnv loads the same file into the shell,
3. In Python, `call load_dotenv()` so the same values are loaded if the script is started outside a direnv-enabled shell.

## Create a `.envrc` File

In the application directory, create a `.envrc` file to load the `.env` variables and activates your virtual environment.
When `.env` file is the same directory, you can simply call `dotenv`:

```text
dotenv
source .venv/bin/activate
```

When `.env` is located somewhere else, reference it explicitly:

```text
dotenv ../../env.d/tycho
source .venv/bin/activate
```

##  Allow `.envrc`

Run the following to allow `direnv` to load the `.envrc` file:

```sh
cd /PATH/TO/THE/PYTHON/APP/
direnv allow
```

After this, the environment variables defined via `dotenv` in `.envrc` will loaded into your shell session whenever you `cd` into that directory.
