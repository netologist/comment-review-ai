# Comment Review AI

An agentic application that analyzes user comments for profanity, sentiment, and relevance to movies or books. It fetches additional information from OMDb and provides a simple API and UI to interact with the system.

## Project Structure

- `src/`: Contains the core application logic.
  - `main.py`: The FastAPI application.
  - `agent.py`: The Pydantic AI agent for comment analysis.
  - `database.py`: A simple in-memory database to store comment analysis results.
- `gradio_app.py`: The Gradio web interface.
- `mcp_client.py`: The Master Control Program client to test the API.
- `requirements.txt`: Python dependencies.
- `.env.example`: Example environment file. Copy to `.env` and fill in your details.
- `start.sh`: Script to start the FastAPI server and Gradio app.
- `stop.sh`: Script to stop the running processes.

## Setup

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Set up environment variables:**
    - Copy `.env.example` to a new file named `.env`.
    - Get a free API key from [OMDb API](https://www.omdbapi.com/apikey.aspx).
    - Add your API key to the `.env` file:
      ```
      OMDB_API_KEY=YOUR_API_KEY_HERE
      ```

## Running the Application

- **To start everything:**
  ```bash
  ./start.sh
  ```
  - FastAPI will be available at `http://127.0.0.1:8000`.
  - Gradio will be available at `http://127.0.0.1:7860`.

- **To stop everything:**
  ```bash
  ./stop.sh
  ```
