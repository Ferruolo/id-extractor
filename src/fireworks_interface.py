import os
from helpers import retry_with_backoff
from fireworks.client import Fireworks
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class FireworkInterface:
    def __init__(self):
        self.client = Fireworks(api_key=os.environ.get("FIREWORKS_API_KEY"))

    # Need to add back off incase API is too busy,
    # Happens all the time with Claude API
    @retry_with_backoff()
    def _fireworks_retry_call(self, model, prompt_content):
        return self.client.chat.completions.create(
            model=f"accounts/fireworks/models/{model}",
            messages=prompt_content
        )

    def call_fireworks(self, prompt: str, model='llama-v3p1-8b-instruct', image_path=None, image_encoding=None):
        prompt_contents = [{
            "role": "user",
            "content": prompt,
        }]

        # Todo: Fix duplicates
        if image_path:
            prompt_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(image_path)}"
                }
            })

        if image_encoding:
            prompt_contents.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_encoding}"
                }
            })

        return self._fireworks_retry_call(model, prompt_contents).choices[0].message.content
