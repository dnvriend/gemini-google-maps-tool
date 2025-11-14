"""Core library functions for Google Maps grounding with Gemini.

This module provides the core business logic for querying Gemini with
Google Maps integration, independent of CLI concerns.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from gemini_google_maps_tool.core.client import get_client
from gemini_google_maps_tool.core.maps import MapsQueryResult, query_maps

__all__ = ["get_client", "query_maps", "MapsQueryResult"]
