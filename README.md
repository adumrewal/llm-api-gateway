# LLM API Gateway

## Current state of repository
This is still in development. As of now you can find the codes for the following:
- Making a simple request to OpenAI API
- Making a simple request to Azure OpenAI API
- Making a simple request to AWS Bedrock Claude API

# Actual Objective
## Overview
The LLM API Gateway is a middleware service designed to manage and route requests to various language model APIs. It provides a unified interface for interacting with multiple language models, ensuring scalability, security, and ease of use.

## Features
- **Unified API Interface**: Interact with multiple language models through a single API.
- **Scalability**: Efficiently manage and route requests to handle high traffic.
- **Security**: Secure API endpoints with authentication and rate limiting.
- **Logging and Monitoring**: Integrated logging and monitoring for better observability.

## Installation
To install the dependencies, run:
```bash
pip install -r requirements.txt
```

## Configuration
Configuration options can be set in the `config.json` file. Example:
```json
{
    "apiKeys": {
        "model1": "your-api-key-here",
        "model2": "your-api-key-here"
    },
    "rateLimit": {
        "windowMs": 60000,
        "max": 100
    }
}
```

## API Endpoints
- `POST /api/v1/query`: Query a language model.
    - **Request Body**:
        ```json
        {
            "model": "model1",
            "input": "Your input text here"
        }
        ```
    - **Response**:
        ```json
        {
            "output": "Model response here"
        }
        ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries, please contact [amoldumrewal@gmail.com](mailto:amoldumrewal@gmail.com).