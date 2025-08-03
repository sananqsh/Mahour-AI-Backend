from openai import OpenAI
from django.conf import settings

api_url=settings.OPENAI_API_URL
api_key = settings.OPENAI_API_KEY
client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=api_key)

def call_llm(
    user_prompt: str,
    prompt_template: str | None = None,
    history: list[dict] | None = None,
    user_context: dict | None = None,
):
    """
    Formats the user_prompt using prompt_template (or settings.PROMPT_TEMPLATE)
    and calls the OpenAI ChatCompletion API. Returns the assistant's reply.
    """
    try:
        if prompt_template:
            user_prompt = prompt_template.format(user_prompt=user_prompt)

        messages = []
        messages = add_initial_context(messages)
        messages = messages + history
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

def add_initial_context(messages: list[dict]):
    return add_context(
        messages,
        settings.INITIAL_LLM_CONTEXT,
    )

def add_context(messages, context):
    return messages + [{"role": "system", "content": context}]
