import urllib.request
import json
import time
import concurrent.futures

API_URL = "http://localhost:8000/ask"

def send_request(student_name, session_id, question):
    """Sends a single request to the FastAPI server and measures the time."""
    payload = json.dumps({
        "session_id": session_id,
        "question": question
    }).encode('utf-8')
    
    req = urllib.request.Request(
        API_URL, 
        data=payload, 
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"[{time.strftime('%X')}] 🚀 {student_name} is sending a question: '{question}'")
    start_time = time.time()
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            elapsed = time.time() - start_time
            print(f"[{time.strftime('%X')}] ✅ {student_name} got an answer in {elapsed:.2f} seconds!")
            return elapsed
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"[{time.strftime('%X')}] ❌ {student_name} request failed after {elapsed:.2f} seconds: {e}")
        return elapsed

if __name__ == "__main__":
    print("--- Starting Concurrency Test ---")
    print("Make sure your FastAPI server is running on port 8000!\n")
    
    total_start_time = time.time()
    
    # We use ThreadPoolExecutor to send two requests at the exact same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # Submit Student A's request
        future_a = executor.submit(
            send_request, 
            "Student A", 
            "session-A-123", 
            "What is the college fee refund policy?"
        )
        
        # Submit Student B's request immediately after (in parallel)
        future_b = executor.submit(
            send_request, 
            "Student B", 
            "session-B-456", 
            "How do I report a ragging incident?"
        )
        
        # Wait for both to finish
        concurrent.futures.wait([future_a, future_b])
        
    total_time = time.time() - total_start_time
    
    print("\n--- Test Complete ---")
    print(f"Total time taken for BOTH requests to finish: {total_time:.2f} seconds.")
    print("\nObservation:")
    print("If your server was synchronous (blocking), the total time would be Student A's time + Student B's time.")
    print("Because your server uses 'async/await', both requests were processed at the same time, meaning the total time should be roughly equal to the time of the single longest request!")
