# Comment Review AI

<img width="1508" height="788" alt="Screenshot 2025-11-25 at 08 16 53" src="https://github.com/user-attachments/assets/ed83e45a-d81e-4182-9f14-8c487224f30c" />


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

2.  **Set up Ollama (Local LLM):**

    This project uses [Ollama](https://ollama.ai/) to run a local LLM (llama3.1) for comment analysis.

    - **Install Ollama:**
      - **macOS/Linux:**
        ```bash
        curl -fsSL https://ollama.ai/install.sh | sh
        ```
      - **Windows:** Download from [https://ollama.ai/download](https://ollama.ai/download)
      - **Or visit:** [https://ollama.ai](https://ollama.ai) for other installation methods

    - **Pull the llama3.1 model:**
      ```bash
      ollama pull llama3.1:latest
      ```

    - **Start Ollama (if not already running):**
      ```bash
      ollama serve
      ```
      Ollama will run on `http://localhost:11434` by default.

    - **Verify Ollama is running:**
      ```bash
      curl http://localhost:11434/api/tags
      ```
      You should see a list of available models including `llama3.1:latest`.

    **Alternative: Using OpenAI instead of Ollama**

    If you prefer to use OpenAI's API instead of a local model, modify `src/agent.py`:
    ```python
    # Replace the ollama_model configuration with:
    ai_analyzer = Agent(
        "openai:gpt-4-turbo",  # or "openai:gpt-3.5-turbo"
        output_type=CommentAnalysis,
    )
    ```
    And set your OpenAI API key in `.env`:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

3.  **Set up environment variables:**
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
