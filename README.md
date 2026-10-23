# CrewAI Agents

A collection of small CrewAI examples for learning how to build agents, tasks, crews, tools, structured outputs, YAML-configured crews, and event-driven flows.

The repository currently uses Python 3.12+, `uv`, CrewAI, CrewAI Tools, and OpenAI. The default application entry point runs a movie recommendation flow powered by `gpt-4o-mini`.

## Features

- Basic single-agent CrewAI workflow for technical writing.
- Structured Pydantic output for extracting entity-relation-entity triplets.
- File summarization with `FileReadTool`.
- Multi-agent research, summarization, and fact-checking with `SerperDevTool`.
- YAML-driven agent and task configuration.
- A reusable `ResearchCrew` built with CrewAI project decorators.
- A custom currency-conversion tool backed by ExchangeRate-API.
- An event-driven movie recommendation flow using CrewAI Flow and the OpenAI API.

## Requirements

- Python `>=3.12`
- [`uv`](https://docs.astral.sh/uv/)
- An OpenAI API key for the movie recommendation flow and examples that use the default OpenAI-backed model.
- A Serper API key for internet research examples.
- An ExchangeRate-API key for the custom currency tool.
- A local Ollama installation with `llama3.2:1b` available for the examples configured with Ollama.

## Setup

Clone the repository and install the locked dependencies:

```bash
uv sync
```

Create a local `.env` file in the repository root. Do not commit this file:

```dotenv
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
```

The repository already ignores `.env` through `.gitignore`. If credentials have been exposed or committed elsewhere, revoke and replace them.

> **Shell note:** `main.py` imports the flow before calling `load_dotenv()`, while the flow creates its OpenAI client at import time. To ensure the key is available before the import, load the variables into the shell before running the default entry point:
>
> ```bash
> set -a
> source .env
> set +a
> ```

## Run the default flow

After setup, run the movie recommendation flow:

```bash
uv run python main.py
```

The flow:

1. Asks `gpt-4o-mini` for a random movie genre.
2. Requests a movie recommendation for that genre.
3. Stores the genre and recommendation in `flow.state`.
4. Prints the final recommendation and flow state.

## Repository layout

```text
.
├── main.py                         # Default executable entry point
├── flows/
│   └── agentic_flow.py             # MovieRecommendationFlow
├── basic_agent_code/
│   ├── introduction.py             # Basic technical-writer crew
│   ├── structured_output.py        # Pydantic structured-output example
│   ├── with_tools.py               # FileReadTool and SerperDevTool examples
│   ├── with_yaml.py                # Crew configured from YAML
│   └── config.yaml                 # Agent and task definitions
├── modular_crews/
│   ├── research_crew.py             # Decorator-based ResearchCrew
│   ├── custom_tools.py              # CurrencyConverterTool
│   └── config/                      # Research crew agent/task YAML files
├── pyproject.toml                   # Project metadata and dependencies
└── uv.lock                          # Locked dependency versions
```

## Examples

The examples expose Python functions rather than separate command-line entry points. They can be invoked from the repository root with `uv run python -c`.

### Basic technical-writing crew

Uses a local Ollama model and writes the result to `output.md`:

```bash
uv run python -c "from basic_agent_code.introduction import basic_crew; basic_crew()"
```

### Structured output

Extracts a structured entity-relation-entity result from the sample sentence:

```bash
uv run python -c "from basic_agent_code.structured_output import structured_output; print(structured_output())"
```

### File summarization

The file-reading example expects an `output.md` file and writes `summary_with_file.md`:

```bash
uv run python -c "from basic_agent_code.with_tools import with_file_read_tool; with_file_read_tool()"
```

### Multi-agent research with Serper

Runs sequential research, summarization, and fact-checking, then writes `with_serper.md`:

```bash
uv run python -c "from basic_agent_code.with_tools import multi_agent_with_serper_tool; multi_agent_with_serper_tool()"
```

### YAML-configured research crew

The function loads `basic_agent_code/config.yaml` by relative path, so run it from that directory:

```bash
cd basic_agent_code
uv run python -c "from with_yaml import multiagent_with_yaml; multiagent_with_yaml()"
cd ..
```

### Modular research crew

`ResearchCrew` reads its agent and task definitions from `modular_crews/config/`:

```python
from modular_crews.research_crew import ResearchCrew

crew = ResearchCrew().crew()
result = crew.kickoff(inputs={"topic": "The impact of AI on job markets"})
print(result)
```

### Custom currency tool

The custom tool calls ExchangeRate-API and uses the sample conversion of USD 100 to EUR:

```bash
uv run python -c "from modular_crews.custom_tools import custom_tool; print(custom_tool())"
```

## Configuration and API keys

| Variable | Used by | Required for |
| --- | --- | --- |
| `OPENAI_API_KEY` | OpenAI client in `flows/agentic_flow.py` | `main.py` and OpenAI-backed examples |
| `SERPER_API_KEY` | `SerperDevTool` | Internet research examples and `ResearchCrew` |
| `EXCHANGE_RATE_API_KEY` | `CurrencyConverterTool` | Currency conversion example |

The basic examples in `basic_agent_code/introduction.py` and `basic_agent_code/with_tools.py` configure Ollama at `http://localhost:11434` with model `ollama/llama3.2:1b`. Start Ollama and make sure that model is available before running them.

## Development checks

Compile all tracked Python source files without executing API calls:

```bash
uv run python -m compileall -q main.py flows basic_agent_code modular_crews
```

Most examples make live LLM or external API requests, so there is currently no repository test suite and a full execution requires valid credentials and, where applicable, local Ollama.

## Notes

- Generated files such as `output.md`, `summary_with_file.md`, and `with_serper.md` are created in the current working directory by the examples.
- `basic_agent_code/with_yaml.py` opens `config.yaml` relative to the current working directory; run it from `basic_agent_code/` as shown above.
- `uv.lock` is committed to keep dependency resolution reproducible.
