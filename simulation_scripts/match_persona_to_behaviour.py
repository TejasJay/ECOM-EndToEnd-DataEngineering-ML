from behaviour import *

def match_persona_to_behavior(persona, order_status, payment_status, session_start_time, session_end_time, order_completed_time=None):
    """
    Match a persona to its corresponding behavior function.

    Parameters:
        persona (str): The name of the persona.
        order_status (str): The order status ("Completed", "Pending", etc.).
        payment_status (str): The payment status ("Successful", "Failed", etc.).
        session_start_time (str): The session start time in "%Y-%m-%dT%H:%M:%S" format.
        session_end_time (str): The session end time in "%Y-%m-%dT%H:%M:%S" format.
        order_completed_time (str, optional): The order completed time (if applicable).

    Returns:
        dict: The behavior values associated with the persona.
    """
    
    persona_to_function = {
        "Bargain Hunter": bargain_hunter_behavior,
        "Impulse Buyer": impulse_buyer_behavior,
        "Brand Loyalist": brand_loyalist_behavior,
        "Casual Browser": casual_browser_behavior,
        "Window Shopper": window_shopper_behavior,
        "Deal Seeker": deal_seeker_behavior,
        "Last-Minute Shopper": last_minute_shopper_behavior,
        "Mobile Shopper": mobile_shopper_behavior,
        "Researcher": researcher_behavior,
        "Subscription Shopper": subscription_shopper_behavior,
        "Loyal Customer": loyal_customer_behavior,
        "Abandoner": abandoner_behavior,
        "Gift Buyer": gift_buyer_behavior,
        "Bulk Buyer": bulk_buyer_behavior,
        "Eco-Conscious Shopper": eco_conscious_shopper_behavior
    }

    # Default behavior for unknown personas
    if persona not in persona_to_function:
        raise ValueError(f"Unknown persona: {persona}")

    # Call the respective behavior function based on the persona
    behavior_function = persona_to_function[persona]
    return behavior_function(order_status, payment_status, session_start_time, session_end_time, order_completed_time)
