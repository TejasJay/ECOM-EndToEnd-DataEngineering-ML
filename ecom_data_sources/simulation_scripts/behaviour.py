from datetime import datetime
import random

def is_within_session_time(session_start_time, session_end_time, action_time):
    """Check if the action time is within the session window."""
    session_start = datetime.strptime(session_start_time, "%Y-%m-%d %H:%M:%S")
    session_end = datetime.strptime(session_end_time, "%Y-%m-%d %H:%M:%S")
    action_time = datetime.strptime(action_time, "%Y-%m-%d %H:%M:%S")
    return session_start <= action_time <= session_end

def get_session_duration(session_start_time, session_end_time):
    """Calculate the session duration in seconds."""
    session_start = datetime.strptime(session_start_time, "%Y-%m-%d %H:%M:%S")
    session_end = datetime.strptime(session_end_time, "%Y-%m-%d %H:%M:%S")
    duration = (session_end - session_start).total_seconds()
    return duration


def adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time):
    # Total duration of behavior (sum the times, considering None or 0 as 0)
    behaviour_duration = (mouse_hover_time or 0) + (scroll_depth or 0) + (cart_view_time or 0) + (checkout_completion_time or 0) + (payment_processing_time or 0)
    
    # Check if behaviour_duration is greater than 0 to avoid divide-by-zero errors
    if behaviour_duration == 0:
        return [0, 0, 0, 0, 0]  # If no valid behavior times, return zeroed times
    
    # If the total behavior time exceeds the session duration, scale it down
    if behaviour_duration > session_duration:
        scale_factor = session_duration / behaviour_duration
        
        # Apply the scale factor to each component, making sure None or 0 values are handled
        mouse_hover_time *= scale_factor
        scroll_depth *= scale_factor
        cart_view_time *= scale_factor
        checkout_completion_time = (checkout_completion_time) * scale_factor
        payment_processing_time = (payment_processing_time) * scale_factor

        return [round(mouse_hover_time, 2), round(scroll_depth, 2), round(cart_view_time, 2),  round(checkout_completion_time, 2), round(payment_processing_time, 2)]
    
    # If no scaling is needed, return the original times
    return [round(mouse_hover_time, 2), round(scroll_depth, 2), round(cart_view_time, 2),  round(checkout_completion_time , 2), round(payment_processing_time, 2)]



