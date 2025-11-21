"""Client management for Gemini API.

Handles creation and caching of Gemini API clients with proper error handling.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import logging
import os

from google import genai

logger = logging.getLogger(__name__)


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
        logger.debug("Initializing Gemini API client")
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable not set")
            raise ClientError(
                "GEMINI_API_KEY environment variable is required. "
                "Set it with: export GEMINI_API_KEY='your-api-key'"
            )
        logger.debug("Creating Gemini client with API key")
        _client = genai.Client(api_key=api_key)
        logger.debug("Gemini client initialized successfully")
    else:
        logger.debug("Reusing existing Gemini client")
    return _client
