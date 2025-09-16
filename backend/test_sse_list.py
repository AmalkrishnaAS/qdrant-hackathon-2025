import requests
import json
import time

def test_sse_list():
    """Test the SSE endpoint for task list updates"""
    print("Connecting to SSE endpoint for task list updates...")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Start listening to the SSE endpoint
        response = requests.get(
            'http://localhost:5001/api/tasks/events/list',
            stream=True,
            headers={'Accept': 'text/event-stream'}
        )
        
        # Process each line from the SSE stream
        for line in response.iter_lines():
            if line:
                # Skip comment lines
                if line.startswith(b':'):
                    continue
                
                # Parse the SSE data
                if line.startswith(b'data: '):
                    try:
                        data = json.loads(line[6:])  # Remove 'data: ' prefix
                        print(f"\n=== New Update ===")
                        print(f"Event: {data.get('event')}")
                        print("Tasks:")
                        
                        # Print each task's status
                        for task in data.get('data', []):
                            print(f"- Task {task.get('task_id')}:")
                            print(f"  Status: {task.get('status')}")
                            if 'progress' in task:
                                print(f"  Progress: {task.get('progress')}%")
                            if 'message' in task:
                                print(f"  Message: {task.get('message')}")
                            print()
                        
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                        print(f"Raw data: {line}")
    
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_sse_list()
