"""CLI entry point for gemini-google-maps-tool.

Main entry point that registers all available commands.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click
from click.shell_completion import BashComplete, FishComplete, ZshComplete

from gemini_google_maps_tool.commands import query


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Query Gemini with Google Maps grounding for location-aware information.

    A CLI tool and Python library that connects to Gemini with Google Maps
    integration (250+ million places), enabling queries about places, businesses,
    directions, and location-specific information with accurate, up-to-date data.

    Features:
      • Multi-level verbosity: -v (INFO), -vv (DEBUG), -vvv (TRACE)
      • Shell completion: bash, zsh, fish
      • Multiple output formats: JSON (default) or Markdown (--text)
      • Location-aware queries with lat/lon coordinates
      • Claude Code plugin integration

    Examples:

    \b
        # Basic query
        gemini-google-maps-tool query "Best coffee shops near me"

    \b
        # Query with location context
        gemini-google-maps-tool query "Italian restaurants nearby" \\
            --lat-lon "37.78193,-122.40476"

    \b
        # Multi-level verbosity
        gemini-google-maps-tool query "Museums" -v     # INFO
        gemini-google-maps-tool query "Hotels" -vv     # DEBUG
        gemini-google-maps-tool query "Parks" -vvv     # TRACE

    \b
        # Generate shell completion
        eval "$(gemini-google-maps-tool completion bash)"

    Get started: gemini-google-maps-tool query --help
    """
    # If invoked without a command, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register commands
main.add_command(query)


@main.command()
@click.argument("shell", type=click.Choice(["bash", "zsh", "fish"]))
def completion(shell: str) -> None:
    """Generate shell completion script for tab-completion support.

    SHELL: The shell type (bash, zsh, or fish)

    Generates completion scripts that enable tab-completion for commands,
    options, and arguments in your shell.

    Examples:

    \b
        # Bash - temporary activation (current session only)
        eval "$(gemini-google-maps-tool completion bash)"

    \b
        # Bash - permanent activation (add to ~/.bashrc)
        echo 'eval "$(gemini-google-maps-tool completion bash)"' >> ~/.bashrc

    \b
        # Zsh - temporary activation (current session only)
        eval "$(gemini-google-maps-tool completion zsh)"

    \b
        # Zsh - permanent activation (add to ~/.zshrc)
        echo 'eval "$(gemini-google-maps-tool completion zsh)"' >> ~/.zshrc

    \b
        # Fish - install to completions directory
        gemini-google-maps-tool completion fish > \\
            ~/.config/fish/completions/gemini-google-maps-tool.fish

    \b
        # Alternative: generate to file for better shell startup performance
        gemini-google-maps-tool completion bash > ~/.gemini-completion.bash
        echo 'source ~/.gemini-completion.bash' >> ~/.bashrc

    \b
    Output:
        Prints shell-specific completion script to stdout.
        Source the output to enable tab-completion.
    """
    ctx = click.get_current_context()

    # Get the appropriate completion class
    completion_classes = {
        "bash": BashComplete,
        "zsh": ZshComplete,
        "fish": FishComplete,
    }

    completion_class = completion_classes.get(shell)
    if completion_class:
        # Get the root command and the command name
        root_command = ctx.find_root().command
        prog_name = ctx.command_path.split()[0]
        completer = completion_class(root_command, {}, prog_name, "_complete")
        click.echo(completer.source())
    else:
        raise click.BadParameter(f"Unsupported shell: {shell}")


if __name__ == "__main__":
    main()
