import random
import time
import uuid
from datetime import datetime, timedelta
import faker
import json
import regex as re
import pandas as pd
from match_persona_to_behaviour import *



class ECOM:

  fake = faker.Faker()

  def __init__(self):
    self.products_catalog = self.generate_product_catalog()
    self.last_session_time = ""


  def user_data(self):
    user_id = ("USR-" + uuid.uuid4().hex)
    gender = random.choice(["M", "F"])
    first_name = self.fake.first_name_male() if gender == "M" else self.fake.first_name_female()
    last_name = self.fake.last_name()
    user_name = f"{first_name} {last_name}"
    user_type = "New" if self.last_session_time == "" else "Returning"
    age_group = random.choices(["12-17", "18-25", "26-35", "36-45", "46-55", "56-65", "65+"], weights=[1, 3, 6, 5, 3, 1, 1], k=1)[0]
    address = self.fake.address()
    city_fn = lambda address: address.split("\n")[-1].split(",")[0] if len(address.split("\n")) > 1 else "Unknown City"
    state_fn = lambda address: re.search(r",\s([A-Z]{2})\s\d{5}", address).group(1) if re.search(r",\s([A-Z]{2})\s\d{5}", address) else "Unknown State"
    city = city_fn(address)
    state = state_fn(address)
    zipcode = address.split(" ")[-1]
    country = "USA"
    # session_date = datetime.strptime(self.last_session_time, "%Y-%m-%d %H:%M:%S")
    account_creation_date = self.fake.date_between(start_date="-3y", end_date=datetime.now()) - timedelta(days=random.randint(0, 10)) if self.last_session_time == "" else self.fake.date_between(start_date="-3y", end_date=datetime.strptime(self.last_session_time, "%Y-%m-%d %H:%M:%S"))
    last_login_time =  account_creation_date if self.last_session_time == "" else datetime.strptime(self.last_session_time, "%Y-%m-%d %H:%M:%S")

    preferred_language = random.choice(["English", "Spanish", "French", "German", "Italian"])
    personas = random.choice(['Bargain Hunter', 'Impulse Buyer', 'Brand Loyalist', 'Casual Browser', 'Window Shopper', 'Deal Seeker', 'Last-Minute Shopper',
                              'Mobile Shopper', 'Researcher', 'Subscription Shopper', 'Loyal Customer', 'Abandoner', 'Gift Buyer',
                              'Bulk Buyer', 'Eco-Conscious Shopper'])

    output = [
        {   "user_id" : user_id,
            "first_name" : first_name,
            "last_name" : last_name,
            "user_name" : user_name,
            "user_type" : user_type,
            "age_group" : age_group,
            "gender": gender,
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country,
            "account_creation_date": account_creation_date.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login_time": last_login_time.strftime("%Y-%m-%d %H:%M:%S"),
            "preferred_language": preferred_language,
            "persona": personas
        }
    ]
    return output


  def session_time(self, user):
    session_start_time = datetime.strptime(self.last_session_time or user['last_login_time'], "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(0, random.randint(0,5) if not self.last_session_time else random.randint(0,2)))
    session_end_time = session_start_time + timedelta(minutes=random.randint(0, 30))
    return [session_start_time, session_end_time]


  def session_data(self, user, session_start_time, session_end_time):
    session_id = ("SES-" + uuid.uuid4().hex)
    user_id = user["user_id"]
    device_types = random.choice(["Smartphone", "Laptop", "Tablet", "Smartwatch", "Smart TV", "Gaming Console", "Voice Assistant"])
    browser_types = random.choices(["Google Chrome", "Mozilla Firefox", "Apple Safari", "Microsoft Edge", "Opera", "Internet Explorer", "Brave", "Vivaldi", "Microsoft Edge (Chromium-based)", "Samsung Internet"],
                                   weights=[7, 5, 6, 2, 1, 1, 1, 1, 1, 4], k=1)
    session_start_time = session_start_time
    session_end_time = session_end_time
    browsing_duration = (session_end_time - session_start_time).total_seconds()
    self.last_session_time = session_end_time.strftime("%Y-%m-%d %H:%M:%S")
    user['last_login_time'] = self.last_session_time

    session_output = [
        {
            "user_id": user_id,
            "session_id": session_id,
            "device_type": device_types,
            "browser_type": browser_types[0],
            "session_start_time": session_start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "session_end_time": session_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "browsing_duration": browsing_duration
        }
    ]
    return session_output


  def marketing_data(self, user):
    user_id = user['user_id']
    ad_campaign_id = "CAM-" + uuid.uuid4().hex
    referral_source = random.choice(["Direct", "Organic Search", "Paid Ads", "Social", "Email"])
    # num_email_clicks = random.randint(0, 50)  # Random clicks from promotional emails
    # num_social_shares = random.randint(0, 20)  # Random number of social shares
    utm_source = random.choice(["Google", "Facebook", "Instagram", "Twitter", "LinkedIn", "Pinterest"])
    utm_medium = random.choice(["CPC", "Organic", "Referral"])
    utm_campaign = random.choice(["Summer Sale", "Black Friday", "Holiday Discounts", "Flash Sale", "New Arrivals"])
    discount_code_used = random.choice([True, False])  # Randomly decide if a discount code was used

    marketing_attribution_data = [
        {
        "user_id": user_id,
        "ad_campaign_id": ad_campaign_id,
        "referral_source": referral_source,
        # "num_email_clicks": num_email_clicks,
        # "num_social_shares": num_social_shares,
        "utm_source": utm_source,
        "utm_medium": utm_medium,
        "utm_campaign": utm_campaign,
        "discount_code_used": discount_code_used
        }
    ]
    return marketing_attribution_data


  def generate_product_catalog(self):
    """Load product catalog from CSV file while preserving actual prices."""
    df = pd.read_csv("./product_catalog.csv")

    # Convert actual_price from ₹475 format to integer (475)
    df["discounted_price"] = (df["discounted_price"].astype(str).str.replace(r"[^\d]", "", regex=True).astype(int))/85.79
    df["actual_price"] = (df["actual_price"].astype(str).str.replace(r"[^\d]", "", regex=True).astype(int))/85.79

    # Convert to list of dictionaries
    products = df[['product_id', 'product_name', 'category', 'actual_price', 'discounted_price']].to_dict(orient='records')
    return products


  def generate_order_products(self, order_id, num_items_in_order):
    """Generate realistic order products without modifying prices."""
    selected_products = random.choices(self.products_catalog, k=num_items_in_order)  # Allow duplicates

    order_products = []
    total_value = 0

    for product in selected_products:
        quantity = random.randint(1, 3)  # Random quantity between 1 and 3
        total_price = product["discounted_price"] * quantity
        total_value += total_price  # Track total order value

        order_products.append({
            "order_id": order_id,
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "actual_price": product["actual_price"],
            "discounted_price": product["discounted_price"],  # Keep the original price
            "quantity": quantity,
            "total_price": total_price
        })

    return order_products, total_value


  def order_data(self, user, session, marketing):
    user_id = user['user_id']
    session_id = session['session_id']
    order_id = "ORD-" + uuid.uuid4().hex
    persona = user.get("persona", "Default Persona")
    address = user.get("address", "Unknown Address")
    if persona == 'Abandoner':
      order_status = "Abandoned"
    else:
      order_status = random.choices(
        ["Completed", "Abandoned", "Failed", "Pending", "Processing", "Canceled"],
        weights=[10, 15, 1, 1, 3, 3], k=1
      )[0]

    num_items_in_order = random.randint(1, 5)

    # Generate realistic product details
    order_products, order_total_value = self.generate_order_products(order_id, num_items_in_order)

    payment_method = random.choice(["Credit Card", "PayPal", "Wallet", "Debit Card", "Bank Transfer"])

    if order_status == 'Abandoned':
      payment_status = "Abandoned"
    elif order_status == 'Pending':
      payment_status = "Pending"
    elif order_status == 'Processing':
      payment_status = "Processing"
    else:
      payment_status = random.choices(
          ["Successful", "Refunded", "Abandoned", "Failed"],
          weights=[10, 2, 6, 1], k=1
        )[0]

    promo_discount_applied = round(random.uniform(0.0, order_total_value * 0.2), 2) if marketing['discount_code_used'] else 0.0

    # Ensure discounted order value is non-negative
    final_order_value = max(0, order_total_value - promo_discount_applied)

    # Order timestamps
    session_start = datetime.strptime(session['session_start_time'], "%Y-%m-%d %H:%M:%S")
    session_end = datetime.strptime(session['session_end_time'], "%Y-%m-%d %H:%M:%S")
    order_created_time = session_start + timedelta(seconds=random.randint(0, int((session_end - session_start).total_seconds() * 0.8)))

    order_completed_time = None
    if order_status in ["Completed", "Canceled"]:
        max_completion_delay = max(1, int((session_end - order_created_time).total_seconds()))
        order_completed_time = order_created_time + timedelta(seconds=random.randint(1, max_completion_delay))

    # Shipping & billing address variations
    if order_status in ["Completed", "Canceled"]:
        shipping_address = self.fake.address() if random.randint(0, 999) < 20 else address
        billing_address = self.fake.address() if random.randint(0, 1999) == 0 else address
    else:
        shipping_address = address
        billing_address = address

    return {
        "user_id": user_id,
        "session_id": session_id,
        "order_id": order_id,
        "order_status": order_status,
        "num_items_in_order": num_items_in_order,
        "order_total_value": round(final_order_value, 2),
        "payment_method": payment_method,
        "payment_status": payment_status,
        "promo_discount_applied": promo_discount_applied,
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "order_created_time": order_created_time.strftime("%Y-%m-%d %H:%M:%S"),
        "order_completed_time": order_completed_time.strftime("%Y-%m-%d %H:%M:%S") if order_completed_time else None,
        "order_products": order_products
    }


  def behaviour_data(self, user, order, session):
    user_id = order['user_id']
    session_id = session['session_id']
    tracking_id = "TRK-" + uuid.uuid4().hex
    persona = user.get("persona", "Default Persona")
    order_status = order.get('order_status', 'Unknown Status')
    payment_status = order.get('payment_status', 'Unknown Status')
    # Convert session start and end times to datetime objects
    session_start_time = datetime.strptime(session['session_start_time'], "%Y-%m-%d %H:%M:%S")
    session_end_time = datetime.strptime(session['session_end_time'], "%Y-%m-%d %H:%M:%S")
    # Format the session start and end times using strftime
    session_start_time_str = session_start_time.strftime("%Y-%m-%d %H:%M:%S")
    session_end_time_str = session_end_time.strftime("%Y-%m-%d %H:%M:%S")
    # Handle order completed time
    order_completed_time = None if order['order_completed_time'] is None else datetime.strptime(order['order_completed_time'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    # Call the match_persona_to_behavior function
    behavior = match_persona_to_behavior(persona, order_status, payment_status, session_start_time_str, session_end_time_str, order_completed_time)
    # Add user_id, session_id, and tracking_id to the behavior
    behavior['user_id'] = user_id
    behavior['session_id'] = session_id
    behavior['tracking_id'] = tracking_id
    if order['order_status'] == 'Abandoned' or order['order_status'] == 'Failed':
      behavior['payment_processing_time'] = 0.0
      return behavior
    return behavior


