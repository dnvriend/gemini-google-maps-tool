---
description: Query Gemini with Google Maps location data
argument-hint: query
---

Query Gemini with Google Maps grounding for location-aware information about places, businesses, and attractions.

## Usage

```bash
gemini-google-maps-tool query "QUERY" [OPTIONS]
```

## Arguments

- `QUERY`: Search query (required)
- `--lat-lon LAT,LON`: Location coordinates (e.g., "52.37,4.89")
- `--model {flash|flash-lite}`: Model selection (default: flash-lite)
- `-v/-vv/-vvv`: Verbosity (INFO/DEBUG/TRACE)
- `--text` / `-t`: Output markdown instead of JSON
- `--stdin` / `-s`: Read query from stdin

## Examples

```bash
# Basic query
gemini-google-maps-tool query "Best coffee shops in Amsterdam"

# With location context
gemini-google-maps-tool query "Italian restaurants nearby" \
  --lat-lon "52.37,4.89"

# Markdown output with sources
gemini-google-maps-tool query "Museums in Paris" --text

# Verbose mode with full metadata
gemini-google-maps-tool query "Best sushi" -v

# From stdin for pipeline
echo "Best hotels in NYC" | gemini-google-maps-tool query --stdin
```

## Output

JSON (default) with `response_text` and optional `grounding_metadata`, or markdown text with citations.
