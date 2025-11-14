"""Query command implementation for Google Maps grounding.

Provides the main 'query' CLI command for querying Gemini with Google Maps data.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import sys

import click

from gemini_google_maps_tool.core import get_client, query_maps
from gemini_google_maps_tool.core.client import ClientError
from gemini_google_maps_tool.core.maps import QueryError
from gemini_google_maps_tool.utils import (
    log_error,
    log_verbose,
    output_json,
    output_markdown,
    read_stdin,
)


@click.command()
@click.argument("query_text", required=False)
@click.option(
    "--lat-lon",
    default=None,
    metavar="LAT,LON",
    help="Location coordinates in format lat,lon (e.g., 37.78193,-122.40476)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output (includes full grounding metadata)",
)
@click.option(
    "--model",
    type=click.Choice(["flash", "flash-lite"], case_sensitive=False),
    default="flash-lite",
    help="Model to use: 'flash' (gemini-2.5-flash) or 'flash-lite' (gemini-2.5-flash-lite)",
)
@click.option(
    "--stdin",
    "-s",
    is_flag=True,
    help="Read query from stdin instead of argument",
)
@click.option(
    "--text",
    "-t",
    is_flag=True,
    help="Output markdown text instead of JSON",
)
def query(
    query_text: str | None,
    lat_lon: str | None,
    verbose: bool,
    model: str,
    stdin: bool,
    text: bool,
) -> None:
    """Query Gemini with Google Maps grounding for location-aware information.

    QUERY_TEXT: The query to send to Gemini (required unless --stdin is used)

    This command connects to Gemini with Google Maps integration, enabling queries
    about places, businesses, directions, and location-specific information with
    accurate, up-to-date data from Google Maps.

    Examples:

    \b
    # Basic query
    gemini-google-maps-tool query "Best coffee shops near me"

    \b
    # Query with location context
    gemini-google-maps-tool query "Italian restaurants nearby" \\
        --lat-lon "37.78193,-122.40476"

    \b
    # Query with verbose output (includes grounding sources)
    gemini-google-maps-tool query "Museums in San Francisco" \\
        --lat-lon "37.7749,-122.4194" \\
        --verbose

    \b
    # Using flash model instead of flash-lite
    gemini-google-maps-tool query "Plan a day in NYC" \\
        --model flash

    \b
    # Reading query from stdin (useful for piping)
    echo "Best sushi restaurants near Times Square" | \\
        gemini-google-maps-tool query --stdin \\
        --lat-lon "40.758,-73.9855"

    \b
    # Output as markdown text with sources
    gemini-google-maps-tool query "Best museums in Paris" \\
        --text

    \b
    Output Format:
        JSON (default):
        {
          "response_text": "...",
          "grounding_metadata": {  // Only with --verbose
            "grounding_chunks": [...],
            "grounding_supports": [...],
            "google_maps_widget_context_token": "..."
          }
        }

        Markdown (with --text):
        <response text>

        ---

        ## Sources

        1. [Place Name](URL)
        2. [Place Name](URL)

    Environment Variables:
        GEMINI_API_KEY: Required API key for Gemini authentication
                       Get your key from: https://aistudio.google.com/app/apikey
    """
    try:
        # Determine query source
        if stdin:
            if query_text:
                raise click.UsageError(
                    "Cannot specify both QUERY_TEXT and --stdin. "
                    "Use either positional argument OR --stdin, not both."
                )
            query_input = read_stdin()
        elif query_text:
            query_input = query_text
        else:
            raise click.UsageError(
                "Missing query. Provide QUERY_TEXT as argument or use --stdin. "
                "Examples:\n"
                "  gemini-google-maps-tool query 'Best coffee shops near me'\n"
                "  echo 'query' | gemini-google-maps-tool query --stdin"
            )

        # Parse location if provided
        lat_lon_tuple = None
        if lat_lon:
            try:
                from gemini_google_maps_tool.core.maps import parse_lat_lon

                lat_lon_tuple = parse_lat_lon(lat_lon)
                if verbose:
                    log_verbose(f"Using location: {lat_lon_tuple[0]}, {lat_lon_tuple[1]}")
            except ValueError as e:
                log_error(str(e))
                sys.exit(1)

        # Map model choice to full model name
        model_name = "gemini-2.5-flash" if model == "flash" else "gemini-2.5-flash-lite"
        if verbose:
            log_verbose(f"Using model: {model_name}")

        # Get client and execute query
        client = get_client()
        if verbose:
            log_verbose("Querying with Google Maps grounding...")

        # Include grounding if verbose OR text mode (for sources)
        include_grounding = verbose or text

        result = query_maps(
            client=client,
            query=query_input,
            lat_lon=lat_lon_tuple,
            model=model_name,
            include_grounding=include_grounding,
        )

        if verbose:
            log_verbose("Query completed successfully")

        # Output based on format preference
        if text:
            # Text/markdown output
            grounding_dict: dict[str, object] | None = None
            if result.grounding_metadata:
                metadata = result.grounding_metadata
                grounding_dict = {}

                # Add grounding chunks for markdown sources
                if metadata.grounding_chunks:
                    grounding_dict["grounding_chunks"] = [
                        {
                            "title": chunk.title,
                            "uri": chunk.uri,
                            "place_id": chunk.place_id,
                        }
                        for chunk in metadata.grounding_chunks
                    ]

            output_markdown(result.response_text, grounding_dict)
        else:
            # JSON output
            output: dict[str, object] = {"response_text": result.response_text}

            if verbose and result.grounding_metadata:
                metadata = result.grounding_metadata
                grounding_dict_json: dict[str, object] = {}

                # Add grounding chunks
                if metadata.grounding_chunks:
                    grounding_dict_json["grounding_chunks"] = [
                        {
                            "title": chunk.title,
                            "uri": chunk.uri,
                            "place_id": chunk.place_id,
                        }
                        for chunk in metadata.grounding_chunks
                    ]

                # Add grounding supports
                if metadata.grounding_supports:
                    grounding_dict_json["grounding_supports"] = [
                        {
                            "segment": {
                                "start_index": support.segment.start_index,
                                "end_index": support.segment.end_index,
                                "text": support.segment.text,
                            },
                            "grounding_chunk_indices": support.grounding_chunk_indices,
                        }
                        for support in metadata.grounding_supports
                    ]

                # Add widget token
                if metadata.google_maps_widget_context_token:
                    grounding_dict_json["google_maps_widget_context_token"] = (
                        metadata.google_maps_widget_context_token
                    )

                if grounding_dict_json:
                    output["grounding_metadata"] = grounding_dict_json

            output_json(output)

    except ClientError as e:
        log_error(str(e))
        sys.exit(1)
    except QueryError as e:
        log_error(str(e))
        sys.exit(1)
    except click.ClickException:
        raise  # Let Click handle these
    except Exception as e:
        log_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
