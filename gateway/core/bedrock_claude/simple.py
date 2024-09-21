import json
import boto3

BASE_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"
AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
AWS_BEDROCK_REGION = "us-east-1"

claude_client = boto3.client(
    "bedrock-runtime",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_BEDROCK_REGION,
)


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


def api_call(
    system_prompt: str,
    user_prompt: str,
    model_id: str = BASE_MODEL,
    json_response: bool = False,
    temperature: int = 0,
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
    response = claude_client.invoke_model(modelId=model_id, body=request)

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
