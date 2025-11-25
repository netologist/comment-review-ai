# gradio_app.py
import gradio as gr
import requests
import pandas as pd
import nest_asyncio

# Apply nest_asyncio to allow running asyncio code within environments
# that already have a running event loop (like Gradio's).
nest_asyncio.apply()

# --- Configuration ---
API_URL = "http://127.0.0.1:8000"
ANALYZE_ENDPOINT = f"{API_URL}/analyze-comment"
COMMENTS_ENDPOINT = f"{API_URL}/comments"

# --- Helper Functions ---

def format_results_to_html(results):
    """Converts the list of comment analyses into a visually appealing HTML string."""
    if not results:
        return "<p>No comments analyzed yet.</p>"

    html = "<div style='display: flex; flex-wrap: wrap; gap: 20px;'>"
    for item in reversed(results):  # Show newest first
        analysis = item.get('analysis', {})
        info = item.get('retrieved_info', {})

        # Determine border color based on publish status
        border_color = 'green' if analysis.get('publish', False) else 'red'
        
        # Safely get poster URL
        poster_url = info.get('poster_url') if info else None
        poster_html = f"<img src='{poster_url}' style='width:100px; height: auto; float: left; margin-right: 15px;'>" if poster_url else "<div style='width:100px; height:150px; background-color:#eee; float: left; margin-right: 15px; text-align:center; line-height:150px;'>No Image</div>"

        html += f"""
        <div style='border: 2px solid {border_color}; border-radius: 10px; padding: 15px; width: 400px; overflow: hidden;'>
            {poster_html}
            <div style='overflow: hidden;'>
                <p><strong>Comment:</strong> "{item.get('original_comment', 'N/A')}"</p>
                <p><strong>Subject:</strong> {analysis.get('subject_title', 'N/A')} ({info.get('year', 'N/A') if info else 'N/A'})</p>
                <p>
                    <strong>Sentiment:</strong> {analysis.get('sentiment', 'N/A')} | 
                    <strong>Profane:</strong> {analysis.get('is_profane', 'N/A')} | 
                    <strong>Relevant:</strong> {analysis.get('is_relevant', 'N/A')}
                </p>
                <p><strong>Publish Status:</strong> {'Approved' if analysis.get('publish', False) else 'Rejected'}</p>
            </div>
        </div>
        """
    html += "</div>"
    return html

def submit_comment(comment):
    """Function to be called when the 'Submit' button is clicked."""
    if not comment:
        return "Please enter a comment.", fetch_all_comments_html()
    try:
        response = requests.post(ANALYZE_ENDPOINT, json={"comment": comment})
        response.raise_for_status()
        # The submission was successful, now refresh the list of all comments
        return f"Successfully analyzed: '{comment}'", fetch_all_comments_html()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to API: {e}", fetch_all_comments_html()

def fetch_all_comments_html():
    """Fetches all comments from the API and formats them as HTML."""
    try:
        response = requests.get(COMMENTS_ENDPOINT)
        response.raise_for_status()
        data = response.json().get("comments", [])
        return format_results_to_html(data)
    except requests.exceptions.RequestException as e:
        return f"<p>Error fetching comments: {e}</p>"

# --- Gradio Interface Definition ---

with gr.Blocks(theme=gr.themes.Soft(), css="footer {display: none !important}") as demo:
    gr.Markdown("# Comment Review AI Interface")
    gr.Markdown("Submit a new comment about a movie or book for analysis, or view the history of analyzed comments below.")
    
    with gr.Row():
        with gr.Column(scale=1):
            comment_input = gr.Textbox(lines=4, label="New Comment", placeholder="e.g., 'The Shawshank Redemption was a masterpiece, one of the best films ever.'")
            submit_button = gr.Button("Submit for Analysis", variant="primary")
            status_output = gr.Markdown()
            
    gr.Markdown("---")
    gr.Markdown("## Analyzed Comments")
    
    # Use an HTML component to display the formatted results
    results_output = gr.HTML(value=fetch_all_comments_html)
    
    # Refresh button to manually update the list of comments
    refresh_button = gr.Button("Refresh List")

    # --- Event Handlers ---
    submit_button.click(
        fn=submit_comment,
        inputs=[comment_input],
        outputs=[status_output, results_output]
    )
    
    refresh_button.click(
        fn=fetch_all_comments_html,
        inputs=[],
        outputs=[results_output]
    )

if __name__ == "__main__":
    print("Starting Gradio UI...")
    print("Gradio will be available at http://127.0.0.1:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
