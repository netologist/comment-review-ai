# src/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

from .agent import analyze_comment, FullAnalysisResult
from .database import add_analysis_to_db, get_all_analyses_from_db

# --- FastAPI App Initialization ---

app = FastAPI(
    title="Comment Review AI API",
    description="An API for analyzing user comments using an AI agent.",
    version="1.0.0",
)

# --- API Models ---

class CommentRequest(BaseModel):
    """The request model for submitting a new comment."""
    comment: str = Field(..., min_length=3, description="The user comment to be analyzed.")

class AnalysisResponse(FullAnalysisResult):
    """The response model for a single analysis result."""
    pass

class AllCommentsResponse(BaseModel):
    """The response model for retrieving all analyzed comments."""
    comments: List[FullAnalysisResult]

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
async def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Comment Review AI API is running."}

@app.post("/analyze-comment", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_comment_endpoint(request: CommentRequest):
    """
    Receives a comment, analyzes it using the AI agent, stores the result,
    and returns the full analysis.
    """
    if not request.comment:
        raise HTTPException(status_code=400, detail="Comment cannot be empty.")
    
    try:
        # The core logic is handled by our agent
        analysis_result = await analyze_comment(request.comment)
        
        # Store the result in our "database"
        add_analysis_to_db(analysis_result.dict())
        
        return analysis_result
    except Exception as e:
        # Handle potential errors during analysis
        print(f"An error occurred during analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze comment.")

@app.get("/comments", response_model=AllCommentsResponse, tags=["Comments"])
async def get_all_comments_endpoint():
    """
    Retrieves all comment analysis results stored in the database.
    """
    all_analyses = get_all_analyses_from_db()
    return {"comments": all_analyses}
