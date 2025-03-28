# How Everything Works!!!!!!
* * *

<img src="Multiprocessing_on_core.png">

* * *


<img src="Multiprocessing_with_Kafka.png">


* * *

## 🧩 Part 1: Imports and Utility Functions

```python
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
from simulator_logic import ECOM
```

### 🔍 What each import does:

-   `asyncio`: Enables asynchronous programming. Used for handling concurrent tasks (simulating users) within each process.
-   `json`: For loading `full_data.json` and basic serialization (not used here for Kafka, since orjson is).
-   `logging`: Used to log activities like session starts, skips, and completions to log files.
-   `multiprocessing`: Enables parallel execution across CPU cores. Each core runs its own asyncio event loop.
-   `os`: Used to interact with the file system (e.g., create log directories).
-   `random`: Random delays, user selection, session lengths, etc., to simulate variability.
-   `signal`: Allows graceful shutdown on keyboard interrupt (`Ctrl+C`).
-   `sys`: Used to terminate the program explicitly via `sys.exit`.
-   `datetime`: Generates session start and end times.
-   `KafkaProducer`: Sends data to Kafka topics (each event type has a dedicated topic).
-   `orjson`: Fast JSON serialization. Used to serialize Python objects into bytes for Kafka.
-   `psutil`: Gets the number of **physical** CPU cores instead of logical ones.
-   `from simulator_logic import ECOM`: Custom ECOM class that generates synthetic user, session, order, etc., data.
* * *

### ⚙️ Utility Function: split\_users

```python
def split_users(users, num_chunks):
    chunk_size = (len(users) + num_chunks - 1) // num_chunks
    return [users[i:i + chunk_size] for i in range(0, len(users), chunk_size)]
```

#### 💡 Purpose:

Splits the entire user list into even chunks — one for each core.

#### 🔬 How it works:

-   `chunk_size` uses **ceiling division** to ensure no users are left out.
-   `return [...]` slices the user list into `num_chunks` evenly distributed sublists.
* * *

### 📝 Utility Function: setup\_logger

```python
def setup_logger(core_id):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/core_{core_id}.log"
    logger = logging.getLogger(f"Core{core_id}")
    logger.setLevel(logging.INFO)
    if logger.hasHandlers():
        logger.handlers.clear()
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('[%(asctime)s] %(message)s'))
    logger.addHandler(fh)
    return logger
```

#### 💡 Purpose:

Creates a per-core log file (e.g., `logs/core_0.log`) for better traceability.

#### 🔬 How it works:

-   Creates a `logs` directory if it doesn't exist.
-   Each logger is uniquely identified by the core number.
-   Removes existing handlers to avoid duplicate logs.
-   Formats logs with timestamps and simple messages.
-   Returns the logger to be used within that process.
* * *


## 🧠 Part 2: `run_on_core` Function

```python
def run_on_core(core_id, user_chunk, avg_sessions, concurrent_users):
```

### 🔍 What it does:

This function is executed in **each process**. It manages simulation for a chunk of users and runs an **async event loop** to generate and send data to Kafka.

* * *

### 🔧 Setup

```python
    logger = setup_logger(core_id)
```

-   Creates a logger specific to the core, e.g., `logs/core_2.log`.

```python
    session_lock = asyncio.Lock()
```

-   Used to **synchronize access** to `active_sessions` to prevent two sessions for the same user at once (even in async).

```python
    active_sessions = set()
```

-   Tracks which users currently have active sessions (in memory).
-   Prevents starting duplicate sessions for the same user.

```python
    session_semaphore = asyncio.Semaphore(concurrent_users)
```

-   Controls the number of concurrent sessions. Ensures we never exceed the number of users we want to simulate in parallel.
-   A **semaphore** allows only `N` coroutines to run at once.

```python
    data = ECOM()
```

-   Initializes your `ECOM` simulator class which knows how to generate synthetic user data (`user_data`, `session_data`, `order_data`, etc.).

```python
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: orjson.dumps(v)
    )
```

-   This sets up a Kafka producer.
-   `bootstrap_servers` is where your Kafka broker is running (localhost here).
-   `value_serializer` uses `orjson` to convert Python dicts → bytes (required by Kafka).
-   Every event (user session/order/etc.) is sent via `producer.send(topic_name, data)`.
* * *

## 🔁 Inner Async Function: `real_time_simulate_data_async`

This function simulates one full user session flow (from login → browsing → checkout → behavior analysis).

```python
    async def real_time_simulate_data_async():
```

### 🕵️ Step-by-step explanation

```python
        async with session_semaphore:
```

-   Limits how many of these coroutines can run in parallel.

```python
            selected_user = random.choice(user_chunk)
            user_id = selected_user["user_id"]
```

-   Randomly picks one user from this process's assigned chunk.

```python
            async with session_lock:
                if user_id in active_sessions:
                    return
                active_sessions.add(user_id)
```

-   If a session is already running for this user, skip it.
-   Adds user to the `active_sessions` set (inside a lock).

```python
            logger.info(f"🔵 Starting session for {user_id}")
```

-   Logs that this user session has begun.
* * *

### 📤 Kafka Data Push Begins

#### 1\. Marketing Data

```python
            marketing_data = data.marketing_data(selected_user)[0]
            producer.send("marketings", marketing_data)
```

-   Generates marketing attribution info and pushes it to the Kafka topic `marketings`.

#### 2\. Session Loop

```python
            for _ in range(random.randint(1, avg_sessions)):
```

-   Simulates between 1 and `avg_sessions` session iterations per user.

##### a. Session Start + Delay + End