def bargain_hunter_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Bargain Hunter: Compares products, spends time checking prices, and looks for discounts."""
    
    # Get session duration
    session_duration = get_session_duration(session_start_time, session_end_time)
    
    # Initial time values
    mouse_hover_time = round(random.uniform(5.0, 30.0), 2)
    scroll_depth = round(random.uniform(40.0, 100.0), 2)
    cart_view_time = round(random.uniform(30.0, 600.0), 2)
    num_clicks_before_purchase = random.randint(10, 30)
    
    # Checkout and payment times
    checkout_completion_time =  round(random.uniform(60.0, 900.0), 2)
    payment_processing_time =  round(random.uniform(2.0, 15.0), 2)  
    
    # Adjust times to fit within the session duration
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }




def impulse_buyer_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Impulse Buyer: Quickly makes purchase decisions with minimal browsing."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    
    # Initial time values
    mouse_hover_time = round(random.uniform(0.5, 5.0), 2)
    scroll_depth = round(random.uniform(10.0, 50.0), 2)
    cart_view_time = round(random.uniform(1.0, 30.0), 2)
    num_clicks_before_purchase = random.randint(1, 5)
    
    # Checkout and payment times
    checkout_completion_time =  round(random.uniform(5.0, 60.0), 2)
    payment_processing_time =  round(random.uniform(1.0, 5.0), 2) 
    
    # Adjust times to fit within the session duration
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def brand_loyalist_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Brand Loyalist: Sticks to specific brands, spends time reading details, but purchases quickly."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    
    mouse_hover_time = round(random.uniform(2.0, 15.0), 2)
    scroll_depth = round(random.uniform(20.0, 60.0), 2)
    cart_view_time = round(random.uniform(5.0, 120.0), 2)
    num_clicks_before_purchase = random.randint(3, 10)
    
    checkout_completion_time =  round(random.uniform(10.0, 120.0), 2)
    payment_processing_time =  round(random.uniform(1.0, 8.0), 2)   
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def casual_browser_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Casual Browser: Browses for fun, rarely buys anything."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    
    mouse_hover_time = round(random.uniform(1.0, 10.0), 2)
    scroll_depth = round(random.uniform(50.0, 100.0), 2)
    cart_view_time = round(random.uniform(0.0, 300.0), 2)
    num_clicks_before_purchase = random.randint(1, 20)
    
    checkout_completion_time = round(random.uniform(30.0, 600.0), 2) if random.random() > 0.8  else 0.0
    payment_processing_time = round(random.uniform(1.0, 10.0), 2) if random.random() > 0.8 else 0.0
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def window_shopper_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Window Shopper: Browses items without intention to purchase."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    
    mouse_hover_time = round(random.uniform(10.0, 50.0), 2)
    scroll_depth = round(random.uniform(40.0, 100.0), 2)
    cart_view_time = round(random.uniform(0.0, 300.0), 2)
    num_clicks_before_purchase = random.randint(1, 10)
    
    checkout_completion_time = 0.0
    payment_processing_time = 0.0
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def deal_seeker_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Deal Seeker: Searches for discounts or promotions before buying."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(15.0, 60.0), 2)
    scroll_depth = round(random.uniform(20.0, 80.0), 2)
    cart_view_time = round(random.uniform(10.0, 300.0), 2)
    num_clicks_before_purchase = random.randint(5, 15)
    checkout_completion_time =  round(random.uniform(30.0, 150.0), 2)
    payment_processing_time =  round(random.uniform(1.0, 5.0), 2) 
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def last_minute_shopper_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Last-Minute Shopper: Makes a purchase just before a deadline or event."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(1.0, 10.0), 2)
    scroll_depth = round(random.uniform(20.0, 60.0), 2)
    cart_view_time = round(random.uniform(1.0, 30.0), 2)
    num_clicks_before_purchase = random.randint(1, 5)
    checkout_completion_time =  round(random.uniform(5.0, 60.0), 2)
    payment_processing_time =  round(random.uniform(1.0, 10.0), 2) 
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def mobile_shopper_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Mobile Shopper: Makes quick decisions, likely using mobile devices for fast browsing."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(0.5, 3.0), 2)
    scroll_depth = round(random.uniform(10.0, 40.0), 2)
    cart_view_time = round(random.uniform(5.0, 50.0), 2)
    num_clicks_before_purchase = random.randint(1, 7)
    checkout_completion_time =  round(random.uniform(10.0, 30.0), 2)
    payment_processing_time =  round(random.uniform(2.0, 5.0), 2)  
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }



def researcher_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Researcher: Spends significant time researching products, comparing options, reading reviews."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(15.0, 60.0), 2)  # Longer hover time, researching details
    scroll_depth = round(random.uniform(40.0, 90.0), 2)  # Scrolls extensively to compare features
    cart_view_time = round(random.uniform(30.0, 120.0), 2)  # Spends a lot of time analyzing cart contents
    num_clicks_before_purchase = random.randint(15, 40)  # Multiple clicks to read through detailed information
    checkout_completion_time = round(random.uniform(30.0, 180.0), 2) 
    payment_processing_time = round(random.uniform(5.0, 20.0), 2)  
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def subscription_shopper_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Subscription Shopper: Regularly buys subscription-based products, likely returns often."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(5.0, 30.0), 2)  # Moderate hover time, quick decisions
    scroll_depth = round(random.uniform(30.0, 60.0), 2)  # Scrolls through subscription options
    cart_view_time = round(random.uniform(20.0, 90.0), 2)  # Brief cart view before subscription confirmation
    num_clicks_before_purchase = random.randint(5, 15)  # Few clicks before subscription decision
    checkout_completion_time = round(random.uniform(10.0, 60.0), 2) 
    payment_processing_time = round(random.uniform(5.0, 15.0), 2) 

    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def loyal_customer_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Loyal Customer: A repeat customer, spends less time deciding, faster checkout, higher engagement."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(5.0, 20.0), 2)  # Short hover time, familiar with the store
    scroll_depth = round(random.uniform(20.0, 60.0), 2)  # Scrolls through favorite products
    cart_view_time = round(random.uniform(20.0, 60.0), 2)  # Familiar with the cart, quick review
    num_clicks_before_purchase = random.randint(3, 10)  # Few clicks before purchase due to familiarity
    checkout_completion_time = round(random.uniform(5.0, 30.0), 2) 
    payment_processing_time = round(random.uniform(1.0, 5.0), 2) 
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def abandoner_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Abandoner: Adds items to the cart but abandons before completing the purchase."""
    
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(5.0, 30.0), 2)  # Brief hover, often distracted
    scroll_depth = round(random.uniform(20.0, 70.0), 2)  # Scrolls casually, doesn't engage fully
    cart_view_time = round(random.uniform(10.0, 180.0), 2)  # Spends time in the cart but leaves without purchase
    num_clicks_before_purchase = random.randint(5, 20)  # Numerous clicks but no purchase
    checkout_completion_time = 0.0  # Abandonment before checkout
    payment_processing_time = 0.0  # No payment processing as purchase is abandoned
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": num_clicks_before_purchase,
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def gift_buyer_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Gift Buyer: Focused on finding the right gift for someone else, possibly spends more time deciding."""
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(10.0, 40.0), 2)  # Focused on detailed product descriptions
    scroll_depth = round(random.uniform(30.0, 80.0), 2)  # Scrolls deeply to find the perfect gift
    cart_view_time = round(random.uniform(30.0, 120.0), 2)  # Spends time choosing multiple options
    num_clicks_before_purchase = random.randint(5, 25)  # More clicks due to comparison
    checkout_completion_time = round(random.uniform(10.0, 60.0), 2) 
    payment_processing_time = round(random.uniform(5.0, 20.0), 2) 
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": random.randint(5, 25),
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def bulk_buyer_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Bulk Buyer: Purchases large quantities, focused on efficiency."""
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(5.0, 20.0), 2)  # Quick hover due to familiarity with items
    scroll_depth = round(random.uniform(20.0, 60.0), 2)  # Scrolls through pages quickly
    cart_view_time = round(random.uniform(10.0, 60.0), 2)  # Quick cart review before bulk checkout
    num_clicks_before_purchase = random.randint(3, 10)  # Fewer clicks, bulk decisions
    checkout_completion_time = round(random.uniform(10.0, 60.0), 2) 
    payment_processing_time = round(random.uniform(1.0, 5.0), 2)   # Bulk payment fast
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": random.randint(3, 10),
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }


