from openai import AzureOpenAI, NotGiven

AZURE_OPENAI_API_KEY = ""
AZURE_OPENAI_API_VERSION = ""
AZURE_OPENAI_API_ENDPOINT = "https://project-name.openai.azure.com/"

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_API_ENDPOINT,
)


def api_call(
    model_name, system_prompt, user_prompt, json_response=False, temperature=0
):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        response_format={"type": "json_object"} if json_response else NotGiven,
    )
    return response.choices[0].message.content
