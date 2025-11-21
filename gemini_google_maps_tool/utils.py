"""Utility functions for CLI operations.

Provides shared utilities for output formatting, validation, and logging.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys

import click


def output_json(data: dict[str, object] | list[object]) -> None:
    """Output JSON to stdout.

    Args:
        data: Dictionary or list to serialize as JSON.

    Example:
        >>> output_json({"status": "success", "count": 42})
    """
    click.echo(json.dumps(data, indent=2))


def log_verbose(message: str, verbose: bool | int = True) -> None:
    """Print verbose message to stderr.

    Deprecated: Use logging module with setup_logging() instead.
    This function is kept for backward compatibility.

    Args:
        message: Message to log.
        verbose: Whether to print (accepts bool for backward compatibility or int for count)

    Example:
        >>> log_verbose("Processing query...")
    """
    if verbose:
        click.echo(f"[INFO] {message}", err=True)


def log_error(message: str) -> None:
    """Print error message to stderr.

    Args:
        message: Error message to log.

    Example:
        >>> log_error("Query failed: invalid API key")
    """
    click.echo(f"Error: {message}", err=True)


def read_stdin() -> str:
    """Read input from stdin.

    Returns:
        The full stdin content as a string.

    Raises:
        click.ClickException: If stdin is empty or cannot be read.

    Example:
        >>> query = read_stdin()
    """
    if sys.stdin.isatty():
        raise click.ClickException("No input provided via stdin. Use --help for usage examples.")

    try:
        content = sys.stdin.read().strip()
        if not content:
            raise click.ClickException("Empty input from stdin")
        return content
    except Exception as e:
        raise click.ClickException(f"Failed to read from stdin: {str(e)}") from e


def output_markdown(
    response_text: str, grounding_metadata: dict[str, object] | None = None
) -> None:
    """Output markdown-formatted text to stdout.

    Args:
        response_text: The main response text from the query.
        grounding_metadata: Optional grounding metadata with sources.

    Example:
        >>> output_markdown("Best coffee shops...", {"grounding_chunks": [...]})
    """
    # Output main response
    click.echo(response_text)

    # Output sources if available
    if grounding_metadata and "grounding_chunks" in grounding_metadata:
        chunks = grounding_metadata["grounding_chunks"]
        if chunks and isinstance(chunks, list):
            click.echo("\n---\n")
            click.echo("## Sources\n")
            for i, chunk in enumerate(chunks, 1):
                if isinstance(chunk, dict):
                    title = chunk.get("title", "Unknown")
                    uri = chunk.get("uri", "")
                    if uri:
                        click.echo(f"{i}. [{title}]({uri})")
                    else:
                        click.echo(f"{i}. {title}")
