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
"preference": ["openai", "azure_openai", "bedrock_claude"]
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[License decision pending]
