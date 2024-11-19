from src.fireworks_interface import FireworkInterface, encode_image
from src.prompts import extract_data
from tqdm import trange, tqdm
from src.helpers import extract_json
from src.types import DriversLicense, Passport
from dotenv import load_dotenv
from PIL import Image
import base64
import os
from io import BytesIO

load_dotenv()

images = []
for file in os.listdir('./data/id-docs'):
    print(file)
    # Open and process the image using Pillow
    with Image.open(f'./data/id-docs/{file}') as img:
        # Convert to RGB if image is in RGBA format
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Save image to bytes buffer
        buffer = BytesIO()
        img.save(buffer, format='JPEG')

        # Base64 encode the image bytes
        img_bytes = base64.b64encode(buffer.getvalue()).decode('utf-8')
        images.append(img_bytes)

with open("models.txt") as f:
    fireworks_models = f.read().split('\n')

fireworks_models = [
    m.lower().replace(' ', '-').replace('.', 'p')
    for m in fireworks_models
]

print(fireworks_models)

num_success = dict()
for model in fireworks_models:
    num_success[model] = 0

num_attempts = num_success.copy()

fireworks = FireworkInterface()

for i in trange(5):
    for model in tqdm(fireworks_models):
        for image in images:
            response = fireworks.call_fireworks(extract_data, model=model, image_encoding=image)
            num_attempts[model] += 1
            try:
                print(response)
                json_out = extract_json(response)
                print(json_out)
                id_type = DriversLicense if json_out['type'] else Passport
                data = id_type(**json_out['data'])
                num_success[model] += 1
            except Exception as e:
                print(e)


