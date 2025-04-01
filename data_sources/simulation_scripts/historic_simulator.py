# Initialize ECOM instance
import random
from data_sources.simulation_scripts.simulator_logic import *
import json

import json
import random
# from ECOM import ECOM  # Make sure ECOM class is defined in your module or same file

class BatchDataSimulator:
    """
    Batch simulator that generates synthetic E-Commerce user activity data and writes to a JSON file.
    """

    def __init__(self, user_count=1, avg_sessions_per_user=10, output_file="./data_sources/json_files/full_data.json"):
        """
        Initializes the simulator.

        Args:
            user_count (int): Number of users to simulate.
            avg_sessions_per_user (int): Average number of sessions per user.
            output_file (str): Filename to export the generated JSON data.
        """
        self.user_count = user_count
        self.avg_sessions_per_user = avg_sessions_per_user
        self.output_file = output_file
        self.data = ECOM()

    def simulate(self):
        """
        Main function to simulate and compile all data types.
        Generates:
            - users
            - sessions
            - marketing metadata
            - orders
            - behavioral insights
        """
        users, sessions, marketings, orders, behaviours = [], [], [], [], []

        for _ in range(self.user_count):
            user = self.data.user_data()[0]
            users.append(user)

            marketing_data = self.data.marketing_data(user)[0]
            marketings.append(marketing_data)

            for _ in range(random.randint(1, self.avg_sessions_per_user)):
                session_times = self.data.session_time(user)
                session_start_time, session_end_time = session_times
                session = self.data.session_data(user, session_start_time, session_end_time)[0]
                sessions.append(session)

                order = self.data.order_data(user, session, marketing_data)
                orders.append(order)

                behaviour = self.data.behaviour_data(user, order, session)
                behaviours.append(behaviour)

        result = [users, sessions, marketings, orders, behaviours]
        self._write_to_json(result)
        print(f"✅ Simulation complete. Data written to `{self.output_file}`")

    def _write_to_json(self, data):
        """
        Writes the given data to the configured output JSON file.

        Args:
            data (list): A list of all generated data types.
        """
        with open(self.output_file, "w") as json_file:
            json.dump(data, json_file, indent=4)

# Example usage:
if __name__ == "__main__":
    simulator = BatchDataSimulator(user_count=1000, avg_sessions_per_user=10)
    simulator.simulate()
