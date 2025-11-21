"""Google Maps grounding query operations.

Provides functions for querying Gemini with Google Maps data integration.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
from dataclasses import dataclass

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class QueryError(Exception):
    """Raised when a query operation fails."""

    pass


@dataclass
class GroundingChunk:
    """Represents a single Google Maps source."""

    title: str | None
    uri: str | None
    place_id: str | None


@dataclass
class GroundingSegment:
    """Represents a text segment linked to sources."""

    start_index: int | None
    end_index: int | None
    text: str


@dataclass
class GroundingSupport:
    """Represents a text segment and its associated source indices."""

    segment: GroundingSegment
    grounding_chunk_indices: list[int]


@dataclass
class GroundingMetadata:
    """Complete grounding metadata from a query response."""

    grounding_chunks: list[GroundingChunk]
    grounding_supports: list[GroundingSupport]
    google_maps_widget_context_token: str | None


@dataclass
class MapsQueryResult:
    """Result from a Google Maps grounded query.

    Attributes:
        response_text: The generated text response from the model.
        grounding_metadata: Optional grounding metadata with sources and citations.
    """

    response_text: str
    grounding_metadata: GroundingMetadata | None = None


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
    parts = lat_lon_str.split(",")
    if len(parts) != 2:
        raise ValueError(
            "Invalid lat-lon format: Expected format 'lat,lon' (e.g., 37.78193,-122.40476). "
            f"Got: {lat_lon_str}"
        )

    try:
        lat = float(parts[0].strip())
        lon = float(parts[1].strip())
    except ValueError as e:
        raise ValueError(
            f"Invalid lat-lon format: Could not parse coordinates as numbers. "
            f"Expected format: 'lat,lon' (e.g., 37.78193,-122.40476). Got: {lat_lon_str}"
        ) from e

    # Validate latitude range
    if not -90 <= lat <= 90:
        raise ValueError(
            f"Invalid latitude: {lat}. Latitude must be between -90 and 90. "
            f"Expected format: 'lat,lon' (e.g., 37.78193,-122.40476)"
        )

    # Validate longitude range
    if not -180 <= lon <= 180:
        raise ValueError(
            f"Invalid longitude: {lon}. Longitude must be between -180 and 180. "
            f"Expected format: 'lat,lon' (e.g., 37.78193,-122.40476)"
        )

    return (lat, lon)


def extract_grounding_metadata(
    response: types.GenerateContentResponse,
) -> GroundingMetadata | None:
    """Extract grounding metadata from Gemini API response.

    Args:
        response: The GenerateContentResponse from Gemini API.

    Returns:
        Parsed GroundingMetadata if available, None otherwise.
    """
    if not response.candidates or len(response.candidates) == 0:
        return None

    candidate = response.candidates[0]
    if not hasattr(candidate, "grounding_metadata"):
        return None

    grounding_metadata = candidate.grounding_metadata
    if not grounding_metadata:
        return None

    # Extract grounding chunks (Google Maps sources)
    grounding_chunks: list[GroundingChunk] = []
    chunks = getattr(grounding_metadata, "grounding_chunks", [])
    # Defensive check: ensure chunks is iterable
    if chunks is None:
        chunks = []
    for chunk in chunks:
        if hasattr(chunk, "maps") and chunk.maps:
            grounding_chunks.append(
                GroundingChunk(
                    title=getattr(chunk.maps, "title", None),
                    uri=getattr(chunk.maps, "uri", None),
                    place_id=getattr(chunk.maps, "place_id", None),
                )
            )

    # Extract grounding supports (text segments linked to sources)
    grounding_supports: list[GroundingSupport] = []
    supports = getattr(grounding_metadata, "grounding_supports", [])
    # Defensive check: ensure supports is iterable
    if supports is None:
        supports = []
    for support in supports:
        segment = getattr(support, "segment", None)
        chunk_indices = getattr(support, "grounding_chunk_indices", [])

        if segment:
            grounding_supports.append(
                GroundingSupport(
                    segment=GroundingSegment(
                        start_index=getattr(segment, "start_index", None),
                        end_index=getattr(segment, "end_index", None),
                        text=getattr(segment, "text", ""),
                    ),
                    grounding_chunk_indices=chunk_indices,
                )
            )

    # Extract widget context token
    widget_token = getattr(grounding_metadata, "google_maps_widget_context_token", None)

    # Only return metadata if we have meaningful data
    if not grounding_chunks and not grounding_supports and not widget_token:
        return None

    return GroundingMetadata(
        grounding_chunks=grounding_chunks,
        grounding_supports=grounding_supports,
        google_maps_widget_context_token=widget_token,
    )


def query_maps(
    client: genai.Client,
    query: str,
    lat_lon: tuple[float, float] | None = None,
    model: str = "gemini-2.5-flash-lite",
    include_grounding: bool = False,
) -> MapsQueryResult:
    """Query Gemini with Google Maps grounding.

    Args:
        client: Initialized Gemini API client.
        query: The query text to send to the model.
        lat_lon: Optional (latitude, longitude) tuple for location context.
        model: Model name to use (default: "gemini-2.5-flash-lite").
        include_grounding: Whether to include grounding metadata in response.

    Returns:
        MapsQueryResult with response text and optional grounding metadata.

    Raises:
        QueryError: If the API query fails.

    Example:
        >>> from gemini_google_maps_tool.core import get_client, query_maps
        >>> client = get_client()
        >>> result = query_maps(
        ...     client,
        ...     "Best coffee shops near me",
        ...     lat_lon=(37.78193, -122.40476),
        ...     include_grounding=True
        ... )
        >>> print(result.response_text)
        >>> if result.grounding_metadata:
        ...     for chunk in result.grounding_metadata.grounding_chunks:
        ...         print(f"Source: {chunk.title} - {chunk.uri}")
    """
    try:
        logger.debug(f"Starting Maps query with model: {model}")
        logger.debug(
            f"Query text: {query[:100]}..." if len(query) > 100 else f"Query text: {query}"
        )

        # Build Google Maps tool
        logger.debug("Building Google Maps tool configuration")
        google_maps_tool = types.Tool(google_maps=types.GoogleMaps())

        # Build config
        config = types.GenerateContentConfig(tools=[google_maps_tool])

        # Add location context if provided
        if lat_lon:
            lat, lon = lat_lon
            logger.debug(f"Adding location context: lat={lat}, lon={lon}")
            lat_lng = types.LatLng(latitude=lat, longitude=lon)
            config.tool_config = types.ToolConfig(
                retrieval_config=types.RetrievalConfig(lat_lng=lat_lng)
            )
        else:
            logger.debug("No location context provided")

        # Generate content
        logger.debug(f"Calling Gemini API with model: {model}")
        response = client.models.generate_content(
            model=model,
            contents=query,
            config=config,
        )
        logger.debug("Received response from Gemini API")

        # Check if response has candidates
        candidate_count = len(response.candidates) if response.candidates else 0
        logger.debug(f"Validating response: candidates count = {candidate_count}")
        if not response.candidates or len(response.candidates) == 0:
            logger.error("API returned no response candidates")
            raise QueryError(
                "API returned no response candidates. This may be due to:\n"
                "  - Rate limiting (too many requests)\n"
                "  - API service issues\n"
                "  - Query content filtering\n"
                "  - Invalid query format\n"
                "Suggestions:\n"
                "  - Wait a few seconds and try again\n"
                "  - Rephrase your query\n"
                "  - Check your API key has sufficient quota"
            )

        # Extract response text
        logger.debug("Extracting response text from candidate")
        response_text = ""
        candidate = response.candidates[0]
        if candidate.content and candidate.content.parts:
            text_parts: list[str] = []
            for part in candidate.content.parts:
                if hasattr(part, "text") and part.text:
                    text_parts.append(part.text)
            response_text = "".join(text_parts)
        logger.debug(f"Extracted response text length: {len(response_text)}")

        # Check if we got empty response text
        if not response_text:
            logger.error("API returned empty response text")
            raise QueryError(
                "API returned empty response text. This may be due to:\n"
                "  - Content filtering or safety blocks\n"
                "  - Query processing issues\n"
                "  - Incomplete API response\n"
                "Suggestions:\n"
                "  - Rephrase your query\n"
                "  - Try a simpler or more specific query\n"
                "  - Wait a few seconds and try again"
            )

        # Extract grounding metadata if requested
        grounding_metadata = None
        if include_grounding:
            logger.debug("Extracting grounding metadata")
            grounding_metadata = extract_grounding_metadata(response)
            if grounding_metadata:
                chunk_count = len(grounding_metadata.grounding_chunks)
                logger.debug(f"Found {chunk_count} grounding chunks (sources)")
            else:
                logger.debug("No grounding metadata found in response")

        logger.debug("Query completed successfully")
        return MapsQueryResult(
            response_text=response_text,
            grounding_metadata=grounding_metadata,
        )

    except QueryError:
        # Re-raise QueryErrors with our detailed messages
        raise
    except Exception as e:
        # Catch unexpected errors and provide agent-friendly message
        logger.error(f"Unexpected error during query: {type(e).__name__}: {str(e)}")
        logger.debug("Full traceback:", exc_info=True)
        raise QueryError(
            f"Unexpected error during query: {str(e)}\n"
            "Suggestions:\n"
            "  - Wait a few seconds and try again\n"
            "  - Check your internet connection\n"
            "  - Verify your API key is valid\n"
            "  - Try a different query"
        ) from e
