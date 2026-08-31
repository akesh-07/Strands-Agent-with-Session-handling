import requests

def main():
    server_url = "http://127.0.0.1:8000/ask"
    
    print("========================================")
    print("   College RAG Assistant CLI Client")
    print("========================================")
    
    session_id = input("Enter Session ID: ").strip()
    if not session_id:
        print("Session ID cannot be empty.")
        return

    print("\nChat started! Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
            
        if not question:
            continue
            
        try:
            # Send the request to the FastAPI server
            response = requests.post(
                server_url, 
                json={"session_id": session_id, "question": question},
                timeout=60 # Give the agent some time to think and review
            )
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer received.")
                print(f"\nAgent: {answer}\n")
            else:
                print(f"\nError {response.status_code}: {response.text}\n")
                
        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to the server. Is Uvicorn running on port 8000?\n")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}\n")

if __name__ == "__main__":
    main()
