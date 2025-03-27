# Initialize ECOM instance
import random
from simulator_logic import *
import json

def simulate_data(user_count= 1, avg_sesssion_count_per_user = 10):
  data = ECOM()

  users = []
  sessions = []
  marketings = []
  orders = []
  behaviours = []


  for _ in range(user_count):
    # print("\n# INITIAL USER DATA\n")  
    # Generate user data
    user = data.user_data()[0]  # Extract dictionary from list
    users.append(user)
    # Print user data
    # print(json.dumps(user, indent=4))

    # print("\n# MARKETING DATA\n")
    marketing_data = data.marketing_data(user)[0]
    marketings.append(marketing_data)
    # Print marketing data
    # print(json.dumps(marketing_data, indent=4))

    # Simulate multiple session runs and observe last_session_time updates
    # print("\n# SESSION DATA UPDATES\n")
    for _ in range(random.randint(1,avg_sesssion_count_per_user)):  # Run multiple sessions
      session = data.session_data(user)[0]  # Extract dictionary from list
      sessions.append(session)
      # print(f"Session {_+1}:")
      # print(json.dumps(session, indent=4))
      # print(f"Updated last_session_time: {data.last_session_time}")
      # print(f"Updated last_login_time: {user['last_login_time']}") 

      # print("\n# ORDER DATA\n")
      order = data.order_data(user, session, marketing_data)
      orders.append(order)
      # print(json.dumps(order, indent=4))
      # print("-" * 100)

      print("\n# BEHAVIOUR DATA\n")
      behaviour = data.behaviour_data(user, order, session)
      behaviours.append(behaviour)
      print(json.dumps(behaviour, indent=4))
      print("-" * 100)

  return users, sessions, marketings, orders, behaviours


simulated_data = simulate_data(user_count= 10000, avg_sesssion_count_per_user = 10)

# Assuming the data parts in the simulated_data are structured as follows
user_data = simulated_data[0]  # Example, adjust based on your data structure
sessions_data = simulated_data[1]
marketings_data = simulated_data[2]
orders_data = simulated_data[3]
behaviours_data = simulated_data[4]

# Combine into a list
full_data = [(user_data, "user_data"), (sessions_data, "sessions_data"), (marketings_data, "marketings_data"), 
             (orders_data, "orders_data"), (behaviours_data, "behaviours_data")]

# Iterate over full_data, where i is the data and j is the name
for data, name in full_data:
    # Convert the simulated data to JSON format
    json_data = json.dumps(data, indent=4)

    # Write to a JSON file
    file_path = f"{name}.json"

    with open(file_path, 'w') as json_file:
        json_file.write(json_data)

    print(f"Data written to {file_path}")