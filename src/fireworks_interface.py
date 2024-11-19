import os
from fireworks.client import Fireworks


def call_fireworks(prompt: str, model='llama-v3p1-8b-instruct'):
    client = Fireworks(api_key=os.environ.get("FIREWORKS_API_KEY"))
    response = client.chat.completions.create(
        model=f"accounts/fireworks/models/{model}",
        messages=[{
            "role": "user",
            "content": "Say this is a test",
        }],
    )
    return response




