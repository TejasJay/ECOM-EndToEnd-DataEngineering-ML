# im running it in google colab EXTERNALLY

from pyngrok import conf
import os
from dotenv import load_dotenv
from pyngrok import conf


load_dotenv(".env")

conf.get_default().auth_token = os.environ["NGROK_AUTH_TOKEN"]

from fastapi import FastAPI
from datetime import datetime, timedelta
import random
import uvicorn
import nest_asyncio
from pyngrok import ngrok

# Allow Colab's notebook loop to run Uvicorn
nest_asyncio.apply()

app = FastAPI()

# Sample promo types
promo_types = ["percentage", "fixed", "bogo"]

@app.get("/promotions")
def get_promotions():
    promos = []
    for _ in range(5):  # generate 5 promo records
        discount = random.choice([5, 10, 15, 20])
        promo = {
            "promo_id": f"PROMO{random.randint(1000, 9999)}",
            "type": random.choice(promo_types),
            "discount": discount,
            "category": random.choice(["electronics", "fashion", "groceries"]),
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=random.randint(3, 10))).isoformat()
        }
        promos.append(promo)
    return {"promotions": promos}


# Expose port 8000
public_url = ngrok.connect(8000)
print(f"🚀 Public API is live at: {public_url}/promotions")

# Run the API
uvicorn.run(app, host="0.0.0.0", port=8000)