# gemini-google-maps-tool - Developer Guide

## Quick Reference

### Common Development Commands

```bash
# Setup
make install              # Install dependencies
uv sync                   # Sync dependencies with uv

# Quality Checks
make format               # Format with ruff
make lint                 # Lint with ruff
make typecheck            # Type check with mypy
make test                 # Run tests
make check                # Run all checks

# Build & Deploy
make build                # Build wheel
make install-global       # Install globally
make pipeline             # Full pipeline (format + check + build + install)

# Testing CLI
uv run gemini-google-maps-tool query "test query"
gemini-google-maps-tool query "test query"  # After install-global
```

### Key Files

| File | Purpose |
|------|---------|
| `core/client.py` | Client management, API key handling, DEBUG logging |
| `core/maps.py` | Maps grounding query logic, comprehensive DEBUG logging |
| `commands/query_commands.py` | CLI query command implementation with verbosity |
| `logging_config.py` | Multi-level verbosity logging configuration |
| `utils.py` | Shared utilities (output, logging, stdin) |
| `cli.py` | Main CLI entry point with completion command |
| `__init__.py` | Public API exports |
| `.claude-plugin/` | Claude Code marketplace and plugin files |

### CLI Command Quick Reference

```bash
# Basic usage
gemini-google-maps-tool query "query text"

# All options with verbosity
gemini-google-maps-tool query "query text" \
  --lat-lon "52.37,4.89" \
  --model flash \
  --text \
  -vv  # Progressive verbosity: -v (INFO), -vv (DEBUG), -vvv (TRACE)

# Stdin
echo "query" | gemini-google-maps-tool query --stdin

# Shell completion
gemini-google-maps-tool completion bash  # or zsh/fish
eval "$(gemini-google-maps-tool completion zsh)"

# Help
gemini-google-maps-tool --help
gemini-google-maps-tool query --help
gemini-google-maps-tool completion --help
```

## Overview

`gemini-google-maps-tool` is a production-ready CLI and Python library for querying Gemini with Google Maps grounding. It provides location-aware responses with accurate, up-to-date data from Google Maps' database of over 250 million places worldwide.

**Tech Stack:**
- **Python 3.14+** with modern syntax (`dict`/`list` over `Dict`/`List`)
- **uv** for fast package management
- **mise** for Python version management
- **Click** for CLI framework
- **google-genai** SDK for Gemini API integration
- **ruff** for linting and formatting
- **mypy** for strict type checking
- **pytest** for testing
- **Multi-level verbosity** with progressive logging (`-v`, `-vv`, `-vvv`)
- **Shell completion** for Bash, Zsh, and Fish
- **Claude Code plugin** with marketplace integration
- **Bandit** security linting
- **pip-audit** dependency vulnerability scanning
- **gitleaks** secret detection

## Architecture

This project follows a **modular, separation-of-concerns architecture** designed for both CLI usage and library imports:

```
gemini_google_maps_tool/
├── __init__.py              # Public API exports for library usage
│                            # Exposes: get_client, query_maps, exceptions, data classes
├── cli.py                   # CLI entry point (Click group)
│                            # Main command group with version option
├── core/                    # Core library functions (CLI-independent)
│   ├── __init__.py         # Exports core functions and classes
│   ├── client.py           # Client management (get_client, ClientError)
│   └── maps.py             # Maps grounding operations (query_maps, QueryError)
├── commands/                # CLI command implementations
│   ├── __init__.py
│   └── query_commands.py   # Query command with Click decorators
└── utils.py                 # Shared utilities (output_json, logging, stdin)
```

### Key Design Principles

1. **Separation of Concerns**
   - `core/` modules contain business logic and are independent of CLI
   - `commands/` modules are thin CLI wrappers that call core functions
   - Core functions are importable and reusable in other Python projects

2. **Exception-Based Error Handling**
   - Core functions raise exceptions (NOT `sys.exit`)
   - CLI layer catches exceptions, formats error messages, and exits with appropriate codes
   - This enables library usage without unexpected process termination

3. **Composability**
   - JSON output to stdout for easy parsing and piping
   - Logs and errors to stderr for human feedback
   - Stdin support for chaining with other tools

