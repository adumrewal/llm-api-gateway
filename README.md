# Heimdall - Your AI Gateway Service

Heimdall is an AI Gateway Service that provides a unified interface for interacting with various LLM models from different providers.

## Features

- Support for multiple AI providers:
  - OpenAI
  - Azure OpenAI
  - AWS Bedrock (Anthropic Claude)
- Flexible routing based on provider preferences
- JSON response support
- Configurable model parameters (temperature, max tokens, etc.)
- FastAPI-based REST API
- Docker support for easy deployment

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/adumrewal/llm-api-gateway.git
   cd llm-api-gateway
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI API version
- `AZURE_OPENAI_API_ENDPOINT`: Azure OpenAI API endpoint
- `AWS_BEDROCK_SERVICE_NAME`: AWS Bedrock service name (default: "bedrock-runtime")
- `AWS_BEDROCK_ACCESS_KEY_ID`: AWS access key ID for Bedrock
- `AWS_BEDROCK_SECRET_ACCESS_KEY`: AWS secret access key for Bedrock
- `AWS_BEDROCK_REGION`: AWS region for Bedrock (default: "us-east-1")

## Usage

### Running locally

```
pip install -r requirements.txt
uvicorn heimdall.contract:app --reload --port 16000
```

The API will be available at `http://localhost:16000`.

### Running with Docker

1. Build the Docker image:

   ```
   docker build -t heimdall:latest .
   ```

2. Run the container:
   ```
   docker-compose up
   ```

The API will be available at `http://localhost:16000`.

## API Endpoints

### API Documentation

For a comprehensive overview of the API, including the FastAPI contract and all available endpoints, visit:

http://localhost:16000/docs#/

This interactive Swagger UI documentation provides:

- Detailed descriptions of all API endpoints
- Request and response schemas
- The ability to test API endpoints directly from your browser

Exploring this documentation will give you a clear understanding of the API's capabilities and how to interact with it effectively.

### Example: POST /base/model_call

Make a call to an AI model.

Request body:

```json
{
  "name_model": "gpt-3.5-turbo",
  "system_prompt": "The system prompt to use for the API call",
  "user_prompt": "The user prompt to use for the API call",
  "json_response": false,
  "temperature": 0,
  "max_tokens": 2000,
  "preference": ["gpt-3.5-turbo", "anthropic.claude-3-5-sonnet-20240620-v1:0", "azure-gpt-4-turbo"]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[License decision pending]

## To-do

- Planning to develop v1 in 3 phases:

  - ✅ Phase 0: Basic structure with 2-3 providers.
  - ✅ Phase 1: Correct fallback mechanism.
    - ✅ Currently fallback is at provider level. Need to add fallback at model level.
  - [ ] Phase 2: Configs for fall back via UI. Logging.
    - 🟨 UI portal where users can add delete models.
    - UI portal where users can manage their configs for fall back.
    - User can select one model and then define fall back models for it.
    - Need to add logging for each API call. Logging includes request, response, latencies, tokens used, etc.
  - [ ] Phase 3: System prompt management from UI. Usecase ID based auto configs.
    - Users can define usecases.
    - Each usecase can have system prompt, model, temperature, max tokens.
    - On each API call, user will specify usecase, and based on that we will auto configure the model, system prompt, temperature, max tokens.
    - Fallback will be managed automatically. If a provider fails, we will try next model in the list.

- Would love contributions for:

  - Add support for streaming responses
  - Add support for webhooks
  - Add support for caching
  - Add support for db integration
  - Add support for rate limiting
  - Add support for content moderation
  - Add support for automatic provider selection

- Would love to get feedback on:

  - What are your favorite usecases of AI Gateways?
  - What are your favorite features in other AI Gateways?
  - What can we do better than others?
  - Any suggestions/open issues/bugs?
