import os
import time
import jwt
import requests
import base64
from dotenv import load_dotenv

# 1. This line pulls the keys from your .env file
load_dotenv()

AK = os.getenv("KLING_ACCESS_KEY")
SK = os.getenv("KLING_SECRET_KEY")

def generate_token(ak, sk):
    headers = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800, # Valid for 30 mins
        "nbf": int(time.time()) - 5
    }
    return jwt.encode(payload, sk, headers=headers)

def start_i2v(image_path, prompt):
    # Convert your caricature image to Base64
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')

    token = generate_token(AK, SK)
    url = "https://api.klingai.com/v1/videos/image2video"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    data = {
        "model": "kling-v1-6", 
        "image": img_data,
        "prompt": prompt,
        "duration": 5
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    # Put your caricature image in the same folder and name it here
    result = start_i2v("my_caricature.png", "A slow cinematic zoom, character blinks and smiles.")
    print(result)