4. **Type Safety**
   - Strict mypy checking enabled (`strict = true`)
   - Comprehensive type hints on all functions
   - Modern Python syntax: `dict`/`list` over `Dict`/`List`

5. **Agent-Friendly**
   - Rich, informative error messages enable AI agents to self-correct
   - Structured output (JSON) for programmatic consumption
   - Clear command examples in help text for ReAct loops

## Development Commands

### Quick Start

```bash
# Clone and enter project
cd gemini-google-maps-tool

# Install dependencies
make install

# Run all quality checks
make check

# Full pipeline (format, check, build, install globally)
make pipeline
```

### Quality Checks

```bash
make format           # Auto-format with ruff
make lint             # Lint with ruff
make typecheck        # Type check with mypy (strict mode)
make test             # Run pytest suite
make check            # Run all checks: lint + typecheck + test
```

### Security Checks

```bash
make security-bandit      # Python security linting with bandit
make security-pip-audit   # Dependency vulnerability scanning
make security-gitleaks    # Secret detection in git history
make security             # Run all security checks
```

**Tools:**
- **Bandit**: Static security analysis for Python code
- **pip-audit**: Scans dependencies for known vulnerabilities
- **Gitleaks**: Prevents committing secrets and credentials

### Build & Install

```bash
make build            # Build wheel package
make install-global   # Install globally with uv tool (from wheel)
make pipeline         # Full workflow: format + check + build + install-global
```

### Running Locally

```bash
# Run without global install (development)
make run ARGS="query 'Best coffee shops' --verbose"

# Or directly with uv
uv run gemini-google-maps-tool query "Best coffee shops"
```

### Cleanup

```bash
make clean            # Remove build artifacts (dist/, *.egg-info)
```

## Logging Architecture

The tool implements a multi-level verbosity system using Python's standard logging module.

### Verbosity Levels

| Flag | Level | Description | Use Case |
|------|-------|-------------|----------|
| (none) | WARNING | Quiet mode, critical issues only | Production use |
| `-v` | INFO | High-level operations | Normal debugging |
| `-vv` | DEBUG | Detailed operations, API calls | Deep debugging |
| `-vvv` | TRACE | Full HTTP traces, library internals | Issue investigation |

### Implementation

**logging_config.py:**
```python
def setup_logging(verbose_count: int = 0) -> None:
    """Configure logging based on verbosity level."""
    if verbose_count == 0:
        level = logging.WARNING
    elif verbose_count == 1:
        level = logging.INFO
    elif verbose_count >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
        force=True,
    )

    # Enable dependent library logging at TRACE level
    if verbose_count >= 3:
        logging.getLogger("google.genai").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)

def get_logger(name: str) -> logging.Logger:
    """Get logger for module."""
    return logging.getLogger(name)
```

**Usage in commands:**
```python
@click.option("-v", "--verbose", count=True,
              help="Enable verbose output (-v=INFO, -vv=DEBUG, -vvv=TRACE)")
def query(verbose: int, ...):
    setup_logging(verbose)
    logger = get_logger(__name__)
    logger.info("Starting query...")
    logger.debug(f"Using model: {model}")
```

## Code Standards

### Type Hints

All functions must have complete type hints:

```python
def query_maps(
    client: genai.Client,
    query: str,
    lat_lon: tuple[float, float] | None = None,
    model: str = "gemini-2.5-flash-lite",
    include_grounding: bool = False,
) -> MapsQueryResult:
    """Query Gemini with Google Maps grounding."""
    ...
```

### Docstrings

All public functions require docstrings with Args, Returns, and Raises sections:

```python
def parse_lat_lon(lat_lon_str: str) -> tuple[float, float]:
    """Parse latitude,longitude string into tuple of floats.

    Args:
        lat_lon_str: String in format "lat,lon" (e.g., "37.78193,-122.40476").

    Returns:
        Tuple of (latitude, longitude) as floats.

    Raises:
        ValueError: If format is invalid or coordinates are out of range.

    Example:
        >>> lat, lon = parse_lat_lon("37.78193,-122.40476")
        >>> print(f"Latitude: {lat}, Longitude: {lon}")
        Latitude: 37.78193, Longitude: -122.40476
    """
    ...
```

### Formatting

