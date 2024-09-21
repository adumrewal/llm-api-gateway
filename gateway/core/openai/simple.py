from openai import OpenAI, NotGiven

OPENAI_API_KEY = ""



client = OpenAI(api_key=OPENAI_API_KEY)

def api_call(model_name, system_prompt, user_prompt, json_response=False, temperature=0):
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
