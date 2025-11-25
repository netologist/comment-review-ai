#!/bin/bash
echo "Starting application..."

# Create a directory for logs and process IDs if it doesn't exist
mkdir -p .logs .pid

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "✓ Using uv (Option A - Faster)"
    USE_UV=true
else
    echo "✓ Using traditional Python (Option B)"
    echo "  Tip: Install uv for faster execution: curl -LsSf https://astral.sh/uv/install.sh | sh"
    USE_UV=false
fi

echo ""

# Start FastAPI server in the background
echo "Starting FastAPI server..."
if [ "$USE_UV" = true ]; then
    uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 > .logs/fastapi.log 2>&1 &
else
    uvicorn src.main:app --host 0.0.0.0 --port 8000 > .logs/fastapi.log 2>&1 &
fi
FASTAPI_PID=$!
echo $FASTAPI_PID > .pid/fastapi.pid

# Start Gradio app in the background
echo "Starting Gradio UI..."
if [ "$USE_UV" = true ]; then
    uv run python gradio_app.py > .logs/gradio.log 2>&1 &
else
    python gradio_app.py > .logs/gradio.log 2>&1 &
fi
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
