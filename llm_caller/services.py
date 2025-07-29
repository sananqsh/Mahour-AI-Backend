from openai import OpenAI
from django.conf import settings

api_url=settings.OPENAI_API_URL
api_key = settings.OPENAI_API_KEY
client = OpenAI(base_url='https://api.gapgpt.app/v1', api_key=api_key)

def call_llm(user_prompt: str, prompt_template: str | None = None):
    """
    Formats the user_prompt using prompt_template (or settings.PROMPT_TEMPLATE)
    and calls the OpenAI ChatCompletion API. Returns the assistant's reply.
    """
    try:
        template = prompt_template or settings.PROMPT_TEMPLATE
        final_prompt = template.format(user_prompt=user_prompt)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.7,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
