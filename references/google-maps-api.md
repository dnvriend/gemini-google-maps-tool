# Google Maps Grounding API Documentation

This reference provides comprehensive documentation for using Grounding with Google Maps in the Gemini API.

**Official Documentation**: [Grounding with Google Maps](https://ai.google.dev/gemini-api/docs/maps-grounding)

## Overview

Grounding with Google Maps connects the generative capabilities of Gemini with the rich, factual, and up-to-date data of Google Maps. This feature enables developers to easily incorporate location-aware functionality into their applications. When a user query has a context related to Maps data, the Gemini model leverages Google Maps to provide factually accurate and fresh answers that are relevant to the user's specified location or general area.

### Key Benefits

- **Accurate, location-aware responses**: Leverage Google Maps' extensive and current data for geographically specific queries
- **Enhanced personalization**: Tailor recommendations and information based on user-provided locations
- **Contextual information and widgets**: Context tokens to render interactive Google Maps widgets alongside generated content

## How Grounding with Google Maps Works

Grounding with Google Maps integrates the Gemini API with the Google Geo ecosystem by using the Maps API as a grounding source. When a user's query contains geographical context, the Gemini model can invoke the Grounding with Google Maps tool. The model can then generate responses grounded in Google Maps data relevant to the provided location.

The process typically involves:

1. **User query**: A user submits a query to your application, potentially including geographical context (e.g., "coffee shops near me," "museums in San Francisco").

2. **Tool invocation**: The Gemini model, recognizing the geographical intent, invokes the Grounding with Google Maps tool. This tool can optionally be provided with the user's `latitude` and `longitude`. The tool is a textual search tool and behaves similarly to searching on Maps, in that local queries ("near me") will use the coordinates, while specific or non-local queries are unlikely to be influenced by the explicit location.

3. **Data retrieval**: The Grounding with Google Maps service queries Google Maps for relevant information (e.g., places, reviews, photos, addresses, opening hours).

4. **Grounded generation**: The retrieved Maps data is used to inform the Gemini model's response, ensuring factual accuracy and relevance.

5. **Response & widget token**: The model returns a text response, which includes citations to Google Maps sources. Optionally, the API response may also contain a `google_maps_widget_context_token`, allowing developers to render a contextual Google Maps widget in their application for visual interaction.

## Why and When to Use Grounding with Google Maps

Grounding with Google Maps is ideal for applications that require accurate, up-to-date, and location-specific information. It enhances the user experience by providing relevant and personalized content backed by Google Maps' extensive database of over 250 million places worldwide.

You should use Grounding with Google Maps when your application needs to:

- Provide complete and accurate responses to geo-specific questions
- Build conversational trip planners and local guides
- Recommend points of interest based on location and user preferences like restaurants or shops
- Create location-aware experiences for social, retail, or food delivery services

Grounding with Google Maps excels in use cases where proximity and current factual data are critical, such as finding the "best coffee shop near me" or getting directions.

## API Methods and Parameters

Grounding with Google Maps is exposed through the Gemini API as a tool within the [`generateContent`](https://ai.google.dev/api/generate-content) method. You enable and configure Grounding with Google Maps by including a [`googleMaps`](https://ai.google.dev/api/caching#GoogleMaps) object in the `tools` parameter of your request.

### Basic Configuration

```json
{
  "contents": [{
    "parts": [
      {"text": "Restaurants near Times Square."}
    ]
  }],
  "tools": [{ "googleMaps": {} }]
}
```

### Enable Widget

The [`googleMaps`](https://ai.google.dev/api/caching#GoogleMaps) tool can additionally accept a boolean `enableWidget` parameter, that is used to control whether the [`googleMapsWidgetContextToken`](https://ai.google.dev/api/generate-content#GroundingMetadata) field is returned in the response. This can be used to display a [contextual Places widget](https://developers.google.com/maps/documentation/javascript/reference/places-widget).

```json
{
  "contents": [{
    "parts": [
      {"text": "Restaurants near Times Square."}
    ]
  }],
  "tools": [{ "googleMaps": { "enableWidget": true } }]
}
```

### Location Context

Additionally, the tool supports passing the contextual location as `toolConfig`.

```json
{
  "contents": [{
    "parts": [
      {"text": "Restaurants near here."}
    ]
  }],
  "tools": [{ "googleMaps": {} }],
  "toolConfig": {
    "retrievalConfig": {
      "latLng": {
        "latitude": 40.758896,
        "longitude": -73.985130
      }
    }
  }
}
```

## Understanding the Grounding Response

When a response is successfully grounded with Google Maps data, the response includes a [`groundingMetadata`](https://ai.google.dev/api/generate-content#GroundingMetadata) field. This structured data is essential for verifying claims and building a rich citation experience in your application, as well as meeting the service usage requirements.

### Response Structure

```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "CanteenM is an American restaurant with..."
          }
        ],
        "role": "model"
      },
      "groundingMetadata": {
        "groundingChunks": [
          {
            "maps": {
              "uri": "https://maps.google.com/?cid=13100894621228039586",
              "title": "Heaven on 7th Marketplace",
              "placeId": "places/ChIJ0-zA1vBZwokRon0fGj-6z7U"
            }
          }
        ],
        "groundingSupports": [
          {
            "segment": {
              "startIndex": 0,
              "endIndex": 79,
              "text": "CanteenM is an American restaurant with a 4.6-star rating and is open 24 hours."
            },
            "groundingChunkIndices": [0]
          }
        ],
        "webSearchQueries": [
          "restaurants near me"
        ],
        "googleMapsWidgetContextToken": "widgetcontent/..."
      }
    }
  ]
}
```

### Response Fields

The Gemini API returns the following information with the [`groundingMetadata`](https://ai.google.dev/api/generate-content#GroundingMetadata):

- **`groundingChunks`**: Array of objects containing the `maps` sources (`uri`, `placeId` and `title`).

- **`groundingSupports`**: Array of chunks to connect model response text to the sources in `groundingChunks`. Each chunk links a text span (defined by `startIndex` and `endIndex`) to one or more `groundingChunkIndices`. This is the key to building inline citations.

- **`googleMapsWidgetContextToken`**: A text token that can be used to render a [contextual Places widget](https://developers.google.com/maps/documentation/javascript/reference/places-widget).

For a code snippet showing how to render inline citations in text, see [the example](https://ai.google.dev/gemini-api/docs/google-search#attributing_sources_with_inline_citations) in the Grounding with Google Search docs.

### Display the Google Maps Contextual Widget

To use the returned `googleMapsWidgetContextToken`, you need to [load the Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript/load-maps-js-api).

## Use Cases

Grounding with Google Maps supports a variety of location-aware use cases. The following examples demonstrate how different prompts and parameters can leverage Grounding with Google Maps.

**Note**: Information in the Google Maps Grounded Results may differ from actual conditions.

### Handling Place-Specific Questions

Ask detailed questions about a specific place to get answers based on Google user reviews and other Maps data.

**Python Example:**
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "Is there a cafe near the corner of 1st and Main that has outdoor seating?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        # Turn on the Maps tool
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        # Provide the relevant location context (this is in Los Angeles)
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            lat_lng=types.LatLng(
                latitude=34.050481, longitude=-118.248526))),
    ),
)

print("Generated Response:")
print(response.text)

if grounding := response.candidates[0].grounding_metadata:
    if chunks := grounding.grounding_chunks:
        print('-' * 40)
        print("Sources:")
        for chunk in chunks:
            print(f'- [{chunk.maps.title}]({chunk.maps.uri})')
```

### Providing Location-Based Personalization

Get recommendations tailored to a user's preferences and a specific geographical area.

**Python Example:**
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "Which family-friendly restaurants near here have the best playground reviews?"

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            # Provide the location as context; this is Austin, TX.
            lat_lng=types.LatLng(
                latitude=30.2672, longitude=-97.7431))),
    ),
)

print("Generated Response:")
print(response.text)

if grounding := response.candidates[0].grounding_metadata:
    if chunks := grounding.grounding_chunks:
        print('-' * 40)
        print("Sources:")
        for chunk in chunks:
            print(f'- [{chunk.maps.title}]({chunk.maps.uri})')
```

### Assisting with Itinerary Planning

Generate multi-day plans with directions and information about various locations, perfect for travel applications.

In this example, the `googleMapsWidgetContextToken` has been requested by enabling the widget in the Google Maps tool. When enabled, the returned token can be used to render a contextual Places widget using the [<gmp-places-contextual> component](https://developers.google.com/maps/documentation/javascript/reference/places-widget#PlaceContextualElement) from the Google Maps JavaScript API.

**Python Example:**
```python
from google import genai
from google.genai import types

client = genai.Client()

prompt = "Plan a day in San Francisco for me. I want to see the Golden Gate Bridge, visit a museum, and have a nice dinner."

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_maps=types.GoogleMaps(enable_widget=True))],
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            # Provide the location as context, this is in San Francisco.
            lat_lng=types.LatLng(
                latitude=37.78193, longitude=-122.40476))),
    ),
)

print("Generated Response:")
print(response.text)

if grounding := response.candidates[0].grounding_metadata:
    if grounding.grounding_chunks:
        print('-' * 40)
        print("Sources:")
        for chunk in grounding.grounding_chunks:
            print(f'- [{chunk.maps.title}]({chunk.maps.uri})')
    
    if widget_token := grounding.google_maps_widget_context_token:
        print('-' * 40)
        print(f'<gmp-place-contextual context-token="{widget_token}"></gmp-place-contextual>')
```

## Service Usage Requirements

This section describes the service usage requirements for Grounding with Google Maps.

### Inform the User about the Use of Google Maps Sources

With each Google Maps Grounded Result, you'll receive sources in `groundingChunks` that support each response. The following metadata is also returned:

- source uri
- title
- ID

When presenting results from Grounding with Google Maps, you must specify the associated Google Maps sources, and inform your users of the following:

- The Google Maps sources must immediately follow the generated content that the sources support. This generated content is also referred to as Google Maps Grounded Result.
- The Google Maps sources must be viewable within one user interaction.

### Display Google Maps Sources with Google Maps Links

For each source in `groundingChunks` and in `grounding_chunks.maps.placeAnswerSources.reviewSnippets`, a link preview must be generated following these requirements:

- Attribute each source to Google Maps following the Google Maps text [attribution guidelines](https://ai.google.dev/gemini-api/docs/maps-grounding#maps-attribution-guidelines).
- Display the source title provided in the response.
- Link to the source using the `uri` or `googleMapsUri` from the response.

You can collapse the view of the sources, but they must be immediately accessible.

**Optional**: Enhance the link preview with additional content, such as:

- A [Google Maps favicon](https://www.google.com/images/branding/product/ico/maps15_bnuw3a_32dp.ico) is inserted before the Google Maps text attribution.
- A photo from the source URL (`og:image`).

For more information about some of our Google Maps data providers and their license terms, see the [Google Maps and Google Earth legal notices](https://www.google.com/help/legalnotices_maps/).

### Google Maps Text Attribution Guidelines

When you attribute sources to Google Maps in text, follow these guidelines:

- Don't modify the text Google Maps in any way:
  - Don't change the capitalization of Google Maps.
  - Don't wrap Google Maps onto multiple lines.
  - Don't localize Google Maps into another language.
  - Prevent browsers from translating Google Maps by using the HTML attribute `translate="no"`.

- Style Google Maps text as described in the following table:

| Property | Style |
|----------|-------|
| Font family | Roboto. Loading the font is optional. |
| Fallback font family | Any sans serif body font already used in your product or "Sans-Serif" to invoke the default system font |
| Font style | Normal |
| Font weight | 400 |
| Font color | White, black (#1F1F1F), or gray (#5E5E5E). Maintain accessible (4.5:1) contrast against the background. |
| Font size | - Minimum font size: 12sp<br>- Maximum font size: 16sp<br>- To learn about sp, see Font size units on the [Material Design website](https://m3.material.io/styles/typography/type-scale-tokens#3f4488e7-3b74-45b0-a143-9d6afa4d62dc). |
| Spacing | Normal |

#### Example CSS

The following CSS renders Google Maps with the appropriate typographic style and color on a white or light background.

```css
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

.GMP-attribution {
  font-family: Roboto, Sans-Serif;
  font-style: normal;
  font-weight: 400;
  font-size: 1rem;
  letter-spacing: normal;
  white-space: nowrap;
  color: #5e5e5e;
}
```

### Context Token, Place ID, and Review ID

The Google Maps data includes context token, place ID, and review ID. You might cache, store, and export the following response data:

- `googleMapsWidgetContextToken`
- `placeId`
- `reviewId`

The restrictions against caching in the Grounding with Google Maps Terms don't apply.

### Prohibited Activity and Territory

Grounding with Google Maps has additional restrictions for certain content and activities to maintain a safe and reliable platform. In addition to the usage restrictions in the Terms, you will not use Grounding with Google Maps for high risk activities including emergency response services. You will not distribute or market your application that offers Grounding with Google Maps in a Prohibited Territory. The current Prohibited Territories are:

- China
- Crimea
- Cuba
- Donetsk People's Republic
- Iran
- Luhansk People's Republic
- North Korea
- Syria
- Vietnam

This list may be updated from time to time.

## Best Practices

- **Provide user location**: For the most relevant and personalized responses, always include the `user_location` (latitude and longitude) in your `googleMapsGrounding` configuration when the user's location is known.

- **Render the Google Maps contextual widget**: The contextual widget is rendered using the context token, `googleMapsWidgetContextToken`, which is returned in the Gemini API response and can be used to render visual content from Google Maps. For more information on the contextual widget, see [Grounding with Google Maps widget](https://developers.google.com/maps/documentation/javascript/maps-grounding-widget) in the Google Developer Guide.

- **Inform End-Users**: Clearly inform your end-users that Google Maps data is being used to answer their queries, especially when the tool is enabled.

- **Monitor Latency**: For conversational applications, ensure that the P95 latency for grounded responses remains within acceptable thresholds to maintain a smooth user experience.

- **Toggle Off When Not Needed**: Grounding with Google Maps is off by default. Only enable it (`"tools": [{"googleMaps": {}}]`) when a query has a clear geographical context, to optimize performance and cost.

## Limitations

- **Geographical Scope**: Currently, Grounding with Google Maps is globally available

- **Model Support**: Only specific Gemini models support Grounding with Google Maps:
  - Gemini 2.5 Flash-Lite
  - Gemini 2.5 Pro
  - Gemini 2.5 Flash
  - Gemini 2.0 Flash (but not 2.0 Flash Lite)

- **Multimodal Inputs/Outputs**: Grounding with Google Maps does not currently support multimodal inputs or outputs beyond text and contextual map widgets.

- **Default State**: The Grounding with Google Maps tool is off by default. You must explicitly enable it in your API requests.

## Pricing and Rate Limits

Grounding with Google Maps pricing is based on queries. The current rate is **$25 / 1K grounded prompts**. The free tier also has up to 500 requests per day available. A request is only counted towards the quota when a prompt successfully returns at least one Google Maps grounded result (i.e., results containing at least one Google Maps source). If multiple queries are sent to Google Maps from a single request, it counts as one request towards the rate limit.

**Note**: The quota for Grounding with Google Maps typically aligns with the underlying Gemini model rate limits.

For detailed pricing information, see the [Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing).

## Supported Models

You can find their capabilities on the [model overview](https://ai.google.dev/gemini-api/docs/models) page.

| Model | Grounding with Google Maps |
|-------|---------------------------|
| [Gemini 2.5 Pro](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-pro) | ✔️ |
| [Gemini 2.5 Flash](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash) | ✔️ |
| [Gemini 2.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/models#gemini-2.5-flash-lite) | ✔️ |
| [Gemini 2.0 Flash](https://ai.google.dev/gemini-api/docs/models#gemini-2.0-flash) | ✔️ |

## Additional Resources

- [Grounding with Google Maps Documentation](https://ai.google.dev/gemini-api/docs/maps-grounding)
- [Grounding with Google Search in the Gemini API Cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Search_Grounding.ipynb)
- [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Safety settings guide](https://ai.google.dev/gemini-api/docs/safety-settings)
- [Google Maps JavaScript API](https://developers.google.com/maps/documentation/javascript)
- [Contextual Places Widget](https://developers.google.com/maps/documentation/javascript/reference/places-widget)

