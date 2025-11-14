"""Client management for Gemini API.

Handles creation and caching of Gemini API clients with proper error handling.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import os

from google import genai


class ClientError(Exception):
    """Raised when client initialization fails."""

    pass


_client: genai.Client | None = None


def get_client() -> genai.Client:
    """Get or create the Gemini API client.

    Returns:
        Initialized Gemini client instance.

    Raises:
        ClientError: If GEMINI_API_KEY environment variable is not set.

    Example:
        >>> client = get_client()
        >>> # Use client for API calls
    """
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ClientError(
                "GEMINI_API_KEY environment variable is required. "
                "Set it with: export GEMINI_API_KEY='your-api-key'"
            )
        _client = genai.Client(api_key=api_key)
    return _client
