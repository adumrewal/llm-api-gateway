import json
import boto3

from gateway.typing import BaseClient


BASE_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"
AWS_SERVICE_NAME = "bedrock-runtime"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_BEDROCK_REGION = "us-east-1"


# Utility functions
def get_assistant_msg(text: str) -> dict:
    return {
        "role": "assistant",
        "content": [{"type": "text", "text": text}],
    }


def get_user_msg(text: str) -> dict:
    return {
        "role": "user",
        "content": [{"type": "text", "text": text}],
    }


# Client Class
class BedrockClaudeClient(BaseClient):
    def __init__(self):
        self.client = boto3.client(
            service_name=AWS_SERVICE_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_BEDROCK_REGION,
        )

    def api_call(
        self,
        model_name: str,
        system_prompt: str,
        user_prompt: str,
        json_response: bool = False,
        temperature: float = 0,
        max_tokens: int = 2000,
    ) -> str:
        msgs = [get_user_msg(user_prompt)]
        if json_response:
            msgs.append(get_assistant_msg("Here is the JSON requested:\n{"))

        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": msgs,
        }

        request = json.dumps(native_request)
        response = self.client.invoke_model(modelId=model_name, body=request)

        model_response = json.loads(response["body"].read())
        answer = model_response["content"][0]["text"]

        if not json_response:
            return answer

        response_text = "{" + answer
        try:
            _ = json.loads(response_text)
            return response_text
        except Exception as e:
            print(
                f"ERROR: Can't parse response JSON. Reason: {e}. Response text: {response_text}"
            )
            raise e
