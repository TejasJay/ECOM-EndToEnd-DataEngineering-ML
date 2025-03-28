import asyncio
import json
import logging
import multiprocessing
import os
import random
import signal
import sys
from datetime import datetime
from kafka import KafkaProducer
import orjson
import psutil
from simulation_scripts.simulator_logic import ECOM


def split_users(users, num_chunks):
    chunk_size = (len(users) + num_chunks - 1) // num_chunks
    return [users[i:i + chunk_size] for i in range(0, len(users), chunk_size)]


def setup_logger(core_id, level=logging.INFO):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/core_{core_id}.log"
    logger = logging.getLogger(f"Core{core_id}")
    logger.setLevel(level)
    if logger.hasHandlers():
        logger.handlers.clear()
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(fh)
    return logger


def create_kafka_producer():
    return KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: orjson.dumps(v),
        linger_ms=10,
        batch_size=32 * 1024,
        compression_type='gzip'
    )


def run_on_core(core_id, user_chunk, avg_sessions, concurrent_users):
    log_level = logging.WARNING if os.getenv("PROD") else logging.INFO
    logger = setup_logger(core_id, level=log_level)
    session_lock = asyncio.Lock()
    active_sessions = set()
    session_semaphore = asyncio.Semaphore(concurrent_users)
    data = ECOM()
    producer = create_kafka_producer()

    async def real_time_simulate_data_async():
        async with session_semaphore:
            selected_user = random.choice(user_chunk)
            user_id = selected_user["user_id"]

            async with session_lock:
                if user_id in active_sessions:
                    return
                active_sessions.add(user_id)

            logger.info(f"🔵 Starting session for {user_id}")

            try:
                producer.send("users", selected_user)
                marketing_data = data.marketing_data(selected_user)[0]
                producer.send("marketings", marketing_data)

                for _ in range(random.randint(1, avg_sessions)):
                    session_start_time = datetime.now()
                    await asyncio.sleep(random.uniform(1, 5))
                    session_end_time = datetime.now()

                    session = data.session_data(selected_user, session_start_time, session_end_time)[0]
                    producer.send("sessions", session)

                    order = data.order_data(selected_user, session, marketing_data)
                    producer.send("orders", order)

                    behaviour = data.behaviour_data(selected_user, order, session)
                    producer.send("behaviours", behaviour)

                    wait_time = random.uniform(1, 3600)
                    logger.info(f"🕒 {user_id} sleeping for {int(wait_time)}s before next session")
                    await asyncio.sleep(wait_time)

                logger.info(f"✅ Finished session for {user_id}")

            finally:
                async with session_lock:
                    active_sessions.remove(user_id)

    async def run_loop():
        try:
            while True:
                cpu_load = psutil.cpu_percent()
                adjusted_concurrent = concurrent_users
                if cpu_load > 90:
                    adjusted_concurrent = max(10, concurrent_users // 2)

                tasks = [asyncio.create_task(real_time_simulate_data_async()) for _ in range(adjusted_concurrent)]
                await asyncio.gather(*tasks)
                await asyncio.sleep(random.uniform(1, 2))
        except asyncio.CancelledError:
            logger.warning("🛑 Coroutine shutdown signal received.")

    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.warning("🛑 KeyboardInterrupt in core. Flushing Kafka...")
    finally:
        producer.flush()
        producer.close()
        logger.warning("✅ Kafka producer closed.")


class RealTimeSimulator:
    def __init__(self, batch_data_path, avg_sessions=10, concurrent_users=100):
        self.batch_data = json.load(open(batch_data_path))[0]
        self.avg_sessions = avg_sessions
        self.concurrent_users = concurrent_users
        self.total_cores = psutil.cpu_count(logical=False)
        self.processes = []

    def terminate_all(self, signum, frame):
        print(f"\n⚠️ Caught signal {signum}. Terminating all processes...")
        for p in self.processes:
            if p.is_alive():
                p.terminate()
                p.join()
        sys.exit(0)

    def run(self):
        print(f"💻 Detected {self.total_cores} physical CPU cores")
        user_chunks = split_users(self.batch_data, self.total_cores)

        signal.signal(signal.SIGINT, self.terminate_all)
        signal.signal(signal.SIGTERM, self.terminate_all)

        for core, chunk in enumerate(user_chunks):
            p = multiprocessing.Process(
                target=run_on_core,
                args=(core, chunk, self.avg_sessions, self.concurrent_users)
            )
            p.start()
            self.processes.append(p)

        for p in self.processes:
            p.join()


if __name__ == "__main__":
    sim = RealTimeSimulator(
        batch_data_path="./json_files/full_data.json",
        avg_sessions=10,
        concurrent_users=50
    )
    sim.run()
