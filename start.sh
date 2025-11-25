#!/bin/bash
echo "Starting application..."

# Create a directory for logs and process IDs if it doesn't exist
mkdir -p .logs .pid

# Start FastAPI server in the background
echo "Starting FastAPI server..."
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > .logs/fastapi.log 2>&1 &
FASTAPI_PID=$!
echo $FASTAPI_PID > .pid/fastapi.pid

# Start Gradio app in the background
echo "Starting Gradio UI..."
uv run python gradio_app.py > .logs/gradio.log 2>&1 &
GRADIO_PID=$!
echo $GRADIO_PID > .pid/gradio.pid

echo ""
echo "Application started successfully!"
echo "---------------------------------"
echo "FastAPI running on http://127.0.0.1:8000 (PID: $FASTAPI_PID)"
echo "Gradio UI running on http://127.0.0.1:7860 (PID: $GRADIO_PID)"
echo "Logs are being saved in the '.logs' directory."
echo "Process IDs are stored in the '.pid' directory."
echo ""