```python
                session_start_time = datetime.now()
                await asyncio.sleep(random.uniform(1, 5))
                session_end_time = datetime.now()
```

-   Simulates browsing time.
-   Realistic delay between session start and end.

##### b. Push Session

```python
                session = data.session_data(selected_user, session_start_time, session_end_time)[0]
                producer.send("sessions", session)
```

##### c. Order Data

```python
                order = data.order_data(selected_user, session, marketing_data)
                producer.send("orders", order)
```

##### d. Behavior Data

```python
                behaviour = data.behaviour_data(selected_user, order, session)
                producer.send("behaviours", behaviour)
```

##### e. Wait for next session login

```python
                await asyncio.sleep(random.uniform(1, 3600))
```

-   Wait between 1 second to 1 hour before user logs in again.
* * *

```python
            logger.info(f"✅ Finished session for {user_id}")
```

### 🧼 Cleanup

```python
        finally:
            async with session_lock:
                active_sessions.remove(user_id)
```

-   Guarantees that even if something fails mid-session, the user is marked inactive again.
* * *



## ⚙️ Part 3: `run_loop` Function

```python
    async def run_loop():
```

This coroutine continuously schedules user sessions for this core using the async function `real_time_simulate_data_async()`.

* * *

### 🔄 What happens inside the loop?

```python
        try:
            while True:
```

-   Runs **indefinitely**, unless interrupted by a `KeyboardInterrupt` or cancellation.
* * *

#### 🧵 Schedule concurrent users

```python
                tasks = [asyncio.create_task(real_time_simulate_data_async()) for _ in range(concurrent_users)]
```

-   This creates `concurrent_users` number of parallel tasks (e.g., 50 at a time).
-   Each task runs the `real_time_simulate_data_async` coroutine, simulating a full user journey and pushing data to Kafka.
* * *

#### 👂 Await their completion

```python
                await asyncio.gather(*tasks)
```

-   Waits for **all parallel tasks** to finish before launching the next batch.
-   Ensures load doesn’t snowball (by not launching too many in parallel).
* * *

#### 💤 Delay between user batches

```python
                await asyncio.sleep(random.uniform(1, 2))
```

-   Slight delay before starting the next round of sessions.
-   This adds randomness, simulating a more natural login pattern.
* * *

#### ✋ Handle graceful shutdown

```python
        except asyncio.CancelledError:
            logger.info("🛑 Coroutine shutdown signal received.")
```

-   If the task is cancelled (due to signal or termination), logs a graceful shutdown message.
* * *

## 🧨 Run the Event Loop

```python
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info("🛑 KeyboardInterrupt in core. Shutting down...")
```

-   `asyncio.run()` spins up the event loop.
-   If you hit `Ctrl+C`, it catches `KeyboardInterrupt` and logs it nicely.
* * *

## 🧠 RealTimeSimulator Class

This class manages **multiple CPU cores** using multiprocessing. Each core runs its own event loop to simulate and stream user data to Kafka.

* * *

### 🏗️ `__init__` Constructor

```python
    def __init__(self, batch_data_path, avg_sessions=10, concurrent_users=100):
```

-   `batch_data_path`: Path to your `full_data.json`.
-   `avg_sessions`: Average number of sessions per user per run.
-   `concurrent_users`: Number of simultaneous sessions per core.

```python
        self.batch_data = json.load(open(batch_data_path))[0]
```

-   Loads the full user list from your dataset.

```python
        self.total_cores = psutil.cpu_count(logical=False)
```

-   Gets the number of **physical cores** (not hyperthreads).

```python
        self.processes = []
```

-   Placeholder for storing multiprocessing `Process` objects.
* * *

### ☠️ `terminate_all` Method

```python
    def terminate_all(self, signum, frame):
```

-   Registered as a signal handler.
-   When you hit `Ctrl+C` (SIGINT) or the OS sends a termination (SIGTERM), this is invoked.

```python
        for p in self.processes:
            if p.is_alive():
                p.terminate()
                p.join()
```

-   Terminates each running process cleanly.
-   `join()` ensures cleanup is finished before exiting.
* * *

### 🚀 `run` Method

```python
    def run(self):
```

This is the main launcher.

* * *

#### 🧠 Split data across cores

```python
        user_chunks = split_users(self.batch_data, self.total_cores)
```

-   Uses your helper `split_users()` to break the user list into evenly distributed chunks across CPU cores.
* * *

#### 📢 Register signal handlers

```python
        signal.signal(signal.SIGINT, self.terminate_all)
        signal.signal(signal.SIGTERM, self.terminate_all)
```

-   On Mac/Linux, this ensures your program shuts down properly when killed.
* * *

#### 🔁 Start processes per core

```python
        for core, chunk in enumerate(user_chunks):
            p = multiprocessing.Process(
                target=run_on_core,
                args=(core, chunk, self.avg_sessions, self.concurrent_users)
            )
            p.start()
            self.processes.append(p)
```

-   Each core gets a dedicated `multiprocessing.Process`.
-   It runs the `run_on_core()` function independently.
-   Each process runs its own async loop and Kafka producer.
* * *

#### 🧼 Wait for all processes

```python
        for p in self.processes:
            p.join()
```

-   Blocks the main process until all child processes exit.
-   Ensures long-running system stays active until explicitly killed.
* * *

### 🎯 Entry Point

```python
if __name__ == "__main__":
```

```python
    sim = RealTimeSimulator(batch_data_path="./json_files/full_data.json", avg_sessions=10, concurrent_users=50)
    sim.run()
```

-   Creates an instance of `RealTimeSimulator` and runs the simulation.
* * *


