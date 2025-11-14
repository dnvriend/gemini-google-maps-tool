# Google Maps Grounding API Setup and Pricing

This reference covers how to obtain and configure your Gemini API key, and details about pricing for Google Maps Grounding.

**Official Documentation**: 
- [Gemini API Keys](https://ai.google.dev/gemini-api/docs/api-key)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Maps Grounding Documentation](https://ai.google.dev/gemini-api/docs/maps-grounding)

## Obtaining an API Key

### Step 1: Access Google AI Studio

1. Navigate to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google Account credentials

### Step 2: Create API Key

1. Click on the "Get API Key" button (usually at the top-right corner)
2. Review and accept the terms of service
3. Choose to create the API key in an existing Google Cloud project or create a new one
4. Once generated, copy your API key immediately
5. **Important**: Store your API key securely - you won't be able to view it again after closing the dialog

### Step 3: Store API Key Securely

**Never commit API keys to version control!** Use one of these secure storage methods:

#### Option 1: macOS Keychain (Recommended for this project)

Store your API key in macOS Keychain using the `security` command:

```bash
security add-generic-password \
  -a "production" \
  -s "GEMINI_API_KEY" \
  -w "your_api_key_here"
```

Retrieve it when needed:

```bash
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

#### Option 2: Environment Variables (Development)

**macOS/Linux (Bash):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export GEMINI_API_KEY='your-api-key-here'
```

**macOS/Linux (Fish):**
```fish
# Add to ~/.config/fish/config.fish
set -gx GEMINI_API_KEY 'your-api-key-here'
```

**Windows (PowerShell):**
```powershell
# Add to PowerShell profile
$env:GEMINI_API_KEY = 'your-api-key-here'
```

#### Option 3: .env File (Local Development)

Create a `.env` file in your project root:

```bash
GEMINI_API_KEY=your-api-key-here
```

Then load it in your shell:

```bash
export $(cat .env | xargs)
```

**Important**: Add `.env` to your `.gitignore` file to prevent committing API keys.

## Pricing

### Google Maps Grounding Pricing

When you use Grounding with Google Maps, your project is billed per API request that successfully returns at least one Google Maps grounded result.

**Key Points:**
- **Pricing**: $25 per 1,000 grounded prompts
- **Free Tier**: Up to 500 requests per day available
- **Billing**: A request is only counted towards the quota when a prompt successfully returns at least one Google Maps grounded result (i.e., results containing at least one Google Maps source)
- **Multiple Queries**: If multiple queries are sent to Google Maps from a single request, it counts as one request towards the rate limit
- **Separate from Model Pricing**: Pricing is separate from the base model pricing

### Model Pricing

Google Maps Grounding works with the following models, each with their own pricing:

#### Supported Models

- **Gemini 2.5 Pro**: Higher quality, more capable
- **Gemini 2.5 Flash**: Fast and efficient (default for this tool)
- **Gemini 2.5 Flash-Lite**: Lightweight version
- **Gemini 2.0 Flash**: Fast and efficient

**Note**: Gemini 2.0 Flash Lite does NOT support Google Maps Grounding.

### Cost Calculation Example

**Example Scenario:**
- You make 100 API requests with Google Maps grounding enabled
- Each request uses `gemini-2.5-flash`
- 80 requests successfully return Google Maps grounded results
- 20 requests do not return any Google Maps results

**Billing:**
- You are billed for 80 uses of the Google Maps tool (only successful grounded results count)
- Cost: 80 ÷ 1,000 × $25 = **$2.00** for Google Maps grounding
- You are also billed for the model usage (input/output tokens) at the standard Gemini 2.5 Flash rates
- Multiple queries within a single request do not multiply the tool usage cost

### Free Tier

The free tier provides up to 500 requests per day for Google Maps Grounding. A request is only counted when it successfully returns at least one Google Maps grounded result.

**Important**: Check the [Gemini API pricing page](https://ai.google.dev/gemini-api/docs/pricing) for current free tier information and limits, as these may change over time.

### Monitoring Usage

1. **Google Cloud Console**: Monitor your API usage in the [Google Cloud Console](https://console.cloud.google.com/)
2. **Billing Dashboard**: Set up billing alerts to track costs
3. **API Quotas**: Check your API quotas and limits in the API dashboard

### Best Practices for Cost Management

1. **Use Flash by Default**: Gemini 2.5 Flash is the default model and is more cost-effective for most queries
2. **Monitor Usage**: Regularly check your API usage and costs
3. **Set Budget Alerts**: Configure billing alerts in Google Cloud Console
4. **Optimize Queries**: Use clear, specific prompts with geographical context to ensure successful grounding
5. **Toggle When Needed**: Only enable Google Maps grounding when queries have clear geographical context
6. **Free Tier**: Take advantage of the free tier (500 requests/day) for development and testing

## Rate Limits

Google Maps Grounding is subject to the same rate limits as the Gemini API:

- **Requests per minute**: Varies by model and tier
- **Tokens per minute**: Varies by model and tier
- **Daily quotas**: May apply based on your account type

**Note**: The quota for Google Maps Grounding typically aligns with the underlying Gemini model rate limits.

Check the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/quota) for current rate limits.

## Troubleshooting

### API Key Issues

**Error: "GEMINI_API_KEY environment variable is required"**

Solution:
1. Verify the API key is set: `echo $GEMINI_API_KEY`
2. If using macOS Keychain, retrieve it: `export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)`
3. Verify the key is valid by testing with a simple API call

**Error: "API key not valid"**

Solution:
1. Verify you copied the full API key
2. Check for extra spaces or newlines
3. Generate a new API key if needed
4. Ensure you're using the correct API key for your project

### Billing Issues

**Unexpected charges:**

1. Check your API usage in Google Cloud Console
2. Review billing breakdown by service
3. Verify you're not making excessive API calls
4. Check if free tier credits have been exhausted
5. Remember: Only requests with successful Google Maps grounded results are billed

**Quota exceeded:**

1. Check your current usage against quotas
2. Request quota increase if needed
3. Implement rate limiting in your application
4. Consider upgrading your account tier

### Location Format Issues

**Error: "Invalid lat-lon format"**

Solution:
1. Ensure format is exactly `lat,lon` (e.g., `37.78193,-122.40476`)
2. Verify latitude is between -90 and 90
3. Verify longitude is between -180 and 180
4. Check for extra spaces or incorrect separators

## Additional Resources

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Maps Grounding Documentation](https://ai.google.dev/gemini-api/docs/maps-grounding)
- [Google Cloud Console](https://console.cloud.google.com/)

## Quick Reference

**API Key Setup:**
```bash
# Store in macOS Keychain
security add-generic-password -a "production" -s "GEMINI_API_KEY" -w "your_key"

# Retrieve
export GEMINI_API_KEY=$(security find-generic-password -a "production" -s "GEMINI_API_KEY" -w)
```

**Pricing:**
- **Google Maps Grounding**: $25 per 1,000 grounded prompts
- **Free Tier**: Up to 500 requests per day
- **Billing**: Only successful grounded results count towards quota

**Supported Models:**
- Gemini 2.5 Pro
- Gemini 2.5 Flash (default)
- Gemini 2.5 Flash-Lite
- Gemini 2.0 Flash

**Useful Links:**
- [Get API Key](https://aistudio.google.com/app/apikey)
- [View Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Monitor Usage](https://console.cloud.google.com/)
- [Maps Grounding Docs](https://ai.google.dev/gemini-api/docs/maps-grounding)

