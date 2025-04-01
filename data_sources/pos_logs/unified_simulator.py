import asyncio
import json
import logging
import multiprocessing
import os
import random
import signal
import sys
from datetime import datetime
import psutil
import argparse
import orjson
from kafka import KafkaProducer
from data_sources.simulation_scripts.simulator_logic import ECOM
from data_sources.simulation_scripts.historic_simulator import BatchDataSimulator

# Utility: Kafka Producer Setup
def create_kafka_producer(bootstrap_servers="localhost:9092"):
    return KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: orjson.dumps(v),
        linger_ms=10,
        batch_size=32 * 1024,
        compression_type='gzip'
    )

# Utility: Logger Setup
def setup_logger(core_id):
    os.makedirs("data_sources/logs/session_logs/", exist_ok=True)
    log_file = f"data_sources/logs/session_logs/core_{core_id}.log"
    logger = logging.getLogger(f"Core{core_id}")
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(fh)
    return logger

# Utility: Data Output Handler
def emit_data(args, producer, topic, data):
    if args.output == "stdout":
        print(json.dumps(data, indent=2))
    elif args.output == "kafka":
        producer.send(topic, data)

# Utility: User chunking
def split_users(users, num_chunks):
    chunk_size = (len(users) + num_chunks - 1) // num_chunks
    return [users[i:i + chunk_size] for i in range(0, len(users), chunk_size)]

# Real-time simulator coroutine
def run_on_core(args, core_id, user_chunk, avg_sessions, concurrent_users):
    logger = setup_logger(core_id)
    session_lock = asyncio.Lock()
    active_sessions = set()
    data = ECOM()
    producer = create_kafka_producer(args.bootstrap) if args.output == "kafka" else None

    

    async def simulate_session():
        user = random.choice(user_chunk)
        user_id = user["user_id"]

        logger.info(f"Starting session for [{user_id}]")

        async with session_lock:
            if user_id in active_sessions:
                return
            active_sessions.add(user_id)

        try:
            emit_data(args, producer, "users", user)
            marketing = data.marketing_data(user)[0]
            emit_data(args, producer, "marketings", marketing)

            for _ in range(random.randint(1, avg_sessions)):
                start = datetime.now()
                await asyncio.sleep(random.uniform(0.5, 2))
                end = datetime.now()

                session = data.session_data(user, start, end)[0]
                emit_data(args, producer, "sessions", session)

                order = data.order_data(user, session, marketing)
                emit_data(args, producer, "orders", order)

                behaviour = data.behaviour_data(user, order, session)
                emit_data(args, producer, "behaviours", behaviour)
                logger.info(f"Session {_} completed [{user_id}]")

                await asyncio.sleep(random.uniform(1, 5))
            logger.info(f"All sessions completed for [{user_id}]")
        
        finally:
            async with session_lock:
                active_sessions.remove(user_id)

    async def run_loop():
        try:
            while True:
                for _ in range(concurrent_users):
                    asyncio.create_task(simulate_session())
                    await asyncio.sleep(random.uniform(0.5, 1.5))
                await asyncio.sleep(random.uniform(3, 5))
        except asyncio.CancelledError:
            logger.info("Cancelled coroutine")

    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info("Shutdown requested")

# Real-time Simulator Class
class RealTimeSimulator:
    def __init__(self, batch_data_path, avg_sessions, concurrent_users, args):
        self.batch_data = json.load(open(batch_data_path))[0]
        self.avg_sessions = avg_sessions
        self.concurrent_users = concurrent_users
        self.total_cores = psutil.cpu_count(logical=False)
        self.args = args
        self.processes = []

    def terminate_all(self, signum, frame):
        print(f"\n⚠️ Caught signal {signum}. Terminating...")
        for p in self.processes:
            if p.is_alive():
                p.terminate()
        sys.exit(0)

    def run(self):
        user_chunks = split_users(self.batch_data, self.total_cores)
        signal.signal(signal.SIGINT, self.terminate_all)
        signal.signal(signal.SIGTERM, self.terminate_all)

        for core, chunk in enumerate(user_chunks):
            p = multiprocessing.Process(
                target=run_on_core,
                args=(self.args, core, chunk, self.avg_sessions, self.concurrent_users)
            )
            p.start()
            self.processes.append(p)

        for p in self.processes:
            p.join()

# Entry Point
def main():
    parser = argparse.ArgumentParser(description="E-Commerce Simulator")
    parser.add_argument("--mode", choices=["batch", "realtime"], default="batch")
    parser.add_argument("--output", choices=["stdout", "kafka"], default="stdout")
    parser.add_argument("--bootstrap", default="localhost:9092")
    parser.add_argument("--topic", default="ecom_events")
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--avg_sessions", type=int, default=5)
    parser.add_argument("--concurrent_users", type=int, default=3)
    parser.add_argument("--batch_data_path", type=str, default="data_sources/json_files/full_data.json")
    args = parser.parse_args()

    if args.mode == "batch":
        simulator = BatchDataSimulator(user_count=args.count, avg_sessions_per_user=args.avg_sessions)
        simulator.simulate()
        
    elif args.mode == "realtime":
        sim = RealTimeSimulator(
            batch_data_path=args.batch_data_path,
            avg_sessions=args.avg_sessions,
            concurrent_users=args.concurrent_users,
            args=args
        )
        sim.run()

if __name__ == "__main__":
    main()
