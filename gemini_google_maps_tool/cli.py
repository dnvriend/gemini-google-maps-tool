"""CLI entry point for gemini-google-maps-tool.

Main entry point that registers all available commands.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from gemini_google_maps_tool.commands import query


@click.group(invoke_without_command=True)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Query Gemini with Google Maps grounding for location-aware information.

    A CLI tool that connects to Gemini with Google Maps integration, enabling
    queries about places, businesses, directions, and location-specific information
    with accurate, up-to-date data from Google Maps.

    Examples:

    \b
        # Basic query
        gemini-google-maps-tool query "Best coffee shops near me"

    \b
        # Query with location context
        gemini-google-maps-tool query "Italian restaurants nearby" \\
            --lat-lon "37.78193,-122.40476"

    \b
        # Query with verbose output (includes sources)
        gemini-google-maps-tool query "Museums in SF" \\
            --lat-lon "37.7749,-122.4194" --verbose

    Get started by running: gemini-google-maps-tool query --help
    """
    # If invoked without a command, show help
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register commands
main.add_command(query)


if __name__ == "__main__":
    main()