- **Line length**: 100 characters
- **Formatting tool**: ruff (auto-format with `make format`)
- **Imports**: Sorted and organized by ruff
- **Quotes**: Double quotes preferred

### Error Handling

Core functions raise exceptions, CLI handles formatting:

```python
# In core/maps.py (library code)
def query_maps(...) -> MapsQueryResult:
    try:
        ...
    except Exception as e:
        raise QueryError(f"Query failed: {str(e)}") from e

# In commands/query_commands.py (CLI code)
@click.command()
def query(...):
    try:
        result = query_maps(...)
    except QueryError as e:
        log_error(str(e))
        sys.exit(1)
```

## CLI Commands

### Main Command Group

```bash
gemini-google-maps-tool --help      # Show main help
gemini-google-maps-tool --version   # Show version (0.1.0)
```

### Query Command

**Signature:**
```bash
gemini-google-maps-tool query [QUERY_TEXT] [OPTIONS]
```

**Arguments:**
- `QUERY_TEXT` (optional): The query to send to Gemini (required unless `--stdin` is used)

**Options:**
- `--lat-lon LAT,LON`: Location coordinates in format `lat,lon` (e.g., `37.78193,-122.40476`)
- `-v, --verbose`: Enable verbose output (includes full grounding metadata)
- `--model [flash|flash-lite]`: Model to use (default: `flash-lite`)
  - `flash`: gemini-2.5-flash (more powerful, higher cost)
  - `flash-lite`: gemini-2.5-flash-lite (default, faster, lower cost)
- `-s, --stdin`: Read query from stdin instead of argument
- `-t, --text`: Output markdown text instead of JSON (includes sources automatically)

**Examples:**

```bash
# Basic query
gemini-google-maps-tool query "Best coffee shops near me"

# With location context
gemini-google-maps-tool query "Italian restaurants nearby" \\
  --lat-lon "37.78193,-122.40476"

# Verbose output with sources
gemini-google-maps-tool query "Museums in SF" \\
  --lat-lon "37.7749,-122.4194" \\
  --verbose

# Using flash model
gemini-google-maps-tool query "Plan a day in NYC" --model flash

# Reading from stdin
echo "Best sushi restaurants" | gemini-google-maps-tool query --stdin

# Text output (markdown with sources)
gemini-google-maps-tool query "Best museums in Amsterdam" --text
```

**Output Format:**

JSON (default):
```json
{
  "response_text": "...",
  "grounding_metadata": {  // Only with --verbose
    "grounding_chunks": [...],
    "grounding_supports": [...],
    "google_maps_widget_context_token": "..."
  }
}
```

Markdown (with `--text`):
```markdown
Here are some of the best museums in Amsterdam:

The Rijksmuseum features Dutch Golden Age masterpieces...

---

## Sources

1. [Rijksmuseum](https://maps.google.com/?cid=...)
2. [Van Gogh Museum](https://maps.google.com/?cid=...)
```

### Completion Command

**Signature:**
```bash
gemini-google-maps-tool completion [bash|zsh|fish]
```

**Purpose:** Generate shell completion scripts for tab-completion support.

**Arguments:**
- `SHELL` (required): Shell type - `bash`, `zsh`, or `fish`

**Examples:**

```bash
# Bash - temporary (current session)
eval "$(gemini-google-maps-tool completion bash)"

# Bash - persistent
echo 'eval "$(gemini-google-maps-tool completion bash)"' >> ~/.bashrc

# Zsh - temporary
eval "$(gemini-google-maps-tool completion zsh)"

# Zsh - persistent
echo 'eval "$(gemini-google-maps-tool completion zsh)"' >> ~/.zshrc

# Fish - install to completions directory
gemini-google-maps-tool completion fish > ~/.config/fish/completions/gemini-google-maps-tool.fish
```

**Implementation:**
- Uses Click's shell completion API (`BashComplete`, `ZshComplete`, `FishComplete`)
- Generates completion scripts dynamically from Click command definitions
- Supports completion for commands, options, and choice parameters

## Claude Code Plugin

The project includes a Claude Code marketplace plugin for seamless IDE integration.

**Location:** `.claude-plugin/` and `plugins/gemini-google-maps-tool/`

