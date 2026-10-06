# Kernelo

A sleek terminal chat UI in the style of Claude Code, supporting local models (via Ollama) and OpenAI-compatible API servers.

## Features

- **Rich Terminal UI**: Streaming markdown rendering, live spinners, banner display, and status indicators.
- **Backends Supported**:
  - **Ollama** (default, connects to `http://localhost:11434` with model `qwen2.5:3b`)
  - **OpenAI-Compatible** (vLLM, llama.cpp, LM Studio, OpenAI, etc.)
  - **Echo** (offline testing backend)
- **Interactive Slash Commands**: `/help`, `/clear`, `/exit`.
- **Keyboard Shortcuts**:
  - `Enter`: Send message / accept autocomplete
  - `Alt+Enter` (or `Esc+Enter`): Insert newline
  - `Ctrl+C`: Cancel generation without exiting the app
  - `Ctrl+D`: Exit application

## Installation

```bash
# Clone the repository
git clone https://github.com/ahad2453l/Kernelo.git
cd Kernelo

# Activate your virtual environment
source .venv/bin/activate

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

## Usage

Make sure your virtual environment is activated:
```bash
source .venv/bin/activate
```

Run Kernelo directly:
```bash
kernelo
```
or via Python module:
```bash
python -m kernelo
```

### Configuration

You can configure Kernelo using environment variables or CLI options:

| Environment Variable | Description | Default |
|---|---|---|
| `CHAT_MODEL` | Model to use | `qwen2.5:3b` |
| `OLLAMA_HOST` | Ollama host address | `http://localhost:11434` |
| `CHAT_BASE_URL` | OpenAI-compatible server URL (e.g. `http://localhost:8000/v1`) | `None` |
| `CHAT_API_KEY` | API key for OpenAI-compatible server | `not-needed` |
| `CHAT_BACKEND` | Set to `echo` to test without running a model | `""` |

#### Testing UI without Ollama:
```bash
CHAT_BACKEND=echo kernelo
```

## Running Tests

```bash
pytest
```

```
dont forgot to intall ollama
```
