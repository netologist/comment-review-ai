# mcp_client.py
import requests
import time
import json

API_URL = "http://127.0.0.1:8000/analyze-comment"

# A list of sample comments to send to the API
SAMPLE_COMMENTS = [
    "The new Dune movie was an absolute visual spectacle. The cinematography was breathtaking.",
    "I read 'Project Hail Mary' recently and it was fantastic! A great blend of science and humor.",
    "This is the worst thing I have ever seen. It was a complete waste of my time and money.",
    "what a load of garbage, the acting was just terrible.",
    "I'm not sure how I feel about this one. The plot was a bit slow, but the ending was surprising.",
    "My favorite team is the lakers, they are the best in the NBA.", # Irrelevant
    "The Godfather is a classic. A must-watch for any film enthusiast.",
    "asdfghjkl; this doesn't make any sense.", # Gibberish / Irrelevant
]

def run_mcp_client():
    """
    Runs the Master Control Program client.

    This function iterates through a list of sample comments and sends them,
    one by one, to the Comment Review AI API. It then prints the JSON
    response received from the server.
    """
    print("--- Starting Master Control Program (MCP) Client ---")
    print(f"MCP will send {len(SAMPLE_COMMENTS)} sample comments to the API at {API_URL}")
    print("-----------------------------------------------------\n")
    
    for i, comment in enumerate(SAMPLE_COMMENTS):
        print(f"[{i+1}/{len(SAMPLE_COMMENTS)}] Sending comment for analysis:")
        print(f"  > \"{comment}\"\n")
        
        try:
            # Send the POST request to the API
            response = requests.post(API_URL, json={"comment": comment})
            
            # Check if the request was successful
            if response.status_code == 200:
                print("  < Analysis successful! Response from server:")
                # Pretty-print the JSON response
                parsed_json = response.json()
                print(json.dumps(parsed_json, indent=2))
            else:
                print(f"  < Error: Received status code {response.status_code}")
                print(f"  < Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("  < CRITICAL ERROR: Could not connect to the API server.")
            print(f"  < Please ensure the FastAPI server is running at {API_URL}")
            break # Stop the client if the server is not running
        except Exception as e:
            print(f"  < An unexpected error occurred: {e}")
            
        print("\n-----------------------------------------------------\n")
        
        # Wait for a few seconds before sending the next comment
        if i < len(SAMPLE_COMMENTS) - 1:
            time.sleep(3)

    print("--- MCP Client has finished its run ---")


if __name__ == "__main__":
    run_mcp_client()
