"""
Title: Test Clip.

Date: May 27, 2024; 7:22 PM

Author: Ujjawal K. Panchal & Ajinkya Chaudhari & Isha S. Joglekar
"""
import requests
from PIL import Image
from datasets import load_dataset
from transformers import AutoProcessor, AutoModelForCausalLM

import projconfig

checkpoint = "microsoft/git-base"
device = "cuda:0"

processor = AutoProcessor.from_pretrained(checkpoint, cache_dir = projconfig.modelstore)
model = AutoModelForCausalLM.from_pretrained(checkpoint, cache_dir = projconfig.modelstore).to(device)

def transforms(example_batch):
    images = [x for x in example_batch["image"]]
    captions = [x for x in example_batch["text"]]
    inputs = processor(images=images, text=captions, padding="max_length")
    inputs.update({"labels": inputs["input_ids"]})
    return inputs

if __name__ == "__main__":
    #1. evaluate.
    sample_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Ravivarmapress.jpg/800px-Ravivarmapress.jpg"
    image = Image.open(requests.get(sample_url, stream=True).raw)
    inputs = processor(images=image, return_tensors="pt").to(device)
    pixel_values = inputs.pixel_values
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_caption)