def eco_conscious_shopper_behavior(order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """Eco-Conscious Shopper: Focused on sustainable and eco-friendly products."""
    session_duration = get_session_duration(session_start_time, session_end_time)
    mouse_hover_time = round(random.uniform(15.0, 45.0), 2)  # Longer hover to check product sustainability
    scroll_depth = round(random.uniform(40.0, 80.0), 2)  # Scrolls to find eco-friendly options
    cart_view_time = round(random.uniform(30.0, 120.0), 2)  # Spends time researching eco-friendly products
    num_clicks_before_purchase = random.randint(10, 30)  # Multiple clicks to make an ethical decision
    checkout_completion_time = round(random.uniform(15.0, 60.0), 2) 
    payment_processing_time = round(random.uniform(5.0, 20.0), 2)  # Payment processing focused on eco-initiatives
    
    adjusted_times = adjust_time_within_session_myway(session_duration, mouse_hover_time, scroll_depth, cart_view_time, checkout_completion_time, payment_processing_time)
    
    return {
        "mouse_hover_time": adjusted_times[0],
        "scroll_depth": adjusted_times[1],
        "cart_view_time": adjusted_times[2],
        "num_clicks_before_purchase": random.randint(10, 30),
        "checkout_completion_time": adjusted_times[3],
        "payment_processing_time": adjusted_times[4]
    }
