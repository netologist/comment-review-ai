# src/agent.py
import os
import httpx
from typing import Literal, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Pydantic Data Models for Analysis Output ---

class FilmOrBookInfo(BaseModel):
    """Model to store fetched information about the film or book."""
    title: str = Field(..., description="The official title of the film or book.")
    year: str = Field(..., description="The release year of the film or book.")
    poster_url: Optional[str] = Field(None, description="The URL for the movie or book cover image.")

class CommentAnalysis(BaseModel):
    """
    The main model for structuring the analysis of a user's comment.
    This model captures profanity, sentiment, relevance, and publication status.
    """
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        ..., description="The overall sentiment of the comment."
    )
    is_profane: bool = Field(
        ..., description="Does the comment contain any profanity or swear words?"
    )
    is_relevant: bool = Field(
        ..., description="Is the comment about a film or a book? This should be false if the comment is gibberish, off-topic, or spam."
    )
    subject_title: str = Field(
        ..., description="The title of the film or book mentioned in the comment. If not mentioned, this should be 'N/A'."
    )
    publish: bool = Field(
        ..., description="Set to `false` if the comment contains profanity OR is not relevant. Otherwise, set to `true`."
    )

class FullAnalysisResult(BaseModel):
    """The final, combined analysis result including fetched data."""
    original_comment: str
    analysis: CommentAnalysis
    retrieved_info: Optional[FilmOrBookInfo] = None

# --- OMDb API Fetching Logic ---

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_URL = "https://www.omdbapi.com/"

async def fetch_movie_or_book_info(title: str) -> Optional[FilmOrBookInfo]:
    """
    Fetches information for a given movie or book title from the OMDb API.
    """
    if not OMDB_API_KEY or OMDB_API_KEY == "YOUR_API_KEY_HERE":
        print("Warning: OMDb API key not configured. Skipping data fetching.")
        return None
    if not title or title == "N/A":
        return None

    params = {"t": title, "apikey": OMDB_API_KEY}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(OMDB_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("Response") == "True":
                return FilmOrBookInfo(
                    title=data.get("Title", "N/A"),
                    year=data.get("Year", "N/A"),
                    poster_url=data.get("Poster", None)
                )
        except httpx.HTTPStatusError as e:
            print(f"Error fetching data from OMDb: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during OMDb fetch: {e}")
    return None

# --- Pydantic AI Agent ---
ollama_model = OpenAIChatModel(
    model_name='llama3.1:latest',
    provider=OllamaProvider(base_url='http://localhost:11434/v1'),  
)

# Note: You might want to swap out the LLM for a different one depending on your needs.
# For example, using a local model with Ollama, or a different provider like Anthropic.
ai_analyzer = Agent(ollama_model, output_type=CommentAnalysis)

async def analyze_comment(comment: str) -> FullAnalysisResult:
    """
    Analyzes a comment using the Pydantic AI agent and enriches it with OMDb data.

    This function performs the following steps:
    1. Takes a raw user comment string.
    2. Uses the PydanticAI agent to analyze it for sentiment, profanity, relevance,
       and to extract the subject title. The agent also decides on the initial
       `publish` status based on profanity and relevance.
    3. If a subject title is identified, it calls the `fetch_movie_or_book_info`
       function to get additional data from OMDb.
    4. Combines all the information into a single `FullAnalysisResult` object.
    5. Returns the final, structured result.
    """
    print(f"Analyzing comment: '{comment}'")
    
    # The core analysis is done by the AI agent.
    # The prompt guides the LLM to perform the checks and structure the output.
    analysis_result: CommentAnalysis = await ai_analyzer.run(
        f"""Analyze the following user comment. Determine its sentiment, check for any profanity, and verify if it's genuinely about a movie or book.
        
        - Sentiment: classify as 'positive', 'negative', or 'neutral'.
        - Profanity: set `is_profane` to true if it contains any swear words or offensive language.
        - Relevance: set `is_relevant` to true only if the comment is clearly discussing a film or book. Comments that are spam, gibberish, or off-topic should be false.
        - Subject Title: extract the name of the movie or book. If no specific title can be found, return 'N/A'.
        - Publish Flag: set `publish` to false if `is_profane` is true OR `is_relevant` is false. Otherwise, set it to true.

        Comment: "{comment}"
        """
    )
    
    print(f"Initial analysis complete: {analysis_result}")
    print(f"Initial analysis complete: {analysis_result.output}")

    # Fetch additional information from OMDb based on the analysis
    retrieved_info = await fetch_movie_or_book_info(analysis_result.output.subject_title)
    if retrieved_info:
        print(f"Successfully retrieved info for '{retrieved_info.title}'")

    # Combine all results into the final data structure
    full_result = FullAnalysisResult(
        original_comment=comment,
        analysis=analysis_result.output,
        retrieved_info=retrieved_info,
    )

    return full_result