**Features:**
- **Slash Commands**: Quick CLI wrappers (`/gemini-google-maps-tool:query`, `/gemini-google-maps-tool:completion`)
- **Skill**: Comprehensive documentation with progressive disclosure (`/skill-gemini-google-maps-tool`)
- **Auto-Discovery**: Automatically available when repository is opened in Claude Code

**Usage in Claude Code:**
```
# Quick query
/gemini-google-maps-tool:query "Best restaurants in Tokyo"

# Get comprehensive help
/skill-gemini-google-maps-tool

# Or use natural language
Use the gemini-google-maps-tool to help me find places
```

## Library Usage

Import and use as a Python library:

### Basic Usage

```python
from gemini_google_maps_tool import get_client, query_maps

# Initialize client (requires GEMINI_API_KEY env var)
client = get_client()

# Execute query
result = query_maps(
    client=client,
    query="Best coffee shops near me",
)

print(result.response_text)
```

### With Location and Grounding

```python
from gemini_google_maps_tool import get_client, query_maps

client = get_client()

result = query_maps(
    client=client,
    query="Italian restaurants nearby",
    lat_lon=(37.78193, -122.40476),
    model="gemini-2.5-flash",
    include_grounding=True,
)

# Access response
print(result.response_text)

# Access grounding metadata
if result.grounding_metadata:
    for chunk in result.grounding_metadata.grounding_chunks:
        print(f"Source: {chunk.title}")
        print(f"  URI: {chunk.uri}")
        print(f"  Place ID: {chunk.place_id}")
```

### Error Handling

```python
from gemini_google_maps_tool import (
    get_client,
    query_maps,
    ClientError,
    QueryError,
)

try:
    client = get_client()
    result = query_maps(client, "Best restaurants")
    print(result.response_text)
except ClientError as e:
    print(f"Client initialization failed: {e}")
    # Handle missing API key, invalid credentials, etc.
except QueryError as e:
    print(f"Query failed: {e}")
    # Handle API errors, network issues, etc.
```

### Exported API

From `gemini_google_maps_tool` you can import:

**Core Functions:**
- `get_client() -> genai.Client`
- `query_maps(...) -> MapsQueryResult`

**Data Classes:**
- `MapsQueryResult` - Query result with response text and optional metadata
- `GroundingMetadata` - Complete grounding metadata
- `GroundingChunk` - Single Google Maps source
- `GroundingSegment` - Text segment linked to sources
- `GroundingSupport` - Segment with source indices

**Exceptions:**
- `ClientError` - Client initialization failures
- `QueryError` - Query execution failures

**Utilities:**
- `parse_lat_lon(lat_lon_str: str) -> tuple[float, float]`

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run with verbose output
uv run pytest tests/ -v

# Run specific test file
uv run pytest tests/test_utils.py

# Run with coverage
uv run pytest tests/ --cov=gemini_google_maps_tool
```

### Test Structure

```
tests/
├── __init__.py
└── test_utils.py           # Tests for utility functions
```

### Writing Tests

Tests use pytest with type hints:

```python
def test_output_json_dict(capsys: object) -> None:
    """Test that output_json correctly formats a dictionary."""
    data = {"status": "success", "count": 42}
    output_json(data)
    captured = capsys.readouterr()  # type: ignore
    parsed = json.loads(captured.out)
    assert parsed == data
```

## Important Notes

### Dependencies

**Core Dependencies:**
- **[google-genai](https://github.com/googleapis/python-genai)** (>=1.0.0): Official Python SDK for Gemini API
- **[Click](https://click.palletsprojects.com/)** (>=8.1.7): CLI framework

**Development Dependencies:**
- **[ruff](https://github.com/astral-sh/ruff)** (>=0.8.0): Fast Python linter and formatter
- **[mypy](https://github.com/python/mypy)** (>=1.7.0): Static type checker
- **[pytest](https://pytest.org/)** (>=7.4.0): Testing framework
- **[types-requests](https://pypi.org/project/types-requests/)**: Type stubs for requests

### Authentication

Requires `GEMINI_API_KEY` environment variable. The tool checks for this on client initialization and provides clear error messages if missing:

```
Error: GEMINI_API_KEY environment variable is required.
Set it with: export GEMINI_API_KEY='your-api-key'
```

Get your API key: [Google AI Studio](https://aistudio.google.com/app/apikey)

### Client Implementation

The client is lazily initialized and cached:

```python
_client: genai.Client | None = None

