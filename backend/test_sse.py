import requests
import json
import threading
import time

BASE_URL = "http://localhost:5001/api"

def create_test_task():
    """Helper function to create a test task"""
    response = requests.post(
        f"{BASE_URL}/tasks/",
        json={"video_id": f"test_video_{int(time.time())}"}
    )
    return response.json()

def test_task_list_sse():
    """Test the task list SSE endpoint"""
    print("Testing task list SSE endpoint...")
    
    # Create a task first
    task = create_test_task()
    print(f"Created test task: {task['task_id']}")
    
    # Start listening to SSE
    def listen_for_updates():
        response = requests.get(
            f"{BASE_URL}/tasks/events/list",
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )
        
        print("Listening for task list updates...")
        for line in response.iter_lines():
            if line:
                # Skip comment lines
                if line.startswith(b':'):
                    continue
                    
                # Parse the SSE data
                if line.startswith(b'data: '):
                    data = json.loads(line[6:])  # Remove 'data: ' prefix
                    print(f"\nReceived update: {json.dumps(data, indent=2)}")
    
    # Start the SSE listener in a separate thread
    listener = threading.Thread(target=listen_for_updates, daemon=True)
    listener.start()
    
    # Create a few more tasks to see updates
    for i in range(2):
        time.sleep(2)
        task = create_test_task()
        print(f"Created additional task: {task['task_id']}")
    
    # Keep the test running for a while
    time.sleep(5)
    print("\nTask list SSE test completed!")

def test_individual_task_sse():
    """Test the individual task SSE endpoint"""
    print("\nTesting individual task SSE endpoint...")
    
    # Create a task
    task = create_test_task()
    task_id = task['task_id']
    print(f"Created test task: {task_id}")
    
    # Start listening to SSE for this specific task
    def listen_for_updates():
        response = requests.get(
            f"{BASE_URL}/tasks/{task_id}/events",
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )
        
        print(f"Listening for updates on task {task_id}...")
        for line in response.iter_lines():
            if line:
                # Skip comment lines
                if line.startswith(b':'):
                    continue
                    
                # Parse the SSE data
                if line.startswith(b'data: '):
                    data = json.loads(line[6:])  # Remove 'data: ' prefix
                    print(f"\nTask update: {json.dumps(data, indent=2)}")
    
    # Start the SSE listener in a separate thread
    listener = threading.Thread(target=listen_for_updates, daemon=True)
    listener.start()
    
    # Keep the test running for a while
    time.sleep(10)
    print("\nIndividual task SSE test completed!")

if __name__ == "__main__":
    print("Starting SSE endpoint tests...")
    test_task_list_sse()
    test_individual_task_sse()
    print("All tests completed!")
