import asyncio
import argparse
import json
import logging
import os
import random
import socket
from datetime import datetime

from kafka import KafkaProducer
from simulation_scripts.simulator_logic import ECOM
from simulation_scripts.historic_simulator import BatchDataSimulator


def get_bootstrap_host():
    try:
        socket.gethostbyname("kafka")
        return "kafka:29092"
    except socket.error:
        return "localhost:9092"


def create_kafka_producer(bootstrap_servers=None):
    if bootstrap_servers is None:
        bootstrap_servers = get_bootstrap_host()
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )


def emit(producer, topic, data):
    producer.send(topic, data)


def simulate_batch(args, user_count=1000, avg_sessions_per_user=10):
    BatchDataSimulator(user_count, avg_sessions_per_user).simulate()


async def simulate_sessions(args):
    data = ECOM()
    producer = create_kafka_producer(args.bootstrap)
    users = json.load(open(args.batch_data_path))[0]

    while True:
        user = random.choice(users)
        print(f"🧪 Simulating session for {user['user_id']}")
        emit(producer, "users", user)

        marketing = data.marketing_data(user)[0]
        emit(producer, "marketings", marketing)

        for _ in range(random.randint(1, args.avg_sessions)):
            start = datetime.now()
            await asyncio.sleep(random.uniform(0.5, 1.0))
            end = datetime.now()

            session = data.session_data(user, start, end)[0]
            emit(producer, "sessions", session)

            order = data.order_data(user, session, marketing)
            emit(producer, "orders", order)

            behaviour = data.behaviour_data(user, order, session)
            emit(producer, "behaviours", behaviour)

            await asyncio.sleep(random.uniform(1, 3))

        await asyncio.sleep(2)


def main():
    parser = argparse.ArgumentParser(description="Kafka Data Simulator")
    parser.add_argument("--bootstrap", default=get_bootstrap_host())
    parser.add_argument("--type", choices=["realtime", "batch"], default="realtime")
    parser.add_argument("--batch_data_path", type=str, default="./json_files/full_data.json")
    parser.add_argument("--avg_sessions", type=int, default=5)
    args = parser.parse_args()

    if args.type == "realtime":
        asyncio.run(simulate_sessions(args))
    else:
        simulate_batch(args, user_count=1000, avg_sessions_per_user=10)


if __name__ == "__main__":
    main()
