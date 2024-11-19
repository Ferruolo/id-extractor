from src.fireworks_interface import FireworkInterface, encode_image
import os

images = []
for file in os.listdir('./data/id-docs'):
    with open(f'./data/id-docs/{file}', 'rb') as f:
        images.append(f.read())

with open("models.txt") as f:
    fireworks_models = f.read().split('\n')






