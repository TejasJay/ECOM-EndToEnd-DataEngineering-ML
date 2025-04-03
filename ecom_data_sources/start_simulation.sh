#!/bin/bash
set -e

# Detect if running inside Docker (mount /proc/1/cgroup is safe on slim too)
if grep -qE "/docker/|/kubepods/" /proc/1/cgroup 2>/dev/null; then
  BOOTSTRAP="kafka:29092"
else
  BOOTSTRAP="host.docker.internal:9092"
fi

# Step 1: Generate batch data if not exists
if [ ! -f ./json_files/full_data.json ]; then
  echo "🛠 Generating batch data..."
  python3 -m pos_logs.unified_simulator --mode batch --count 10000 --avg_sessions 10
  echo "🧹 Cleaning session logs..."
  rm -f ./logs/session_logs/core.*
fi

# Step 2: Run external API fetcher in background if not already running
if ! pgrep -f promotion_fetch_api_request.py > /dev/null; then
  echo "🔄 Starting promotion fetch API in background..."
  nohup python3 -m external_apis.promotion_fetch_api_request > ./logs/promotion.log 2>&1 &
fi

# Step 3: Run real-time simulator
echo "🚀 Launching real-time simulator..."
python3 -m pos_logs.unified_simulator --mode realtime --output kafka --bootstrap "kafka:29092" --avg_sessions 10 --concurrent_users 5
