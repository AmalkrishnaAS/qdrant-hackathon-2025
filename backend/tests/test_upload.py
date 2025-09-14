import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env')

def test_file_upload():
    """Test file upload to the upload endpoint"""
    # URL of your local development server
    base_url = "http://localhost:5000"  # Update if your server runs on a different port
    upload_url = f"{base_url}/api/upload/"
    
    # Path to a test file (using the BigBuckBunny.mp4 in the tests directory)
    test_file_path = os.path.join(os.path.dirname(__file__), 'BigBuckBunny.mp4')
    
    if not os.path.exists(test_file_path):
        print(f"Test file not found at {test_file_path}")
        print("Please make sure the test file exists or update the path in the test script.")
        return
    
    # Prepare the file for upload
    files = {'files': ('test_video.mp4', open(test_file_path, 'rb'), 'video/mp4')}
    
    try:
        print(f"Uploading test file: {test_file_path}")
        response = requests.post(upload_url, files=files)
        
        print(f"Status Code: {response.status_code}")
        print("Response:", response.json())
        
        if response.status_code == 200:
            print("\n✅ Upload successful!")
            result = response.json()
            if 'data' in result and len(result['data']) > 0:
                file_info = result['data'][0]
                print(f"\nUploaded File Info:")
                print(f"- Original Filename: {file_info.get('original_filename')}")
                print(f"- File Type: {file_info.get('file_type')}")
                print(f"- File Size: {file_info.get('file_size')} bytes")
                if 'secure_url' in file_info:
                    print(f"- Cloudinary URL: {file_info.get('secure_url')}")
        else:
            print("\n❌ Upload failed!")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error making request: {e}")
        print("Please make sure the server is running and accessible at", upload_url)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        # Make sure to close the file
        if 'files' in locals():
            files['files'][1].close()

if __name__ == "__main__":
    # Check if Cloudinary credentials are set
    required_vars = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        print("\nPlease make sure to set these in your .env file and restart your server.")
    else:
        test_file_upload()
