import os, time, jwt, requests, base64, sys
from dotenv import load_dotenv

load_dotenv()
AK, SK = os.getenv("KLING_ACCESS_KEY"), os.getenv("KLING_SECRET_KEY")

def generate_token(ak, sk):
    payload = {"iss": ak, "exp": int(time.time()) + 1800, "nbf": int(time.time()) - 5}
    return jwt.encode(payload, sk, headers={"alg": "HS256", "typ": "JWT"})

def start_i2v(image_path, prompt):
    with open(image_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode('utf-8')
    token = generate_token(AK, SK)
    url = "https://api.klingai.com/v1/videos/image2video"
    data = {"model": "kling-v1-6", "image": img_data, "prompt": prompt, "duration": 5}
    response = requests.post(url, headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}, json=data)
    return response.json()

if __name__ == "__main__":
    # Pulls image and prompt from the GitHub "Run" button
    img = sys.argv[1] if len(sys.argv) > 1 else "caricature.png"
    prmt = sys.argv[2] if len(sys.argv) > 2 else "Smile and blink"
    print(f"Starting task for {img}...")
    print(start_i2v(img, prmt))