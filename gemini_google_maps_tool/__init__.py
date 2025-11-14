"""gemini-google-maps-tool: Query Gemini with Google Maps grounding.

A CLI and Python library that enables you to query Gemini with Google Maps
grounding, connecting the model to accurate, up-to-date Google Maps data.

This package provides both a command-line interface and a programmable API
for querying Gemini with location-aware information from Google Maps.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_google_maps_tool.core import MapsQueryResult, get_client, query_maps
from gemini_google_maps_tool.core.client import ClientError
from gemini_google_maps_tool.core.maps import (
    GroundingChunk,
    GroundingMetadata,
    GroundingSegment,
    GroundingSupport,
    QueryError,
    parse_lat_lon,
)

__version__ = "0.1.0"

__all__ = [
    # Core functions
    "get_client",
    "query_maps",
    # Data classes
    "MapsQueryResult",
    "GroundingMetadata",
    "GroundingChunk",
    "GroundingSegment",
    "GroundingSupport",
    # Exceptions
    "ClientError",
    "QueryError",
    # Utilities
    "parse_lat_lon",
]
