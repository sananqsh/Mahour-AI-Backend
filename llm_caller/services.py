from openai import OpenAI
from django.conf import settings

api_url=settings.OPENAI_API_URL
api_key = settings.OPENAI_API_KEY
client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=api_key)

def call_llm(
    user_prompt: str,
    prompt_template: str | None = None,
    history: list[dict] | None = None,
    context: str | None = None,
):
    """
    Formats user prompt with prompt_template alongside history and context
    and calls the OpenAI ChatCompletion API. Returns the assistant's reply.
    """
    try:
        messages = []
        messages = add_context(messages, context)
        messages = messages + history

        user_prompt = formatted_user_prompt(user_prompt, prompt_template)
        messages.append({"role": "user", "message": user_prompt})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)

def formatted_user_prompt(user_prompt, prompt_template: str | None = None):
    if prompt_template is None:
        return user_prompt

    return prompt_template.format(user_prompt=user_prompt)

def add_context(messages, context):
    return messages + [{"role": "system", "content": context}]
