import requests

# def get_promo_data(user_id):
#     try:
#         response = requests.get(f"https://a0ae-34-90-248-11.ngrok-free.app?user_id={user_id}", timeout=5)
#         response.raise_for_status()
#         return response.json()
#     except requests.RequestException as e:
#         print(f"⚠️ Failed to fetch promo data: {e}")
#         return {"discount": 0, "message": "No promo"}
    


response = requests.get("https://a0ae-34-90-248-11.ngrok-free.app/promotions")
print(response.json())

