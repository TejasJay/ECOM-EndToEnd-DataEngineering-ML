import requests
from time import sleep
import random
import json

def get_promo_data():
    try:
        response = requests.get("https://126a-35-204-82-160.ngrok-free.app/promotions", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch promo data: {e}")
        return {"discount": 0, "message": "No promo"}
    

while True:
    sleep(random.randint(10, 100))
    response = get_promo_data()
    print(response)

