"""Tests for gemini_google_maps_tool.utils module.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json

from gemini_google_maps_tool.utils import output_json


def test_output_json_dict(capsys: object) -> None:
    """Test that output_json correctly formats a dictionary."""
    data = {"status": "success", "count": 42}
    output_json(data)
    captured = capsys.readouterr()  # type: ignore
    # Parse the captured output to verify it's valid JSON
    parsed = json.loads(captured.out)
    assert parsed == data


def test_output_json_list(capsys: object) -> None:
    """Test that output_json correctly formats a list."""
    data = [1, 2, 3, "test"]
    output_json(data)
    captured = capsys.readouterr()  # type: ignore
    parsed = json.loads(captured.out)
    assert parsed == data
