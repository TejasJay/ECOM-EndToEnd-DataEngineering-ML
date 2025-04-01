#!/bin/bash

set -e  # Exit on any error

# Step 1: Check if JSON already exists
if [ ! -f ../json_files/full_data.json ]; then
  echo "🛠 Generating batch data..."
  python3 -m pos_logs.unified_simulator --mode batch --count 10000 --avg_sessions 10
  echo "🧹 Cleaning session logs..."
  rm -f ../logs/session_logs/core.*
fi

# Step 2: Run external API fetcher in background if not running
if ! pgrep -f promotion_fetch_api_request.py > /dev/null; then
  echo "🔄 Starting promotion fetch API in background..."
  nohup python3 -m external_apis.promotion_fetch_api_request > ../logs/promotion.log 2>&1 &
fi

# Step 3: Start real-time simulation
echo "🚀 Launching real-time simulator..."
python3 -m pos_logs.unified_simulator --mode realtime --output stdout --avg_sessions 2 --concurrent_users 10