def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ClientError("GEMINI_API_KEY environment variable is required. ...")
        _client = genai.Client(api_key=api_key)
    return _client
```

This ensures:
- Single client instance per process
- Clear error messages if API key is missing
- No unnecessary re-initialization

### Model Selection

Two models are supported:

1. **gemini-2.5-flash** (`--model flash`)
   - More powerful and capable
   - Higher cost
   - Best for complex queries and itinerary planning

2. **gemini-2.5-flash-lite** (`--model flash-lite`, default)
   - Faster and more cost-effective
   - Good for simple location queries
   - Default choice for most use cases

### Location Format

Location coordinates must be in `lat,lon` format:
- Latitude: -90 to 90
- Longitude: -180 to 180
- Example: `37.78193,-122.40476`

The `parse_lat_lon` utility validates ranges and provides clear error messages.

### Version Sync

The version is defined in **three places** and must stay synchronized:

1. `pyproject.toml` - `[project]` section: `version = "0.1.0"`
2. `cli.py` - `@click.version_option(version="0.1.0")`
3. `__init__.py` - `__version__ = "0.1.0"`

When bumping versions, update all three locations.

### Grounding Metadata Extraction

Grounding metadata extraction uses `getattr` with defaults to handle optional fields:

```python
def extract_grounding_metadata(response) -> GroundingMetadata | None:
    chunks = getattr(grounding_metadata, "grounding_chunks", [])
    for chunk in chunks:
        if hasattr(chunk, "maps") and chunk.maps:
            source = GroundingChunk(
                title=getattr(chunk.maps, "title", None),
                uri=getattr(chunk.maps, "uri", None),
                place_id=getattr(chunk.maps, "place_id", None),
            )
```

This handles the dynamic nature of the Gemini API response structure gracefully.

## Troubleshooting

### Common Issues

#### API Key Not Found

**Error:**
```
Error: GEMINI_API_KEY environment variable is required.
```

**Solution:**
```bash
# Set API key
export GEMINI_API_KEY="your-api-key"

# Or retrieve from macOS Keychain
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

#### Import Errors After Changes

**Error:**
```
ImportError: cannot import name 'function_name'
```

**Solution:**
```bash
# Reinstall the package
make clean
make build
make install-global
```

#### Type Errors with dict/list

**Error:**
```
error: Missing type parameters for generic type "dict"
```

**Solution:**
Use `dict[str, object]` instead of `dict` and `list[object]` instead of `list`:
```python
# Wrong
def foo(data: dict) -> None:
    pass

# Correct
def foo(data: dict[str, object]) -> None:
    pass
```

#### Makefile Install Caching Issues

**Problem:** Changes not reflected after `make install-global`

**Solution:**
The Makefile installs from the wheel file to avoid caching:
```bash
make clean
make build
make install-global  # Installs from dist/*.whl with --force
```

#### Tests Failing After Refactoring

**Problem:** Import errors in tests after moving functions

**Solution:**
Update test imports to match new module structure:
```python
# Old
from gemini_google_maps_tool.utils import get_greeting

# New
from gemini_google_maps_tool.utils import output_json
```

### Debug Mode

Enable verbose logging to see what's happening:

```bash
# Verbose CLI output
gemini-google-maps-tool query "test" --verbose

# Python logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. Check `--help` output first
2. Review error messages - they include solutions
3. Verify API key is set correctly
4. Check [Gemini API Status](https://status.cloud.google.com/)
5. Review [official documentation](https://ai.google.dev/gemini-api/docs)

## Resources

### Official Documentation

- [Gemini API - Google Maps Grounding](https://ai.google.dev/gemini-api/docs/maps-grounding)
- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Pricing](https://ai.google.dev/pricing)

### Related Projects

- [google-genai Python SDK](https://github.com/googleapis/python-genai)
- [Click Documentation](https://click.palletsprojects.com/)
- [uv Documentation](https://github.com/astral-sh/uv)

---

**Note:** This project was generated with assistance from [Claude Code](https://www.anthropic.com/claude/code) and follows best practices for CLI-first, agent-friendly design.
