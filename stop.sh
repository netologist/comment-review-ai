#!/bin/bash
echo "Stopping application..."

PID_DIR=".pid"

if [ -d "$PID_DIR" ]; then
    FASTAPI_PID_FILE="$PID_DIR/fastapi.pid"
    GRADIO_PID_FILE="$PID_DIR/gradio.pid"

    if [ -f "$FASTAPI_PID_FILE" ]; then
        FASTAPI_PID=$(cat "$FASTAPI_PID_FILE")
        echo "Stopping FastAPI server (PID: $FASTAPI_PID)..."
        kill "$FASTAPI_PID"
    else
        echo "FastAPI PID file not found."
    fi

    if [ -f "$GRADIO_PID_FILE" ]; then
        GRADIO_PID=$(cat "$GRADIO_PID_FILE")
        echo "Stopping Gradio UI (PID: $GRADIO_PID)..."
        kill "$GRADIO_PID"
    else
        echo "Gradio PID file not found."
    fi

    # Clean up the pid and log directories
    rm -rf "$PID_DIR"
    # Keeping logs for debugging, but you could uncomment the next line to clear them on stop
    # rm -rf .logs
else
    echo "PID directory not found. Nothing to stop."
fi

echo "Application stopped."
